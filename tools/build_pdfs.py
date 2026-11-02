#!/usr/bin/env python3
"""Build PDFs from the literature Markdown files (Hebrew RTL and English).

Convention: <name>.he.md -> right-to-left, <name>.en.md -> left-to-right.
Each PDF is written next to its Markdown file. Text is never modified; the
script only renders it (Markdown -> HTML -> Chromium print-to-PDF).

Setup (once):
    pip install markdown playwright
    playwright install chromium

Usage:
    python tools/build_pdfs.py literature/01-asvspoof5          # one paper folder
    python tools/build_pdfs.py literature/01-asvspoof5/research-card.he.md
    python tools/build_pdfs.py --all                            # every paper
    python tools/build_pdfs.py --all --only-stale               # skip up-to-date PDFs

Fonts: the stylesheet prefers David Libre / Frank Ruhl Libre / Noto Serif Hebrew
/ David / Times New Roman, then FreeSerif / Liberation Serif. Install one of the
first ones for the best academic look; the fallbacks render correctly too.
"""
import argparse
import html
import re
import sys
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
LIT = ROOT / "literature"
HEBREW = re.compile(r"[\u0590-\u05FF]")

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')

CSS = """
html { font-family: %(font)s; color: #1b1b1b; }
body { font-size: %(size)s; line-height: 1.55; margin: 0; }
h1 { font-size: 21pt; text-align: center; margin: 0 0 0.9em; padding-bottom: 0.35em;
     border-bottom: 2px solid #1f3a5f; color: #14284a; line-height: 1.25; }
h2 { font-size: 15pt; color: #1f3a5f; margin: 1.5em 0 0.55em; padding-bottom: 0.15em;
     border-bottom: 1px solid #9fb0c8; page-break-after: avoid; }
h3 { font-size: 12.5pt; color: #2a2a2a; margin: 1.15em 0 0.4em; page-break-after: avoid; }
p { margin: 0.5em 0; text-align: %(align)s; orphans: 3; widows: 3; }
hr { display: none; }
ul, ol { margin: 0.4em 0 0.7em; padding-%(start)s: 1.7em; }
li { margin: 0.22em 0; }
strong { color: #111; }
a { color: #1f3a5f; overflow-wrap: anywhere; }
p.subtitle { text-align: center; font-style: italic; font-size: 13pt; color: #333;
             margin: -0.3em 0 1.2em; unicode-bidi: plaintext; }
p.src { font-size: 10pt; color: #555; font-style: italic; margin-top: 0.8em; }
div.chain { margin: 0.8em auto; width: fit-content; text-align: left; }
div.chain p { margin: 0.15em 0; text-align: left; }
p.formula { direction: ltr; text-align: center; font-size: 12.5pt; margin: 0.7em 0;
            font-style: italic; }
table { border-collapse: collapse; width: 100%%; margin: 0.9em 0 1.1em; font-size: 10.5pt;
        border-top: 1.6px solid #222; border-bottom: 1.6px solid #222;
        page-break-inside: avoid; }
th { background: #eaeef4; border-bottom: 1px solid #222; padding: 5px 8px; font-weight: bold; }
td { padding: 4px 8px; border-bottom: 1px solid #d3d8e0; }
tr:last-child td { border-bottom: none; }
th, td { vertical-align: top; text-align: start; }
figure { margin: 1.1em 0 1.3em; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%%; height: auto; }
figcaption { font-size: 10pt; color: #444; font-style: italic; margin-top: 0.4em;
             text-align: center; }
"""


