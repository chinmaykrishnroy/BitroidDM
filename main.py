if __name__ == "__main__":
    from bitroid.services.libtorrent_loader import LibtorrentUnavailableError, load_libtorrent

    try:
        load_libtorrent()
    except LibtorrentUnavailableError:
        pass

    from bitroid.app import run

    raise SystemExit(run())
