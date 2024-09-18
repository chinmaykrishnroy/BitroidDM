import sys
import json
import logging
import re
from typing import Any, Dict, Optional
from PySide6.QtCore import Qt, QThread, Signal, QMutex
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QScrollArea, QFrame
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from functools import partial

# Configuration
BASE_URL = "https://snowfl.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
SITE = "https://snowfl.com/"
REGEX_FOR_KEY = re.compile(r'findNextItem.*?"(.*?)"')
REGEX_FOR_JS = re.compile(r'((?:b.min.js).*)(?=")')

# Logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Custom exceptions
class ApiError(Exception):
    pass

class FetchError(Exception):
    pass

# Utility function to create a requests session with retry
def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Thread for fetching API key and torrent results
class SnowflWorker(QThread):
    results_ready = Signal(list)

    def __init__(self, query, sort, include_nsfw):
        super().__init__()
        self.query = query
        self.sort = sort
        self.include_nsfw = include_nsfw
        self.api_key = None
        self.mutex = QMutex()

    def run(self):
        try:
            self.mutex.lock()
            self.api_key = self.get_api_key()
            if not self.api_key:
                raise ApiError("Failed to obtain API key")
            data = self.parse(self.query, self.sort, self.include_nsfw)
            self.results_ready.emit(data)
        except (FetchError, ApiError) as e:
            logger.error(e)
        finally:
            self.mutex.unlock()

    def get_api_key(self) -> str:
        session = requests_retry_session()
        home = session.get(url=SITE, headers=HEADERS)
        if home.status_code != 200:
            raise FetchError(f"Error in fetching homepage: Status {home.status_code}")
        js_file_match = REGEX_FOR_JS.search(home.text)
        if not js_file_match:
            raise ApiError("JS file link not found in homepage")
        js_file_link = f"{SITE}{js_file_match.group(0)}"
        js_res = session.get(js_file_link)
        if js_res.status_code != 200:
            raise FetchError(f"Error in fetching JS file: Status {js_res.status_code}")
        api_key_match = REGEX_FOR_KEY.search(js_res.text)
        if not api_key_match:
            raise ApiError("API key not found in JS file")
        return api_key_match.group(1)

    def parse(self, query: str, sort: str = "NONE", include_nsfw: bool = False) -> list[Dict[str, Any]]:
        if len(query) <= 2:
            raise FetchError("Query should be of length >= 3")
        sort_option = self.get_sort_url_segment(sort)
        include_nsfw_flag = 1 if include_nsfw else 0
        url = f"{BASE_URL}{self.api_key}/{query}{sort_option}{include_nsfw_flag}"
        logger.info(f"URL: {url}")
        session = requests_retry_session()
        res = session.get(url=url, headers=HEADERS)
        if res.status_code != 200:
            raise FetchError(f"Failed to fetch data, HTTP status: {res.status_code}")
        data = json.loads(res.text)
        return data

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

# Main application UI
class SnowflApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Snowfl Torrent Search')

        layout = QVBoxLayout()

        self.query_input = QLineEdit(self)
        self.query_input.setPlaceholderText("Enter search query")
        layout.addWidget(self.query_input)

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.start_search)
        layout.addWidget(self.search_button)

        self.results_area = QScrollArea(self)
        self.results_area.setWidgetResizable(True)
        self.results_frame = QFrame(self.results_area)
        self.results_layout = QVBoxLayout(self.results_frame)
        self.results_area.setWidget(self.results_frame)
        layout.addWidget(self.results_area)

        self.setLayout(layout)

    def start_search(self):
        query = self.query_input.text().strip()
        sort = "MAX_SEED"
        include_nsfw = True
        if len(query) < 3:
            self.show_message("Query should be at least 3 characters.")
            return
        # Start the worker thread to fetch data
        self.worker = SnowflWorker(query, sort, include_nsfw)
        self.worker.results_ready.connect(self.display_results)
        self.worker.start()

    def display_results(self, results):
        for i in reversed(range(self.results_layout.count())):
            self.results_layout.itemAt(i).widget().deleteLater()

        if not results:
            self.show_message("No results found.")
        else:
            for result in results:
                if "name" in result:
                    magnet_link = result.get("magnet_link", "")
                    button = QPushButton(result["name"], self)
                    if magnet_link:
                        button.clicked.connect(partial(self.copy_to_clipboard, magnet_link))
                    else:
                        button.setEnabled(False)
                    self.results_layout.addWidget(button)

    def copy_to_clipboard(self, magnet_link: str):
        QApplication.clipboard().setText(magnet_link)
        logger.info(f"Copied to clipboard: {magnet_link}")

    def show_message(self, message: str):
        button = QPushButton(message, self)
        button.setEnabled(False)
        self.results_layout.addWidget(button)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnowflApp()
    window.show()
    sys.exit(app.exec())
