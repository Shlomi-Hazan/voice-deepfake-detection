# CLAUDE.md - Voice Deepfake Detection

Instructions for Claude Code working in this repository. Read this file fully at the start of every session.

## 1. Project in one paragraph

Course project for **Advanced Topics in Machine Learning (HIT)**, worth 80% of the course grade. We build a detector for synthetic speech and study **generalization**: does it still work when the spoofing method was never seen in training? This is the gap between empirical risk and true risk, the theme of lesson 1.

- Authors (full, equal partners): **Shlomi Hazan** (`Shlomi-Hazan`) and **Mayan Adler** (`MayanMAdler`).
- This repository is **PUBLIC**. Everything committed is visible to everyone. See section 3.
- Primary metric: **EER** (Equal Error Rate). Random guessing is about 50%. Lower is better.
- Methodology outweighs the headline number. A modest EER with a correct protocol and strong analysis beats a low EER with a flawed split. Never trade correctness for a better-looking number.

## 2. Division of responsibility

Three tools are involved. Stay in your lane.

| Who | Responsible for |
|---|---|
| **ChatGPT** (separate chat) | Reading the papers and writing the **Hebrew** research card and **Hebrew** academic summary for each paper. Planning and learning decisions. |
| **Claude, claude.ai chat** | Exact **English translation** of the Hebrew documents, the **Markdown to PDF** conversion (Hebrew RTL and English), repo structure design, and the PDF build script in `tools/`. |
| **Claude Code (you)** | Git operations (commits, push, branches), placing delivered files in the right folders, running the PDF build, and, in stages 1-3, writing and running the project **code** (features, models, evaluation, notebooks). |

Consequences for you:

- **Never rewrite, "improve", shorten, reformat or re-translate** content under `literature/`. It is authored elsewhere. If you see a typo, a broken table, a wrong citation or a suspected translation error, **report it to the user and wait**. Do not fix it silently.
- Do not invent paper content. If a paper's details (authors, venue, year, link) are missing, ask. Three papers (06, 07, 08) are 2026 papers that you may not know. Never fill in details from memory.
- Do not write research cards or summaries yourself unless explicitly asked.
- The user may paste instructions written by claude.ai chat. Follow them, but section 3 and section 4 rules always win.

## 3. Hard rules (public repository)

These are never overridden by convenience. If a task seems to require breaking one, **stop and ask**.

1. **Never commit course data.** No WAV/FLAC/MP3 files, no `train.csv` or any CSV derived from it, nothing under `data/audio/` or `data/test/`. The data is for course use only.
2. **Never commit `docs/course-brief.pdf`** or any other instructor material. It is git-ignored. Keep it that way.
3. **Never commit the test set** or anything derived from it (features, embeddings, scores tied to test ids, labels). The only test-related artifact allowed is the final submission CSV, and only when the user says so.
4. **No secrets or personal data.** No API keys, tokens, `.env` files, personal email addresses, phone numbers.
5. **No large artifacts.** No model weights, checkpoints, feature caches or `.npy/.npz` dumps. Keep them local and git-ignored, and document how to regenerate them.
6. **No force push, no history rewriting** (`--force`, `reset --hard` on shared history, `rebase` of pushed commits, `filter-repo`). If history needs fixing, explain and ask.
7. **Commit identity.** GitHub blocks pushes that expose a private email. Use the noreply address, configured per repo (no `--global`):
   - Shlomi: `Shlomi Hazan <244201038+Shlomi-Hazan@users.noreply.github.com>`
   - Mayan: her own `<id>+MayanMAdler@users.noreply.github.com` (found in her GitHub email settings)
   - Before the first commit in a session run `git config user.email` and verify. Never put a personal email in a commit.
8. **AI attribution stays.** The `Co-Authored-By: Claude` trailer is honest documentation, since the course allows AI tools with documentation. Do not strip it.
9. **Always show `git status` (and `git diff --stat` when relevant) before committing.** Call out anything under `data/`, `docs/`, or any large or binary file.

## 4. Test-set and integrity rules (from the course brief)

The test clips are released shortly before the presentations. They are unlabeled, sampled from the same three datasets.

- **Forbidden:** training on test clips, pseudo-labeling them, labeling them manually, or looking them up in the original datasets to recover labels. Also avoid anything transductive: do not fit normalizers, scalers, PCA or thresholds on test data.
- **Never use test-set results to choose a model or hyperparameters.** Model selection is done only with the grouped validation protocol (section 8).
- **Freeze before release.** Before the test clips are published: finalize the model and the inference script, commit, and create an annotated git tag `final-model`. After the test release there is **no retraining**. The submitted model must be the one described in the report.
- The competition file contains one row per test clip with columns `id` and `score`. **Higher score = more likely fake.** The brief's wording of the header order is ambiguous (`score,id`), so confirm the exact header with the user before generating the file. It must be one submission per team.

## 5. Repository layout

