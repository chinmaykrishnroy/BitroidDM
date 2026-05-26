from __future__ import annotations

import argparse
import json
import time
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

from torrent_engine import TorrentEngine


UBUNTU_RELEASE = "26.04"
UBUNTU_RELEASE_NAME = "Ubuntu 26.04 LTS Resolute Raccoon"
UBUNTU_IMAGES = {
    "server": {
        "torrent_url": "https://releases.ubuntu.com/26.04/ubuntu-26.04-live-server-amd64.iso.torrent",
        "description": "64-bit PC server install image",
        "expected_size": "2.7G",
    },
    "desktop": {
        "torrent_url": "https://releases.ubuntu.com/26.04/ubuntu-26.04-desktop-amd64.iso.torrent",
        "description": "64-bit PC desktop image",
        "expected_size": "6.1G",
    },
}

REAL_SESSION_SETTINGS: dict[str, Any] = {
    "enable_dht": True,
    "enable_lsd": True,
    "enable_upnp": True,
    "enable_natpmp": True,
    "listen_interfaces": "0.0.0.0:0,[::]:0",
}

HOOK_CATALOG = {
    "torrent_added": "create a row in the downloads list",
    "metadata_received": "populate torrent details after adding a magnet",
    "metadata_failed": "show magnet metadata failures",
    "status": "refresh progress, peers, state, ETA, and totals",
    "speed": "drive app-specific download/upload speed meters",
    "file_progress": "render per-file progress and file list state",
    "file_priority_changed": "support skip/normal/high priority file selection",
    "file_renamed": "sync file rename operations",
    "file_rename_failed": "surface file rename failures",
    "state_changed": "update status chips such as checking/downloading/finished",
    "checked": "finish force-recheck/checking flows",
    "alert": "surface generic libtorrent events for diagnostics",
    "tracker_reply": "show tracker availability and seed/peer discovery",
    "tracker_error": "surface tracker failures without crashing the client",
    "tracker_warning": "surface tracker warnings without crashing the client",
    "listen_succeeded": "confirm incoming port binding",
    "listen_failed": "surface port binding failures",
    "peer_connected": "confirm peer connectivity",
    "peer_disconnected": "track peer churn",
    "piece_finished": "drive fine-grained progress updates",
    "file_completed": "mark individual files complete",
    "finished": "mark a torrent complete and optionally seed",
    "resume_data_requested": "begin save/resume state persistence",
    "resume_data_ready": "persist resume data for next launch",
    "resume_data_failed": "surface resume persistence failures",
    "storage_moved": "support changing download location",
    "storage_move_failed": "surface move-storage failures",
    "error": "show actionable torrent/storage errors",
    "limits_changed": "sync per-torrent speed limit controls",
    "paused": "reflect pause commands",
    "resumed": "reflect resume commands",
    "removed": "remove download rows and cleanup state",
    "deleted": "confirm delete-data cleanup",
    "delete_failed": "surface failed delete-data cleanup",
}

CRITICAL_HOOKS = {"torrent_added", "status", "speed", "file_progress", "state_changed", "alert"}


def default_download_dir() -> Path:
    downloads = Path.home() / "Downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    return downloads


def fetch_torrent_file(url: str, destination_dir: Path, *, refresh: bool = False) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)
    filename = url.rsplit("/", 1)[-1]
    destination = destination_dir / filename
    if destination.exists() and destination.stat().st_size > 0 and not refresh:
        return destination

    request = urllib.request.Request(url, headers={"User-Agent": "BitroidDM libtorrent lab"})
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    with urllib.request.urlopen(request, timeout=60) as response:
        temporary.write_bytes(response.read())
    temporary.replace(destination)
    return destination


def human_speed(value: int) -> str:
    units = ["B/s", "KB/s", "MB/s", "GB/s"]
    speed = float(max(value, 0))
    unit_index = 0
    while speed >= 1024 and unit_index < len(units) - 1:
        speed /= 1024
        unit_index += 1
    return f"{speed:.2f} {units[unit_index]}"


