import threading
import socket
import time
import psutil
from PySide6.QtCore import QObject, Signal, QThread

class InternetChecker(QThread):
    connectivity_changed = Signal(bool)
    network_speed = Signal(int)

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.connected_to_internet = False
        self.previous_bytes_sent = psutil.net_io_counters().bytes_sent
        self.previous_bytes_recv = psutil.net_io_counters().bytes_recv

    def run(self):
        self.connected_to_internet = self.check_internet_connection()
        self.connectivity_changed.emit(self.connected_to_internet)
        while not self._stop_event.is_set():
            new_status = self.check_internet_connection()
            if new_status != self.connected_to_internet:
                self.connected_to_internet = new_status
                self.connectivity_changed.emit(self.connected_to_internet)
            if self.connected_to_internet: self.check_network_speed()
            else: self.network_speed.emit(0)
            time.sleep(1)

    def stop(self):
        self._stop_event.set()
        self.quit()
        self.wait()

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
        bytes_sent_per_sec = bytes_sent - self.previous_bytes_sent
        bytes_recv_per_sec = bytes_recv - self.previous_bytes_recv
        total_speed_bps = bytes_sent_per_sec + bytes_recv_per_sec
        self.network_speed.emit(total_speed_bps)
        self.previous_bytes_sent = bytes_sent
        self.previous_bytes_recv = bytes_recv
