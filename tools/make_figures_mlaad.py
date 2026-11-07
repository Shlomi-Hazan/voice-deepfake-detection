#!/usr/bin/env python3
"""Render the three illustrations of the MLAAD dataset research card (HE + EN).

Every number and phrase comes from
literature/datasets/01-mlaad/research-card.*.md.
Output: literature/datasets/01-mlaad/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_mlaad.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = (Path(__file__).resolve().parent.parent / "literature" / "datasets" / "01-mlaad" / "figures")

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
BLUE, GREEN, GRAY, RED, INK = "#2b5d8a", "#3f7d53", "#8a8f98", "#b5472f", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""


# ---------------------------------------------------------------- figure 1: MLAAD growth across versions (Section 6)
VERSIONS = [("v1", 63.0), ("v3", 163.9), ("v5", 398.3), ("v8", 570.3), ("v10", 1002.9), ("v11", 1153.6)]


def fig1(lang):
    he = lang == "he"
    scale = 230 / 1200
    bars = ""
    for v, hrs in VERSIONS:
        bars += (f'<div class="col"><span class="v">{hrs:,.1f}</span>'
                 f'<span class="bar" style="height:{hrs*scale:.1f}px;background:{BLUE}"></span>'
                 f'<span class="lab">{v}</span></div>')
    ytitle = "שעות דיבור סינתטי" if he else "Synthetic speech hours"
    return f"""<div id="fig" style="width:640px"><style>
      .ytitle{{font-size:12.5px;color:#555;margin-bottom:6px;text-align:{'right' if he else 'left'};direction:{'rtl' if he else 'ltr'}}}
      .plot{{display:flex;justify-content:space-around;align-items:flex-end;height:270px;
             border-left:1.5px solid #555;border-bottom:1.5px solid #555;padding:0 10px;direction:ltr}}
      .col{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:70px}}
      .bar{{display:block;width:44px}}
      .v{{font-size:12px;margin-bottom:3px}}
      .lab{{margin-top:6px;font-size:14px;font-weight:bold}}
    </style><div class="ytitle">{ytitle}</div><div class="plot">{bars}</div></div>"""


# ---------------------------------------------------------------- figure 2: data creation pipeline (Section 8)
STEPS = {
    "en": ["1. Select source\nexamples", "2. Prepare text\n(original or translated)",
           "3. Produce synthetic\nspeech (TTS)", "4. Speaker Reference\n(if supported)",
           "5. Save recording\n+ Metadata"],
    "he": ["1. בחירת דוגמאות\nמקור", "2. הכנת טקסט\n(מקורי או מתורגם)",
           "3. הפקת דיבור\nסינתטי (TTS)", "4. Speaker Reference\n(אם נתמך)",
           "5. שמירת הקלטה\n+ Metadata"],
}


def fig2(lang):
    he = lang == "he"
    steps = STEPS[lang]
    arrow = "←" if he else "→"
    boxes = ""
    for i, s in enumerate(steps):
        boxes += f'<div class="box">{s.replace(chr(10), "<br>")}</div>'
        if i < len(steps) - 1:
            boxes += f'<div class="arr">{arrow}</div>'
    return f"""<div id="fig" style="width:980px;direction:{'rtl' if he else 'ltr'}"><style>
      .row{{display:flex;align-items:stretch;justify-content:center}}
      .box{{direction:{'rtl' if he else 'ltr'};width:168px;border:1.5px solid #444;border-radius:6px;
            padding:10px;background:#f7f8fa;font-size:13.5px;font-weight:bold;text-align:center;
            display:flex;align-items:center;justify-content:center;line-height:1.3}}
      .arr{{display:flex;align-items:center;font-size:20px;color:#444;padding:0 5px}}
    </style><div class="row">{boxes}</div></div>"""


# ---------------------------------------------------------------- figure 3: Cross-Dataset Accuracy (Table VI, Section 20)
ROWS = [
    ("SSL-W2V2", "ASVspoof2021DF", 91.6, 75.5),
    ("SSL-W2V2", "WaveFake", 51.3, 69.8),
    ("WhisperDF", "WaveFake", 2.2, 97.2),
]
LEGEND = {"en": ("Trained on ASVspoof 2019", "Trained on MLAAD v1"),
          "he": ("אומן על ASVspoof 2019", "אומן על MLAAD v1")}


def fig3(lang):
    he = lang == "he"
    legend = LEGEND[lang]
    scale = 230 / 100
    groups = ""
    for model, evalset, a19, amlaad in ROWS:
        groups += (f'<div class="grp"><div class="bars">'
                   f'<div class="col"><span class="v">{a19:.1f}</span><span class="bar" style="height:{a19*scale:.1f}px;background:{GRAY}"></span></div>'
                   f'<div class="col"><span class="v">{amlaad:.1f}</span><span class="bar" style="height:{amlaad*scale:.1f}px;background:{BLUE}"></span></div>'
                   f'</div><div class="gl">{model}<br><span class="sub">on {evalset}</span></div></div>')
    return f"""<div id="fig" style="width:620px"><style>
      .legend{{display:flex;gap:18px;justify-content:center;margin-bottom:10px;font-size:13.5px;direction:ltr}}
      .sw{{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-1px}}
      .ytitle{{font-size:12.5px;color:#555;margin:0 0 4px 4px;direction:ltr;text-align:left}}
      .plot{{display:flex;justify-content:space-around;align-items:flex-end;height:260px;
             border-left:1.5px solid #555;border-bottom:1.5px solid #555;padding:0 10px;direction:ltr}}
      .grp{{display:flex;flex-direction:column;align-items:center}}
      .bars{{display:flex;align-items:flex-end;gap:10px;height:235px}}
      .col{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:40px}}
      .bar{{display:block;width:100%}}
      .v{{font-size:12px;margin-bottom:3px}}
      .gl{{margin-top:6px;font-size:13px;font-weight:bold;text-align:center;line-height:1.3}}
      .sub{{font-weight:normal;font-size:11px;color:#555}}
    </style><div class="legend">
      <span><i class="sw" style="background:{GRAY}"></i>{legend[0]}</span>
      <span><i class="sw" style="background:{BLUE}"></i>{legend[1]}</span></div>
    <div class="ytitle">Accuracy (%)</div><div class="plot">{groups}</div></div>"""


FIGS = [("fig1-mlaad-growth", fig1), ("fig2-pipeline", fig2), ("fig3-cross-dataset", fig3)]


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
