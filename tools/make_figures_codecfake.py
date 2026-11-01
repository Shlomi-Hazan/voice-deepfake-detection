#!/usr/bin/env python3
"""Render the three illustrations of the CodecFake research card (HE + EN).

Every number and phrase comes from literature/06-codecfake/research-card.*.md.
Output: literature/06-codecfake/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_codecfake.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "literature" / "06-codecfake" / "figures"

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
BLUE, GREEN, GRAY, RED, INK = "#2b5d8a", "#3f7d53", "#8a8f98", "#b5472f", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""


# ---------------------------------------------------------------- figure 1: Generation vs Resynthesis (5.1-5.2)
TXT1 = {
    "en": dict(
        title_a="Full Speech Generation", title_b="Codec Resynthesis",
        a=["Context / Text", "Context Encoder", "Neural Codec Language Model",
           "Generated Speech Codes", "Neural Codec Decoder", "Generated Speech"],
        b=["Original Speech", "Neural Codec Encoder", "Discrete Speech Codes",
           "Neural Codec Decoder", "Reconstructed Speech"]),
    "he": dict(
        title_a="Full Speech Generation", title_b="Codec Resynthesis",
        a=["Context / Text", "Context Encoder", "Neural Codec Language Model",
           "Generated Speech Codes", "Neural Codec Decoder", "Generated Speech"],
        b=["Original Speech", "Neural Codec Encoder", "Discrete Speech Codes",
           "Neural Codec Decoder", "Reconstructed Speech"]),
}


def fig1(lang):
    he = lang == "he"
    d = TXT1[lang]
    arrow = "↓"

    def col(title, steps, fill_last):
        boxes = ""
        for i, s in enumerate(steps):
            cls = "box fill" if (fill_last and i == len(steps) - 1) else "box"
            boxes += f'<div class="{cls}">{s}</div>'
            if i < len(steps) - 1:
                boxes += f'<div class="arr">{arrow}</div>'
        return f'<div class="col"><div class="ct">{title}</div>{boxes}</div>'

    return f"""<div id="fig" style="width:760px;direction:{'rtl' if he else 'ltr'}"><style>
      .row{{display:flex;justify-content:space-around;align-items:flex-start;gap:30px}}
      .col{{display:flex;flex-direction:column;align-items:center;width:330px}}
      .ct{{font-size:16px;font-weight:bold;margin-bottom:10px;color:{BLUE}}}
      .box{{direction:ltr;width:280px;border:1.5px solid #444;border-radius:6px;padding:8px;
            background:#f7f8fa;font-size:13.5px;font-weight:bold;text-align:center;margin:2px 0}}
      .box.fill{{background:{BLUE};color:#fff;border-color:{BLUE}}}
      .arr{{font-size:18px;color:#444;margin:1px 0}}
    </style><div class="row">{col(d['title_a'], d['a'], True)}{col(d['title_b'], d['b'], True)}</div></div>"""


# ---------------------------------------------------------------- figure 2: Cross-Testing matrix (Section 12.4)
MATRIX = [
    ("A", [0.00, 1.06, 5.56]),
    ("B1", [36.16, 1.46, 29.27]),
    ("E", [35.23, 31.79, 0.00]),
]
COLS = ["A", "B1", "E"]


def fig2(lang):
    he = lang == "he"
    header = ("בדיקה על →" if he else "Tested on →")
    rowhdr = ("אומן על ↓" if he else "Trained on ↓")

    def color(v):
        if v < 10:
            return "#eaf3ee"
        if v < 25:
            return "#fbead9"
        return "#fbe3e0"

    rows = ""
    for name, vals in MATRIX:
        cells = "".join(f'<td style="background:{color(v)}">{v:.2f}%</td>' for v in vals)
        rows += f'<tr><th>{name}</th>{cells}</tr>'
    cols = "".join(f'<th>{c}</th>' for c in COLS)
    return f"""<div id="fig" style="width:480px;direction:{'rtl' if he else 'ltr'}"><style>
      table{{border-collapse:collapse;width:100%;font-size:15px}}
      th,td{{border:1px solid #999;padding:8px 10px;text-align:center}}
      th{{background:#eaeef4;font-weight:bold}}
      td{{font-weight:bold}}
      .cap{{font-size:12.5px;color:#555;margin-top:6px;text-align:center}}
    </style><table><tr><th></th><th colspan="3">{header}</th></tr>
      <tr><th>{rowhdr}</th>{cols}</tr>{rows}</table></div>"""


# ---------------------------------------------------------------- figure 3: CodecFake vs ASVspoof (Section 13.2)
SYS = [
    ("AASIST-L — ASVspoof", 13.91, 33.33, 25.00, GRAY),
    ("AASIST-L — CodecFake E", 0.40, 5.56, 8.33, BLUE),
]
TASKS = {"en": ["VALL-E", "VALL-E X", "SpeechX"], "he": ["VALL-E", "VALL-E X", "SpeechX"]}


def fig3(lang):
    he = lang == "he"
    tasks = TASKS[lang]
    legend = "".join(f'<span><i class="sw" style="background:{c}"></i>{n}</span>' for n, *_, c in SYS)
    scale = 170 / 35
    groups = ""
    for ti, task in enumerate(tasks):
        bars = ""
        for name, *vals, col in SYS:
            v = vals[ti]
            bars += (f'<div class="col"><span class="v">{v:.2f}</span>'
                     f'<span class="bar" style="height:{v*scale:.1f}px;background:{col}"></span></div>')
        groups += f'<div class="grp"><div class="bars">{bars}</div><div class="gl">{task}</div></div>'
    return f"""<div id="fig" style="width:560px"><style>
      .legend{{display:flex;gap:18px;justify-content:center;margin-bottom:12px;font-size:14px;direction:ltr}}
      .sw{{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-1px}}
      .plot{{display:flex;justify-content:space-around;align-items:flex-end;height:210px;direction:ltr}}
      .grp{{display:flex;flex-direction:column;align-items:center}}
      .bars{{display:flex;align-items:flex-end;gap:12px;height:190px}}
      .col{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:40px}}
      .bar{{display:block;width:100%}}
      .v{{font-size:12.5px;margin-bottom:3px}}
      .gl{{margin-top:6px;font-size:14px;font-weight:bold}}
    </style><div class="legend">{legend}</div><div class="plot">{groups}</div></div>"""


FIGS = [("fig1-generation-vs-resynthesis", fig1), ("fig2-cross-testing", fig2),
        ("fig3-codec-vs-asvspoof", fig3)]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=2)
        for name, fn in FIGS:
            for lang in ("he", "en"):
                html = (f'<html lang="{lang}"><head><meta charset="utf-8"><style>{CSS}</style></head>'
                        f"<body>{fn(lang)}</body></html>")
                page.set_content(html)
                path = OUT / f"{name}.{lang}.png"
                page.locator("#fig").screenshot(path=str(path))
                print("wrote", path)
        browser.close()


if __name__ == "__main__":
    main()
