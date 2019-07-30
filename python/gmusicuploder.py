#!/usr/bin/env python
import sys
from gmusicapi import Musicmanager

if __name__ == "__main__" and len(sys.argv) > 1:
    mm = Musicmanager()
    ##mm.perform_oauth(storage_filepath='/data/data/com.termux/files/home/.oauth.cred')
    mm.login(oauth_credentials='/data/data/com.termux/files/home/.oauth.cred', uploader_id='D4:38:9C:04:CD:F7')
    # uploader_id = MAC adderss with big letter
    mm.upload(sys.argv[1:])
    mm.logout()
