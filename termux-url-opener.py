#!/data/data/com.termux/files/usr/bin/env python
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse
import subprocess
import io
import mimetypes

import requests
from bs4 import BeautifulSoup
import img2pdf
import PIL.Image

def html2pdf(url, name):
    resp = requests.get(url)
    if resp.status_code != requests.codes.ok:
        return resp.status_code
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    urls = []
    
    for tag in soup.find_all(['img', 'a']):
        if tag.name == 'img':
            img = tag['src']
        else:
            img = tag['href']
        
        if mimetypes.guess_type(img)[0] == 'image/jpeg' or mimetypes.guess_type(img)[0] == 'image/png':
            urls.append(img)
    
    fp = tempfile.NamedTemporaryFile(mode='w', delete=False)
    fp.write('\n'.join(urls))
    fp.close()
    
    subprocess.call(['vim', fp.name])
    tmp = Path(fp.name)
    
    imgs = []
    for url in tmp.read_text().splitlines():
        resp = requests.get(url)
        if resp.status_code == requests.codes.ok:
            if resp.url.rsplit('.')[-1] == 'png':
                jpg = io.BytesIO()
                PIL.Image.open(io.BytesIO(resp.content)).convert('RGB').save(jpg, format='JPEG')
                imgs.append(jpg.getvalue())
            else:
                imgs.append(resp.content)
    
    largest = Path(name).stem
    Path('/sdcard/secret/' + str(int(largest)+1 ) + '.pdf').write_bytes(img2pdf.convert(imgs))
    tmp.unlink()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    
    html2pdf(sys.argv[1], sys.argv[2])