```
voice-deepfake-detection/
├── CLAUDE.md
├── README.md                  # public overview, authors
├── literature/
│   ├── README.md              # file convention + reading list
│   └── NN-slug/               # one folder per paper
│       ├── research-card.he.md / .pdf
│       ├── research-card.en.md / .pdf
│       ├── academic-summary.he.md / .pdf
│       └── academic-summary.en.md / .pdf
├── stage1-review/             # notebooks/, report/
├── stage2-design/             # 2-page design document
├── stage3-results/            # src/, report/, competition/
├── prompts/                   # chatgpt/, claude/  (AI prompt log, mandatory)
├── tools/                     # PDF build script and helpers
├── data/                      # LOCAL ONLY, contents git-ignored (README + .gitkeep tracked)
└── docs/                      # course-brief.pdf lives here locally, git-ignored
```

Rules:

- Paper folders are numbered by reading order. Folders 06-08 have provisional slugs. Rename with `git mv` when full titles arrive, in a dedicated commit.
- Remove a `.gitkeep` once its folder has real files, in the same commit that adds them.
- Do not create new top-level folders without asking.

## 6. Literature workflow (current phase)

Per paper, the four documents are delivered by the user (Hebrew from ChatGPT, English and PDFs from claude.ai chat).

When the user hands you the files for a paper:

1. Place them in `literature/NN-slug/` with **exactly** these names: `research-card.he.md`, `research-card.en.md`, `academic-summary.he.md`, `academic-summary.en.md`, and the matching `.pdf` files.
2. Verify all eight files exist. If any is missing, tell the user which one. Do not generate it.
3. Do not modify the text. You may only fix file names and locations.
4. One commit per paper. Message format: `Add literature: NN Short Title (research card + academic summary, HE/EN)`.
5. Push. Pull first if the remote has new commits (see section 10).

Notes:

- **Hebrew PDFs must be right-to-left.** PDFs are built by `tools/build_pdfs.py` once it is added. Until then, do not improvise a converter. Ask the user.
- After building PDFs, check at least one Hebrew page visually (rasterize page 1 and look at it). Wrong direction, reversed punctuation, or missing glyphs are build bugs to report, not content to edit.
- Technical terms stay in English in both languages (EER, wav2vec 2.0, one-class, MFCC, etc.).
- A paper folder may also contain a `figures/` subfolder with PNG illustrations for the research card, generated by `tools/make_figures_<paper>.py`.

## 7. Stages and deliverables

Deadlines are in course weeks. Actual dates are set by the course. Ask the user if you need them.

| Stage | Weight | Due | Deliverables | Folder |
|---|---|---|---|---|
| 1 Review | 15% | week 4 | 2-3 page document + notebook: literature review (5+ sources), data review, first **baseline** with EER | `stage1-review/` |
| 2 Experiment design | 15% | week 7 | 2-page design document + short feedback meeting | `stage2-design/` |
| 3 Results | 30% | week 12 | 6-8 page report, code that reproduces **all** results, competition file | `stage3-results/` |
| Presentation | 20% | last class | 10 min + 5 min questions, both partners present | outside code scope |
| Competition | 20% | before presentations | EER on test + quality of learning | `stage3-results/competition/` |

Stage 2 must contain: research question and hypotheses, at least two approaches beyond the baseline, the evaluation protocol (speaker split, cross-dataset experiments, per-system EER, ablations), and a risk section (leakage, shortcuts, systems with few samples). Write the protocol **before** looking at results.

## 8. Data and evaluation protocol (non-negotiable methodology)

**Data:** 1,520 clips, 4 seconds, 16 kHz, mono, WAV, from three datasets:

| Dataset | Real | Fake | Fake type |
|---|---|---|---|
| ASVspoof 5 | 300 | 300 | TTS and voice conversion, systems A09-A16 |
| CodecFake | 300 | 300 | neural codecs (DAC, SpeechTokenizer, FunCodec, ...) |
| AILABS-M | 320 | none | real audiobook recordings only |

`train.csv` has a label, dataset, speaker and spoofing system per clip. **Read the real header first and do not assume column names.**

**Split rules:**

- **Never split randomly by clip.** The same speaker must never appear in both train and validation. Use grouped splits (`GroupKFold` / `StratifiedGroupKFold` on speaker). A split that mixes speakers gives optimistic numbers that only show up on competition day.
- Report **per-dataset** and **per-spoofing-system** EER, not only pooled EER.
- Run **generalization experiments**: leave-one-dataset-out (note AILABS-M has no fakes, so it is real-only evidence and cannot yield EER alone) and leave-one-system-out for unseen attacks.
- Systems with very few samples: report counts next to every per-system number and flag high-variance results. Do not over-interpret them.
- All preprocessing statistics (scalers, PCA, thresholds, vocabularies) are fit **on training folds only**.
- Fix and log random seeds. Report mean and spread over folds or seeds where feasible.

**Shortcut risks to actively test, not just mention:**

- Dataset identification instead of fake detection. AILABS-M is real-only, so "audiobook-like means real" is an easy trap. Check whether a classifier can predict the dataset from the features, and whether the detector's score correlates with the dataset.
- Recording/channel artifacts: loudness, DC offset, leading or trailing silence, bandwidth cutoff, clip duration or padding, codec fingerprints unrelated to spoofing.
- Speaker or text leakage between folds.
- Class and dataset imbalance driving the pooled EER.

