#!/bin/bash
# libxml2 libxslt : for bs4, libjpeg-turbo : for Pillow
pkg install -y rclone ffmpeg-dev libxml2 libxslt libjpeg-turbo vim
ln -s $PREFIX/include/{libxml2/libxml,libxml}
pip install requests mutagen img2pdf bs4 ffmpeg gmusicapi Pillow
python -c "from gmusicapi import Musicmanager; Musicmanager().perform_oauth(storage_filepath='/data/data/com.termux/files/home/.oauth.cred')"
rclone config create upload_pic drive env_auth true