def summarize_samples(samples: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    return {event: values[:3] for event, values in samples.items() if values}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a real Ubuntu torrent through the BitroidDM dev engine.")
    parser.add_argument("--image", choices=sorted(UBUNTU_IMAGES), default="server")
    parser.add_argument("--download-dir", type=Path, default=default_download_dir())
    parser.add_argument("--max-seconds", type=int, default=180)
    parser.add_argument("--min-downloaded", type=int, default=5 * 1024 * 1024)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--complete", action="store_true", help="Run until the image fully downloads or max-seconds expires.")
    parser.add_argument("--refresh-torrent", action="store_true", help="Fetch a fresh .torrent file even if one already exists.")
    parser.add_argument("--report", type=Path, default=Path(__file__).resolve().parent / "live_report.json")
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    image = UBUNTU_IMAGES[args.image]
    download_dir = args.download_dir.expanduser().resolve()
    torrent_file = fetch_torrent_file(image["torrent_url"], download_dir, refresh=args.refresh_torrent)

    hook_counts: Counter[str] = Counter()
    hook_samples: dict[str, list[dict[str, Any]]] = {event: [] for event in HOOK_CATALOG}
    largest_download_bps = 0
    largest_upload_bps = 0

    def record_hook(event: str):
        def _record(payload: dict[str, Any]) -> None:
            hook_counts[event] += 1
            if len(hook_samples[event]) < 3:
                hook_samples[event].append(payload)
        return _record

    engine = TorrentEngine(download_dir=download_dir, session_settings=REAL_SESSION_SETTINGS)
    engine.enable_client_alerts()
    for event in HOOK_CATALOG:
        engine.on(event, record_hook(event))

    torrent_id = engine.add_torrent_file(torrent_file, paused=False)
    target_files = engine.file_statuses(torrent_id)
    target_paths = [str(download_dir / file.path) for file in target_files]
    start_snapshot = engine.status(torrent_id)
    start_done = start_snapshot.total_wanted_done
    started_at = time.monotonic()
    final_snapshot = start_snapshot
    timeout = False

    try:
        while True:
            tick = engine.tick()
            final_snapshot = engine.status(torrent_id)
            speed = tick["speed"]
            largest_download_bps = max(largest_download_bps, int(speed["download_bps"]))
            largest_upload_bps = max(largest_upload_bps, int(speed["upload_bps"]))
            checked_or_downloaded_this_run = max(final_snapshot.total_wanted_done - start_done, 0)
            payload_downloaded_this_run = int(final_snapshot.all_time_download)
            elapsed = time.monotonic() - started_at

            if not args.quiet:
                progress = final_snapshot.progress * 100
                print(
                    f"{elapsed:6.1f}s {progress:6.2f}% "
                    f"down={human_speed(speed['download_bps'])} up={human_speed(speed['upload_bps'])} "
                    f"peers={final_snapshot.num_peers} seeds={final_snapshot.num_seeds} "
                    f"state={final_snapshot.state}"
                )

            critical_ready = CRITICAL_HOOKS.issubset(set(hook_counts))
            transfer_ready = payload_downloaded_this_run >= args.min_downloaded or final_snapshot.is_finished
            if final_snapshot.is_finished:
                break
            if not args.complete and critical_ready and transfer_ready and largest_download_bps > 0:
                break
            if elapsed >= args.max_seconds:
                timeout = True
                break
            time.sleep(args.interval)
    finally:
        engine.close()

    observed_hooks = sorted(event for event, count in hook_counts.items() if count > 0)
    missing_critical_hooks = sorted(CRITICAL_HOOKS - set(observed_hooks))
    checked_or_downloaded_this_run = max(final_snapshot.total_wanted_done - start_done, 0)
    payload_downloaded_this_run = int(final_snapshot.all_time_download)
    passed = not missing_critical_hooks and largest_download_bps > 0 and (payload_downloaded_this_run >= args.min_downloaded or final_snapshot.is_finished)

    report = {
        "ok": passed,
        "timed_out": timeout,
        "release": UBUNTU_RELEASE_NAME,
        "image": args.image,
        "description": image["description"],
        "expected_size": image["expected_size"],
        "torrent_url": image["torrent_url"],
        "torrent_file": str(torrent_file),
        "download_dir": str(download_dir),
        "target_paths": target_paths,
        "torrent_id": torrent_id,
        "elapsed_seconds": round(time.monotonic() - started_at, 1),
        "payload_downloaded_this_run": payload_downloaded_this_run,
        "checked_or_downloaded_this_run": checked_or_downloaded_this_run,
        "largest_download_bps": largest_download_bps,
        "largest_upload_bps": largest_upload_bps,
        "final_snapshot": final_snapshot.to_dict(),
        "hook_catalog": HOOK_CATALOG,
        "hook_counts": dict(sorted(hook_counts.items())),
        "observed_hooks": observed_hooks,
        "missing_critical_hooks": missing_critical_hooks,
        "sample_payloads": summarize_samples(hook_samples),
    }

    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
