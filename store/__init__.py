import requests
from urllib.parse import urlsplit
from pathlib import Path
from os import makedirs
from bs4 import BeautifulSoup

class Store:
    def __init__(self, path = './pages'):
        self.path = Path(path)
        pass

    def get(self, url):
        u = urlsplit(url)

        cache_path = self.path / ('.' + u.path) / 'content.html'

        if cache_path.exists():
            return BeautifulSoup(cache_path.read_text(), "html.parser")

        res = requests.get(url)
        res.raise_for_status()
        content = res.text

        makedirs(cache_path.parent, exist_ok=True)
        cache_path.write_text(content)

        return BeautifulSoup(content, "html.parser")

