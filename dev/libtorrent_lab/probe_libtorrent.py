from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path


LAB_DIR = Path(__file__).resolve().parent
SANDBOX_DIR = LAB_DIR / "sandbox"

DLL_CANDIDATES = [
    os.environ.get("BITROID_LIBTORRENT_DLL_DIR"),
    str(LAB_DIR / "dlls"),
]


def find_openssl_runtime_dir() -> tuple[str | None, object | None]:
    for candidate in DLL_CANDIDATES:
        if not candidate:
            continue
        path = Path(candidate)
        if (path / "libcrypto-1_1-x64.dll").exists() and (path / "libssl-1_1-x64.dll").exists():
            dll_handle = os.add_dll_directory(str(path)) if hasattr(os, "add_dll_directory") else None
            return str(path), dll_handle
    return None, None


def load_libtorrent():
    try:
        import libtorrent as lt
        return lt, "libtorrent package directory", None
    except ImportError as error:
        first_error = str(error)

    dll_dir, dll_handle = find_openssl_runtime_dir()
    try:
        import libtorrent as lt
    except ImportError as error:
        payload = {
            "ok": False,
            "stage": "import",
            "error": str(error),
            "first_error": first_error,
            "hint": "libtorrent 2.0.11 imports require libcrypto-1_1-x64.dll and libssl-1_1-x64.dll on Windows.",
            "dll_dir_used": dll_dir,
        }
        print(json.dumps(payload, indent=2))
        raise SystemExit(1)
    return lt, dll_dir, dll_handle


def build_local_torrent(lt, sandbox_dir: Path | None = None):
    sandbox_dir = sandbox_dir or SANDBOX_DIR
    shutil.rmtree(sandbox_dir, ignore_errors=True)
    content_dir = sandbox_dir / "content"
    content_dir.mkdir(parents=True)
    (content_dir / "sample.txt").write_text("hello from BitroidDM libtorrent lab\n", encoding="utf-8")

    file_storage = lt.file_storage()
    lt.add_files(file_storage, str(content_dir))

    torrent = lt.create_torrent(file_storage)
    torrent.set_creator("BitroidDM libtorrent lab")
    lt.set_piece_hashes(torrent, str(content_dir.parent))

    torrent_path = sandbox_dir / "sample.torrent"
    torrent_path.write_bytes(lt.bencode(torrent.generate()))
    return torrent_path


def probe_session(lt, torrent_path: Path, sandbox_dir: Path | None = None):
    sandbox_dir = sandbox_dir or SANDBOX_DIR
    settings = {
        "enable_dht": False,
        "enable_lsd": False,
        "enable_upnp": False,
        "enable_natpmp": False,
        "listen_interfaces": "127.0.0.1:0",
    }
    session = lt.session(settings)
    torrent_info = lt.torrent_info(str(torrent_path))

    params = lt.add_torrent_params()
    params.ti = torrent_info
    params.save_path = str(sandbox_dir / "downloads")
    if hasattr(lt, "torrent_flags"):
        params.flags |= lt.torrent_flags.paused

    handle = session.add_torrent(params)
    status = handle.status()
    result = {
        "name": torrent_info.name(),
        "num_files": torrent_info.num_files(),
        "total_size": torrent_info.total_size(),
        "handle_valid": handle.is_valid(),
        "progress": float(status.progress),
        "state": str(status.state),
    }
    magnet_uri = lt.make_magnet_uri(torrent_info)
    result["magnet_prefix"] = magnet_uri[:96]
    result["magnet_parse_ok"] = bool(lt.parse_magnet_uri(magnet_uri).info_hashes)
    session.remove_torrent(handle)
    return result


def main() -> int:
    lt, dll_dir, dll_handle = load_libtorrent()
    torrent_path = build_local_torrent(lt, SANDBOX_DIR / "probe")
    session_result = probe_session(lt, torrent_path, SANDBOX_DIR / "probe")

    payload = {
        "ok": True,
        "python": sys.version.split()[0],
        "libtorrent_version": getattr(lt, "version", "unknown"),
        "dll_dir_used": dll_dir,
        "torrent_path": str(torrent_path),
        "capabilities": {
            name: hasattr(lt, name)
            for name in (
                "session",
                "add_torrent_params",
                "torrent_info",
                "parse_magnet_uri",
                "make_magnet_uri",
                "create_torrent",
                "set_piece_hashes",
            )
        },
        "session_probe": session_result,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
