FROM rust:1.56.0-slim-bullseye
RUN apt update && \
    apt install -y --no-install-recommends git ssh pkg-config build-essential && \
    apt -y clean && \
    rm -rf /var/lib/apt/lists/*

