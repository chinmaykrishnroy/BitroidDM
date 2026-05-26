import json
import os
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker
from bitroid.core.paths import app_data_dir

class FavoriteTorrent(QThread):
    favoriteListChanged = Signal(list)
    torrentExists = Signal(bool)

    def __init__(self, json_file=None, parent=None):
        super().__init__(parent)
        self.json_file = json_file or str(app_data_dir() / 'favourites.json')
        self.mutex = QMutex()
        self.favorites = []
        self.running = True
        self.load_favorites()
        
    def run(self):
        # while self.running: pass
        self.favoriteListChanged.emit(self.favorites)

    def load_favorites(self):
        with QMutexLocker(self.mutex):
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as file:
                    try:
                        self.favorites = json.load(file)
                        if not isinstance(self.favorites, list):
                            self.favorites = []
                    except json.JSONDecodeError:
                        self.favorites = []
            else:
                self.favorites = []
                self.save_favorites()
        self.favoriteListChanged.emit(self.favorites)

    def add_favorite(self, result):
        with QMutexLocker(self.mutex):
            magnet = result.get('magnet')
            exists = bool(magnet) and any(fav.get('magnet') == magnet for fav in self.favorites)
            self.torrentExists.emit(exists)

            if magnet and not exists:
                self.favorites.append(result)
                self.save_favorites()
                self.favoriteListChanged.emit(self.favorites)

    def remove_favorite(self, magnet):
        with QMutexLocker(self.mutex):
            self.favorites = [fav for fav in self.favorites if fav['magnet'] != magnet]
            self.save_favorites()
            self.favoriteListChanged.emit(self.favorites)

    def save_favorites(self):
        directory = os.path.dirname(self.json_file)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.json_file, 'w', encoding='utf-8') as file:
            json.dump(self.favorites, file, indent=4)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.running = False
        self.quit()
        self.wait()
