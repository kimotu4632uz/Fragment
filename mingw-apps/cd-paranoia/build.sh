#!/bin/bash

apt update
apt install -y autoconf automake libtool texinfo pkg-config

libiconv_ver="1.16"
libcdio_ver="2.1.0"
libcdio_paranoia_ver="10.0.2+2.0.1"

wget -O - "https://ftp.gnu.org/pub/gnu/libiconv/libiconv-${libiconv_ver}.tar.gz" | tar xzv
wget -O - "http://git.savannah.gnu.org/cgit/libcdio.git/snapshot/libcdio-release-${libcdio_ver}.tar.gz" | tar xzv
wget -O - "https://github.com/rocky/libcdio-paranoia/archive/release-${libcdio_paranoia_ver}.tar.gz" | tar xzv

cd "libiconv-${libiconv_ver}"
./configure \
  --prefix=$PWD/../deps \
  --host=x86_64-w64-mingw32 \
  --disable-shared \
  --enable-static \
  CC=x86_64-w64-mingw32-gcc
make
make install

cd "../libcdio-release-${libcdio_ver}"
./autogen.sh \
  --prefix=$PWD/../deps \
  --host=x86_64-w64-mingw32 \
  --disable-shared \
  --enable-static \
  --disable-cxx \
  --disable-cpp-progs \
  --disable-example-progs \
  --disable-joliet \
  --disable-rock \
  --disable-cddb \
  --disable-vcd-info \
  --without-cd-drive \
  --without-cd-read \
  --without-cd-info \
  --without-cdda-player \
  --without-iso-read \
  --without-iso-info \
  --with-libiconv-prefix=$PWD/../deps \
  CC=x86_64-w64-mingw32-gcc
make
make install

cd "../libcdio-paranoia-release-${libcdio_paranoia_ver}"
./autogen.sh \
  --prefix=$PWD/../app \
  --host=x86_64-w64-mingw32 \
  --disable-cxx \
  --disable-shared \
  --enable-static \
  --disable-cpp-progs \
  --disable-example-progs \
  --without-versioned-libs \
  CC=x86_64-w64-mingw32-gcc \
  LIBCDIO_CFLAGS=-I$PWD/../deps/include \
  LIBCDIO_LIBS=$PWD/../deps/lib/libcdio.la \
  LDFLAGS="-Wl,-Bstatic -lpthread"
make
make install

cd ..
cp app/bin/cd-paranoia.exe .
