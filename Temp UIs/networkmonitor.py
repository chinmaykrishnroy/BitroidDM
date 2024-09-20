import sys
import time
import requests
from PySide6.QtCore import QObject, QThread, Signal


class AppNetworkMonitor(QObject):
    connectivity_changed = Signal(bool)
    speed_changed = Signal(int)

    def __init__(self, interval=3, url="https://speed.hetzner.de/100MB.bin", parent=None):
        super().__init__(parent)
        self.interval = interval
        self.url = url
        self.monitor_thread = NetworkMonitorThread(self.interval, self.url)
        self.monitor_thread.connectivity_signal.connect(self.connectivity_changed)
        self.monitor_thread.speed_signal.connect(self.speed_changed)

    def start(self):
        self.monitor_thread.start()

    def stop(self):
        self.monitor_thread.stop()


class NetworkMonitorThread(QThread):
    connectivity_signal = Signal(bool)
    speed_signal = Signal(int)

    def __init__(self, interval, url):
        super().__init__()
        self.interval = interval
        self.url = url
        self.running = True

    def run(self):
        while self.running:
            # Check for internet connectivity by attempting to download a small part of the file
            try:
                start_time = time.time()
                # Downloading 1MB of the file to measure speed
                response = requests.get(self.url, stream=True, timeout=5)
                downloaded_size = 0
                chunk_size = 1024  # 1KB
                for chunk in response.iter_content(chunk_size):
                    downloaded_size += len(chunk)
                    if downloaded_size >= 1024 * 1024:  # Stop after 1MB
                        break
                end_time = time.time()
                download_time = end_time - start_time

                is_connected = True if download_time > 0 else False

                # Calculate speed in B/s
                download_speed = downloaded_size / download_time if download_time > 0 else 0
            except Exception as e:
                is_connected = False
                download_speed = 0

            # Emit connectivity status
            self.connectivity_signal.emit(is_connected)

            # Emit download speed
            self.speed_signal.emit(int(download_speed))

            time.sleep(self.interval)

    def stop(self):
        self.running = False
        self.wait()


# Example usage
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

    class NetworkWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.label = QLabel("Application Network Monitor")
            self.speed_label = QLabel("Speed: 0 B/s")
            self.connectivity_label = QLabel("Connected: False")
            layout = QVBoxLayout()
            layout.addWidget(self.label)
            layout.addWidget(self.speed_label)
            layout.addWidget(self.connectivity_label)
            self.setLayout(layout)

            self.monitor = AppNetworkMonitor()
            self.monitor.connectivity_changed.connect(self.update_connectivity)
            self.monitor.speed_changed.connect(self.update_speed)
            self.monitor.start()

        def update_connectivity(self, connected):
            self.connectivity_label.setText(f"Connected: {connected}")

        def update_speed(self, speed):
            self.speed_label.setText(f"Speed: {speed} B/s")

    app = QApplication(sys.argv)
    window = NetworkWidget()
    window.show()
    sys.exit(app.exec())
