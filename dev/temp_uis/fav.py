import json
import os
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker

class FavoriteTorrent(QThread):
    favoriteListChanged = Signal(list)  # Signal to notify changes in the favorite list
    
    def __init__(self, json_file='favourites.json', parent=None):
        super().__init__(parent)
        self.json_file = json_file
        self.mutex = QMutex()  # Mutual exclusion lock for thread safety
        self.favorites = []
        self.load_favorites()  # Load the favorite torrents from file, or create a new file if not found
        
    def run(self):
        # Immediately emit the current list of favorites when the thread starts
        self.favoriteListChanged.emit(self.favorites)

    def load_favorites(self):
        """Load the favorites from the JSON file, or create a new file if it doesn't exist."""
        with QMutexLocker(self.mutex):  # Ensure thread safety
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r') as file:
                    try:
                        self.favorites = json.load(file)
                    except json.JSONDecodeError:
                        # If the file exists but is corrupt, reset it to an empty list
                        self.favorites = []
            else:
                # If the file doesn't exist, create an empty JSON file
                self.favorites = []
                self.save_favorites()
        self.favoriteListChanged.emit(self.favorites)  # Emit the updated list

    def add_favorite(self, result):
        """Add a torrent to favorites if it doesn't already exist."""
        with QMutexLocker(self.mutex):  # Ensure thread safety
            if not any(fav['magnet'] == result['magnet'] for fav in self.favorites):
                self.favorites.append(result)
                self.save_favorites()
                self.favoriteListChanged.emit(self.favorites)  # Emit the updated list

    def remove_favorite(self, magnet):
        """Remove a torrent from favorites by its magnet link."""
        with QMutexLocker(self.mutex):  # Ensure thread safety
            self.favorites = [fav for fav in self.favorites if fav['magnet'] != magnet]
            self.save_favorites()
            self.favoriteListChanged.emit(self.favorites)  # Emit the updated list

    def save_favorites(self):
        """Save the favorites list to the JSON file."""
        with open(self.json_file, 'w') as file:
            json.dump(self.favorites, file, indent=4)

# Example usage in a PySide6 application
# Assuming you connect signals and slots properly to update the UI, etc.

# Create an instance of the thread and connect signals
fav_thread = FavoriteTorrent()

# Connect signal to update the UI
fav_thread.favoriteListChanged.connect(lambda fav_list: print(f"Favorites updated: {fav_list}"))

# Start the thread (it will emit the current list immediately)
fav_thread.start()

# Adding a favorite torrent
fav_thread.add_favorite({
    "magnet": "magnet:?xt=urn:btih:7CAC56B95FB322733B88CE65DA2E7AF0EB2B6D61&...",
    "age": "8 years",
    "name": "Harry Potter 1-7 Audiolibros en Español",
    "size": "2.46 GB",
    "seeder": 5,
    "leecher": 0,
    "type": "Audio > Audio books",
    "site": "thepiratebay",
    "url": "https://thepiratebay.org/description.php?id=16549447",
    "trusted": False,
    "nsfw": False
})

# Removing a favorite torrent by its magnet link
fav_thread.remove_favorite("magnet:?xt=urn:btih:7CAC56B95FB322733B88CE65DA2E7AF0EB2B6D61&...")
