#!/bin/bash
# VERSION: 0.0.0
# AUTHORS: Ogekuri

./htmldownloader --from-url "https://www.ti.com/document-viewer/am6442/datasheet" --to-dir ./out_am6442

./htmldownloader --from-url "https://software-dl.ti.com/mcu-plus-sdk/esd/AM64X/latest/exports/docs/api_guide_am64x/index.html" --to-dir ./out_doxygen
