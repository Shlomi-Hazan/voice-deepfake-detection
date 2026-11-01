# Tools

| Script | Purpose |
|---|---|
| `build_pdfs.py` | Builds PDFs from `*.he.md` (right-to-left) and `*.en.md` (left-to-right) with Chromium. Never edits the Markdown. |
| `make_figures_asvspoof5.py` | Renders the three illustrations of the ASVspoof 5 research card (HE + EN) into `literature/01-asvspoof5/figures/`. |
| `make_figures_cqcc.py` | Renders the three illustrations of the CQCC research card (HE + EN) into `literature/02-cqcc/figures/`. |
| `make_figures_aasist.py` | Renders the three illustrations of the AASIST research card (HE + EN) into `literature/03-aasist/figures/`. |

## Setup (once)
```
pip install markdown playwright
playwright install chromium
```

## Usage
```
python tools/build_pdfs.py literature/01-asvspoof5      # one paper
python tools/build_pdfs.py --all                         # all papers
python tools/build_pdfs.py --all --only-stale            # only outdated PDFs
```
For the best academic look install one of: David Libre, Frank Ruhl Libre, Noto Serif Hebrew (the script falls back to FreeSerif / Liberation Serif).
