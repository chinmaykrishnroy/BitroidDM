# BitroidDM Libtorrent Lab

This folder is for isolated experiments before wiring torrent downloading into the app runtime.

## Current findings

- `pip install libtorrent` installs `libtorrent 2.0.11` for Python 3.12 on Windows.
- The wheel does not bundle OpenSSL 1.1 DLLs.
- `libtorrent-windows-dll 0.0.3` supplies `libcrypto-1_1-x64.dll` and `libssl-1_1-x64.dll` in the `libtorrent` package directory.
- After installing `libtorrent-windows-dll`, direct `import libtorrent` and `lt.session(...)` work without borrowing DLLs from unrelated applications.
- Local `.torrent` generation, magnet generation/parsing, session creation, and adding a paused torrent handle all work.

## Probe

Run:

```powershell
.\venv\Scripts\python.exe -m pip install -r dev\libtorrent_lab\requirements-lab.txt
.\venv\Scripts\python.exe -B dev\libtorrent_lab\probe_libtorrent.py
```

The probe creates `dev/libtorrent_lab/sandbox/probe/sample.torrent`, starts a local libtorrent session with DHT/LSD/UPnP/NAT-PMP disabled, adds the torrent paused, reports capabilities, and exits.

## Engine smoke test

Run:

```powershell
.\venv\Scripts\python.exe -B dev\libtorrent_lab\test_torrent_engine.py
```

The engine test wraps libtorrent behind `TorrentEngine`, writes its generated files under `dev/libtorrent_lab/sandbox/engine/`, then checks local `.torrent` add, status snapshots, pause, resume, remove, magnet add, and cleanup without contacting the public torrent network.

## Live Ubuntu torrent test

Run:

```powershell
.\venv\Scripts\python.exe -B dev\libtorrent_lab\run_ubuntu_live_test.py
```

By default this fetches the official Ubuntu 26.04 LTS server `.torrent`, saves the actual image into the OS Downloads directory, and stops after the critical client hooks plus a small real transfer are observed. Use `--image desktop` for the larger desktop image or `--complete --max-seconds 7200` when you intentionally want the test to keep running until the ISO is complete.

The live test records hook coverage for torrent rows, magnet metadata, status updates, app-specific download/upload speed, per-file progress, file priority/rename events, state changes, tracker events, port binding, peer events, resume-data persistence, storage moves, completion, pause/resume/remove, delete-data cleanup, speed limits, and error handling. It writes a generated report to `dev/libtorrent_lab/live_report.json`, which is ignored by git.

## Integration notes

- Keep libtorrent work off the Qt UI thread. Run `TorrentEngine` inside a worker object or service thread and emit progress snapshots to the UI.
- Store user-facing defaults in JSON-backed settings before moving this from `dev/` into the main app: download directory, listen interface, DHT/LSD/UPnP/NAT-PMP, connection limits, queue limits, and speed limits.
- Use `libtorrent-windows-dll` for Windows OpenSSL runtime DLLs instead of copying DLLs from unrelated installed apps.
- Feed `TorrentEngine.aggregate_speed()` into the app speed monitor so the footer shows Bitroid-specific traffic rather than machine-wide network traffic.
