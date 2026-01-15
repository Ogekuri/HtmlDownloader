#!/bin/bash
# VERSION: 0.0.4
# AUTHORS: Ogekuri

cd -- "$(dirname "$0")/"
echo "Run on path: "$(pwd -P)

VENVDIR=".venv"

if [ -d "${VENVDIR}/" ]; then
    echo -n "Remove old virtual enviromnet ..."
    rm -rf ${VENVDIR}/
    echo "done."
fi

# Se non c'è il ${VENVDIR} lo crea
if ! [ -d "${VENVDIR}/" ]; then
    echo -n "Create virtual environment ..."
    mkdir ${VENVDIR}/
    virtualenv --python=python3 ${VENVDIR}/ >/dev/null
    echo "done."
fi

# Install requirements
source ${VENVDIR}/bin/activate

echo -n "Install python requirements ..."
${VENVDIR}/bin/pip install -r requirements.txt
${VENVDIR}/bin/playwright install chromium
echo "done."
