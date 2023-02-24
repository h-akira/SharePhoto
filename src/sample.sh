#!/bin/sh
#
# Created:      2023-02-23 21:49:57
set -eu

BASE="${HOME}/.local/opt/Share_Photo"
TOKEN="${BASE}/secret/token.json"
CREDENTIALS="${BASE}/secret/credentials.json"
LOG="${BASE}/secret/log.txt"
DIR_A="${HOME}/Share/Screenshots"
DIR_B="${HOME}/Share/Capture"
STATE="${BASE}/secret/state.txt"
${BASE}/src/rename_windows_screenshots.py ${DIR_A}/*
${BASE}/src/rename_windows_capture.py ${DIR_B}/*
${BASE}/src/upload2photo.py ${DIR_A}/* -t ${TOKEN} -c ${CREDENTIALS} -l ${LOG} -s ${STATE} --no-stdout
${BASE}/src/upload2photo.py ${DIR_B}/* -t ${TOKEN} -c ${CREDENTIALS} -l ${LOG} -s ${STATE} --no-stdout
echo "Photo: `cat ${BASE}/secret/state.txt`"
