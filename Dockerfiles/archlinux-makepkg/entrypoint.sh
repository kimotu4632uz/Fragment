#!/bin/bash

USER_ID=${LOCAL_UID:-9001}
GROUP_ID=${LOCAL_GID:-9001}

useradd -u $USER_ID -o -m -G wheel docker
groupmod -g $GROUP_ID docker
echo '%wheel ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
export HOME=/home/docker

exec /usr/sbin/su docker "$@"
