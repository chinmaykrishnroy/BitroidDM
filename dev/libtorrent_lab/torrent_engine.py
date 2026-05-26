from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

try:
    from probe_libtorrent import load_libtorrent
except ImportError:  # pragma: no cover - useful when imported as a package later.
    from .probe_libtorrent import load_libtorrent


DEFAULT_SESSION_SETTINGS: dict[str, Any] = {
    "enable_dht": False,
    "enable_lsd": False,
    "enable_upnp": False,
    "enable_natpmp": False,
    "listen_interfaces": "127.0.0.1:0",
}

DEFAULT_TORRENT_OPTIONS: dict[str, Any] = {
    "paused": True,
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
    """Small libtorrent wrapper shaped for the future PyQt worker thread."""

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
        paused: bool = DEFAULT_TORRENT_OPTIONS["paused"],
    ) -> str:
        torrent_info = self.lt.torrent_info(str(torrent_path))
        params = self.lt.add_torrent_params()
        params.ti = torrent_info
        params.save_path = str(Path(save_path) if save_path else self.download_dir)
        self._set_paused_flag(params, paused)
        return self._track(self.session.add_torrent(params))

    def add_magnet(
        self,
        magnet_uri: str,
        save_path: str | Path | None = None,
        *,
        paused: bool = DEFAULT_TORRENT_OPTIONS["paused"],
    ) -> str:
        params = self.lt.parse_magnet_uri(magnet_uri)
        params.save_path = str(Path(save_path) if save_path else self.download_dir)
        self._set_paused_flag(params, paused)
        return self._track(self.session.add_torrent(params))

    def status(self, torrent_id: str) -> TorrentSnapshot:
        handle = self._handles[torrent_id]
        return self._snapshot(torrent_id, handle)

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

    def tick(self, *, include_files: bool = True) -> dict[str, Any]:
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

        files: dict[str, list[dict[str, Any]]] = {}
        if include_files:
            for torrent_id in list(self._handles):
                file_snapshots = [file.to_dict() for file in self.file_statuses(torrent_id)]
                files[torrent_id] = file_snapshots
                if file_snapshots:
                    self._emit("file_progress", {"torrent_id": torrent_id, "files": file_snapshots})

        return {
            "alerts": alerts,
            "statuses": statuses,
            "speed": speed,
            "files": files,
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

    def rename_file(self, torrent_id: str, file_index: int, name: str) -> None:
        self._handles[torrent_id].rename_file(int(file_index), str(name))

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

    def _set_paused_flag(self, params: Any, paused: bool) -> None:
        if not hasattr(self.lt, "torrent_flags"):
            return
        if paused:
            params.flags |= self.lt.torrent_flags.paused
        else:
            params.flags &= ~self.lt.torrent_flags.paused

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
