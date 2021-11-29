#!/bin/bash -e

migu_ver="migu-1m-20200307"

apt update
apt install -y curl unzip git fontforge python3-fontforge
ln -s /usr/bin/python3 /usr/bin/python

curl -LO https://rictyfonts.github.io/files/ricty_generator.sh
curl -LO https://github.com/google/fonts/raw/main/ofl/inconsolata/static/Inconsolata-Regular.ttf
curl -LO https://github.com/google/fonts/raw/main/ofl/inconsolata/static/Inconsolata-Bold.ttf
curl -LO "https://osdn.net/projects/mix-mplus-ipa/downloads/72511/${migu_ver}.zip"
git clone --depth 1 https://github.com/ryanoasis/nerd-fonts.git

unzip "${migu_ver}.zip"
mv "${migu_ver}/migu-1m-bold.ttf" .
mv "${migu_ver}/migu-1m-regular.ttf" .

chmod +x ricty_generator.sh
./ricty_generator.sh auto

./nerd-fonts/font-patcher -c -l -w --careful Ricty-Regular.ttf
./nerd-fonts/font-patcher -c -l -w --careful Ricty-Oblique.ttf

./rename.py
