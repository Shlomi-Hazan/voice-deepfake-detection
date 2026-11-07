#!/usr/bin/env python3
"""Render the three illustrations of the AT-ADD research card (HE + EN).

Every number comes from literature/10-at-add/research-card.*.md.
Output: literature/10-at-add/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_at_add.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "literature" / "10-at-add" / "figures"

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
BLUE, GREEN, GRAY, RED, INK = "#2b5d8a", "#3f7d53", "#8a8f98", "#b5472f", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""


# ------------------------------------------------ figure 1: class composition per split (Section 6)
SPLITS = [("Train", 9999, 39576), ("Dev", 10000, 39734), ("Progress", 4000, 25269), ("Eval", 19998, 126348)]
LEG1 = {"en": ("Real", "Fake"), "he": ("Real", "Fake")}


def fig1(lang):
    leg = LEG1[lang]
    scale = 250 / 126348
    groups = ""
    for name, real, fake in SPLITS:
        groups += (f'<div class="grp"><div class="bars">'
                   f'<div class="col"><span class="v">{real:,}</span><span class="bar" style="height:{max(real*scale,2):.1f}px;background:{GREEN}"></span></div>'
                   f'<div class="col"><span class="v">{fake:,}</span><span class="bar" style="height:{fake*scale:.1f}px;background:{BLUE}"></span></div>'
                   f'</div><div class="gl">{name}</div></div>')
    return f"""<div id="fig" style="width:680px"><style>
      .legend{{display:flex;gap:20px;justify-content:center;margin-bottom:10px;font-size:14px;direction:ltr}}
      .sw{{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-1px}}
      .plot{{display:flex;justify-content:space-around;align-items:flex-end;height:285px;
             border-left:1.5px solid #555;border-bottom:1.5px solid #555;padding:0 8px;direction:ltr}}
      .grp{{display:flex;flex-direction:column;align-items:center}}
      .bars{{display:flex;align-items:flex-end;gap:8px;height:265px}}
      .col{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:56px}}
      .bar{{display:block;width:100%}}
      .v{{font-size:11px;margin-bottom:3px}}
      .gl{{margin-top:6px;font-size:14px;font-weight:bold}}
    </style><div class="legend">
      <span><i class="sw" style="background:{GREEN}"></i>{leg[0]}</span>
      <span><i class="sw" style="background:{BLUE}"></i>{leg[1]}</span></div>
    <div class="plot">{groups}</div></div>"""


# ------------------------------------------------ figure 2: Dev vs Eval Macro-F1 (Section 14)
GAP = [("AASIST", 94.16, 60.39), ("FT-XLSR-AASIST", 99.70, 76.73), ("WPT-XLSR-AASIST", 96.27, 73.35)]
LEG2 = {"en": ("Dev Macro-F1", "Eval Macro-F1"), "he": ("Macro-F1 ב-Dev", "Macro-F1 ב-Eval")}


def fig2(lang):
    leg = LEG2[lang]
    scale = 250 / 100
    groups = ""
    for name, dev, ev in GAP:
        groups += (f'<div class="grp"><div class="bars">'
                   f'<div class="col"><span class="v">{dev:.2f}</span><span class="bar" style="height:{dev*scale:.1f}px;background:{GRAY}"></span></div>'
                   f'<div class="col"><span class="v">{ev:.2f}</span><span class="bar" style="height:{ev*scale:.1f}px;background:{BLUE}"></span></div>'
                   f'</div><div class="gl">{name}</div></div>')
    return f"""<div id="fig" style="width:640px"><style>
      .legend{{display:flex;gap:20px;justify-content:center;margin-bottom:10px;font-size:14px;direction:ltr}}
      .sw{{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-1px}}
      .ytitle{{font-size:12.5px;color:#555;margin:0 0 4px 4px;direction:ltr;text-align:left}}
      .plot{{display:flex;justify-content:space-around;align-items:flex-end;height:285px;
             border-left:1.5px solid #555;border-bottom:1.5px solid #555;padding:0 8px;direction:ltr}}
      .grp{{display:flex;flex-direction:column;align-items:center}}
      .bars{{display:flex;align-items:flex-end;gap:10px;height:268px}}
      .col{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:64px}}
      .bar{{display:block;width:100%}}
      .v{{font-size:12px;margin-bottom:3px}}
      .gl{{margin-top:6px;font-size:13.5px;font-weight:bold}}
    </style><div class="legend">
      <span><i class="sw" style="background:{GRAY}"></i>{leg[0]}</span>
      <span><i class="sw" style="background:{BLUE}"></i>{leg[1]}</span></div>
    <div class="ytitle">Macro-F1 (%)</div><div class="plot">{groups}</div></div>"""


# ------------------------------------------------ figure 3: top-5 leaderboard (Section 15)
BOARD = [("1. WaveShield", 90.71, BLUE), ("2. Fosafer", 86.67, GRAY), ("3. sonomsl", 86.63, GRAY),
         ("4. ThreeTO", 83.79, GRAY), ("5. NKU-HLT", 83.68, GRAY)]


def fig3(lang):
    scale = 330 / 100
    rows = ""
    for name, v, col in BOARD:
        rows += (f'<div class="row"><div class="lab">{name}</div>'
                 f'<div class="bars"><span class="bar" style="width:{v*scale:.1f}px;background:{col}"></span>'
                 f'<span class="v">{v:.2f}%</span></div></div>')
    return f"""<div id="fig" style="width:640px"><style>
      .row{{display:flex;align-items:center;margin:9px 0;direction:ltr}}
      .lab{{width:150px;text-align:right;padding-right:14px;font-size:15px;font-weight:bold}}
      .bars{{flex:1;border-left:1.5px solid #555;display:flex;align-items:center;height:30px}}
      .bar{{display:inline-block;height:22px}}
      .v{{margin-left:8px;font-size:15px;font-weight:bold}}
    </style>{rows}</div>"""


FIGS = [("fig1-class-composition", fig1), ("fig2-dev-eval-gap", fig2), ("fig3-leaderboard", fig3)]


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
