#!/usr/bin/env python3
"""Render the three illustrations of the AASIST research card (HE + EN).

Every number and phrase comes from literature/03-aasist/research-card.*.md.
Output: literature/03-aasist/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_aasist.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "literature" / "03-aasist" / "figures"

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
BLUE, RED, GRAY, INK = "#2b5d8a", "#b5472f", "#8a8f98", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""


# ---------------------------------------------------------------- figure 1: information flow (Section 6.1)
STEPS = [  # (label, is one of the three architectural novelties of Section 2)
    ("Raw Waveform", False),
    ("RawNet2-based Encoder", False),
    ("Temporal Graph + Spectral Graph", False),
    ("Combined Heterogeneous Graph", False),
    ("HS-GAL", True),
    ("Max Graph Operation", True),
    ("Readout", True),
    ("Binary Classification", False),
]
LEGEND1 = {"en": "Architectural novelty", "he": "חידוש ארכיטקטוני"}


def fig1(lang):
    he = lang == "he"
    arrow = "←" if he else "→"
    back = "→" if he else "←"

    def box(i):
        label, nov = STEPS[i]
        cls = "box nov" if nov else "box"
        return f'<div class="{cls}">{label}</div>'

    row1 = f'<div class="arr">{arrow}</div>'.join(box(i) for i in range(4))
    row2 = f'<div class="arr">{back}</div>'.join(box(i) for i in range(4, 8))
    row2_dir = "ltr" if he else "rtl"
    return f"""<div id="fig" style="width:900px;direction:{'rtl' if he else 'ltr'}"><style>
      .flow{{display:flex;align-items:stretch;justify-content:space-between;width:856px}}
      .box{{direction:ltr;width:170px;border:1.5px solid #444;border-radius:6px;padding:12px 10px;
            background:#f7f8fa;font-size:17px;font-weight:bold;text-align:center;
            display:flex;align-items:center;justify-content:center;min-height:74px}}
      .box.nov{{background:{BLUE};color:#fff;border-color:{BLUE}}}
      .arr{{display:flex;align-items:center;font-size:26px;color:#444}}
      .dn{{font-size:26px;color:#444;padding:4px 0;text-align:center;width:170px;
           margin-{'right' if he else 'left'}:auto}}
      .lg{{margin-top:12px;font-size:15px;display:flex;align-items:center;gap:8px}}
      .sw{{display:inline-block;width:16px;height:16px;background:{BLUE}}}
    </style><div class="flow">{row1}</div><div class="dn">↓</div>
    <div class="flow" style="direction:{row2_dir}">{row2}</div>
    <div class="lg"><i class="sw"></i>{LEGEND1[lang]}</div></div>"""


# ---------------------------------------------------------------- figure 2: Table 2 (Section 10.4)
SYSTEMS = [  # name, params, EER in the reported run, own model?
    ("AASIST", "297K", 0.83, True),
    ("AASIST-L", "85K", 0.99, True),
    ("RawGAT-ST", "437K", 1.19, False),
    ("SENet", "1,100K", 1.14, False),
    ("Res-TSSDNet", "350K", 1.64, False),
    ("Raw PC-DARTS", "24,480K", 1.77, False),
]


def fig2(lang):
    he = lang == "he"
    head = ("EER בריצה המדווחת", "פרמטרים") if he else ("EER in the reported run", "Parameters")
    scale = 330 / 1.8
    rows = ""
    for name, params, eer, own in SYSTEMS:
        col = BLUE if own else GRAY
        rows += (f'<div class="row"><div class="lab">{name}</div>'
                 f'<div class="bars"><span class="bar" style="width:{eer*scale:.1f}px;background:{col}"></span>'
                 f'<span class="v">{eer:.2f}%</span></div><div class="pm">{params}</div></div>')
    return f"""<div id="fig" style="width:820px"><style>
      .hd{{display:flex;align-items:flex-end;margin-bottom:6px;font-size:14px;color:#555;direction:ltr}}
      .hd .a{{width:172px}} .hd .b{{flex:1;text-align:left;padding-left:8px}} .hd .c{{width:120px;text-align:center}}
      .row{{display:flex;align-items:center;margin:7px 0;direction:ltr}}
      .lab{{width:160px;text-align:right;padding-right:12px;font-size:16px;font-weight:bold}}
      .bars{{flex:1;border-left:1.5px solid #555;display:flex;align-items:center;height:30px}}
      .bar{{display:inline-block;height:22px}}
      .v{{margin-left:8px;font-size:15px;font-weight:bold}}
      .pm{{width:120px;text-align:center;font-size:15px;color:#333}}
    </style><div class="hd"><div class="a"></div><div class="b">{head[0]}</div><div class="c">{head[1]}</div></div>{rows}</div>"""


# ---------------------------------------------------------------- figure 3: ablation (Section 11.2)
ABL = {
    "en": [("Full AASIST", 1.13, True), ("Without Heterogeneous Attention", 1.44, False),
           ("Without Stack Node, with a conventional Readout", 1.21, False), ("Without MGO", 1.35, False)],
    "he": [("AASIST מלא", 1.13, True), ("ללא Heterogeneous Attention", 1.44, False),
           ("ללא Stack Node, עם Readout קונבנציונלי", 1.21, False), ("ללא MGO", 1.35, False)],
}


def fig3(lang):
    he = lang == "he"
    scale = 360 / 1.6
    rows = ""
    for name, eer, full in ABL[lang]:
        col = BLUE if full else GRAY
        rows += (f'<div class="row"><div class="lab" style="direction:{"rtl" if he else "ltr"}">{name}</div>'
                 f'<div class="bars"><span class="bar" style="width:{eer*scale:.1f}px;background:{col}"></span>'
                 f'<span class="v">{eer:.2f}%</span></div></div>')
    axis = "EER" + (" ממוצע" if he else " (average)")
    return f"""<div id="fig" style="width:900px"><style>
      .row{{display:flex;align-items:center;margin:9px 0;direction:ltr}}
      .lab{{width:320px;text-align:{'right' if he else 'right'};padding-right:14px;font-size:16px;line-height:1.3}}
      .bars{{flex:1;border-left:1.5px solid #555;display:flex;align-items:center;height:32px}}
      .bar{{display:inline-block;height:24px}}
      .v{{margin-left:10px;font-size:16px;font-weight:bold}}
      .axis{{margin-left:320px;font-size:13px;color:#555;padding-top:2px;direction:ltr}}
    </style>{rows}<div class="axis">{axis}</div></div>"""


FIGS = [("fig1-aasist-pipeline", fig1), ("fig2-systems-comparison", fig2), ("fig3-ablation", fig3)]


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
