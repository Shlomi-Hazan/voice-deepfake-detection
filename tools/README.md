# Tools

| Script | Purpose |
|---|---|
| `build_pdfs.py` | Builds PDFs from `*.he.md` (right-to-left) and `*.en.md` (left-to-right) with Chromium. Never edits the Markdown. |
| `make_figures_asvspoof5.py` | Renders the three illustrations of the ASVspoof 5 research card (HE + EN) into `literature/01-asvspoof5/figures/`. |
| `make_figures_cqcc.py` | Renders the three illustrations of the CQCC research card (HE + EN) into `literature/02-cqcc/figures/`. |
| `make_figures_aasist.py` | Renders the three illustrations of the AASIST research card (HE + EN) into `literature/03-aasist/figures/`. |
| `make_figures_wav2vec2.py` | Renders the two illustrations of the wav2vec 2.0 research card (HE + EN) into `literature/04-wav2vec2/figures/`. |
| `make_figures_wavlm.py` | Renders the three illustrations of the WavLM research card (HE + EN) into `literature/05-wavlm/figures/`. |
| `make_figures_codecfake.py` | Renders the three illustrations of the CodecFake research card (HE + EN) into `literature/06-codecfake/figures/`. |
| `make_figures_enhanced_forensic_trace.py` | Renders the two illustrations of the Enhanced Forensic Trace Generation research card (HE + EN) into `literature/07-enhanced-forensic-trace/figures/`. |
| `make_figures_intelligent_voice_fraud.py` | Renders the three illustrations of the Intelligent Voice Fraud Detection research card (HE + EN) into `literature/08-intelligent-voice-fraud/figures/`. |
| `make_figures_one_class_wav2vec2.py` | Renders the two illustrations of the One-Class Learning + wav2vec 2.0 research card (HE + EN) into `literature/09-one-class-wav2vec2/figures/`. |
| `make_figures_mlaad.py` | Renders the three illustrations of the MLAAD dataset research card (HE + EN) into `literature/datasets/01-mlaad/figures/`. |
| `make_figures_phonemedf.py` | Renders the three illustrations of the PhonemeDF dataset research card (HE + EN) into `literature/datasets/02-phonemedf/figures/`. |

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
