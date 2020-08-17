import re, html, sys
from datetime import datetime, timezone, timedelta
import xml.etree.ElementTree as ET
from pathlib import Path

# +メッセージ の会話履歴ファイル to SMS
# see https://synctech.com.au/sms-backup-restore/fields-in-xml-backup-files/

phone_me = ''
phone_to = ''
talk_to = ''

xmls = []
mmss = []

for line in Path(sys.argv[1]).read_text().splitlines():
    result = re.match(r'(\d{4})年(\d*)月(\d*)日 (\d{2}):(\d{2}):(\d{2}) \| (.*): (.*)', line)

    if result:
        time = datetime(int(result.group(1)),int(result.group(2)),int(result.group(3)),int(result.group(4)),int(result.group(5)),int(result.group(6)),tzinfo=timezone(timedelta(hours=9)))

        if result.group(7) == '自分':
            type_s = '2'
        else:
            type_s = '1'

        if result.group(8) == 'スタンプ':
            mmss.append(f'{time.isoformat()} {str(time.timestamp()).split(".")[0]}000 {type_s}')

        else:
            body = html.escape(result.group(8))
            xmls.append(ET.Element('sms', { 'protocol': '0', 'address': phone_to, 'date': str(time.timestamp()).split('.')[0] + '000', 'type': type_s, 'subject': 'null', 'body': body, 'toa': 'null', 'sc_toa': 'null', 'service_center': 'null', 'read': '1', 'status': '-1', 'readable_date': time.isoformat(' ').replace('-', '/').split('+')[0], 'contact_name': talk_to }))
    
    else:
        xmls[-1].attrib['body'] += html.escape('\n' + line)

for xml in xmls:
    print(ET.tostring(xml, encoding="unicode"))

for mms in mmss:
    print(mms)
