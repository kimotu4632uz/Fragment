import sys
import mimetypes
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def main(url, path):
    resp = requests.get(url)
    if resp.status_code != requests.codes.ok:
        return resp.status_code
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    for img in soup.find_all('img'):
        resp = requests.get(img['src'])
        if resp.status_code == requests.codes.ok:
            fname = urlparse(url).path.split('/')[-1]
            ext = mimetypes.guess_all_extensions(resp.headers['content-type'])[-1]
            (Path(path) / (fname + ext)).write_bytes(resp.content)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])