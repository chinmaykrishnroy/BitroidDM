# BitroidDM

BitroidDM is a PySide6 desktop torrent search, download, file browsing, and media utility. The app is being shaped into a full Bitroid Studio-style desktop client with an internal libtorrent engine, a custom themed interface, a file manager, and a wired media player.

## Current Status

The original Python 3.11+ libtorrent blocker has been resolved for Windows by using the proper `libtorrent-windows-dll` runtime package. The internal downloader is validated in the dev lab and is ready for UI integration, but the production downloads screen is still the next step.

## What Has Been Done

- Reorganized the app into a professional package structure under `bitroid/`, with dev prototypes moved under `dev/`.
- Reworked app paths so runtime state uses the user's OS data directories instead of hardcoded project paths.
- Improved custom window behavior, title bar dragging, resize cursors, and Windows shadow handling.
- Rebuilt the file manager around layer-by-layer directory browsing with folders and files shown together.
- Added Explorer-like path dropdown behavior, context menus, rename handling, properties UI, and responsive elided filenames.
- Wired the PySide6 media player controls, playlist behavior, light/dark player styling, repeat/shuffle/lock controls, and state persistence hooks.
- Tightened dropdown/menu spacing and themed properties dialogs.
- Added app-specific network speed reporting instead of whole-system `psutil.net_io_counters()` traffic.
- Built and tested a dev libtorrent engine with torrent files, magnets, progress, file progress, speed, peers, tracker events, pause/resume/remove, speed limits, file priorities, storage movement, recheck, and resume-data hooks.
- Validated the engine against an official Ubuntu 26.04 LTS torrent in the OS Downloads directory.

## Windows Libtorrent Runtime DLLs

Windows needs these OpenSSL runtime DLLs for the Python `libtorrent==2.0.11` wheel:

- `libcrypto-1_1-x64.dll`
- `libssl-1_1-x64.dll`

They are committed under `vendor/windows/libtorrent/` and were sourced from the PyPI package `libtorrent-windows-dll==0.0.3`. See `vendor/windows/libtorrent/SOURCE.md` for hashes and source notes.

The preferred install path is still dependency-based:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

The committed DLLs are included so packaged Windows builds and future CI/release scripts have a stable runtime source in the repository.

## Development Setup

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe main.py
```

## Torrent Engine Lab

The isolated downloader work lives in `dev/libtorrent_lab/`.

Useful checks:

```powershell
.\venv\Scripts\python.exe -B dev\libtorrent_lab\probe_libtorrent.py
.\venv\Scripts\python.exe -B dev\libtorrent_lab\test_torrent_engine.py
.\venv\Scripts\python.exe -B dev\libtorrent_lab\run_ubuntu_live_test.py
```

The live Ubuntu test uses the official Ubuntu 26.04 LTS torrent, saves into the OS Downloads directory, and stops once critical hooks plus real payload transfer are observed. It does not need to download the full ISO unless run with `--complete`.

## Verification Used

```powershell
.\venv\Scripts\python.exe -B -m py_compile main.py bitroid\app.py bitroid\services\network.py dev\libtorrent_lab\*.py
.\venv\Scripts\pyside6-uic.exe bitroid\ui\designer\interface.ui -o $env:TEMP\bitroiddm_uic_check.py
```

Qt Designer currently emits one known warning from the existing UI file:

```text
Buddy assignment: '' is not a valid widget.
```

## Next Step

Integrate the validated `TorrentEngine` behind a PySide worker/service and wire the Downloads UI so BitroidDM handles magnet/torrent downloads internally instead of opening the system torrent app.
