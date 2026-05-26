import threading
import socket
import time
from dataclasses import dataclass
from PySide6.QtCore import Signal, QThread


@dataclass(frozen=True)
class AppNetworkSpeed:
    download_bps: int = 0
    upload_bps: int = 0

    @property
    def total_bps(self) -> int:
        return self.download_bps + self.upload_bps


class InternetChecker(QThread):
    connectivity_changed = Signal(bool)
    network_speed = Signal(object)

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.connected_to_internet = False
        self._speed_lock = threading.Lock()
        self._reported_download_bps = 0
        self._reported_upload_bps = 0
        self._interval_download_bytes = 0
        self._interval_upload_bytes = 0
        self._last_speed_sample = time.monotonic()

    def run(self):
        self.connected_to_internet = self.check_internet_connection()
        self.connectivity_changed.emit(self.connected_to_internet)
        while not self._stop_event.is_set():
            new_status = self.check_internet_connection()
            if new_status != self.connected_to_internet:
                self.connected_to_internet = new_status
                self.connectivity_changed.emit(self.connected_to_internet)
            if self.connected_to_internet: self.check_network_speed()
            else: self.network_speed.emit(AppNetworkSpeed())
            time.sleep(1)

    def stop(self):
        self._stop_event.set()
        self.quit()
        self.wait()

    @staticmethod
    def check_internet_connection():
        for host in ("1.1.1.1", "8.8.8.8"):
            try:
                with socket.create_connection((host, 53), timeout=1):
                    return True
            except OSError:
                continue
        return False

    def check_network_speed(self):
        now = time.monotonic()
        with self._speed_lock:
            elapsed = max(now - self._last_speed_sample, 0.001)
            download_bps = self._reported_download_bps + int(self._interval_download_bytes / elapsed)
            upload_bps = self._reported_upload_bps + int(self._interval_upload_bytes / elapsed)
            self._interval_download_bytes = 0
            self._interval_upload_bytes = 0
            self._last_speed_sample = now

        self.network_speed.emit(AppNetworkSpeed(download_bps, upload_bps))

    def set_app_network_rates(self, download_bps=0, upload_bps=0):
        with self._speed_lock:
            self._reported_download_bps = max(int(download_bps), 0)
            self._reported_upload_bps = max(int(upload_bps), 0)

    def record_app_transfer(self, download_bytes=0, upload_bytes=0):
        with self._speed_lock:
            self._interval_download_bytes += max(int(download_bytes), 0)
            self._interval_upload_bytes += max(int(upload_bytes), 0)
