#!/bin/bash
pkg install -y rclone libjpeg-turbo ffmpeg-dev libxml2 libxslt
ln -s $PREFIX/include/{libxml2/libxml,libxml}
pip install requests mutagen Pillow img2pdf bs4 ffmpeg gmusicapi
python -c "from gmusicapi import Musicmanager; Musicmanager().perform_oauth(storage_filepath='/data/data/com.termux/files/home/.oauth.cred')"