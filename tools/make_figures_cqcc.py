#!/usr/bin/env python3
"""Render the three illustrations of the CQCC research card (HE + EN).

Every number and phrase comes from literature/02-cqcc/research-card.*.md.
Output: literature/02-cqcc/figures/figN-<name>.<lang>.png

Requires: playwright (+ `playwright install chromium`).
Usage:    python tools/make_figures_cqcc.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "literature" / "02-cqcc" / "figures"

FONT = ('"David Libre","Frank Ruhl Libre","Noto Serif Hebrew","David",'
        '"Times New Roman","FreeSerif","Liberation Serif",serif')
BLUE, RED, GRAY, INK = "#2b5d8a", "#b5472f", "#8a8f98", "#222"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fff;font-family:{FONT};color:{INK}}}
#fig{{display:inline-block;padding:18px 22px;background:#fff}}
"""


# ---------------------------------------------------------------- figure 1: pipeline (Section 6.1)
FIG1 = {
    "en": dict(inp="Speech signal", out="CQCC Features", stage="Stage", steps=[
        ("Constant Q Transform", "Time–frequency representation with geometrically spaced frequency intervals"),
        ("Power Spectrum", "Square of the absolute value of the CQT coefficients"),
        ("Logarithm", "Applied to the power spectrum"),
        ("Uniform Resampling", "Resampling onto a frequency axis with uniform intervals"),
        ("Discrete Cosine Transform", "Yields a series of cepstral coefficients"),
    ]),
    "he": dict(inp="אות הדיבור", out="CQCC Features", stage="שלב", steps=[
        ("Constant Q Transform", "ייצוג זמן–תדר בעל מרווחי תדר גאומטריים"),
        ("Power Spectrum", "ריבוע הערך המוחלט של מקדמי CQT"),
        ("Logarithm", "הפעלה על ספקטרום ההספק"),
        ("Uniform Resampling", "דגימה מחדש לציר תדרים בעל מרווחים אחידים"),
        ("Discrete Cosine Transform", "קבלת סדרת מקדמים קפסטרליים"),
    ]),
}


def fig1(lang):
    he = lang == "he"
    d = FIG1[lang]
    arrow = "←" if he else "→"
    down = "↓"

    def box(i, name, sub):
        return (f'<div class="box"><div class="n">{d["stage"]} {i}</div><div class="nm">{name}</div>'
                f'<div class="sb">{sub}</div></div>')

    st = d["steps"]
    row1 = (f'<div class="pill">{d["inp"]}</div><div class="arr">{arrow}</div>'
            + f'<div class="arr">{arrow}</div>'.join(box(i, *st[i - 1]) for i in (1, 2, 3)))
    back = "→" if he else "←"  # second row runs in the opposite direction (serpentine)
    row2 = (box(4, *st[3]) + f'<div class="arr">{back}</div>' + box(5, *st[4])
            + f'<div class="arr">{back}</div><div class="pill out">{d["out"]}</div>')
    row2_dir = "ltr" if he else "rtl"
    return f"""<div id="fig" style="width:900px;direction:{'rtl' if he else 'ltr'}"><style>
      .flow{{display:flex;align-items:stretch;justify-content:space-between;width:856px}}
      .flow.r2{{justify-content:flex-start}}
      .pill{{display:flex;align-items:center;justify-content:center;border:1.5px solid #444;border-radius:22px;
             padding:6px 14px;font-size:17px;background:#fff;text-align:center;width:130px}}
      .pill.out{{background:{BLUE};color:#fff;border-color:{BLUE};font-weight:bold}}
      .box{{direction:{'rtl' if he else 'ltr'};width:200px;border:1.5px solid #444;border-radius:6px;padding:10px 12px;background:#f7f8fa}}
      .n{{font-size:14px;color:#555}}
      .nm{{font-size:17.5px;font-weight:bold;color:{BLUE};margin:2px 0 6px;direction:ltr;
           text-align:{'right' if he else 'left'}}}
      .sb{{font-size:15.5px;line-height:1.4}}
      .arr{{display:flex;align-items:center;padding:0 8px;font-size:26px;color:#444}}
      .dn{{font-size:26px;color:#444;padding:4px 0;text-align:center;width:200px;
           margin-{'right' if he else 'left'}:auto}}
    </style><div class="flow">{row1}</div><div class="dn">{down}</div><div class="flow r2" style="direction:{row2_dir}">{row2}</div></div>"""


# ---------------------------------------------------------------- figure 2: Table 16 (Section 10.2)
CONF = [("A, 19+C0", GRAY), ("SDA, 19+C0", BLUE), ("DA, 29+C0", RED)]
T16 = [  # dataset label, values for the 3 configurations (same order as CONF)
    ("ASVspoof (EER)", [0.26, 0.76, 0.42]),
    ("AVspoof (HTER)", [5.65, 0.67, 4.70]),
    ("RedDots (EER)", [3.27, 6.48, 1.85]),
]


