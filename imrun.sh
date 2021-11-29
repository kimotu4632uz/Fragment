#!/bin/bash

export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
export DefaultIMModule=fcitx
fcitx-autostart &> /dev/null &
xset -r 49  > /dev/null 2>&1

export DONT_PROMPT_WSL_INSTALL=1

"$@"
