#!/bin/bash
# VERSION: 0.1.2
# AUTHORS: Ogekuri

set -euo pipefail

rm -f examples.log


rm -rf temp/
mkdir temp/


N=5  # quanti segmenti finali del path usare per rendere "last" univoco e leggibile

make_last() {
  local url="$1" clean host rest path
  local -a seg
  local start i out=""

  clean=${url%%\#*}
  clean=${clean%%\?*}
  clean=${clean%/}

  # se finisce con un file html (index.html o altro), ignoralo
  [[ "$clean" == *.html ]] && clean=${clean%/*}

  # host (opzionale ma aumenta leggibilità/unicità)
  host=${clean#*://}
  host=${host%%/*}

  # solo path senza schema+host
  rest=${clean#*://}
  path=${rest#*/}         # rimuove host/
  IFS=/ read -r -a seg <<< "$path"

  # prendi gli ultimi N segmenti
  start=0
  if (( ${#seg[@]} > N )); then
    start=$((${#seg[@]} - N))
  fi

  for ((i=start; i<${#seg[@]}; i++)); do
    [[ -z "${seg[i]}" ]] && continue
    out+="${out:+_}${seg[i]}"
  done

  printf '%s_%s\n' "$host" "$out"
}

urls=(
    "https://www.ti.com/document-viewer/lit/html/sprz457"
    "https://www.ti.com/document-viewer/lit/html/spradh8"
    "https://www.ti.com/document-viewer/lit/html/spradj8"
    "https://www.ti.com/document-viewer/lit/html/tiduf35"
    "https://www.ti.com/document-viewer/lit/html/spradr2"
    "https://www.ti.com/document-viewer/am6442/datasheet"
)

for url in "${urls[@]}"; do
    last="$(make_last "$url")"
    echo "============================================================" | tee -a examples.log
    echo "[INFO] Input url:  $url"  | tee -a examples.log
    echo "[INFO] Output dir: temp/out_${last}" | tee -a examples.log
    echo ./htmldownloader.sh --from-url "${url}" --to-dir ./temp/out_${last} --verbose --debug | tee -a examples.log
    ./htmldownloader.sh --from-url "${url}" --to-dir ./temp/out_${last} --verbose --debug >>examples.log 2>&1 && echo "[OK] on path out_${last}" | tee -a examples.log || { rc=$?; echo "[ERROR] (rc=$rc) on path out_${last}" | tee -a examples.log; continue; }
done

# AM64x MCU+ SDK  11.02.00
# AM64x MCU+ SDK  08.00.00

# AM64x INDUSTRIAL COMMUNICATIONS SDK  2025.00.00

# AM243x MCU+ SDK  11.02.00
# AM243x Motor Control SDK  11.00.00

# AM263x MCU+ SDK  11.01.00
# AM263x Motor Control SDK  09.00.00

# C2000Ware Digital Power SDK  5.03.00.00

urls=(
    "https://software-dl.ti.com/mcu-plus-sdk/esd/AM64X/latest/exports/docs/api_guide_am64x/index.html"
    "https://software-dl.ti.com/mcu-plus-sdk/esd/AM64X/08_00_00_21/exports/docs/api_guide_am64x/index.html"
    "https://software-dl.ti.com/processor-industrial-sw/esd/ind_comms_sdk/am64x/latest/docs/api_guide_am64x/index.html"
    "https://software-dl.ti.com/mcu-plus-sdk/esd/AM243X/latest/exports/docs/api_guide_am243x/index.html"
    "https://software-dl.ti.com/processor-industrial-sw/esd/motor_control_sdk/am243x/11_00_00_06/docs/api_guide_am243x/index.html"
    "https://software-dl.ti.com/mcu-plus-sdk/esd/AM263X/latest/exports/docs/api_guide_am263x/index.html"
    "https://software-dl.ti.com/processor-industrial-sw/esd/motor_control_sdk/am263x/09_00_00_06/docs/api_guide_am263x/index.html"
    "https://software-dl.ti.com/C2000/c2000_apps_public_sw/c2000ware_sdk/digitalpowersdk/5_03_00_00/html_guide/index.html"
)

for url in "${urls[@]}"; do
    last="$(make_last "$url")"
    echo "============================================================" | tee -a examples.log
    echo "[INFO] Input url:  $url"  | tee -a examples.log
    echo "[INFO] Output dir: temp/out_${last}" | tee -a examples.log
    echo ./htmldownloader.sh --from-url "${url}" --to-dir ./temp/out_${last} --verbose --debug --limit 30 | tee -a examples.log
    ./htmldownloader.sh --from-url "${url}" --to-dir ./temp/out_${last} --verbose --debug --limit 30 >>examples.log 2>&1 && echo "[OK] on path out_${last}" | tee -a examples.log || { rc=$?; echo "[ERROR] (rc=$rc) on path out_${last}" | tee -a examples.log; continue; }
done

# AM263x Digital Power SDK  09.01.00


urls=(
    "https://dev.ti.com/tirex/explore/node?node=A__AD2nw6Uu4txAz2eqZdShBg__DIGITAL-POWER-SDK-AM263X__k-hvNHd__LATEST"
)

for url in "${urls[@]}"; do
    last="$(make_last "$url")"
    echo "============================================================" | tee -a examples.log
    echo "[INFO] Input url:  $url"  | tee -a examples.log
    echo "[INFO] Output dir: temp/out_${last}" | tee -a examples.log
    echo ./htmldownloader.sh --from-url "${url}" --to-dir ./temp/out_${last} --verbose --debug --limit 30 | tee -a examples.log
    ./htmldownloader.sh --from-url "${url}" --to-dir ./temp/out_${last} --verbose --debug --limit 30 >>examples.log 2>&1 && echo "[OK] on path out_${last}" | tee -a examples.log || { rc=$?; echo "[ERROR] (rc=$rc) on path out_${last}" | tee -a examples.log; continue; }
done