def render_html(md_path: Path) -> tuple[str, str]:
    """Return (html, title) for one Markdown file."""
    lang = "he" if md_path.name.endswith(".he.md") else "en"
    is_summary = "summary" in md_path.name
    text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "sane_lists"])

    # figure + caption: <p><img></p><p><em>caption</em></p>
    body = re.sub(
        r"<p>(<img [^>]+>)</p>\s*<p><em>(.*?)</em></p>",
        r"<figure>\1<figcaption>\2</figcaption></figure>", body, flags=re.S)

    # source lines ("Source:" / "מקור:")
    body = re.sub(r"<p>(<strong>(?:Source(?: in the paper)?|מקור(?: במאמר)?):</strong>)", r'<p class="src">\1', body)

    # standalone formulas (no Hebrew, contain "=")
    def formula(m):
        inner = m.group(1)
        plain = re.sub(r"<[^>]+>", "", inner)
        if any(c in plain for c in "=∈≈") and not HEBREW.search(plain) and "<img" not in inner and len(plain) < 120:
            return f'<p class="formula">{inner}</p>'
        return m.group(0)
    body = re.sub(r"<p>(.*?)</p>", formula, body, flags=re.S)

    def chain(m):
        first, arrows = m.group(1) or "", m.group(2)
        if HEBREW.search(first):  # the preceding paragraph is normal prose
            return first + f'<div class="chain" dir="ltr">{arrows}</div>'
        return f'<div class="chain" dir="ltr">{first}{arrows}</div>'
    body = re.sub(r"(<p>(?!→)[^<]*</p>\s*)?((?:<p>→[^<]*</p>\s*)+)", chain, body)

    body = re.sub(r"(</h1>\s*)<h2>(?!\d)(.*?)</h2>", r'\1<p class="subtitle">\2</p>', body, flags=re.S)

    if lang == "he":
        # A closing . ? ; : after a Latin word inside an RTL paragraph would otherwise
        # jump to the visual left of the whole Latin run. A left-to-right mark (display
        # only, the Markdown is untouched) keeps it attached to the word.
        def lrm(m):
            inner = m.group(2)
            plain = re.sub(r"<[^>]+>", "", inner).rstrip()
            strong = re.findall(r"[A-Za-z\u0590-\u05FF]", plain)
            if plain and plain[-1] in ".?;:" and strong and strong[-1].isascii():
                return f"{m.group(1)}{inner}&lrm;{m.group(3)}"
            return m.group(0)
        body = re.sub(r"(<(?:p|li)(?: [^>]*)?>)(.*?)(</(?:p|li)>)", lrm, body, flags=re.S)

    m = re.search(r"<h1>(.*?)</h1>", body, flags=re.S)
    title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))) if m else md_path.stem

    css = CSS % dict(
        font=FONT,
        size=((("11.6pt" if len(text) < 3300 else "11.0pt" if len(text) < 4000 else "10.4pt" if len(text) < 4300 else "10.0pt" if len(text) < 4600 else "9.5pt" if len(text) < 5100 else "9.1pt") if lang == "he"
               else ("10.8pt" if len(text) < 3300 else "10.2pt" if len(text) < 4200 else "9.6pt" if len(text) < 5200 else "9.1pt" if len(text) < 6200 else "8.6pt" if len(text) < 7000 else "8.2pt")) if is_summary
              else ("12.2pt" if lang == "he" else "11.5pt")),
        align="justify" if is_summary else "start",
        start="right" if lang == "he" else "left",
    )
    if is_summary:  # compact: the summary should fit one page
        css += "body{line-height:1.45} h1{font-size:18pt} h2{margin-top:1.1em} p{margin:0.4em 0}"
    doc = (f'<!DOCTYPE html><html lang="{lang}" dir="{"rtl" if lang == "he" else "ltr"}">'
           f'<head><meta charset="utf-8"><title>{html.escape(title)}</title>'
           f"<style>{css}</style></head><body>{body}</body></html>")
    return doc, title


FOOTER = ('<div style="width:100%;text-align:center;font-size:9px;color:#555;'
          'font-family:serif"><span class="pageNumber"></span> / '
          '<span class="totalPages"></span></div>')


def collect(targets, build_all):
    files = []
    if build_all:
        targets = [LIT]
    for t in targets:
        p = Path(t)
        if not p.is_absolute():
            p = (Path.cwd() / p).resolve()
        if p.is_file():
            files.append(p)
        else:
            files.extend(sorted(p.rglob("*.he.md")) + sorted(p.rglob("*.en.md")))
    return sorted(set(f for f in files if f.name.endswith((".he.md", ".en.md"))))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("targets", nargs="*", help="paper folder(s) or .md file(s)")
    ap.add_argument("--all", action="store_true", help="build every paper under literature/")
    ap.add_argument("--only-stale", action="store_true", help="skip PDFs newer than their Markdown")
    args = ap.parse_args()
    if not args.targets and not args.all:
        ap.error("give a folder/file or --all")

    files = collect(args.targets, args.all)
    if not files:
        sys.exit("no *.he.md / *.en.md files found")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for md in files:
            pdf = md.parent / (md.name[:-3] + ".pdf")
            if args.only_stale and pdf.exists() and pdf.stat().st_mtime >= md.stat().st_mtime:
                print("up to date:", pdf.relative_to(ROOT))
                continue
            doc, title = render_html(md)
            tmp = md.parent / f".{md.stem}.tmp.html"  # same folder so relative images resolve
            tmp.write_text(doc, encoding="utf-8")
            try:
                page.goto(tmp.as_uri())
                page.wait_for_load_state("load")
                page.pdf(path=str(pdf), format="A4", print_background=True,
                         margin=(dict(top="13mm", bottom="13mm", left="18mm", right="18mm")
                                 if "summary" in md.name else
                                 dict(top="22mm", bottom="22mm", left="22mm", right="22mm")),
                         display_header_footer=True, header_template="<div></div>",
                         footer_template=FOOTER)
            finally:
                tmp.unlink(missing_ok=True)
            print("built:", pdf.relative_to(ROOT))
        browser.close()


if __name__ == "__main__":
    main()
