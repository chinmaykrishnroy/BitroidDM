from pprint import pprint
import os
import json
import logging
from typing import Any, Dict, Optional
import re
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

# Custom exceptions


class ApiError(Exception):
    def __init__(self, message="API error occurred"):
        super().__init__(message)


class FetchError(Exception):
    def __init__(self, message="Fetch error occurred", status_code=None):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        return f"{self.__class__.__name__}: {self.args[0]} (Status Code: {self.status_code})"

# Utility functions


def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_api_key() -> str:
    logger.info("Fetching API key")
    try:
        session = requests_retry_session()
        home = session.get(url=SITE, headers=HEADERS)
        if home.status_code != 200:
            raise FetchError(f"Error in fetching homepage: Status {
                             home.status_code}")
        home_text = home.text

        js_file_match = REGEX_FOR_JS.search(home_text)
        if not js_file_match:
            raise ApiError("JS file link not found in homepage")

        js_file_link = f"{SITE}{js_file_match.group(0)}"
        js_res = session.get(js_file_link)
        if js_res.status_code != 200:
            raise FetchError(f"Error in fetching JS file: Status {
                             js_res.status_code}")
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

# Main class


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
        url = f"{BASE_URL}{
            self.api_key}/{query}{sort_option}{include_nsfw_flag}"
        logger.info(f"URL: {url}")

        session = requests_retry_session()
        res = session.get(url=url, headers=HEADERS)

        if res.status_code != 200:
            raise FetchError(f"Failed to fetch data, HTTP status: {
                             res.status_code}")

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

    def __str__(self):
        return "Snowfl API Wrapper"

    def __repr__(self):
        return "Snowfl()"

# Save Cache


def append_to_history(data: list[Dict[str, Any]], filename="searchhistory.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                history = json.load(file)
            except json.decoder.JSONDecodeError:
                print("Can't load history!")
                history = []
    else:
        history = []

    history.extend(data)

    with open(filename, 'w') as file:
        json.dump(history, file, indent=4)

# Usage


snowfl = Snowfl()
try:
    snowfl.initialize()
except ApiError as e:
    print(f"Error initializing Snowfl: {e}")

try:
    query = "harry potter"
    sort = "MAX_SEED"
    include_nsfw = False
    results = snowfl.parse(query, sort=sort, include_nsfw=include_nsfw)
    pprint(results)
    append_to_history(results)
    # print(len(results))
    # for result in results:
    #     print(result)
except FetchError as e:
    print(f"Error searching Snowfl: {e}")
