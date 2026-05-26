import sys
import psutil
import time
from PySide6.QtCore import QObject, QThread, Signal


class AppNetworkMonitor(QObject):
    connectivity_changed = Signal(bool)
    speed_changed = Signal(int)

    def __init__(self, interval=3, parent=None):
        super().__init__(parent)
        self.interval = interval
        self.is_connected = False
        self.process = psutil.Process()
        self.previous_recv, self.previous_sent = self.get_network_usage()
        self.monitor_thread = NetworkMonitorThread(self.interval, self.previous_recv, self.previous_sent, self.process)
        self.monitor_thread.connectivity_signal.connect(self.connectivity_changed)
        self.monitor_thread.speed_signal.connect(self.speed_changed)

    def get_network_usage(self):
        try:
            net_io_counters = self.process.io_counters()
            return net_io_counters.read_bytes, net_io_counters.write_bytes
        except psutil.AccessDenied:
            return 0, 0

    def start(self):
        self.monitor_thread.start()

    def stop(self):
        self.monitor_thread.stop()


class NetworkMonitorThread(QThread):
    connectivity_signal = Signal(bool)
    speed_signal = Signal(int)

    def __init__(self, interval, previous_recv, previous_sent, process):
        super().__init__()
        self.interval = interval
        self.previous_recv = previous_recv
        self.previous_sent = previous_sent
        self.process = process
        self.running = True

    def run(self):
        while self.running:
            try:
                psutil.net_if_addrs()
                is_connected = True
            except Exception:
                is_connected = False
            self.connectivity_signal.emit(is_connected)
            current_recv, current_sent = self.get_network_usage()
            download_speed = (current_recv - self.previous_recv) / self.interval
            self.previous_recv = current_recv
            self.speed_signal.emit(int(download_speed))
            time.sleep(self.interval)

    def get_network_usage(self):
        try:
            net_io_counters = self.process.io_counters()
            return net_io_counters.read_bytes, net_io_counters.write_bytes
        except psutil.AccessDenied:
            return 0, 0

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
