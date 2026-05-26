from __future__ import annotations

import base64
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

from bitroid.services.libtorrent_loader import LibtorrentUnavailableError, load_libtorrent


DEFAULT_SESSION_SETTINGS: dict[str, Any] = {
    "enable_dht": True,
    "enable_lsd": True,
    "enable_upnp": True,
    "enable_natpmp": True,
    "listen_interfaces": "0.0.0.0:6881,[::]:6881",
    "user_agent": "BitroidDM/0.1",
}

CLIENT_ALERT_CATEGORIES = (
    "error_notification",
    "storage_notification",
    "status_notification",
    "progress_notification",
    "file_progress_notification",
    "tracker_notification",
    "connect_notification",
    "peer_notification",
    "port_mapping_notification",
    "performance_warning",
)

HookCallback = Callable[[dict[str, Any]], None]


@dataclass(frozen=True)
class TorrentSnapshot:
    torrent_id: str
    name: str
    progress: float
    download_rate: int
    upload_rate: int
    total_done: int
    total_wanted: int
    total_wanted_done: int
    all_time_download: int
    all_time_upload: int
    num_peers: int
    num_seeds: int
    num_connections: int
    distributed_copies: float
    state: str
    paused: bool
    has_metadata: bool
    is_finished: bool
    is_seeding: bool
    save_path: str
    eta_seconds: int | None
    error: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TorrentFileSnapshot:
    index: int
    path: str
    size: int
    progress: int
    priority: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TorrentAlertSnapshot:
    event: str
    category: str
    message: str
    torrent_id: str | None
    torrent_name: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TorrentEngine:
    def __init__(
        self,
        download_dir: str | Path,
        session_settings: dict[str, Any] | None = None,
    ) -> None:
        self.lt, self.dll_dir_used, self._dll_handle = load_libtorrent()
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

        settings = dict(DEFAULT_SESSION_SETTINGS)
        if session_settings:
            settings.update(session_settings)

        self.session = self.lt.session(settings)
        self._handles: dict[str, Any] = {}
        self._hooks: dict[str, list[HookCallback]] = defaultdict(list)
        self._last_states: dict[str, str] = {}

    def on(self, event: str, callback: HookCallback) -> None:
        self._hooks[event].append(callback)

    def default_alert_mask(self) -> int:
        categories = self.lt.alert.category_t
        mask = 0
        for name in CLIENT_ALERT_CATEGORIES:
            mask |= int(getattr(categories, name))
        return mask

    def enable_client_alerts(self, mask: int | None = None) -> int:
        mask = self.default_alert_mask() if mask is None else int(mask)
        self.session.set_alert_mask(mask)
        return mask

    def add_torrent_file(
        self,
        torrent_path: str | Path,
        save_path: str | Path | None = None,
        *,
        paused: bool = False,
        sequential: bool = False,
    ) -> str:
        torrent_info = self.lt.torrent_info(str(torrent_path))
        params = self.lt.add_torrent_params()
        params.ti = torrent_info
        params.save_path = str(Path(save_path) if save_path else self.download_dir)
        self._set_torrent_flags(params, paused=paused, sequential=sequential)
        return self._track(self.session.add_torrent(params))

    def add_magnet(
        self,
        magnet_uri: str,
        save_path: str | Path | None = None,
        *,
        paused: bool = False,
        sequential: bool = False,
    ) -> str:
        params = self.lt.parse_magnet_uri(magnet_uri)
        params.save_path = str(Path(save_path) if save_path else self.download_dir)
        self._set_torrent_flags(params, paused=paused, sequential=sequential)
        return self._track(self.session.add_torrent(params))

    def add_resume_data(
        self,
        resume_data: str,
        save_path: str | Path | None = None,
        *,
        paused: bool = False,
        sequential: bool = False,
    ) -> str:
        payload = base64.b64decode(resume_data.encode("ascii"))
        params = self.lt.read_resume_data(payload)
        if save_path:
            params.save_path = str(Path(save_path))
        self._set_torrent_flags(params, paused=paused, sequential=sequential)
        return self._track(self.session.add_torrent(params))

    def status(self, torrent_id: str) -> TorrentSnapshot:
        return self._snapshot(torrent_id, self._handles[torrent_id])

    def list_statuses(self) -> list[TorrentSnapshot]:
        return [self._snapshot(torrent_id, handle) for torrent_id, handle in self._handles.items()]

    def file_statuses(self, torrent_id: str) -> list[TorrentFileSnapshot]:
        handle = self._handles[torrent_id]
        if not handle.has_metadata():
            return []

        torrent_info = handle.torrent_file()
        files = torrent_info.files()
        progress = handle.file_progress()
        try:
            priorities = list(handle.get_file_priorities())
        except Exception:
            priorities = list(handle.file_priorities())

        snapshots: list[TorrentFileSnapshot] = []
        for index in range(files.num_files()):
            snapshots.append(
                TorrentFileSnapshot(
                    index=index,
                    path=str(files.file_path(index)),
                    size=int(files.file_size(index)),
                    progress=int(progress[index]) if index < len(progress) else 0,
                    priority=int(priorities[index]) if index < len(priorities) else 0,
                )
            )
        return snapshots

    def tracker_statuses(self, torrent_id: str) -> list[dict[str, Any]]:
        handle = self._handles[torrent_id]
        rows: list[dict[str, Any]] = []
        try:
            trackers = handle.trackers()
        except Exception:
            trackers = []
        for tracker in trackers:
            url = str(getattr(tracker, "url", ""))
            rows.append(
                {
                    "url": url,
                    "tier": int(getattr(tracker, "tier", 0)),
                    "protocol": "UDP" if url.lower().startswith("udp:") else "HTTP",
                    "status": "Known",
                    "peers": "N/A",
                    "seeds": "N/A",
                }
            )
        return rows

    def peer_statuses(self, torrent_id: str) -> list[dict[str, Any]]:
        handle = self._handles[torrent_id]
        try:
            peers = handle.get_peer_info()
        except Exception:
            peers = []

        rows: list[dict[str, Any]] = []
        for peer in peers:
            ip_value = getattr(peer, "ip", "")
            if isinstance(ip_value, tuple):
                ip_text = f"{ip_value[0]}:{ip_value[1]}"
            else:
                ip_text = str(ip_value)
            rows.append(
                {
                    "country": "",
                    "ip": ip_text,
                    "port": ip_text.rsplit(":", 1)[-1] if ":" in ip_text else "",
                    "connection": str(getattr(peer, "connection_type", "")),
                    "client": str(getattr(peer, "client", "")),
                    "progress": float(getattr(peer, "progress", 0.0)),
                    "down_speed": int(getattr(peer, "down_speed", 0)),
                }
            )
        return rows

    def aggregate_speed(self) -> dict[str, int]:
        statuses = self.list_statuses()
        download_bps = sum(status.download_rate for status in statuses)
        upload_bps = sum(status.upload_rate for status in statuses)
        return {
            "download_bps": download_bps,
            "upload_bps": upload_bps,
            "total_bps": download_bps + upload_bps,
        }

    def poll_alerts(self) -> list[TorrentAlertSnapshot]:
        snapshots = [self._alert_snapshot(alert) for alert in self.session.pop_alerts()]
        for snapshot in snapshots:
            payload = snapshot.to_dict()
            self._emit("alert", payload)
            if snapshot.event != "alert":
                self._emit(snapshot.event, payload)
        return snapshots

    def tick(self) -> dict[str, Any]:
        alerts = [alert.to_dict() for alert in self.poll_alerts()]
        statuses = [status.to_dict() for status in self.list_statuses()]
        speed = self.aggregate_speed()

        for status in statuses:
            self._emit("status", status)
            previous_state = self._last_states.get(status["torrent_id"])
            if previous_state != status["state"]:
                self._last_states[status["torrent_id"]] = status["state"]
                self._emit(
                    "state_changed",
                    {
                        "torrent_id": status["torrent_id"],
                        "previous_state": previous_state,
                        "state": status["state"],
                    },
                )
        self._emit("speed", speed)

        return {
            "alerts": alerts,
            "statuses": statuses,
            "speed": speed,
        }

    def pause(self, torrent_id: str) -> None:
        self._handles[torrent_id].pause()
        self._emit("paused", {"torrent_id": torrent_id})

    def resume(self, torrent_id: str) -> None:
        self._handles[torrent_id].resume()
        self._emit("resumed", {"torrent_id": torrent_id})

    def set_speed_limits(
        self,
        torrent_id: str,
        *,
        download_bps: int | None = None,
        upload_bps: int | None = None,
    ) -> None:
        handle = self._handles[torrent_id]
        if download_bps is not None:
            handle.set_download_limit(int(download_bps))
        if upload_bps is not None:
            handle.set_upload_limit(int(upload_bps))
        self._emit(
            "limits_changed",
            {
                "torrent_id": torrent_id,
                "download_bps": download_bps,
                "upload_bps": upload_bps,
            },
        )

    def set_file_priority(self, torrent_id: str, file_index: int, priority: int) -> None:
        self._handles[torrent_id].file_priority(int(file_index), int(priority))
        self._emit(
            "file_priority_changed",
            {
                "torrent_id": torrent_id,
                "file_index": int(file_index),
                "priority": int(priority),
            },
        )

    def set_sequential_download(self, torrent_id: str, enabled: bool) -> None:
        handle = self._handles[torrent_id]
        if hasattr(handle, "set_sequential_download"):
            handle.set_sequential_download(bool(enabled))
        elif hasattr(self.lt, "torrent_flags"):
            flag = self.lt.torrent_flags.sequential_download
            if enabled:
                handle.set_flags(flag)
            else:
                handle.unset_flags(flag)
        self._emit("sequential_changed", {"torrent_id": torrent_id, "enabled": bool(enabled)})

    def move_storage(self, torrent_id: str, destination: str | Path) -> None:
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)
        self._handles[torrent_id].move_storage(str(destination))

    def force_recheck(self, torrent_id: str) -> None:
        self._handles[torrent_id].force_recheck()
        self._emit("recheck_requested", {"torrent_id": torrent_id})

    def request_resume_data(self, torrent_id: str) -> None:
        self._handles[torrent_id].save_resume_data()
        self._emit("resume_data_requested", {"torrent_id": torrent_id})

    def export_resume_data(self, torrent_id: str) -> str:
        handle = self._handles[torrent_id]
        resume_data = handle.write_resume_data()
        if isinstance(resume_data, dict):
            encoded = self.lt.bencode(resume_data)
        else:
            encoded = self.lt.write_resume_data(resume_data)
        return base64.b64encode(bytes(encoded)).decode("ascii")

    def remove(self, torrent_id: str, *, delete_files: bool = False) -> None:
        handle = self._handles.pop(torrent_id)
        self._last_states.pop(torrent_id, None)
        options = 0
        if delete_files and hasattr(self.lt, "options_t"):
            options = self.lt.options_t.delete_files
        self.session.remove_torrent(handle, options)
        self._emit("removed", {"torrent_id": torrent_id, "delete_files": delete_files})

    def close(self) -> None:
        for torrent_id in list(self._handles):
            self.remove(torrent_id)

    def _track(self, handle: Any) -> str:
        torrent_id = self._torrent_id(handle)
        self._handles[torrent_id] = handle
        self._emit("torrent_added", {"torrent_id": torrent_id})
        return torrent_id

    def _emit(self, event: str, payload: dict[str, Any]) -> None:
        for callback in self._hooks.get(event, []):
            callback(payload)
        for callback in self._hooks.get("*", []):
            callback({"event": event, **payload})

    def _set_torrent_flags(self, params: Any, *, paused: bool, sequential: bool) -> None:
        if not hasattr(self.lt, "torrent_flags"):
            return
        if paused:
            params.flags |= self.lt.torrent_flags.paused
        else:
            params.flags &= ~self.lt.torrent_flags.paused
        if sequential and hasattr(self.lt.torrent_flags, "sequential_download"):
            params.flags |= self.lt.torrent_flags.sequential_download

    def _torrent_id(self, handle: Any) -> str:
        try:
            return str(handle.info_hash())
        except Exception:
            hashes = handle.info_hashes()
            v1_hash = getattr(hashes, "v1", None)
            v2_hash = getattr(hashes, "v2", None)
            return str(v1_hash or v2_hash)

    def _snapshot(self, torrent_id: str, handle: Any) -> TorrentSnapshot:
        status = handle.status()
        download_rate = int(getattr(status, "download_rate", 0))
        total_wanted = int(getattr(status, "total_wanted", 0))
        total_wanted_done = int(getattr(status, "total_wanted_done", 0))
        remaining = max(total_wanted - total_wanted_done, 0)
        eta_seconds = int(remaining / download_rate) if download_rate > 0 else None
        return TorrentSnapshot(
            torrent_id=torrent_id,
            name=str(getattr(status, "name", "")),
            progress=float(getattr(status, "progress", 0.0)),
            download_rate=download_rate,
            upload_rate=int(getattr(status, "upload_rate", 0)),
            total_done=int(getattr(status, "total_done", 0)),
            total_wanted=total_wanted,
            total_wanted_done=total_wanted_done,
            all_time_download=int(getattr(status, "all_time_download", 0)),
            all_time_upload=int(getattr(status, "all_time_upload", 0)),
            num_peers=int(getattr(status, "num_peers", 0)),
            num_seeds=int(getattr(status, "num_seeds", 0)),
            num_connections=int(getattr(status, "num_connections", 0)),
            distributed_copies=float(getattr(status, "distributed_copies", 0.0)),
            state=str(getattr(status, "state", "")),
            paused=bool(getattr(status, "paused", False)),
            has_metadata=bool(getattr(status, "has_metadata", False)),
            is_finished=bool(getattr(status, "is_finished", False)),
            is_seeding=bool(getattr(status, "is_seeding", False)),
            save_path=str(getattr(status, "save_path", "")),
            eta_seconds=eta_seconds,
            error=str(getattr(status, "error", "")),
        )

    def _alert_snapshot(self, alert: Any) -> TorrentAlertSnapshot:
        torrent_id = None
        torrent_name = None
        handle = getattr(alert, "handle", None)
        if handle is not None:
            try:
                if handle.is_valid():
                    torrent_id = self._torrent_id(handle)
                    torrent_name = str(handle.status().name)
            except Exception:
                pass

        return TorrentAlertSnapshot(
            event=self._classify_alert(alert),
            category=alert.what() if hasattr(alert, "what") else type(alert).__name__,
            message=alert.message() if hasattr(alert, "message") else str(alert),
            torrent_id=torrent_id,
            torrent_name=torrent_name,
        )

    def _classify_alert(self, alert: Any) -> str:
        alert_events = {
            "add_torrent_alert": "torrent_added",
            "torrent_added_alert": "torrent_added",
            "metadata_received_alert": "metadata_received",
            "metadata_failed_alert": "metadata_failed",
            "file_progress_alert": "file_progress_alert",
            "file_completed_alert": "file_completed",
            "piece_finished_alert": "piece_finished",
            "state_changed_alert": "state_changed",
            "torrent_checked_alert": "checked",
            "torrent_finished_alert": "finished",
            "torrent_paused_alert": "paused",
            "torrent_resumed_alert": "resumed",
            "torrent_removed_alert": "removed",
            "torrent_deleted_alert": "deleted",
            "torrent_delete_failed_alert": "delete_failed",
            "torrent_error_alert": "error",
            "file_error_alert": "error",
            "file_renamed_alert": "file_renamed",
            "file_rename_failed_alert": "file_rename_failed",
            "file_prio_alert": "file_priority_changed",
            "save_resume_data_alert": "resume_data_ready",
            "save_resume_data_failed_alert": "resume_data_failed",
            "storage_moved_alert": "storage_moved",
            "storage_moved_failed_alert": "storage_move_failed",
            "tracker_reply_alert": "tracker_reply",
            "tracker_error_alert": "tracker_error",
            "tracker_warning_alert": "tracker_warning",
            "listen_succeeded_alert": "listen_succeeded",
            "listen_failed_alert": "listen_failed",
            "peer_connect_alert": "peer_connected",
            "peer_disconnected_alert": "peer_disconnected",
        }
        for class_name, event in alert_events.items():
            alert_class = getattr(self.lt, class_name, None)
            if alert_class is not None and isinstance(alert, alert_class):
                return event
        return "alert"
