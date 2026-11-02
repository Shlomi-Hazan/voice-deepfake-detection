#!/usr/bin/env python3
"""Render the three illustrations of the Intelligent Voice Fraud Detection research card (HE + EN).

Every number and phrase comes from
literature/08-intelligent-voice-fraud/research-card.*.md.
Output: literature/08-intelligent-voice-fraud/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_intelligent_voice_fraud.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = (Path(__file__).resolve().parent.parent / "literature" / "08-intelligent-voice-fraud" / "figures")

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
BLUE, GREEN, GRAY, RED, INK = "#2b5d8a", "#3f7d53", "#8a8f98", "#b5472f", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""


# ---------------------------------------------------------------- figure 1: architecture flow (Section 6.2)
STEPS = {
    "en": ["Speech Audio", "Preprocessing", "MFCC + PLP", "GMM\u2013UBM Statistical\nRepresentation",
           "Lightweight CNN", "Voice Authentication /\nForgery Detection"],
    "he": ["Speech Audio", "Preprocessing", "MFCC + PLP", "ייצוג סטטיסטי\nGMM\u2013UBM",
           "Lightweight CNN", "אימות קולי /\nזיהוי זיוף"],
}


def fig1(lang):
    he = lang == "he"
    steps = STEPS[lang]
    arrow = "←" if he else "→"
    boxes = ""
    for i, s in enumerate(steps):
        fill = i == len(steps) - 1
        cls = "box fill" if fill else "box"
        boxes += f'<div class="{cls}">{s.replace(chr(10), "<br>")}</div>'
        if i < len(steps) - 1:
            boxes += f'<div class="arr">{arrow}</div>'
    return f"""<div id="fig" style="width:980px;direction:{'rtl' if he else 'ltr'}"><style>
      .row{{display:flex;align-items:stretch;justify-content:center}}
      .box{{direction:{'rtl' if he else 'ltr'};width:150px;border:1.5px solid #444;border-radius:6px;
            padding:10px;background:#f7f8fa;font-size:14px;font-weight:bold;text-align:center;
            display:flex;align-items:center;justify-content:center;line-height:1.3}}
      .box.fill{{background:{BLUE};color:#fff;border-color:{BLUE}}}
      .arr{{display:flex;align-items:center;font-size:20px;color:#444;padding:0 5px}}
    </style><div class="row">{boxes}</div></div>"""


# ---------------------------------------------------------------- figure 2: four decision categories (13.1-13.4)
CATS = {
    "en": [("Pass Test", "Speech considered authentic; verification succeeds", GREEN),
           ("Fail Test", "Speech does not match the identity's required features", GRAY),
           ("Level A Forgery", "Strong signs of synthesis or a Replay attack", RED),
           ("Level B Forgery", "Moderate signs of voice manipulation", "#c98a3e")],
    "he": [("Pass Test", "הדיבור נחשב אותנטי; האימות עובר", GREEN),
           ("Fail Test", "הדיבור אינו תואם את המאפיינים הנדרשים לזהות", GRAY),
           ("Level A Forgery", "סימנים חזקים לסינתזה או להתקפת Replay", RED),
           ("Level B Forgery", "סימנים מתונים למניפולציה קולית", "#c98a3e")],
}


def fig2(lang):
    he = lang == "he"
    cats = CATS[lang]
    boxes = ""
    for name, desc, col in cats:
        boxes += (f'<div class="cat"><div class="bar" style="background:{col}"></div>'
                  f'<div class="txt"><div class="nm">{name}</div><div class="ds">{desc}</div></div></div>')
    return f"""<div id="fig" style="width:680px;direction:{'rtl' if he else 'ltr'}"><style>
      .cat{{display:flex;align-items:stretch;margin:8px 0;border:1px solid #ccc;border-radius:6px;overflow:hidden}}
      .bar{{width:8px}}
      .txt{{padding:9px 14px;flex:1}}
      .nm{{font-size:15px;font-weight:bold;direction:ltr;text-align:{'right' if he else 'left'}}}
      .ds{{font-size:13.5px;color:#333;margin-top:2px}}
    </style>{boxes}</div>"""


# ---------------------------------------------------------------- figure 3: Table 1, EER comparison (16.1)
ROWS = [("LFCC + GMM", 7.44, GRAY), ("CQCC + GMM", 6.27, GRAY), ("MFCC+PLP+GMM+CNN", 4.79, BLUE)]


def fig3(lang):
    he = lang == "he"
    scale = 300 / 8
    rows = ""
    for name, eer, col in ROWS:
        rows += (f'<div class="row"><div class="lab">{name}</div>'
                 f'<div class="bars"><span class="bar" style="width:{eer*scale:.1f}px;background:{col}"></span>'
                 f'<span class="v">{eer:.2f}%</span></div></div>')
    return f"""<div id="fig" style="width:700px"><style>
      .row{{display:flex;align-items:center;margin:9px 0;direction:ltr}}
      .lab{{width:180px;text-align:right;padding-right:12px;font-size:15px;font-weight:bold}}
      .bars{{flex:1;border-left:1.5px solid #555;display:flex;align-items:center;height:30px}}
      .bar{{display:inline-block;height:22px}}
      .v{{margin-left:8px;font-size:15px;font-weight:bold}}
    </style>{rows}</div>"""


FIGS = [("fig1-architecture", fig1), ("fig2-decision-categories", fig2), ("fig3-eer-comparison", fig3)]


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
