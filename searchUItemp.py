from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QScrollArea, QLabel, QFrame, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QFont
from searchthread import SearchThread, Snowfl

class TorrentSearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.search_thread = SearchThread()
        self.search_thread.search_result.connect(self.handle_search_result)

        self.query_input = QLineEdit(self)
        self.query_input.setPlaceholderText("Enter search query...")

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.start_search)

        # Scroll area setup
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Widget inside scroll area to hold the tiles
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.query_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.scroll_area)

        self.setWindowTitle("Torrent Search App")
        self.resize(400, 600)

    @Slot(int, list)
    def handle_search_result(self, status: int, results: list):
        # Clear previous search results
        for i in reversed(range(self.scroll_layout.count())):
            widget_to_remove = self.scroll_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        if status == 1:
            if results:
                for result in results:
                    # Assuming the dictionary has a 'name' field
                    name = result.get('name', 'Unnamed')
                    self.add_tile(name)
            else:
                self.add_tile("No results found.")
        else:
            self.add_tile("Search failed or no results found.")

    def add_tile(self, text: str):
        tile = QLabel(text)
        tile.setFrameStyle(QFrame.Panel | QFrame.Raised)
        tile.setAlignment(Qt.AlignCenter)
        tile.setFont(QFont("Arial", 12))
        tile.setMinimumHeight(40)
        tile.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        self.scroll_layout.addWidget(tile)

    def start_search(self):
        query = self.query_input.text()
        if query:
            self.search_thread.start_search(query=query, sort="MAX_SEED", include_nsfw=True)

if __name__ == "__main__":
    app = QApplication([])
    window = TorrentSearchApp()
    window.show()
    app.exec()
