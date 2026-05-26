from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from probe_libtorrent import SANDBOX_DIR, build_local_torrent, load_libtorrent
from torrent_engine import TorrentEngine


ENGINE_SANDBOX_DIR = SANDBOX_DIR / "engine"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    lt, dll_dir, _dll_handle = load_libtorrent()
    torrent_path = build_local_torrent(lt, ENGINE_SANDBOX_DIR)
    torrent_info = lt.torrent_info(str(torrent_path))
    magnet_uri = lt.make_magnet_uri(torrent_info)

    engine = TorrentEngine(ENGINE_SANDBOX_DIR / "downloads")
    result: dict[str, Any] = {
        "ok": False,
        "python": sys.version.split()[0],
        "libtorrent_version": getattr(lt, "version", "unknown"),
        "dll_dir_used": dll_dir,
        "checks": [],
    }

    try:
        torrent_id = engine.add_torrent_file(Path(torrent_path), paused=True)
        file_status = engine.status(torrent_id)
        require(file_status.name == torrent_info.name(), "torrent file name did not match torrent metadata")
        require(file_status.total_wanted == torrent_info.total_size(), "torrent size did not match metadata")
        require(file_status.paused, "torrent should be added in a paused state")
        require(len(engine.list_statuses()) == 1, "engine should be tracking one torrent")
        require(engine.file_statuses(torrent_id)[0].path.endswith("sample.txt"), "file_statuses() did not expose torrent files")
        require(engine.aggregate_speed()["total_bps"] == 0, "paused local torrent should have no transfer speed")
        result["checks"].append("add_torrent_file")

        engine.set_speed_limits(torrent_id, download_bps=1024 * 1024, upload_bps=512 * 1024)
        result["checks"].append("set_speed_limits")

        engine.set_file_priority(torrent_id, 0, 4)
        result["checks"].append("set_file_priority")

        engine.pause(torrent_id)
        paused_status = engine.status(torrent_id)
        require(paused_status.paused, "pause() did not leave torrent paused")
        result["checks"].append("pause")

        engine.resume(torrent_id)
        result["checks"].append("resume")

        engine.remove(torrent_id)
        require(engine.list_statuses() == [], "remove() did not clear the tracked torrent")
        result["checks"].append("remove")

        magnet_id = engine.add_magnet(magnet_uri, paused=True)
        magnet_status = engine.status(magnet_id)
        require(bool(magnet_status.torrent_id), "magnet torrent id should not be empty")
        require(magnet_status.paused, "magnet should be added in a paused state")
        result["checks"].append("add_magnet")

        engine.remove(magnet_id)
        require(engine.list_statuses() == [], "magnet remove() did not clear the tracked torrent")
        result["checks"].append("remove_magnet")

        result.update(
            {
                "ok": True,
                "torrent_id": torrent_id,
                "torrent_path": str(torrent_path),
                "snapshot": file_status.to_dict(),
                "magnet_prefix": magnet_uri[:96],
            }
        )
    finally:
        engine.close()

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