def fig2(lang):
    he = lang == "he"
    unit = "EER / HTER (%)"
    h = 220 / 6.48
    legend = "".join(f'<span><i class="sw" style="background:{c}"></i>{n}</span>' for n, c in CONF)
    groups = ""
    for label, vals in T16:
        best = min(vals)
        bars = ""
        for (n, c), v in zip(CONF, vals):
            fw = "bold" if v == best else "normal"
            bars += (f'<div class="col"><span class="v" style="font-weight:{fw}">{v:.2f}</span>'
                     f'<span class="bar" style="height:{max(v*h,2):.1f}px;background:{c}"></span></div>')
        groups += f'<div class="grp"><div class="bars">{bars}</div></div>'
    return f"""<div id="fig" style="width:820px"><style>
      .legend{{display:flex;gap:22px;justify-content:center;margin-bottom:10px;font-size:16px;direction:ltr}}
      .sw{{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-1px}}
      .ytitle{{font-size:13px;color:#555;margin:0 0 4px 4px;direction:ltr;text-align:left}}
      .plot{{display:flex;justify-content:space-around;align-items:flex-end;height:270px;
             border-left:1.5px solid #555;border-bottom:1.5px solid #555;padding:0 10px;direction:ltr}}
      .grp{{display:flex;flex-direction:column;align-items:center}}
      .bars{{display:flex;align-items:flex-end;gap:8px;height:250px}}
      .col{{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:46px}}
      .bar{{display:block;width:100%}}
      .v{{font-size:13.5px;margin-bottom:3px}}
      .labels{{display:flex;justify-content:space-around;padding:6px 10px 0;font-size:15px;font-weight:bold;direction:ltr}}
      .labels div{{width:220px;text-align:center}}
    </style><div class="legend">{legend}</div><div class="ytitle">{unit}</div>
    <div class="plot">{groups}</div>
    <div class="labels">{"".join(f"<div>{l}</div>" for l, _ in T16)}</div></div>"""


# ---------------------------------------------------------------- figure 3: improvements (Sections 9.1, 9.3)
def fig3(lang):
    he = lang == "he"
    L = {
        "en": dict(
            a="ASVspoof 2015 — unknown attacks (EER)", b="RedDots Replayed — overall EER",
            rows_a=[("Previous best system", 1.670, GRAY), ("CQCC-A", 0.462, BLUE)],
            rows_b=[("LFCC Baseline", 5.11, GRAY), ("CQCC-DA", 1.85, BLUE)]),
        "he": dict(
            a="ASVspoof 2015 — מתקפות בלתי מוכרות (EER)", b="RedDots Replayed — EER כולל",
            rows_a=[("המערכת הקודמת הטובה ביותר", 1.670, GRAY), ("CQCC-A", 0.462, BLUE)],
            rows_b=[("LFCC Baseline", 5.11, GRAY), ("CQCC-DA", 1.85, BLUE)]),
    }[lang]
    scale = 400 / 5.5

    def panel(title, rows):
        out = f'<div class="pt" style="direction:{"rtl" if he else "ltr"}">{title}</div>'
        for name, v, col in rows:
            txt = f"{v:.3f}%" if v < 1 or v == 1.670 else f"{v:.2f}%"
            out += (f'<div class="row"><div class="lab" style="direction:{"rtl" if he else "ltr"}">{name}</div>'
                    f'<div class="bars"><span class="bar" style="width:{v*scale:.1f}px;background:{col}"></span>'
                    f'<span class="v">{txt}</span></div></div>')
        return f'<div class="panel">{out}</div>'

    return f"""<div id="fig" style="width:820px"><style>
      .panel{{margin:0 0 18px}}
      .pt{{font-size:16px;font-weight:bold;margin-bottom:6px;text-align:{'right' if he else 'left'}}}
      .row{{display:flex;align-items:center;margin:6px 0;direction:ltr}}
      .lab{{width:230px;text-align:right;padding-right:12px;font-size:15px}}
      .bars{{flex:1;border-left:1.5px solid #555;display:flex;align-items:center;height:30px}}
      .bar{{display:inline-block;height:22px}}
      .v{{margin-left:8px;font-size:15px;font-weight:bold}}
    </style>{panel(L['a'], L['rows_a'])}{panel(L['b'], L['rows_b'])}</div>"""


FIGS = [("fig1-cqcc-pipeline", fig1), ("fig2-cross-database", fig2), ("fig3-improvements", fig3)]


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
