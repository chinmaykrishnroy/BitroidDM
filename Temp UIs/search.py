import json
import re
import requests
from typing import Dict, Any

# Configuration
BASE_URL = "https://snowfl.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
SITE = "https://snowfl.com/"
REGEX_FOR_KEY = re.compile(r'findNextItem.*?"(.*?)"')
REGEX_FOR_JS = re.compile(r'((?:b.min.js).*)(?=")')

def requests_retry_session(retries=3, backoff_factor=0.3):
    session = requests.Session()
    retry = requests.adapters.Retry(total=retries, backoff_factor=backoff_factor)
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_api_key() -> str:
    session = requests_retry_session()
    home = session.get(url=SITE, headers=HEADERS)
    home_text = home.text
    js_file_match = REGEX_FOR_JS.search(home_text)
    js_file_link = f"{SITE}{js_file_match.group(0)}"
    js_res = session.get(js_file_link)
    js_text = js_res.text
    api_key_match = REGEX_FOR_KEY.search(js_text)
    return api_key_match.group(1)

class Snowfl:
    def __init__(self):
        self.api_key = get_api_key()

    def parse(self, query: str, sort: str = "NONE", include_nsfw: bool = False) -> Dict[str, Any]:
        sort_option = self.get_sort_url_segment(sort)
        url = f"{BASE_URL}{self.api_key}/{query}{sort_option}{int(include_nsfw)}"
        session = requests_retry_session()
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

# Usage
snowfl = Snowfl()
query = input("Query: ")
sort = "MAX_SEED"
include_nsfw = True
results = snowfl.parse(query, sort=sort, include_nsfw=include_nsfw)
print(results)
