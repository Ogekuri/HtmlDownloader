#!/usr/bin/env python3
"""Verifica selezione modulo Resource Explorer per iframe Doxygen."""

from bs4 import BeautifulSoup

from htmldownloader.cli import RMModuleDoxigen


HTML_SAMPLE = """
<div class="css-1aefuid-contentContainer">
  <iframe id="test-id-iframe-element"
    class="css-1rezoj0-iframe css-5qovnk-root css-5qovnk-root css-98f4iy-root css-1lww3ic-contentDisplay css-1pco5ke-content css-1npbx69-iframe"
    src="content/digital_power_sdk_am263x_09_01_00_01/docs/api_guide_am263x/index.html">
  </iframe>
</div>
""".strip()


def test_rm_module_doxigen_selects_iframe():
    module = RMModuleDoxigen()
    soup = BeautifulSoup(HTML_SAMPLE, "lxml")
    selection = module.select(
        "https://dev.ti.com/tirex/explore/node?node=test",
        HTML_SAMPLE,
        soup,
    )

    assert selection is not None
    assert selection.get("doxygen_url") == (
        "https://dev.ti.com/tirex/explore/"
        "content/digital_power_sdk_am263x_09_01_00_01/docs/api_guide_am263x/index.html"
    )


def test_rm_module_doxigen_skips_missing_iframe():
    html = "<div class='css-1aefuid-contentContainer'></div>"
    soup = BeautifulSoup(html, "lxml")
    module = RMModuleDoxigen()

    assert module.select("https://dev.ti.com/tirex/explore/node?node=test", html, soup) is None
