from __future__ import annotations

import os
from pathlib import Path


class LibtorrentUnavailableError(RuntimeError):
    pass


_LOADED_LIBTORRENT = None
_DLL_DIR_USED: str | None = None
_DLL_HANDLE = None


def _candidate_dll_dirs() -> list[Path]:
    candidates: list[Path] = []
    env_dir = os.environ.get("BITROID_LIBTORRENT_DLL_DIR")
    if env_dir:
        candidates.append(Path(env_dir))

    project_root = Path(__file__).resolve().parents[2]
    candidates.extend(
        [
            project_root / "dlls",
            project_root / "vendor" / "libtorrent",
            project_root / "dev" / "libtorrent_lab" / "dlls",
        ]
    )
    return candidates


def _find_openssl_runtime_dir() -> tuple[str | None, object | None]:
    for candidate in _candidate_dll_dirs():
        if (
            (candidate / "libcrypto-1_1-x64.dll").exists()
            and (candidate / "libssl-1_1-x64.dll").exists()
        ):
            dll_handle = os.add_dll_directory(str(candidate)) if hasattr(os, "add_dll_directory") else None
            return str(candidate), dll_handle
    return None, None


def load_libtorrent():
    global _LOADED_LIBTORRENT, _DLL_DIR_USED, _DLL_HANDLE
    if _LOADED_LIBTORRENT is not None:
        return _LOADED_LIBTORRENT, _DLL_DIR_USED, _DLL_HANDLE

    try:
        import libtorrent as lt

        _LOADED_LIBTORRENT = lt
        _DLL_DIR_USED = "libtorrent package directory"
        _DLL_HANDLE = None
        return _LOADED_LIBTORRENT, _DLL_DIR_USED, _DLL_HANDLE
    except ImportError as first_error:
        dll_dir, dll_handle = _find_openssl_runtime_dir()
        try:
            import libtorrent as lt

            _LOADED_LIBTORRENT = lt
            _DLL_DIR_USED = dll_dir
            _DLL_HANDLE = dll_handle
            return _LOADED_LIBTORRENT, _DLL_DIR_USED, _DLL_HANDLE
        except ImportError as second_error:
            raise LibtorrentUnavailableError(
                "libtorrent could not be imported. On Windows, install libtorrent-windows-dll "
                "or provide OpenSSL DLLs through BITROID_LIBTORRENT_DLL_DIR."
            ) from second_error
