#!/bin/bash
from ytmusicapi import YTMusic
from pathlib import Path
import json
import requests

yt = YTMusic("ytmusic.json")
songs = yt.get_library_upload_songs(1000)
artists = {}
album_ids = []

for song in songs:
    artists[song["videoId"]] = song["artist"][0]["name"]

    if song["album"]["id"] not in album_ids:
        album_ids.append(song["album"]["id"])


for album_id in album_ids:
    album = yt.get_library_upload_album(album_id)

    tracks = []
    for track in album["tracks"]:
        meta = {
            "title": track["title"],
            "artist": artists[track["videoId"]]
        }
        tracks.append(meta)

    meta = {
        "album": album["title"],
        "date": album["year"],
        "genre": "",
        "tracks": tracks
    }

    pic = sorted(album["thumbnails"], key=lambda m: m["height"], reverse=True)[0]["url"]

