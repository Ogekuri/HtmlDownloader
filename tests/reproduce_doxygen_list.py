import re
from bs4 import BeautifulSoup
import sys

def escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )

def _convert_doxygen_definition_lists(soup: BeautifulSoup) -> None:
    # Handle <dl><dt>/<dd> pairs first
    for dl in list(soup.find_all("dl")):
        parts = []
        for dt in dl.find_all("dt"):
            dd = dt.find_next_sibling("dd")
            if not dd:
                continue
            label = (dt.get_text(" ", strip=True) or "").upper()
            desc_html = dd.decode_contents() or ""
            parts.append(f"<p><strong>{escape_html(label)}:</strong> {desc_html}</p>")
        if parts:
            frag = BeautifulSoup("\n".join(parts), "html.parser")
            dl.replace_with(frag)

    # Handle adjacent paragraph style: <p>Label</p> followed by <p>: description</p>
    for p in list(soup.find_all("p")):
        nxt = p.find_next_sibling()
        if not nxt or nxt.name != "p":
            continue
        left_text = (p.get_text(" ", strip=True) or "").strip()
        right_text = (nxt.get_text("\n", strip=True) or "")
        
        print(f"Checking pair: '{left_text}' + '{right_text}'")

        if not left_text or not right_text:
            continue
        # right_text should start with a colon-like prefix
        if re.match(r"^\s*:\s+", right_text):
            print("MATCHED!")
            # Merge
            desc_html = re.sub(r"^\s*:\s+", "", nxt.decode_contents(), count=1)
            label = left_text.upper()
            new_frag = BeautifulSoup(
                f"<p><strong>{escape_html(label)}:</strong> {desc_html}</p>",
                "html.parser",
            )
            p.replace_with(new_frag)
            nxt.decompose()
        else:
            print("NO MATCH")

html = """
<html>
<body>
    <p>Attention</p>
    <p>:   Please be aware that this version of DCL is supported only on ARM R5F.</p>

    <p>Note</p>
    <p>:   This requires CCS 12.5 and SysConfig 1.18.0 or later.</p>
</body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")
_convert_doxygen_definition_lists(soup)
print(soup.prettify())
