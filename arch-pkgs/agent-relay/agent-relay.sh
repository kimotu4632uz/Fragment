#!/bin/bash

GPGDIR="${XDG_RUNTIME_DIR}/gnupg"
WIN_AFUNIX_SOCK="$(wslpath -m $USERPROFILE)/AppData/Local/gnupg/agent-gui"
SORELAY="${USERPROFILE}/scoop/apps/win-gpg-agent/current/sorelay.exe"

rm -f "${GPGDIR}/S.gpg-agent" "${GPGDIR}/S.gpg-agent.ssh"

socat UNIX-LISTEN:"${GPGDIR}/S.gpg-agent",fork EXEC:"${SORELAY} '${WIN_AFUNIX_SOCK}/S.gpg-agent'",nofork &
socat UNIX-LISTEN:"${GPGDIR}/S.gpg-agent.ssh",fork EXEC:"${SORELAY} '${WIN_AFUNIX_SOCK}/S.gpg-agent.ssh'",nofork &

