import json
import re
import requests
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker, QTimer
from typing import Dict, Any
from requests.exceptions import ConnectionError, Timeout, RequestException
import time

BASE_URL = "https://snowfl.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
SITE = "https://snowfl.com/"
REGEX_FOR_KEY = re.compile(r'findNextItem.*?"(.*?)"')
REGEX_FOR_JS = re.compile(r'((?:b.min.js).*)(?=")')

class Snowfl:
    def __init__(self):
        self.api_key = self.get_api_key()

    def get_api_key(self) -> str:
        try:
            session = requests.Session()
            home = session.get(url=SITE, headers=HEADERS)
            home.raise_for_status()
            home_text = home.text
            js_file_match = REGEX_FOR_JS.search(home_text)
            js_file_link = f"{SITE}{js_file_match.group(0)}"
            js_res = session.get(js_file_link)
            js_res.raise_for_status()
            js_text = js_res.text
            api_key_match = REGEX_FOR_KEY.search(js_text)
            return api_key_match.group(1)
        except (ConnectionError, Timeout) as e:
            raise ConnectionError("Network connection issue.")
        except RequestException as e:
            raise RequestException("An error occurred while retrieving the API key.")

    def parse(self, query: str, sort: str = "NONE", include_nsfw: bool = False) -> Dict[str, Any]:
        sort_option = self.get_sort_url_segment(sort)
        url = f"{BASE_URL}{self.api_key}/{query}{sort_option}{int(include_nsfw)}"
        session = requests.Session()
        try:
            res = session.get(url=url, headers=HEADERS)
            res.raise_for_status()
            return json.loads(res.text)
        except (ConnectionError, Timeout):
            raise ConnectionError("Failed to retrieve search results due to network issues.")
        except RequestException as e:
            raise RequestException(f"Error occurred while parsing data: {e}")

    @staticmethod
    def get_sort_url_segment(sort_key: str) -> str:
        sort_options = {
            "MAX_SEED": "SEED",
            "MAX_LEECH": "LEECH",
            "SIZE_ASC": "SIZE_ASC",
            "SIZE_DSC": "SIZE",
            "RECENT": "DATE",
            "NONE": "NONE",
        }
        sort_type = sort_options.get(sort_key, "NONE")
        return f"/DH5kKsJw/0/{sort_type}/NONE/"

class SearchThread(QThread):
    search_result = Signal(int, list, str)
    connectivity_changed = Signal(bool)
    speed_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.snowfl = Snowfl()
        self.mutex = QMutex()
        self.query = ""
        self.sort = "NONE"
        self.include_nsfw = False
        self._stop_flag = False
        self.previous_connectivity_status = None
        self.connectivity_timer = QTimer()
        self.connectivity_timer.timeout.connect(self.check_and_emit_connectivity_status)
        self.connectivity_timer.start(3000)
        self.speed_timer = QTimer()
        self.speed_timer.timeout.connect(self.update_speed)  # Periodically update speed
        self.speed_timer.start(1000)  # Emit speed every second
        self.current_speed = 0

    def run(self):
        """
        Run the search process in a thread.
        """
        with QMutexLocker(self.mutex):
            if not self.query:
                self.search_result.emit(0, [], "BLANK")
                return
            try:
                is_connected = self.check_connectivity()
                if is_connected != self.previous_connectivity_status:
                    self.connectivity_changed.emit(is_connected)
                    self.previous_connectivity_status = is_connected
                
                if not is_connected:
                    self.search_result.emit(0, [], "No internet connection.")
                    return

                # Start speed measurement
                start_time = time.time()
                results = self.snowfl.parse(self.query, self.sort, self.include_nsfw)
                end_time = time.time()

                # Speed calculation: bytes per second
                data_size = len(results)  # Assuming results is a bytes-like object
                elapsed_time = end_time - start_time
                self.current_speed = int(data_size / elapsed_time)  # Bytes per second

                self.search_result.emit(1, results, "OK")
            except Exception as e:
                print(f"Error occurred during search: {str(e)}")
                self.search_result.emit(0, [], str(e))

    def start_search(self, query: str, sort: str = "NONE", include_nsfw: bool = False):
        if self.isRunning():
            return
        self.query = query
        self.sort = sort
        self.include_nsfw = include_nsfw
        self._stop_flag = False
        self.start()

    def stop(self):
        self._stop_flag = True
        self.wait()

    def update_speed(self):
        """
        Emit the current speed every second, even if no search is running.
        """
        self.speed_changed.emit(self.current_speed)

    def check_and_emit_connectivity_status(self):
        """
        Check and emit connectivity status every 3 seconds.
        """
        is_connected = self.check_connectivity()
        if is_connected != self.previous_connectivity_status:
            self.connectivity_changed.emit(is_connected)
            self.previous_connectivity_status = is_connected

    def check_connectivity(self) -> bool:
        """
        Check if the network is connected.
        """
        try:
            requests.get('https://www.google.com', timeout=5)
            return True
        except (ConnectionError, Timeout, RequestException):
            return False


