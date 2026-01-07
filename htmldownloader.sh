#!/bin/bash
# VERSION: 0.0.0
# AUTHORS: Ogekuri

# 1. Ottieni il percorso assoluto completo del file (risolvendo i link simbolici)
FULL_PATH=$(readlink -f "$0")

# 2. Estrai la directory (il percorso senza il nome del file)
SCRIPT_PATH=$(dirname "$FULL_PATH")

# 3. Estrai il nome del file
SCRIPT_NAME=$(basename "$FULL_PATH")

# --- Test di output (puoi rimuoverli) ---
#echo "Full Path:   $FULL_PATH"
#echo "Directory:   $SCRIPT_PATH"
#echo "Script Name: $SCRIPT_NAME"

VENVDIR="${SCRIPT_PATH}/.venv"
#echo ${VENVDIR}

# Se non c'è il ${VENVDIR} lo crea
if ! [ -d "${VENVDIR}/" ]; then
    echo "ERROR! Virtual environment not present!"
    exit
fi

source ${VENVDIR}/bin/activate

now=$(date '+%Y-%m-%d_%H-%M-%S')

#
# Only local packages on virtual environment
#  pip freeze -l > pip-freeze.txt # or --local instead of -l
#
# Only local packages installed by the user on virtual environment
#  pip freeze --user > pip-freeze.txt
#

${VENVDIR}/bin/python3.12 ${SCRIPT_PATH}/${SCRIPT_NAME}.py "$@"
