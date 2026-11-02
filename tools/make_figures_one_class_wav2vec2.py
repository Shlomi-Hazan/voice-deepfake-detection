#!/usr/bin/env python3
"""Render the two illustrations of the One-Class Learning + wav2vec 2.0 research card (HE + EN).

Every number and phrase comes from
literature/09-one-class-wav2vec2/research-card.*.md.
Output: literature/09-one-class-wav2vec2/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_one_class_wav2vec2.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = (Path(__file__).resolve().parent.parent / "literature" / "09-one-class-wav2vec2" / "figures")

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
BLUE, GREEN, GRAY, RED, INK = "#2b5d8a", "#3f7d53", "#8a8f98", "#b5472f", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""


# ---------------------------------------------------------------- figure 1: architecture (Sections 7-12)
TXT1 = {
    "en": dict(audio="Speech Audio", lfcc="LFCC\n(192-d)", wav2vec="wav2vec 2.0 Base\n(frozen, 768-d)",
               subnets="4 Sub-networks\n(Bi-LSTM + LCNN)", fusion="Weighted Fusion\n(Optuna-tuned)",
               svdd="Deep SVDD\nHypersphere (c, R)", score="Anomaly Score\nd(x) = \u2016f(x) \u2212 c\u2016\u2082"),
    "he": dict(audio="אות הדיבור", lfcc="LFCC\n(192 מימדים)", wav2vec="wav2vec 2.0 Base\n(קפוא, 768 מימדים)",
               subnets="4 רשתות משנה\n(Bi-LSTM + LCNN)", fusion="Weighted Fusion\n(מכוונן ב-Optuna)",
               svdd="Deep SVDD\nHypersphere (c, R)", score="ציון חריגה\nd(x) = \u2016f(x) \u2212 c\u2016\u2082"),
}


def fig1(lang):
    he = lang == "he"
    d = TXT1[lang]
    arrow = "←" if he else "→"
    down = "↓"

    def box(txt, fill=False):
        cls = "box fill" if fill else "box"
        return f'<div class="{cls}">{txt.replace(chr(10), "<br>")}</div>'

    top = (f'{box(d["lfcc"])}<div class="plus">+</div>{box(d["wav2vec"])}')
    return f"""<div id="fig" style="width:760px;direction:{'rtl' if he else 'ltr'}"><style>
      .col{{display:flex;flex-direction:column;align-items:center}}
      .row{{display:flex;align-items:center;justify-content:center}}
      .box{{direction:{'rtl' if he else 'ltr'};width:200px;border:1.5px solid #444;border-radius:6px;
            padding:10px;background:#f7f8fa;font-size:14px;font-weight:bold;text-align:center;line-height:1.35}}
      .box.fill{{background:{BLUE};color:#fff;border-color:{BLUE}}}
      .plus{{font-size:20px;color:#444;padding:0 10px}}
      .arr{{font-size:24px;color:#444;margin:3px 0}}
      .audio{{border:1.5px solid #444;border-radius:20px;padding:8px 18px;background:#fff;font-size:14px;
              font-weight:bold;margin-bottom:6px}}
    </style>
    <div class="col">
      <div class="audio">{d['audio']}</div>
      <div class="arr">{down}</div>
      <div class="row">{top}</div>
      <div class="arr">{down}</div>
      {box(d['subnets'])}
      <div class="arr">{down}</div>
      {box(d['fusion'])}
      <div class="arr">{down}</div>
      {box(d['svdd'], True)}
      <div class="arr">{down}</div>
      {box(d['score'], True)}
    </div></div>"""


# ---------------------------------------------------------------- figure 2: Table I + Table II (16.1, 17.1)
MODELS = ["LFCC + One-Class SVM", "Deep SVDD\n(no wav2vec 2.0)", "wav2vec 2.0 +\nBinary Classification",
          "Proposed Method"]
EER_2019 = [8.76, 5.42, 2.35, 2.13]
EER_2021 = [22.31, 15.67, 18.45, 6.89]
LEGEND = {"en": ("ASVspoof 2019 LA", "ASVspoof 2021 DF"), "he": ("ASVspoof 2019 LA", "ASVspoof 2021 DF")}


def fig2(lang):
    he = lang == "he"
    legend = LEGEND[lang]
    scale = 230 / 23
    groups = ""
    for name, e19, e21 in zip(MODELS, EER_2019, EER_2021):
        col = BLUE if "Proposed" in name else GRAY
        groups += (f'<div class="grp"><div class="bars">'
                   f'<div class="col"><span class="v">{e19:.2f}</span>'
                   f'<span class="bar" style="height:{e19*scale:.1f}px;background:{col}"></span></div>'
                   f'<div class="col"><span class="v">{e21:.2f}</span>'
                   f'<span class="bar" style="height:{e21*scale:.1f}px;background:{col};opacity:0.55"></span></div>'
                   f'</div><div class="gl">{name.replace(chr(10), "<br>")}</div></div>')
    return f"""<div id="fig" style="width:860px"><style>
      .legend{{display:flex;gap:20px;justify-content:center;margin-bottom:10px;font-size:14px;direction:ltr}}
      .sw{{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-1px}}
      .ytitle{{font-size:12.5px;color:#555;margin:0 0 4px 4px;direction:ltr;text-align:left}}
      .plot{{display:flex;justify-content:space-around;align-items:flex-end;height:270px;
             border-left:1.5px solid #555;border-bottom:1.5px solid #555;padding:0 8px;direction:ltr}}
      .grp{{display:flex;flex-direction:column;align-items:center;width:180px}}
      .bars{{display:flex;align-items:flex-end;gap:8px;height:250px}}
      .col{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:38px}}
      .bar{{display:block;width:100%}}
      .v{{font-size:11px;margin-bottom:3px}}
      .gl{{margin-top:6px;font-size:12.5px;font-weight:bold;text-align:center;line-height:1.3}}
    </style><div class="legend">
      <span><i class="sw" style="background:{GRAY}"></i>{legend[0]}</span>
      <span><i class="sw" style="background:{GRAY};opacity:0.55"></i>{legend[1]}</span></div>
    <div class="ytitle">EER (%)</div><div class="plot">{groups}</div></div>"""


FIGS = [("fig1-architecture", fig1), ("fig2-eer-both-datasets", fig2)]


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