from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QApplication
from PySide6.QtCore import Qt

class NetworkStatusUI(QWidget):
    def __init__(self, search_thread):
        super().__init__()
        self.search_thread = search_thread
        
        # Set up the UI layout
        self.setWindowTitle("Network Status & Torrent Search")
        self.setGeometry(300, 300, 400, 300)

        # Connectivity label
        self.connectivity_label = QLabel("Checking Connectivity...", self)
        self.connectivity_label.setAlignment(Qt.AlignCenter)

        # Speed label
        self.speed_label = QLabel("Speed: 0 bps", self)
        self.speed_label.setAlignment(Qt.AlignCenter)

        # Search button for 'Harry Potter'
        self.search_button = QPushButton("Search Torrents for 'Harry Potter'", self)
        self.search_button.clicked.connect(self.start_search)

        # Search result area
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.connectivity_label)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_area)
        self.setLayout(layout)

        # Connect signals from the search thread
        self.search_thread.connectivity_changed.connect(self.update_connectivity_status)
        self.search_thread.speed_changed.connect(self.update_speed)
        self.search_thread.search_result.connect(self.display_search_result)

    def update_connectivity_status(self, is_connected):
        """
        Update the connectivity status label based on the signal.
        """
        if is_connected:
            self.connectivity_label.setText("Status: Online")
            self.connectivity_label.setStyleSheet("color: green;")
        else:
            self.connectivity_label.setText("Status: Offline")
            self.connectivity_label.setStyleSheet("color: red;")

    def update_speed(self, speed_bps):
        """
        Update the network speed label based on the signal.
        """
        self.speed_label.setText(f"Speed: {speed_bps} bps")

    def start_search(self):
        """
        Start the torrent search for 'Harry Potter'.
        """
        if self.search_thread.isRunning():
            return
        self.result_area.setText("Searching for 'Harry Potter' torrents...")
        self.search_thread.start_search(query="harry potter", sort="MAX_SEED", include_nsfw=False)

    def display_search_result(self, status_code, results, message):
        """
        Display the search results or error message.
        """
        if status_code == 1:
            # Check if the results is a list (torrents), then iterate through it
            if isinstance(results, list):
                if results:
                    result_text = "\n".join([f"{torrent['name']} - {torrent['size']} - Seeders: {torrent['seeder']}" for torrent in results])
                    self.result_area.setText(result_text)
                else:
                    self.result_area.setText("No torrents found for 'Harry Potter'.")
            else:
                self.result_area.setText("Unexpected data format.")
        else:
            # If search fails, display the error message
            self.result_area.setText(f"Error: {message}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Assuming 'search_thread' is the instance of SearchThread
    search_thread = SearchThread()  # Replace with your actual SearchThread object
    ui = NetworkStatusUI(search_thread)
    ui.show()

    # Start the thread to begin monitoring
    search_thread.start()

    sys.exit(app.exec())
