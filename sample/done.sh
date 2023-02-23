#!/bin/sh
#
# Created:      2023-02-23 21:49:57
set -eu

TOKEN="${HOME}/Share/secret/token.json"
CREDENTIALS="${HOME}/Share/secret/credentials.json"
LOG="${HOME}/Share/secret/log.txt"
DIR_A="${HOME}/Share/Screenshots"
DIR_B="${HOME}/Share/Capture"

${HOME}/Share/src/rename_windows_screenshots.py ${DIR_A}/*
${HOME}/Share/src/upload2photo.py ${DIR_A}/* -t ${TOKEN} -c ${CREDENTIALS} -l ${LOG}
${HOME}/Share/src/rename_windows_capture.py ${DIR_B}/*
${HOME}/Share/src/upload2photo.py ${DIR_B}/* -t ${TOKEN} -c ${CREDENTIALS} -l ${LOG}
