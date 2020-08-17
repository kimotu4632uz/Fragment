from pathlib import Path
import base64, sys, random
import xml.etree.ElementTree as ET

# +メッセージ の会話履歴ファイル to MMS
# see https://synctech.com.au/sms-backup-restore/fields-in-xml-backup-files/

phone_me = ''
phone_you = ''
talk_to = '' # Name

xmls = []

for index, line in enumerate(Path(sys.argv[1]).read_text().splitlines()):
    data = line.split()
    date = data[1]
    msgbox = data[2]
    pic = data[3] + '.png'

    if msgbox == '1':
        phone_from = phone_you
        phone_to = phone_me
    else:
        phone_from = phone_me
        phone_to = phone_you
    
    pic_count = str(index).zfill(6)

    mms_attr = {
        'date': date,
        'rr': '129',
        'sequence_time': date,
        'ct_t': 'application/vnd.wap.multipart.related',
        'seen': '1',
        'msg_box': msgbox,
        'address': phone_you,
        'text_only': '0',
        'exp': '604800',
        'locked': '0',
        'creator': 'com.google.android.apps.messaging',
        'data_sent': '0',
        'read': '1',
        'm_size': str(Path(pic).stat().st_size),
        'pri': '129',
        'sub_id': '1',
        'tr_id': 'T' + str(random.random()).split('.')[1][:11],
        'm_cls': 'personal',
        'd_rpt': '129',
        'v': '18',
        'm_type': '128',
        'contact_name': talk_to,
    }
    
    part1_attr = {
        'seq': '-1',
        'ct': 'application/smil',
        'name': 'null',
        'chset': 'null',
        'cid': '<smil>',
        'cl': 'smil.xml',
        'text': f'<smil><head><layout><root-layout/><region id="Image" fit="meet" top="0" left="0" height="100%" width="100%"/></layout></head><body><par dur="5000ms"><img src="image{pic_count}.png" region="Image" /></par></body></smil>' 
    }
    
    part2_attr = {
        'seq': '0',
        'ct': 'image/png',
        'name': 'null',
        'chset': 'null',
        'cid': f'<image{pic_count}>',
        'cl': f'image{pic_count}.png',
        'data': base64.b64encode(Path(pic).read_bytes()).decode()
    }
    
    addr1_attr = {
        'address': phone_from,
        'type': '137',
        'charset': '106'
    }
    
    addr2_attr = {
        'address': phone_to,
        'type': '151',
        'charset': '106'
    }
    
    mms = ET.Element('mms', mms_attr)
    
    parts = ET.SubElement(mms, 'parts')
    part1 = ET.SubElement(parts, 'part', part1_attr)
    part2 = ET.SubElement(parts, 'part', part2_attr)
    
    addrs = ET.SubElement(mms, 'addrs')
    addr1 = ET.SubElement(addrs, 'addr', addr1_attr)
    addr1 = ET.SubElement(addrs, 'addr', addr2_attr)
    
    xmls.append(mms)

for xml in xmls:
    print(ET.tostring(xml, encoding='unicode'))