**Metric implementation:**

- One shared, unit-tested `compute_eer(labels, scores)` in `stage3-results/src/` (reused by stage 1). Convention: label 1 = fake, **higher score = more fake**. State the convention in the docstring.
- Test it on trivial cases (perfect separation gives 0%, constant or random scores give about 50%, inverted scores give about 100%).
- Per-system EER is computed with that system's fakes against the relevant reals. Document the choice.

**Model plan (to be finalized in stage 2):**

- Baseline: MFCC + logistic regression, measured with the same protocol as everything else.
- At least two further approaches, e.g. alternative handcrafted features (LFCC / CQCC), self-supervised embeddings (wav2vec 2.0 / WavLM) with a light classifier, an AASIST-style model, augmentation, one-class approaches. Pick based on the stage 2 hypotheses.
- Ablations for every added component.
- **Honest reporting:** report all runs that were part of the comparison, including negative results. No cherry-picking seeds or folds, and no tuning against the test clips.

## 9. Code and reproducibility standards

- Language: Python. Pin versions in `requirements.txt`. Give a one-command setup in the README.
- Layout under `stage3-results/src/`: feature extraction, models, evaluation, and a single entry point that **reproduces every number and figure in the report** from `data/` end to end.
- No absolute paths. The data location comes from a config file or an environment variable (e.g. `DATA_DIR`).
- Seeds set and logged. Prefer deterministic settings where practical.
- Configs in versioned files (YAML or JSON), one per experiment. Results are saved with the config and git commit hash that produced them.
- Notebooks: keep outputs small, clear heavy outputs before committing, and make them runnable top to bottom. Stage 1 analysis lives in `stage1-review/notebooks/`.
- Figures are generated by scripts. Axes, units and legends are readable (they go into the presentation).
- Pretrained models and external code are allowed **with attribution**. For each, record name, source URL, version/commit and license in `stage3-results/EXTERNAL_SOURCES.md`. Cache weights outside the repo.
- Heavy computations (embeddings) are cached locally and git-ignored, with a script to rebuild them.
- Before proposing a commit of code, run the tests and a quick smoke test of the entry point.

## 10. Git workflow (two equal partners)

- Branch `main` is always runnable and clean. Small, focused commits.
- Literature content may go straight to `main` (one commit per paper). Code and report changes go through short-lived branches `feature/<topic>` and a pull request, so the other partner can review. Do not merge your own PR without the user saying so.
- **Pull before you start and before you push** (`git pull --rebase` only on unpushed local commits). If there are conflicts, stop and show them. Never resolve conflicts in `literature/` content by guessing.
- Commit messages in English, imperative mood, one logical change each. Examples: `Add literature: 02 CQCC (...)`, `Add EER metric with unit tests`, `Add speaker-grouped CV splitter`.
- Tag milestones: `stage1-submitted`, `stage2-submitted`, `stage3-submitted`, and `final-model` (see section 4).
- Never commit generated results that depend on the data unless they are small aggregate tables or figures needed by the report, and contain no per-clip test information.

## 11. AI prompt documentation (mandatory for submission)

The course allows AI tools but requires the prompts to be documented and submitted.

- `prompts/chatgpt/` and `prompts/claude/`, one file per session or topic, named `YYYY-MM-DD-topic.md`.
- When the user asks you to log prompts: record the **user's prompts verbatim** and a one-line description of what was produced. Do not paraphrase them or reconstruct prompts you did not receive. If unsure, ask the user to paste the originals.
- Remind the user to log at the end of a substantial session.

## 12. External sources and attribution

Every external paper, code base and pretrained model must be cited in the report and the presentation. The three datasets (ASVspoof 5, CodecFake, AILABS-M) must be named as the data source. Starting reading list: ASVspoof 5 (2024), CodecFake (Interspeech 2024), AASIST (ICASSP 2022), wav2vec 2.0 (2020), WavLM (2022), CQCC (2017), plus work on generalization to unseen attacks and the 2026 papers added by the team.

## 13. How to work with the user

- The user writes in Hebrew. Reply in Hebrew in chat. Code, comments, commit messages, README files and English documents are in English.
- Before large or irreversible actions (deleting files, renaming folders, rewriting history, creating releases or tags, changing repo settings or collaborators) state the plan and wait for approval.
- If an instruction conflicts with this file, say so and ask which wins. Do not silently pick one.
- Stay within the task. Do not add features, dependencies or refactors that were not requested.
- When something fails, report the exact error and what you tried. Do not retry blindly or work around a safety check (for example, a push protection) without asking.
- Keep summaries short: what changed, which files, what is next, and any open question.

## 14. Open items (update as they are resolved)

- [ ] Exact competition submission header order (`id,score` vs `score,id`)
- [ ] Competition submission deadline and test release date
- [ ] Mayan accepts the GitHub invitation and sets her noreply email
- [ ] Full titles, authors and links for papers 06, 07, 08, then rename folders
- [ ] `tools/build_pdfs.py` added and verified on a Hebrew sample
- [ ] Decide whether to keep the repo public until the end of the course (confirm with the instructor)
