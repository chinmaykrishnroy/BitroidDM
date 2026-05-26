import threading
import socket
import time
import psutil
from PySide6.QtCore import QObject, Signal, QThread

class InternetChecker(QThread):
    connection_status_changed = Signal(bool)
    network_speed = Signal(int)  # Signal for network speed in B/s

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.connected_to_internet = False
        self.previous_bytes_sent = psutil.net_io_counters().bytes_sent
        self.previous_bytes_recv = psutil.net_io_counters().bytes_recv

    def run(self):
        while not self._stop_event.is_set():
            new_status = self.check_internet_connection()
            if new_status != self.connected_to_internet:
                self.connected_to_internet = new_status
                self.connection_status_changed.emit(self.connected_to_internet)

            self.check_network_speed()  # Emit network speed
            time.sleep(1)

    def stop(self):
        self._stop_event.set()

    @staticmethod
    def check_internet_connection():
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=1)
            return True
        except OSError:
            return False

    def check_network_speed(self):
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent
        bytes_recv = net_io.bytes_recv

        # Calculate the speed in bytes per second
        bytes_sent_per_sec = bytes_sent - self.previous_bytes_sent
        bytes_recv_per_sec = bytes_recv - self.previous_bytes_recv

        # Total network speed in bytes per second
        total_speed_bps = bytes_sent_per_sec + bytes_recv_per_sec

        # Emit the network speed signal
        self.network_speed.emit(total_speed_bps)

        # Update previous bytes values
        self.previous_bytes_sent = bytes_sent
        self.previous_bytes_recv = bytes_recv

# Example usage
def handle_connection_status_change(is_connected):
    if is_connected:
        print("Connected to the Internet")
    else:
        print("Disconnected from the Internet")

def handle_network_speed(speed):
    print(f"Network Speed: {speed} B/s")

# Ensure a QApplication instance exists
from PySide6.QtWidgets import QApplication
app = QApplication([])

internet_checker = InternetChecker()
internet_checker.connection_status_changed.connect(handle_connection_status_change)
internet_checker.network_speed.connect(handle_network_speed)
internet_checker.start()

app.exec()

# Remember to stop the thread when your application is closing
internet_checker.stop()
