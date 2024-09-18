import json
import logging
import os
import re
from pprint import pprint
from typing import Any, Dict, Optional

from PySide6.QtCore import QThread, Signal, QObject, QMutex, QMutexLocker
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

# Mutex for thread-safe operations
mutex = QMutex()

# Snowfl class for API interaction
class Snowfl:
    def __init__(self):
        self.api_key: Optional[str] = None

    def initialize(self):
        self.api_key = get_api_key()
        if self.api_key is None:
            raise ApiError("Failed to obtain API key.")

    def parse(self, query: str, sort: str = "NONE", include_nsfw: bool = False) -> Dict[str, Any]:
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

# Worker class to perform searches in a persistent thread
class SearchWorker(QThread):
    result_signal = Signal(int, dict)  # Signal to return results (status, results)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.snowfl = Snowfl()
        self.snowfl.initialize()
        self.query = None
        self.nsfw = None
        self.sort = None

    def search_torrent(self, query: str, nsfw: bool, sort: str):
        with QMutexLocker(mutex):
            self.query = query
            self.nsfw = nsfw
            self.sort = sort
            self.start()

    def run(self):
        if self.query is None:
            return

        try:
            with QMutexLocker(mutex):
                results = self.snowfl.parse(self.query, self.sort, self.nsfw)
                
                # Debugging: Log full response
                logger.info(f"Full response content: {json.dumps(results, indent=2)}")
                
                if results:
                    self.result_signal.emit(1, results)  # Success with results
                else:
                    logger.warning("No results found for the query.")
                    self.result_signal.emit(0, {})  # No results, empty dict
                
        except (ApiError, FetchError) as e:
            logger.error(f"Error: {e}")
            self.result_signal.emit(0, {})

# GUI class to display the application
class TorrentSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Create a persistent worker thread
        self.worker = SearchWorker()
        self.worker.result_signal.connect(self.handle_results)

    def init_ui(self):
        self.setWindowTitle("Torrent Search")

        self.query_input = QLineEdit(self)
        self.query_input.setPlaceholderText("Enter search query")

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.start_search)

        layout = QVBoxLayout()
        layout.addWidget(self.query_input)
        layout.addWidget(self.search_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_search(self):
        query = self.query_input.text()
        nsfw = True  # Example value
        sort = "MAX_SEED"  # Example value

        # Reuse the existing worker thread to search torrents
        self.worker.search_torrent(query, nsfw, sort)

    def handle_results(self, status: int, results: dict):
        if status == 1:
            print("Search successful!")
            pprint(results)
        else:
            print("Search failed!")

# Utility functions
def get_api_key() -> str:
    logger.info("Fetching API key")
    try:
        session = requests_retry_session()
        home = session.get(url=SITE, headers=HEADERS)
        if home.status_code != 200:
            raise FetchError(f"Error in fetching homepage: Status {home.status_code}")
        home_text = home.text

        js_file_match = REGEX_FOR_JS.search(home_text)
        if not js_file_match:
            raise ApiError("JS file link not found in homepage")

        js_file_link = f"{SITE}{js_file_match.group(0)}"
        js_res = session.get(js_file_link)
        if js_res.status_code != 200:
            raise FetchError(f"Error in fetching JS file: Status {js_res.status_code}")
        js_text = js_res.text

        api_key_match = REGEX_FOR_KEY.search(js_text)
        if not api_key_match:
            raise ApiError("API key not found in JS file")

        return api_key_match.group(1)

    except requests.exceptions.RequestException as e:
        logger.error("HTTP error occurred", exc_info=e)
        raise FetchError("Error during HTTP request") from e
    except Exception as e:
        logger.error("Unexpected error occurred", exc_info=e)
        raise

# FetchError and ApiError classes
class FetchError(Exception):
    def __init__(self, message="Fetch error occurred", status_code=None):
        super().__init__(message)
        self.status_code = status_code

class ApiError(Exception):
    def __init__(self, message="API error occurred"):
        super().__init__(message)

# Requests retry session setup
def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Main entry point
if __name__ == "__main__":
    app = QApplication([])
    window = TorrentSearchApp()
    window.show()
    app.exec()
