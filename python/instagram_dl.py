import mimetypes
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def get(url, path):
    resp = requests.get(url)
    if resp.status_code != requests.codes.ok:
        return resp.status_code
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    meta = soup.find('meta', property='og:image')
    
    resp = requests.get(meta['content'])
    if resp.status_code != requests.codes.ok:
        return resp.status_code
    
    fname = urlparse(url).path.split('/')[2]
    ext = mimetypes.guess_all_extensions(resp.headers['content-type'])[-1]
    
    (Path(path) / (fname + ext)).write_bytes(resp.content)
