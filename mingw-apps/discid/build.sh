#!/bin/bash

libdiscid_ver="0.6.2"

apt update
apt install -y automake autoconf libtool
wget -O - "https://github.com/metabrainz/libdiscid/archive/refs/tags/v${libdiscid_ver}.tar.gz" | tar xzv

cd libdiscid-${libdiscid_ver}
patch src/disc_win32.c < ../disc_win32.patch
./autogen.sh
./configure --prefix=$PWD/../deps \
  --build=x86_64-unknown-linux-gnu \
  --host=x86_64-w64-mingw32 \
  --enable-shared \
  --enable-static \
  CC=x86_64-w64-mingw32-gcc
make
make install

cd ..
x86_64-w64-mingw32-gcc main.c -o discid.exe -Dlibdiscid_EXPORTS -I./deps/include -L./deps/lib -static -ldiscid
