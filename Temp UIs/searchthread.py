import json
import re
import requests
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker
from typing import Dict, Any

# Configuration
BASE_URL = "https://snowfl.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
SITE = "https://snowfl.com/"
REGEX_FOR_KEY = re.compile(r'findNextItem.*?"(.*?)"')
REGEX_FOR_JS = re.compile(r'((?:b.min.js).*)(?=")')

# Thread-safe Snowfl class

class Snowfl:
    def __init__(self):
        self.api_key = self.get_api_key()

    def get_api_key(self) -> str:
        session = requests.Session()
        home = session.get(url=SITE, headers=HEADERS)
        home_text = home.text
        js_file_match = REGEX_FOR_JS.search(home_text)
        js_file_link = f"{SITE}{js_file_match.group(0)}"
        js_res = session.get(js_file_link)
        js_text = js_res.text
        api_key_match = REGEX_FOR_KEY.search(js_text)
        return api_key_match.group(1)

    def parse(self, query: str, sort: str = "NONE", include_nsfw: bool = False) -> Dict[str, Any]:
        sort_option = self.get_sort_url_segment(sort)
        url = f"{BASE_URL}{self.api_key}/{query}{sort_option}{int(include_nsfw)}"
        session = requests.Session()
        res = session.get(url=url, headers=HEADERS)
        return json.loads(res.text)

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
    search_result = Signal(int, list)  # Signal: emits 1 with results on success, 0 with empty list on failure

    def __init__(self):
        super().__init__()
        self.snowfl = Snowfl()
        self.mutex = QMutex()  # Mutex for mutual exclusion
        self.query = "harry potter"
        self.sort = "NONE"
        self.include_nsfw = False

    def run(self):
        with QMutexLocker(self.mutex):  # Ensure thread safety
            try:
                results = self.snowfl.parse(self.query, self.sort, self.include_nsfw)
                self.search_result.emit(1, results)  # Emit success signal with results
            except Exception:
                self.search_result.emit(0, [])  # Emit failure signal with empty list

    def start_search(self, query: str, sort: str = "NONE", include_nsfw: bool = False):
        # Set the parameters for the search
        self.query = query
        self.sort = sort
        self.include_nsfw = include_nsfw
        # Start the thread
        if not self.isRunning():  # Ensure thread is not already running
            self.start()
