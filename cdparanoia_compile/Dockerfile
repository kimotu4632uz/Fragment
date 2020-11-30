FROM amd64/debian:stable-slim

WORKDIR /root

RUN apt update && \
    apt install -y \
        curl \
        git \
        build-essential \
        mingw-w64 \
        autoconf \
        automake \
        libtool \
        texinfo \
        pkg-config

RUN curl https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.16.tar.gz | tar xzv && \
    curl http://git.savannah.gnu.org/cgit/libcdio.git/snapshot/libcdio-release-2.1.0.tar.gz | tar xzv && \
    curl -L https://github.com/rocky/libcdio-paranoia/archive/release-10.2+2.0.1.tar.gz | tar xzv && \
    git clone https://github.com/kimotu4632uz/libcdio-discid.git


WORKDIR /root/libiconv-1.16
RUN ./configure \
        --prefix=$PWD/build \
        --host=x86_64-w64-mingw32 \
        --disable-shared \
        --enable-static \
        CC=x86_64-w64-mingw32-gcc && \
    make && \
    make install


WORKDIR /root/libcdio-release-2.1.0
RUN ./autogen.sh \
        --prefix=$PWD/build \
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
        --with-libiconv-prefix=${PWD%/*}/libiconv-1.16/build \
        CC=x86_64-w64-mingw32-gcc && \
    make && \
    make install

WORKDIR /root/libcdio-paranoia-release-10.2-2.0.1
RUN ./autogen.sh \
        --prefix=$PWD/build \
        --host=x86_64-w64-mingw32 \
        --disable-cxx \
        --disable-shared \
        --enable-static \
        --disable-cpp-progs \
        --disable-example-progs \
        --without-versioned-libs \
        CC=x86_64-w64-mingw32-gcc \
        LIBCDIO_CFLAGS=-I${PWD%/*}/libcdio-release-2.1.0/build/include \
        LIBCDIO_LIBS=${PWD%/*}/libcdio-release-2.1.0/build/lib/libcdio.la \
        LDFLAGS="-Wl,-Bstatic -lpthread" && \
    make && \
    make install

WORKDIR /root/libcdio-discid
RUN ./autogen.sh \
        --prefix=$PWD/build \
        --host=x86_64-w64-mingw32 \
        CC=x86_64-w64-mingw32-gcc \
        LIBCDIO_CFLAGS=-I${PWD%/*}/libcdio-release-2.1.0/build/include \
        LIBCDIO_LIBS=${PWD%/*}/libcdio-release-2.1.0/build/lib/libcdio.la \
        LDFLAGS="-Wl,-Bstatic -lpthread" && \
    make && \
    make install

Run mkdir /apps && \
    cp /root/libcdio-paranoia-release-10.2-2.0.1/build/bin/cd-paranoia.exe /apps && \
    cp /root/libcdio-discid/build/bin/cdio-discid.exe /apps

