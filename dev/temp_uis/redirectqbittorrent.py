from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QEvent, QTimer
import sys
import webbrowser

class TorrentDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set up the main window
        self.setWindowTitle("Magnet Link Downloader")
        self.setGeometry(100, 100, 300, 100)
        
        # Create a central widget and layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        
        # Magnet link button
        self.magnet_link_btn = QPushButton("Download with qBittorrent")
        self.magnet_link_btn.installEventFilter(self)  # Install event filter for double-click
        self.layout.addWidget(self.magnet_link_btn)
        
        # Magnet link to use
        self.magnet_link = "magnet:?xt=urn:btih:491aa0e19cbdb03b100961db82315c08643a6139&dn=Oppenheimer.2023.1080p.BluRay.DD5.1.x264-GalaxyRG%5BTGx%5D&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2920%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce"

        # Timer to differentiate between single and double clicks
        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.open_magnet_link)  # Single-click action

    def open_magnet_link(self):
        # Open the magnet link with the system's default torrent downloader
        webbrowser.open(self.magnet_link)
        print(f"Opening magnet link: {self.magnet_link}")
    
    def eventFilter(self, obj, event):
        if obj == self.magnet_link_btn:
            if event.type() == QEvent.Type.MouseButtonDblClick:
                self.click_timer.stop()  # Stop single-click action if double-clicked
                self.copy_magnet_link_to_clipboard()
                return True
            elif event.type() == QEvent.Type.MouseButtonPress:
                self.click_timer.start(250)  # Start timer for single-click
        return super().eventFilter(obj, event)

    def copy_magnet_link_to_clipboard(self):
        # Copy the magnet link to the clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(self.magnet_link)
        print(f"Magnet link copied to clipboard: {self.magnet_link}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TorrentDownloaderApp()
    window.show()
    sys.exit(app.exec())
