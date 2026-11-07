#!/usr/bin/env python3
"""Render the three illustrations of the PhonemeDF dataset research card (HE + EN).

Every number and phrase comes from
literature/datasets/02-phonemedf/research-card.*.md.
Output: literature/datasets/02-phonemedf/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_phonemedf.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = (Path(__file__).resolve().parent.parent / "literature" / "datasets" / "02-phonemedf" / "figures")

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
BLUE, GREEN, GRAY, RED, INK = "#2b5d8a", "#3f7d53", "#8a8f98", "#b5472f", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""


# ---------------------------------------------------------------- figure 1: hours by source (Table 1, Section 8)
SOURCES = [
    ("LibriSpeech Real", 100, GREEN), ("MeloTTS", 80, BLUE), ("XTTS v2", 82, BLUE),
    ("Chatterbox TTS", 80, BLUE), ("VITS TTS", 85, BLUE), ("Chatterbox VC", 100, GRAY),
    ("FreeVC", 100, GRAY), ("StarGAN VC", 100, GRAY),
]
LEG1 = {"en": ("Real", "TTS", "VC"), "he": ("אמיתי", "TTS", "VC")}


def fig1(lang):
    he = lang == "he"
    leg = LEG1[lang]
    scale = 340 / 100
    rows = ""
    for name, hrs, col in SOURCES:
        rows += (f'<div class="row"><div class="lab">{name}</div>'
                 f'<div class="bars"><span class="bar" style="width:{hrs*scale:.1f}px;background:{col}"></span>'
                 f'<span class="v">{hrs}</span></div></div>')
    return f"""<div id="fig" style="width:720px"><style>
      .legend{{display:flex;gap:20px;justify-content:center;margin-bottom:10px;font-size:14px;direction:ltr}}
      .sw{{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-1px}}
      .row{{display:flex;align-items:center;margin:7px 0;direction:ltr}}
      .lab{{width:160px;text-align:right;padding-right:14px;font-size:15px;font-weight:bold}}
      .bars{{flex:1;border-left:1.5px solid #555;display:flex;align-items:center;height:28px}}
      .bar{{display:inline-block;height:20px}}
      .v{{margin-left:8px;font-size:14px}}
    </style><div class="legend">
      <span><i class="sw" style="background:{GREEN}"></i>{leg[0]}</span>
      <span><i class="sw" style="background:{BLUE}"></i>{leg[1]}</span>
      <span><i class="sw" style="background:{GRAY}"></i>{leg[2]}</span></div>{rows}</div>"""


# ---------------------------------------------------------------- figure 2: parallel structure (Section 9)
TXT2 = {
    "en": dict(src="Real Source\n(LibriSpeech recording)", tts="TTS", vc="VC"),
    "he": dict(src="הקלטת מקור אמיתית\n(LibriSpeech)", tts="TTS", vc="VC"),
}
TTS = ["MeloTTS", "XTTS v2", "Chatterbox TTS", "VITS"]
VC = ["Chatterbox VC", "FreeVC", "StarGAN VC"]


def fig2(lang):
    he = lang == "he"
    d = TXT2[lang]
    tts_boxes = "".join(f'<div class="sbox tts">{n}</div>' for n in TTS)
    vc_boxes = "".join(f'<div class="sbox vc">{n}</div>' for n in VC)
    arrow = "←" if he else "→"
    return f"""<div id="fig" style="width:760px;direction:{'rtl' if he else 'ltr'}"><style>
      .wrap{{display:flex;align-items:center;justify-content:center;gap:12px}}
      .src{{width:190px;border:2px solid {GREEN};border-radius:8px;padding:14px;background:#eef5f0;
            font-size:14.5px;font-weight:bold;text-align:center;line-height:1.35}}
      .arr{{font-size:30px;color:#444}}
      .grp{{display:flex;flex-direction:column;gap:14px}}
      .fam{{border:1.5px dashed #888;border-radius:8px;padding:8px 10px}}
      .fl{{font-size:13px;font-weight:bold;color:#555;margin-bottom:5px;direction:ltr;text-align:center}}
      .sbox{{direction:ltr;width:170px;border-radius:5px;padding:5px 8px;margin:3px 0;font-size:13.5px;
             font-weight:bold;text-align:center;color:#fff}}
      .tts{{background:{BLUE}}} .vc{{background:{GRAY}}}
    </style><div class="wrap">
      <div class="src">{d['src'].replace(chr(10), '<br>')}</div>
      <div class="arr">{arrow}</div>
      <div class="grp">
        <div class="fam"><div class="fl">{d['tts']}</div>{tts_boxes}</div>
        <div class="fam"><div class="fl">{d['vc']}</div>{vc_boxes}</div>
      </div></div></div>"""


# ---------------------------------------------------------------- figure 3: KLD by phoneme (Section 19.4)
PHON = [("AH", 3.75), ("OY", 46.17), ("T", 3.87), ("ZH", 83.08)]


def fig3(lang):
    he = lang == "he"
    scale = 240 / 85
    cols = ""
    for ph, kld in PHON:
        cols += (f'<div class="col"><span class="v">{kld:.2f}</span>'
                 f'<span class="bar" style="height:{kld*scale:.1f}px;background:{BLUE}"></span>'
                 f'<span class="lab">{ph}</span></div>')
    ytitle = "KLD (WavLM, MeloTTS)"
    return f"""<div id="fig" style="width:520px"><style>
      .ytitle{{font-size:12.5px;color:#555;margin-bottom:6px;direction:ltr;text-align:left}}
      .plot{{display:flex;justify-content:space-around;align-items:flex-end;height:290px;
             border-left:1.5px solid #555;border-bottom:1.5px solid #555;padding:0 10px;direction:ltr}}
      .col{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:80px}}
      .bar{{display:block;width:50px}}
      .v{{font-size:13px;margin-bottom:3px}}
      .lab{{margin-top:6px;font-size:15px;font-weight:bold}}
    </style><div class="ytitle">{ytitle}</div><div class="plot">{cols}</div></div>"""


FIGS = [("fig1-hours-by-source", fig1), ("fig2-parallel-structure", fig2), ("fig3-kld-phonemes", fig3)]


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
