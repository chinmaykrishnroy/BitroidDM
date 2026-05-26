# Windows libtorrent runtime DLLs

These DLLs are required by the Windows Python `libtorrent==2.0.11` wheel:

- `libcrypto-1_1-x64.dll`
- `libssl-1_1-x64.dll`

Source used for this repository: PyPI package `libtorrent-windows-dll==0.0.3`.

The package installs these files into `Lib/site-packages/libtorrent/`, which lets `import libtorrent` and `lt.session(...)` work without copying DLLs from unrelated desktop applications.

SHA256 hashes of the committed files:

```text
93e2aa20251e1a0485828c3e29b60e17ff2f3ec1285455d059ffe1b1a24518eb  libcrypto-1_1-x64.dll
62e5635463c3a1b57e9e9886ed5c6aad2bb99cd5b082d207a3becac64c2f8928  libssl-1_1-x64.dll
```
