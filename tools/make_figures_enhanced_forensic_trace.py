#!/usr/bin/env python3
"""Render the two illustrations of the Enhanced Forensic Trace Generation research card (HE + EN).

Every number and phrase comes from
literature/08-enhanced-forensic-trace/research-card.*.md.
Output: literature/08-enhanced-forensic-trace/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_enhanced_forensic_trace.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = (Path(__file__).resolve().parent.parent / "literature" / "08-enhanced-forensic-trace" / "figures")

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
BLUE, GREEN, GRAY, INK = "#2b5d8a", "#3f7d53", "#8a8f98", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""


# ---------------------------------------------------------------- figure 1: two processes (Section 5.1)
TXT1 = {
    "en": dict(
        title_a="Process A — Training the Generator", title_b="Process B — Producing features for detection",
        a=["Extract spectral features", "Reconstruct real speech via VQ-VAE",
           "Pass source + reconstruction through frozen Encoder",
           "Compute Loss functions in feature space", "Update the VQ-VAE (Backpropagation)"],
        b=["Extract spectral features from the recording", "Reconstruct via the trained VQ-VAE",
           "Combine original + reconstructed features", "Feed into the ResNet classifier",
           "Fake/Real decision or score"]),
    "he": dict(
        title_a="תהליך א — אימון ה-Generator", title_b="תהליך ב — הפקת מאפיינים לזיהוי",
        a=["חילוץ מאפיינים ספקטרליים", "שחזור דיבור אמיתי באמצעות VQ-VAE",
           "העברת המקור והשחזור דרך Encoder קפוא",
           "חישוב פונקציות Loss במרחב המאפיינים", "עדכון ה-VQ-VAE (Backpropagation)"],
        b=["חילוץ מאפיינים ספקטרליים מההקלטה", "שחזור באמצעות ה-VQ-VAE המאומן",
           "שילוב מאפיינים מקוריים + משוחזרים", "הזנה למסווג ResNet",
           "החלטה או ציון Fake/Real"]),
}


def fig1(lang):
    he = lang == "he"
    d = TXT1[lang]
    arrow = "↓"

    def col(title, steps):
        boxes = ""
        for i, s in enumerate(steps):
            boxes += f'<div class="box">{i + 1}. {s}</div>'
            if i < len(steps) - 1:
                boxes += f'<div class="arr">{arrow}</div>'
        return f'<div class="col"><div class="ct">{title}</div>{boxes}</div>'

    return f"""<div id="fig" style="width:900px;direction:{'rtl' if he else 'ltr'}"><style>
      .row{{display:flex;justify-content:space-around;align-items:flex-start;gap:26px}}
      .col{{display:flex;flex-direction:column;align-items:stretch;width:410px}}
      .ct{{font-size:15px;font-weight:bold;margin-bottom:10px;color:{BLUE};text-align:center}}
      .box{{direction:{'rtl' if he else 'ltr'};border:1.5px solid #444;border-radius:6px;padding:7px 10px;
            background:#f7f8fa;font-size:13px;text-align:{'right' if he else 'left'};margin:2px 0}}
      .arr{{font-size:16px;color:#444;margin:1px 0;text-align:center}}
    </style><div class="row">{col(d['title_a'], d['a'])}{col(d['title_b'], d['b'])}</div></div>"""


# ---------------------------------------------------------------- figure 2: Table 1, EER on 2021 (Section 15.1)
ROWS = [
    ("LFCC", 26.89, 20.87), ("CQCC", 23.29, 19.33), ("LPS", 22.64, 14.04),
]
LEGEND = {"en": ("Original", "Improved (FVQ)"), "he": ("מקורי", "משופר (FVQ)")}


def fig2(lang):
    he = lang == "he"
    legend = LEGEND[lang]
    scale = 230 / 27
    groups = ""
    for name, orig, impr in ROWS:
        groups += (f'<div class="grp"><div class="bars">'
                   f'<div class="col"><span class="v">{orig:.2f}%</span><span class="bar" style="height:{orig*scale:.1f}px;background:{GRAY}"></span></div>'
                   f'<div class="col"><span class="v">{impr:.2f}%</span><span class="bar" style="height:{impr*scale:.1f}px;background:{BLUE}"></span></div>'
                   f'</div><div class="gl">{name}</div></div>')
    return f"""<div id="fig" style="width:620px"><style>
      .legend{{display:flex;gap:18px;justify-content:center;margin-bottom:10px;font-size:14px;direction:ltr}}
      .sw{{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-1px}}
      .ytitle{{font-size:12.5px;color:#555;margin:0 0 4px 4px;direction:ltr;text-align:left}}
      .plot{{display:flex;justify-content:space-around;align-items:flex-end;height:270px;
             border-left:1.5px solid #555;border-bottom:1.5px solid #555;padding:0 10px;direction:ltr}}
      .grp{{display:flex;flex-direction:column;align-items:center}}
      .bars{{display:flex;align-items:flex-end;gap:10px;height:250px}}
      .col{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:40px}}
      .bar{{display:block;width:100%}}
      .v{{font-size:12px;margin-bottom:3px}}
      .gl{{margin-top:6px;font-size:15px;font-weight:bold}}
    </style><div class="legend">
      <span><i class="sw" style="background:{GRAY}"></i>{legend[0]}</span>
      <span><i class="sw" style="background:{BLUE}"></i>{legend[1]}</span></div>
    <div class="ytitle">EER on ASVspoof 2021 LA (%)</div><div class="plot">{groups}</div></div>"""


FIGS = [("fig1-architecture", fig1), ("fig2-eer-improvement", fig2)]


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
