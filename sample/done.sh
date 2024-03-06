#!/bin/sh
#
# Created:      2023-02-23 21:49:57
set -eu

BASE="${HOME}/.local/opt/SharePhoto"
TOKEN="${BASE}/secret/token.json"
CREDENTIALS="${BASE}/secret/credentials.json"
LOG="${BASE}/secret/log.txt"
DIR_A="${HOME}/Share/Screenshots"
DIR_B="${HOME}/Share/Capture"
STATE="${BASE}/secret/state.txt"
${BASE}/bin/rename_windows_screenshots.py ${DIR_A}/*
${BASE}/bin/rename_windows_capture.py ${DIR_B}/*
${BASE}/bin/upload2photo.py ${DIR_A}/* -t ${TOKEN} -c ${CREDENTIALS} -l ${LOG} -s ${STATE} --no-stdout
${BASE}/bin/upload2photo.py ${DIR_B}/* -t ${TOKEN} -c ${CREDENTIALS} -l ${LOG} -s ${STATE} --no-stdout
# echo "Photo: `cat ${STATE}`"
