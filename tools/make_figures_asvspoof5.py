#!/usr/bin/env python3
"""Render the three illustrations of the ASVspoof 5 research card (HE + EN).

Every number and phrase comes from literature/01-asvspoof5/research-card.*.md.
Output: literature/01-asvspoof5/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_asvspoof5.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "literature" / "01-asvspoof5" / "figures"

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
REAL, FAKE = "#2b5d8a", "#b5472f"
GRAY, BLUE, INK = "#8a8f98", "#2b5d8a", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""

# ---------------------------------------------------------------- figure 1
PARTS = [  # Table 1 of the card, section 5.2
    ("Training", 18797, 163560),
    ("Development", 31334, 109616),
    ("Evaluation Track 1", 138688, 542086),
    ("Evaluation Track 2", 100708, 395924),
]


def fig1(lang):
    he = lang == "he"
    real_l, fake_l = ("אמיתי", "מזויף") if he else ("Real", "Fake")
    scale = 520 / 542086
    rows = ""
    for name, r, f in PARTS:
        rows += f"""
        <div class="row"><div class="lab">{name}</div>
          <div class="bars">
            <div class="b"><span class="bar" style="width:{max(r*scale,2):.1f}px;background:{REAL}"></span><span class="v">{r:,}</span></div>
            <div class="b"><span class="bar" style="width:{max(f*scale,2):.1f}px;background:{FAKE}"></span><span class="v">{f:,}</span></div>
          </div></div>"""
    return f"""<div id="fig" style="width:860px"><style>
      .legend{{display:flex;gap:22px;justify-content:center;margin-bottom:12px;font-size:17px;direction:{'rtl' if he else 'ltr'}}}
      .sw{{display:inline-block;width:14px;height:14px;margin:0 6px;vertical-align:-1px}}
      .row{{display:flex;align-items:center;margin:10px 0;direction:ltr}}
      .lab{{width:170px;font-size:16px;text-align:right;padding-right:14px;font-weight:bold}}
      .bars{{flex:1;border-left:1.5px solid #555;padding-left:0}}
      .b{{display:flex;align-items:center;height:22px;margin:2px 0}}
      .bar{{display:inline-block;height:18px}}
      .v{{font-size:14px;margin-left:8px}}
    </style>
    <div class="legend"><span><i class="sw" style="background:{REAL}"></i>{real_l}</span>
    <span><i class="sw" style="background:{FAKE}"></i>{fake_l}</span></div>{rows}</div>"""


# ---------------------------------------------------------------- figure 2
FIG2 = {
    "en": dict(
        head="MLS divided into three separate source sets: A, B and C",
        stages=[
            ("First stage", "Partition A",
             "Developing TTS systems; the fake data is used to train Surrogate systems."),
            ("Second stage", "Partition B",
             "Developing and improving TTS and VC systems; Surrogate systems are used to evaluate the "
             "effectiveness of the forgeries and to tune the systems."),
            ("Third stage", "Partition C",
             "The improved systems create fake recordings of speakers, including combining some of the "
             "attacks with Adversarial processing."),
        ]),
    "he": dict(
        head="MLS חולק לשלוש קבוצות מקור נפרדות: A, B ו-C",
        stages=[
            ("שלב ראשון", "Partition A",
             "פיתוח מערכות TTS; הנתונים המזויפים משמשים לאימון מערכות Surrogate."),
            ("שלב שני", "Partition B",
             "פיתוח ושיפור מערכות TTS ו-VC; מערכות Surrogate משמשות להערכת אפקטיביות הזיופים ולכוונון המערכות."),
            ("שלב שלישי", "Partition C",
             "המערכות המשופרות מפיקות הקלטות מזויפות של דוברים, לרבות שילוב של חלק מהמתקפות עם עיבודים Adversarial."),
        ]),
}


def fig2(lang):
    he = lang == "he"
    d = FIG2[lang]
    arrow = "←" if he else "→"
    boxes = ""
    for i, (st, part, txt) in enumerate(d["stages"]):
        boxes += f"""<div class="box"><div class="st">{st}</div><div class="pt">{part}</div><div class="tx">{txt}</div></div>"""
        if i < 2:
            boxes += f'<div class="arr">{arrow}</div>'
    return f"""<div id="fig" style="width:900px;direction:{'rtl' if he else 'ltr'}"><style>
      .head{{text-align:center;font-size:18px;font-weight:bold;margin-bottom:14px}}
      .flow{{display:flex;align-items:stretch;justify-content:center}}
      .box{{flex:1;border:1.5px solid #444;border-radius:6px;padding:12px 14px;background:#f7f8fa}}
      .st{{font-size:14px;color:#555}}
      .pt{{font-size:20px;font-weight:bold;color:{BLUE};margin:2px 0 8px;direction:ltr;text-align:{'right' if he else 'left'}}}
      .tx{{font-size:15px;line-height:1.45}}
      .arr{{display:flex;align-items:center;padding:0 10px;font-size:30px;color:#444}}
    </style><div class="head">{d['head']}</div><div class="flow">{boxes}</div></div>"""


# ---------------------------------------------------------------- figure 3
SYS = [  # table of section 11.1
    ("RawNet2 — B01", "Closed Baseline", 36.04, "base"),
    ("AASIST — B02", "Closed Baseline", 29.12, "base"),
    ("T32", "Closed", 8.61, "top"),
    ("T45", "Open", 2.59, "top"),
]


def fig3(lang):
    he = lang == "he"
    scale = 480 / 40.0
    rows = ""
    for name, cond, eer, kind in SYS:
        col = GRAY if kind == "base" else BLUE
        rows += f"""<div class="row"><div class="lab"><b>{name}</b><br><span>{cond}</span></div>
          <div class="bars"><span class="bar" style="width:{eer*scale:.1f}px;background:{col}"></span><span class="v">{eer:.2f}%</span></div></div>"""
    return f"""<div id="fig" style="width:820px"><style>
      .row{{display:flex;align-items:center;margin:12px 0;direction:ltr}}
      .lab{{width:190px;text-align:right;padding-right:14px;font-size:16px;line-height:1.3}}
      .lab span{{font-size:13px;color:#555}}
      .bars{{flex:1;border-left:1.5px solid #555;display:flex;align-items:center;height:34px}}
      .bar{{display:inline-block;height:26px}}
      .v{{margin-left:10px;font-size:16px;font-weight:bold}}
      .axis{{margin-left:190px;font-size:13px;color:#555;padding-top:2px;direction:{'rtl' if he else 'ltr'}}}
    </style>{rows}<div class="axis">EER</div></div>"""


FIGS = [("fig1-data-partitions", fig1), ("fig2-data-creation", fig2), ("fig3-track1-eer", fig3)]


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
