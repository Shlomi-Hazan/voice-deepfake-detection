#!/usr/bin/env python3
"""Render the two illustrations of the wav2vec 2.0 research card (HE + EN).

Every number and phrase comes from literature/04-wav2vec2/research-card.*.md.
Output: literature/04-wav2vec2/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_wav2vec2.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "literature" / "04-wav2vec2" / "figures"

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
BLUE, GREEN, GRAY, INK = "#2b5d8a", "#3f7d53", "#8a8f98", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""


# ---------------------------------------------------------------- figure 1: architecture flow (Section 5.1)
TXT1 = {
    "en": dict(
        raw="Raw Waveform", cnn="CNN Feature\nEncoder", lat="Continuous Latent\nRepresentations",
        mask="Masking +\nTransformer", quant="Quantization",
        ctx="Contextual\nrepresentations", disc="Discrete target\nrepresentations",
        meet="Contrastive Learning"),
    "he": dict(
        raw="אות אודיו גולמי", cnn="CNN Feature\nEncoder", lat="ייצוגים לטנטיים\nרציפים",
        mask="Masking +\nTransformer", quant="Quantization",
        ctx="ייצוגים\nהקשריים", disc="ייצוגי מטרה\nבדידים",
        meet="Contrastive Learning"),
}


def fig1(lang):
    he = lang == "he"
    d = TXT1[lang]
    arrow = "←" if he else "→"

    def box(label, fill=False):
        cls = "box fill" if fill else "box"
        return f'<div class="{cls}">{label.replace(chr(10), "<br>")}</div>'

    top = f'{box(d["raw"])}<div class="arr">{arrow}</div>{box(d["cnn"])}<div class="arr">{arrow}</div>{box(d["lat"])}'
    down = '<div class="splitv">↙</div><div class="splitv" style="margin-right:0">↘</div>' if he else \
           '<div class="splitv">↙</div><div class="splitv" style="margin-left:0">↘</div>'
    branches = (f'{box(d["mask"], True)}<div class="arr">{arrow}</div>{box(d["ctx"])}'
                f'<div class="meetarr">{arrow}</div>'
                f'<div class="meet">{d["meet"]}</div>'
                f'<div class="meetarr">{"←" if he else "←"}</div>'
                f'{box(d["disc"])}<div class="arr">{arrow}</div>{box(d["quant"], True)}')
    return f"""<div id="fig" style="width:900px;direction:{'rtl' if he else 'ltr'}"><style>
      .row{{display:flex;align-items:center;justify-content:center}}
      .box{{direction:{'rtl' if he else 'ltr'};width:150px;min-height:58px;border:1.5px solid #444;border-radius:6px;
            padding:8px;background:#f7f8fa;font-size:14.5px;font-weight:bold;text-align:center;
            display:flex;align-items:center;justify-content:center;line-height:1.3}}
      .box.fill{{background:{BLUE};color:#fff;border-color:{BLUE}}}
      .arr{{display:flex;align-items:center;font-size:22px;color:#444;padding:0 6px}}
      .meetarr{{display:flex;align-items:center;font-size:22px;color:#444;padding:0 4px}}
      .meet{{width:150px;min-height:58px;border:1.5px solid {GREEN};border-radius:6px;background:#eef6ef;
             display:flex;align-items:center;justify-content:center;font-size:14.5px;font-weight:bold;
             text-align:center;color:{GREEN};padding:6px}}
      .mid{{text-align:center;font-size:26px;color:#444;margin:4px 0}}
    </style><div class="row">{top}</div><div class="mid">↓</div><div class="row">{branches}</div></div>"""


# ---------------------------------------------------------------- figure 2: Table 1 (Section 10.1)
ROWS = [  # labeled data, test-clean, test-other
    ("10 min", 4.8, 8.2), ("1 h", 2.9, 5.8), ("10 h", 2.6, 4.9), ("100 h", 2.0, 4.0), ("960 h", 1.8, 3.3),
]
ROWS_HE = [("10 דקות", 4.8, 8.2), ("שעה", 2.9, 5.8), ("10 שעות", 2.6, 4.9), ("100 שעות", 2.0, 4.0), ("960 שעות", 1.8, 3.3)]


def fig2(lang):
    he = lang == "he"
    rows = ROWS_HE if he else ROWS
    legend = ("test-clean", "test-other")
    scale = 240 / 8.2
    groups = ""
    for label, a, b in rows:
        groups += (f'<div class="grp"><div class="bars">'
                   f'<div class="col"><span class="v">{a:.1f}%</span><span class="bar" style="height:{a*scale:.1f}px;background:{BLUE}"></span></div>'
                   f'<div class="col"><span class="v">{b:.1f}%</span><span class="bar" style="height:{b*scale:.1f}px;background:{GRAY}"></span></div>'
                   f'</div><div class="gl">{label}</div></div>')
    return f"""<div id="fig" style="width:820px"><style>
      .legend{{display:flex;gap:22px;justify-content:center;margin-bottom:10px;font-size:16px;direction:ltr}}
      .sw{{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-1px}}
      .ytitle{{font-size:13px;color:#555;margin:0 0 4px 4px;direction:ltr;text-align:left}}
      .plot{{display:flex;justify-content:space-around;align-items:flex-end;height:280px;
             border-left:1.5px solid #555;border-bottom:1.5px solid #555;padding:0 10px;direction:ltr}}
      .grp{{display:flex;flex-direction:column;align-items:center}}
      .bars{{display:flex;align-items:flex-end;gap:7px;height:260px}}
      .col{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:40px}}
      .bar{{display:block;width:100%}}
      .v{{font-size:12.5px;margin-bottom:3px}}
      .gl{{margin-top:6px;font-size:15px;font-weight:bold;direction:{'rtl' if he else 'ltr'}}}
    </style><div class="legend">
      <span><i class="sw" style="background:{BLUE}"></i>{legend[0]}</span>
      <span><i class="sw" style="background:{GRAY}"></i>{legend[1]}</span></div>
    <div class="ytitle">WER (%)</div><div class="plot">{groups}</div></div>"""


FIGS = [("fig1-architecture", fig1), ("fig2-low-resource", fig2)]


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
