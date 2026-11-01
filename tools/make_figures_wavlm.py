#!/usr/bin/env python3
"""Render the three illustrations of the WavLM research card (HE + EN).

Every number and phrase comes from literature/05-wavlm/research-card.*.md.
Output: literature/05-wavlm/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_wavlm.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "literature" / "05-wavlm" / "figures"

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
BLUE, GREEN, GRAY, RED, INK = "#2b5d8a", "#3f7d53", "#8a8f98", "#b5472f", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""


# ---------------------------------------------------------------- figure 1: architecture flow (Section 6.1)
STEPS = {
    "en": ["Raw Audio", "CNN Feature\nEncoder", "Masking",
           "Transformer with Gated\nRelative Position Bias", "Prediction of Original\nSpeech Pseudo-labels"],
    "he": ["אות אודיו גולמי", "CNN Feature\nEncoder", "Masking",
           "Transformer with Gated\nRelative Position Bias", "חיזוי Pseudo-labels\nשל הדיבור המקורי"],
}


def fig1(lang):
    he = lang == "he"
    steps = STEPS[lang]
    arrow = "←" if he else "→"
    boxes = ""
    for i, s in enumerate(steps):
        fill = i >= 3
        cls = "box fill" if fill else "box"
        boxes += f'<div class="{cls}">{s.replace(chr(10), "<br>")}</div>'
        if i < len(steps) - 1:
            boxes += f'<div class="arr">{arrow}</div>'
    return f"""<div id="fig" style="width:980px;direction:{'rtl' if he else 'ltr'}"><style>
      .row{{display:flex;align-items:stretch;justify-content:center}}
      .box{{direction:{'rtl' if he else 'ltr'};width:168px;border:1.5px solid #444;border-radius:6px;
            padding:10px;background:#f7f8fa;font-size:14.5px;font-weight:bold;text-align:center;
            display:flex;align-items:center;justify-content:center;line-height:1.3}}
      .box.fill{{background:{BLUE};color:#fff;border-color:{BLUE}}}
      .arr{{display:flex;align-items:center;font-size:22px;color:#444;padding:0 6px}}
    </style><div class="row">{boxes}</div></div>"""


# ---------------------------------------------------------------- figure 2: Mix-94k dataset (Section 9.2)
PARTS = [("Libri-Light", 60000), ("GigaSpeech", 10000), ("VoxPopuli", 24000)]


def fig2(lang):
    he = lang == "he"
    total_l = "סה\"כ: 94,000 שעות" if he else "Total: 94,000 hours"
    scale = 420 / 60000
    rows = ""
    for name, hours in PARTS:
        rows += (f'<div class="row"><div class="lab">{name}</div>'
                 f'<div class="bars"><span class="bar" style="width:{max(hours*scale,2):.1f}px;background:{BLUE}"></span>'
                 f'<span class="v">{hours:,}</span></div></div>')
    return f"""<div id="fig" style="width:760px"><style>
      .row{{display:flex;align-items:center;margin:10px 0;direction:ltr}}
      .lab{{width:140px;text-align:right;padding-right:14px;font-size:16px;font-weight:bold}}
      .bars{{flex:1;border-left:1.5px solid #555;display:flex;align-items:center;height:30px}}
      .bar{{display:inline-block;height:22px}}
      .v{{margin-left:8px;font-size:15px}}
      .tot{{margin-top:10px;font-size:15px;font-weight:bold;text-align:{'right' if he else 'left'};
            direction:{'rtl' if he else 'ltr'}}}
    </style>{rows}<div class="tot">{total_l}</div></div>"""


# ---------------------------------------------------------------- figure 3: SUPERB Base comparison (Section 12.1)
MODELS = [
    ("wav2vec 2.0 Base", 75.18, 6.02, 6.08, 6.43, GRAY),
    ("HuBERT Base", 81.42, 5.11, 5.88, 6.42, GRAY),
    ("WavLM Base", 84.51, 4.69, 4.55, 6.21, BLUE),
]
METRICS = {
    "en": ["SID Accuracy (%) \u2191", "ASV EER (%) \u2193", "SD DER (%) \u2193", "ASR WER (%) \u2193"],
    "he": ["SID Accuracy (%) \u2191", "ASV EER (%) \u2193", "SD DER (%) \u2193", "ASR WER (%) \u2193"],
}


def fig3(lang):
    he = lang == "he"
    legend = "".join(f'<span><i class="sw" style="background:{c}"></i>{n}</span>' for n, *_, c in MODELS)
    metrics = METRICS[lang]
    panels = ""
    for mi, title in enumerate(metrics):
        vals = [m[mi + 1] for m in MODELS]
        vmax = max(vals)
        scale = 150 / vmax
        bars = ""
        for (name, *v), col in zip(MODELS, (m[-1] for m in MODELS)):
            val = v[mi]
            bars += (f'<div class="col"><span class="v">{val:.2f}</span>'
                     f'<span class="bar" style="height:{val*scale:.1f}px;background:{col}"></span></div>')
        panels += f'<div class="panel"><div class="bars">{bars}</div><div class="pt">{title}</div></div>'
    return f"""<div id="fig" style="width:900px"><style>
      .legend{{display:flex;gap:20px;justify-content:center;margin-bottom:14px;font-size:15px;direction:ltr}}
      .sw{{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-1px}}
      .row4{{display:flex;justify-content:space-around}}
      .panel{{display:flex;flex-direction:column;align-items:center;width:210px}}
      .bars{{display:flex;align-items:flex-end;gap:10px;height:170px}}
      .col{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:26px}}
      .bar{{display:block;width:100%}}
      .v{{font-size:11.5px;margin-bottom:3px}}
      .pt{{margin-top:8px;font-size:13px;color:#444;text-align:center;direction:ltr}}
    </style><div class="legend">{legend}</div><div class="row4">{panels}</div></div>"""


FIGS = [("fig1-architecture", fig1), ("fig2-mix94k", fig2), ("fig3-superb-base", fig3)]


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
