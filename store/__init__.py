import requests
from urllib.parse import urlsplit
from pathlib import Path
from os import makedirs

class Store:
    def __init__(self, path = './pages'):
        self.path = Path(path)
        pass

    def get(self, url):
        u = urlsplit(url)

        cache_path = self.path / ('.' + u.path)

        if cache_path.exists():
            return cache_path.read_text()

        res = requests.get(url)
        res.raise_for_status()
        content = res.text

        makedirs(cache_path.parent)
        cache_path.write_text(content)

        return content

