import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QComboBox, QCheckBox
from searchthread import *
import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit,
    QComboBox, QCheckBox, QLabel, QScrollArea, QFrame, QGridLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QClipboard


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snowfl API Search")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.query_input = QLineEdit(self)
        self.query_input.setPlaceholderText("Enter your search query")
        layout.addWidget(self.query_input)

        self.sort_input = QComboBox(self)
        self.sort_input.addItems(
            ["NONE", "MAX_SEED", "MAX_LEECH", "SIZE_ASC", "SIZE_DSC", "RECENT"])
        layout.addWidget(self.sort_input)

        self.nsfw_checkbox = QCheckBox("Include NSFW", self)
        layout.addWidget(self.nsfw_checkbox)

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.start_search)
        layout.addWidget(self.search_button)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        self.scroll_content = QFrame(self.scroll_area)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.log_label = QLabel(self)
        self.log_label.setAlignment(Qt.AlignLeft)
        self.log_label.setStyleSheet(
            "QLabel { background-color : lightgray; padding: 5px; }")
        layout.addWidget(self.log_label)

        self.setLayout(layout)

    def start_search(self):
        query = self.query_input.text()
        sort = self.sort_input.currentText()
        include_nsfw = self.nsfw_checkbox.isChecked()

        self.thread = SnowflThread(
            query=query, sort=sort, include_nsfw=include_nsfw)
        self.thread.result_signal.connect(self.display_results)
        self.thread.log_signal.connect(self.display_log)
        self.thread.start()

    def display_results(self, results):
        for result in results:
            tile = self.create_result_tile(result)
            self.scroll_layout.addWidget(tile)

    def display_log(self, log):
        self.log_label.setText(log)

    def create_result_tile(self, result):
        tile = QFrame()
        tile.setFrameShape(QFrame.Box)
        tile.setLineWidth(1)
        layout = QGridLayout()

        fields = [
            ("Name", result.get("name", "")),
            ("Type", result.get("type", "")),
            ("Size", result.get("size", "")),
            ("Age", result.get("age", "")),
            ("Seeder", str(result.get("seeder", ""))),
            ("Leecher", str(result.get("leecher", ""))),
            ("Site", result.get("site", "")),
            ("Trusted", "Yes" if result.get("trusted", False) else "No"),
            ("NSFW", "Yes" if result.get("nsfw", False) else "No")
        ]

        for i, (label_text, value) in enumerate(fields):
            label = QLabel(f"{label_text}:")
            value_label = QLabel(str(value))
            layout.addWidget(label, i, 0)
            layout.addWidget(value_label, i, 1)

        magnet_button = QPushButton("Copy Magnet Link")
        magnet_button.clicked.connect(
            lambda: self.copy_to_clipboard(result.get("magnet", "")))
        layout.addWidget(magnet_button, len(fields), 0)

        url_button = QPushButton("Copy URL")
        url_button.clicked.connect(
            lambda: self.copy_to_clipboard(result.get("url", "")))
        layout.addWidget(url_button, len(fields), 1)

        tile.setLayout(layout)
        return tile

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.display_log(f"Copied to clipboard: {text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
