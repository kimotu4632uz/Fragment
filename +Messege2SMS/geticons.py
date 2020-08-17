from pathlib import Path
import re, requests

# get icons from +メッセージ backup file

txt = Path('/sdcard/PlusMessage/backup/KzgxOTA5MjM5NjcyN18xNTk3OTA2ODIyMDIx.backup').read_text(encoding='ascii', errors='replace')
result = re.findall(r'(?<=<data url=")https://sticker-a.e01.rcs.kddi.ne.jp/[^"]*(?=")', txt)

i = 0
for url in list(set(result)):
    if 'thumbnail' not in url:
        resp = requests.get(url)
        if resp.status_code == requests.codes.ok:
            Path(f'/sdcard/{i}.png').write_bytes(resp.content)
            i += 1

