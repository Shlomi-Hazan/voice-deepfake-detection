# Document B — Research Synthesis & Experimental Blueprint
## Fake or Real: Voice Deepfake Detection — Research and Experiment Design Document

**Researchers:** Shlomi Hazan & Maayan Adler  
**Course:** Advanced Topics in Machine Learning, HIT  
**Version:** 2.2 — November 7, 2026  
**Status:** Experimental Blueprint — **Pre-EDA; the decision protocol is defined but the splits themselves have not yet been verified**  
**Base document:** *Document A — Integrated Literature Review, Final Revised (HE)*  
**Literature foundation:** 12 papers studied by guided reading; the nine original research papers, Research Paper 10 — AT-ADD, and the two dataset papers MLAAD and PhonemeDF.

> **Validity note:** v2.2 preserves the corrections of v2.1 and sharpens two experimental contracts: (a) OC-Pure also requires an advance choice of Checkpoint/Layer/Pooling without Fake labels; (b) Contrast S increases external Real and Fake proportionally and preserves as far as possible the **overall** class ratio. This is not evidence that a Split Manifest was created or that EDA, Model Selection, Bootstrap, or Dataset Admission Gates were run.

**Framing note:** This is an internal master document, not a two-page Stage 2 report. It gathers decisions, conditional plans, and validity rules; the submission documents and notebooks will be derived from it. Every numerical result attributed to a paper is a **published finding** and not a result of the project. There is no claim here that the external dataset has already been downloaded, that the speaker identifiers in the course file were checked, or that a model was run.

---

## Executive Summary

The project seeks to build a detector for real versus fake speech, and to examine not only the quality of classification on known examples but also the generalization ability under changes in generation systems, speech source, and processing conditions. In order to do so without turning a course experiment into an unbounded study, we will proceed along **two core axes and a third conditional axis**: (1) the speech representation — MFCC/CQCC versus SSL representations; (2) the learning paradigm — binary classification versus One-Class on the same Encoder; (3) training expansion — an experimental distinction between the *number of examples* and the *diversity of forgery systems*, if the access, licensing, and Metadata checks allow it. A shared evaluation layer will distinguish between internal evaluation, Leave-One-System-Out (LOSO), transitions between datasets, and robustness to signal changes.

The course dataset contains **1,520 WAV clips, four seconds long, 16kHz, mono**: 300 Real and 300 Fake from ASVspoof 5, 300 Real and 300 Fake from CodecFake, and 320 Real from M-AILABS. In total **920 Real and 600 Fake**. A separate competition test set will be published later, without labels, and the project is required to produce for it a CSV in the format `id,score`, where a high score means a higher suspicion of forgery. The first training will be **MFCC + Logistic Regression**; the minimal representation comparison will also include **CQCC + Logistic Regression** and **Frozen wav2vec 2.0 + Logistic Regression**; subsequently **M3 — One-Class SVM** on the same wav2vec 2.0 representations is a **planned core experiment** for examining the learning axis, subject to documented feasibility gates. WavLM, AASIST-L, Deep SVDD, Feature Fusion, Forensic Reconstruction, and Ensemble will remain reasoned extensions, not automatic commitments.

The document anchors the lessons from the new papers: **MLAAD** offers TTS and language diversity but does not prove that v11 is superior thanks to the diversity, since the generalization experiments in the paper were carried out on v1; **PhonemeDF** enables parallel source/output and phonetic analysis, but requires grouping source families and distinguishing between KLD/Accuracy at the phoneme level and EER at the recording level; **AT-ADD** demonstrates that success on Dev does not guarantee Robustness on Eval, and that Macro-F1, Real/Fake metrics, and error analysis complement a single metric, but its audio is **not a verified, available training/test source** for us. The document preserves all the earlier decisions, and adds an expansion protocol that can be falsified and not only an argument that "more data" should help.

## 1. The Purpose of the Document, Sources, and Types of Claims

### 1.1 The Roles of Document A and Document B

- **Document A**: presents what is known in the literature, the evidence and the gaps, and the justification for the choice of research questions.
- **Document B**: translates the framework into a sequence of actions, experiments, controls, stopping rules, model selection, and metrics.
- **Stage 1/2/3**: short submission documents or a results report, derived from the two documents; they are not a copy of the master document.

We will not attribute to a paper an ability or result that was not measured in it; we will explicitly separate **a reported finding**, **a cautious inference**, **a project hypothesis**, **an approved decision**, and **a condition not yet verified**. The term "approved" means a working decision of the team, and not a research result that has already been tested.

### 1.2 Decision Register: What Was Preserved and What Is New

| Component | Decision preserved | What was added following the three readings and the editing of A |
|---|---|---|
| Research question | Generalization to forgeries and sources not seen in training | Three prioritized axes and a shared evaluation layer |
| Initial model | MFCC + Logistic Regression | Preserving M0 as a binding reference point, without loading architectures |
| Representations | CQCC, wav2vec 2.0, and later WavLM | Control over layer/Pooling selection, and separating ASR/speech knowledge from Anti-Spoofing evidence |
| One-Class | Comparison on the same frozen Encoder | A clear separation between Pure One-Class and Supervised Validation |
| Split | Speaker-aware, preventing Leakage | A distinction between true Leakage and Protocol Mismatch; grouping source derivatives |
| Evaluation | EER central, checks by source/system | Macro-F1, Real/Fake Recall, CI, documenting Threshold conditions, and defining three types of Shift |
| Training expansion | No external dataset was decided in advance | MLAAD and PhonemeDF as *Conditional GO* only; experiments to isolate size versus diversity |
| AT-ADD | Does not appear in the old Document B | A methodological source only, not an available Dataset; adopting analysis of Replay/BigVGAN failures and Real Shift |
| Course conditions | 1,520 recordings, a separate competition | Priority that every novelty meet the requirements and be reproducible |

### 1.3 Project Boundaries

The task is **Recording-Level Binary Speech Deepfake Detection**, not Speaker Verification, artificial-music detection, cryptographic protection, or local forgery detection within a sentence. Some of the papers deal with broader topics; from them we will take ideas that have a justification for our task, and will not broaden the project's goal without need. One should not commit in advance to carrying out Fine-Tuning of several large Encoders or to reproducing a competitive system such as WaveShield.

## 2. Research Basis — What Evidence Justifies the Plan?

| Source | Contribution to the design | A limitation that must be remembered |
|---|---|---|
| ASVspoof 5 [1] | A challenge of new attacks, adversarial examples, EER/minDCF, and split validity | The evaluation conditions of the full Benchmark do not necessarily hold in the course subsample |
| CodecFake [2] | A change of forgery family following Codec Resynthesis | Legitimate Codec processing of Real is not always Fake; do not infer a global rule about a "Codec artifact" |
| CQCC [3] | A classical spectral representation for comparing features | A result on a particular Benchmark does not indicate a fixed advantage on the course data |
| AASIST [4] | Graph-based spectro-temporal learning; an extension candidate | The classical results on ASVspoof 2019 LA are not proof of generalization to the course data |
| wav2vec 2.0 [5] | A frozen Encoder as a basis for representation comparison | Pretraining for speech/ASR does not by itself prove forgery-detection ability |
| WavLM [6] | An alternative Encoder, the possibility of layer analysis | Denoising/rich representation may also blur artifacts — to be checked and not assumed |
| Enhanced Forensic Trace [7] | Reconstruction and Feature Enhancement as an extension | The benefit is not uniform between features; computational cost, and the paper includes Ablation experiments, but not on the course data and not for every extension we propose |
| Intelligent Voice Fraud [8] | Fusion and combining cues | The effect of a component cannot be isolated when the study does not do so |
| One-Class + wav2vec2 [9] | Comparing anomaly detection to binary classification | Validation with Fake and component differences prevent automatically attributing an improvement to One-Class alone |
| MLAAD [10] | A multilingual TTS dataset and generation-model metadata | Cross-Dataset results were reported on v1; v11 and 205 systems are not a proof experiment of "more diversity" |
| PhonemeDF [11] | Parallel TTS+VC, phoneme alignment, a shared source for control experiments | KLD/Accuracy at the phoneme level are not EER at the clip level; licensing/source grouping require checking |
| AT-ADD [12] | Generator separation, Macro-F1 metrics, Real Recall, channel-condition analysis, and stable ranking | Combined Shift does not locate a cause; 18 Common Voice speakers overlap; access to the audio was not verified |

Central implication: the benefit of **a representation change**, **a learning change**, or **a training-dataset change** should be measured in an experiment that separates these changes. A numerical advantage in a particular table is not an instruction to copy the model that was reported, and metrics from different datasets do not constitute a shared ranking.

## 3. Formulating the Research Question and Hypotheses

### 3.1 The Overarching Question

**How do the choice of speech representation, the learning paradigm, and the composition of the training data affect voice forgery detection performance and the generalization ability to systems and sources not seen in training, within evaluation protocols that can be verified?**

### 3.2 Three Prioritized Research Axes

**RQ1 — Representation (a mandatory core).** How do EER and error patterns change when replacing MFCC with CQCC and with wav2vec 2.0 representations, with the same simple classification head, the same splits, and the same selection process? A WavLM comparison is an applicable extension if the added extraction is justified.

**RQ2 — Learning Paradigm (a planned core).** On the same frozen Encoder, does a One-Class SVM trained on Real only cope better with unknown attacks compared with a binary Logistic Regression? For every result it will be noted whether Fake labels were used in Validation.

**RQ3 — Training Data Diversity (conditional on Gates).** For the same training-example budget, does increasing the number of TTS/VC systems/families improve generalization to Generators not included in training, beyond the effect of adding a number of examples from the same family? If the variables cannot be isolated, the question will be defined as a limited descriptive experiment, and not as proof of causality.

**A cross-cutting evaluation layer:** Speaker-Disjoint, Leave-One-System-Out, Cross-Dataset, channel conditions, and analysis by source; it is not a collection of independent research questions. The adaptation of each protocol to the data will depend on the EDA and the Metadata.

### 3.3 Falsifiable Hypotheses

| ID | Pre-registered hypothesis | Deciding test | Inference boundary |
|---|---|---|---|
| H1 — Representation | Frozen wav2vec 2.0 + LR (M2) will show a lower EER than M0 on the **main generalization protocol chosen before training** | A paired EER difference `EER(M2) − EER(M0)` negative, reported with spread/uncertainty | A point advantage only; a reversal between Folds or an In-domain-only advantage is not a sweeping confirmation |
| H1b — Alternative Classical | M1 will differ from M0 in failure features / EER | M1 versus M0 on the same Folds, the same classifier and tuning budget | H1b is secondary; a positive direction should not be chosen retrospectively according to the result |
| H2 — Learning Paradigm | M3 may achieve a lower EER than the M2 system on the main generalization test | `EER(M3) − EER(M2)` with Real Recall and False Alarms on a new Real source | A comparison of whole paradigms and a different label budget, not isolation of the classifier alone |
| H3a — Size | A proportional addition of Real and Fake from the same Generator mix may improve generalization | E1 versus E2 on a fixed Holdout, while controlling the final class ratio in Train | Does not isolate Generator diversity; if the balance changes, Confounding should be reported |
| H3b — Diversity Allocation | With the same number of external Fake **and Real**, spreading the Fake across more Generators/families may improve generalization | E3 versus E4 with N and R fixed, replications of system composition and matched Real | Tests a **budget-allocation policy**; the number of examples per Generator necessarily varies |
| H4 — Augmentation | Processing balanced in Real and Fake may improve robustness | Perturbed EER without unreasonable harm to Clean EER | A secondary analysis/extension |
| H5 — Error Heterogeneity | The error distribution is not uniform by Generator and Real source | Fake/Real Recall and descriptions of the Score distribution by subset | Does not prove which causal feature the model learned |

**A pre-registration rule:** a single primary endpoint will be chosen according to the gates of Section 6.7, before training and before viewing model scores on Test. The decision will be reported as supported / not supported / undecided due to uncertainty or feasibility. Success of H1/H2 should not be declared on the basis of a single Fold chosen retrospectively. H3a/H3b are conditional on access, rights, data composition, and Gates, and are not a condition for completing the course.

## 4. Course Data, Labels, and Task Definition

### 4.1 Known Composition and Immediate Limitations

| Source | Real | Fake | Total | Intended role |
|---|---:|---:|---:|---|
| ASVspoof 5 | 300 | 300 | 600 | Training/evaluation and examining TTS/VC attacks |
| CodecFake | 300 | 300 | 600 | Training/evaluation and Codec-family tests |
| M-AILABS | 320 | 0 | 320 | Real, source control, and generalization planning |
| **Total** | **920** | **600** | **1,520** | 16kHz, mono, 4 seconds |

According to the course document, `train.csv` includes a label, source, speaker, and forgery system. **The column names, the actual number of systems, the speaker identities, and the associations between derivatives have not yet been checked.** Before writing split code, the file itself should be examined, and one should not infer that the IDs of the full ASVspoof 5/CodecFake world are fully represented in the subsample.

### 4.2 Three Definition Layers That Must Not Be Mixed

1. **Authenticity according to the task:** Real/Bona Fide versus Fake/Spoof — the course label is used as the binding Target for submission.
2. **The example-generation mechanism:** TTS, VC, Codec Resynthesis, Neural Vocoder, or another mechanism, when the documentation allows.
3. **Processing/channel conditions:** MP3/Opus, Resampling, Replay, noise, or loudness change, which do not necessarily change authenticity.

Therefore one should not set a rule that "everything that passed through a Neural Codec is a forgery". In the CodecFake definition, a particular Codec Resynthesis is labeled Spoof; in other datasets, processing real speech in a codec may preserve the Real label. In Robustness experiments **the course label** is preserved after permitted processing unless it is an explicit protocol creating a new forgery example. A possible contradiction between dataset definitions will be documented and not blurred.

### 4.3 Model and Evaluation Conventions

- `label=1` denotes Spoof/Fake and `label=0` denotes Real/Bona Fide, after verifying the actual convention.
- `score` is continuous, **higher = more suspicion of Fake**; it does not have to be a calibrated probability.
- A threshold `t` is learned only by means of Validation when a binary decision is required; EER is computed from a threshold sweep but is not a deployment threshold known in advance.
- If a One-Class classifier returns a "more normal" score, we will reverse its direction once, in a documented manner, before all the evaluations.

### 4.4 The Unique Problem of M-AILABS

On M-AILABS alone there is no Fake and therefore **an independent EER cannot be computed**. One can report Real Recall, the False Alarm Rate relative to the Spoof class, the distribution of Real scores, and the system's performance at a threshold chosen outside M-AILABS. One should not present a combination of Real from M-AILABS with Fake from another dataset as if it were an "EER of M-AILABS"; this is a composite test, potentially biased toward the source, and it requires an explicit protocol label. If M-AILABS enters training, the same recordings cannot be presented in the same experiment as an OOD Real Test.

## 5. Stage 1 — EDA, Audit, and Validity Gates

### 5.1 Audit of the Course File

Since `train.csv` has not yet been opened and the source and speaker identifiers have not yet been checked, the following schema is a **proposed Audit schema**, not a claim that the fields exist in the files. For each clip we will verify: valid path and duration, sample rate, channels, label, source, speaker, system/family, authentic source, derived versions, and the ability to locate overlaps.

| Audit field | Meaning and validity note |
|---|---|
| `clip_id`, `path`, `label` | Recording identifier, local path, Real/Fake according to the source task |
| `dataset_id` | ASVspoof5 / CodecFake / M-AILABS / MLAAD / PhonemeDF — *the dataset name does not identify a parent recording* |
| `speaker_id_raw`, `speaker_namespace`, `speaker_global_id` | Source identifier, identifier namespace, merging identities only when evidence exists |
| `original_recording_id` | The identifier of the specific parent recording, if known; otherwise `UNKNOWN` |
| `derivation_group_id` | A source group and all its derivatives (VC, Codec resynthesis, windows, Augmentation), if identifiable |
| `generator_id`, `generator_family` | A specific system versus TTS/VC/Vocoder/Codec-resynthesis; `UNKNOWN` if there is no evidence |
| `channel_condition`, `processing_chain` | Codec / Noise / Replay / Resampling and capture conditions, if known |
| `transcript_id`, `reference_speaker_id` | Text/reference-speaker identifiers, in recordings that depend on them |
| `audit_confidence`, `audit_evidence` | Confidence level and a link to the source evidence for presumed associations |

**Building a Group unit:** when a clip is related to several clips through a parent recording, speaker, long segment, or derivative, we will manage a relations graph and compute *connected components* according to the relation types required for the protocol. A single column is not necessarily sufficient. At the source-disjoint level we will verify that there is no derivative edge between the parts of the split; at the speaker-disjoint level we will also add speaker-identity edges. Excessively large connected components will lead to re-examining the feasibility of the split, **not** to an arbitrary split.

**Deliverable:** a local `metadata_audit`, an `unknowns_report`, a list of Group IDs, and verification of the number of Real/Fake examples for each Holdout group; unknowns should not be presented as an Audit that was passed.

### 5.2 Distribution and Shortcut Checks

We will produce tables and plots: source × label, Generator × label, speaker × label, number of examples per system/speaker, durations, and signal integrity. We will also check RMS, Peak, silence rate, DC Offset, bandwidth, loudness levels, Codec/frequency features, and cropping boundaries; we will carry out listening and spectrograms for representative examples. We will check whether the recording source can be predicted from features on **Real only**, as a diagnostic of available domain information and not as proof that the final classifier uses it.

### 5.3 Provenance and Pretraining

- **Source/Derivative Integrity:** every derivative of the same parent recording must belong to the same split group in an experiment requiring Source-Disjoint. We will also check segments cut from the same long recording, playbacks/re-recordings, and versions that underwent Codec Resynthesis.
- **Locating associations:** source paths, speaker identifiers, Transcript/Content ID, Metadata, and identical or nearly identical files. An exact Hash does not detect Resampling, Codec, or re-synthesis; every presumed match will receive a confidence level.
- **Encoder Pretraining:** for each Checkpoint we will record the known pre-training data, the list of sources reported, and the level of certainty regarding overlap with Test. Exposure to audio without labels is not necessarily leakage of supervised labels, but it limits claims of complete independence.
- **External datasets:** we will not assume there is no overlap between M-AILABS and MLAAD, or between LibriSpeech/LibriVox and subsamples of ASVspoof/PhonemeDF. A check will be carried out at the source level as far as the information allows.
- **Gate:** proven prohibited overlap → fixing the split or disqualifying the experiment; unknown source → a limited experiment only with a visible reservation. The `UNKNOWN` label must not be replaced with `PASS`.

### 5.4 Gate-0: Is It Possible at All to Carry Out a Strict Protocol?

Before setting the Train/Validation/Test ratio, an Audit is required of the number of speaker groups, systems, Real available for each condition, and source associations. We will not set the number of Folds in advance. If it is not possible to keep together **Speaker-Disjoint, Source-Family Grouping, and representation of both classes**, we will choose an alternative protocol that can be justified and explicitly report what was not achieved. **The split must not be changed retrospectively in order to obtain a lower EER.**

## 6. The Split Architecture and Generalization Protocols

### 6.1 Concept: Three Different Protocols, Not Different Names for the Same Test

| Protocol | What is held out | What it measures | What it does not prove alone |
|---|---|---|---|
| In-domain grouped evaluation | Speakers and source families (as far as possible) | Detection on the same mix of sources under split conditions | Detection of a new Generator or a broad Domain Shift |
| Leave-One-System-Out (LOSO) | A particular Generator or a defined family of forgeries | Unseen-Generator Detection under the conditions defined | A change of an entire dataset, a channel change, or speakers automatically |
| Cross-Dataset Holdout | All examples of the target dataset | Transfer to a different source/domain | Isolating the cause of the decline (system, speaker, Codec, channel) |
| Perturbation Robustness | Processing variations of the same reserved examples | Sensitivity to a defined signal change | Unseen TTS / VC |

LOSO means **Leave-One-System-Out** only in this document; it should not be confused with Leave-One-Speaker-Out. We will not call a Within-Distribution evaluation "Data Leakage" merely because the same generation systems appear on both sides of the split; it is a **Protocol Mismatch** only if it is used to claim Unseen-Generator Generalization. True Leakage includes crossing source derivatives, fitting Preprocessing on Test, or changing a selection according to Test performance.

### 6.2 Protocol P0 — Grouped Internal Evaluation

1. We start from Group units that do not overlap at the speaker level and source derivatives; a grouping unit as strict as the data allows.
2. We build Train/Validation/Internal Test or Grouped Nested CV when the speaker sample is too small. The structure and rationale are fixed before training.
3. Training and tuning on Train/Validation only; Internal Test is reserved for final reporting (or fixed-in-advance Outer Folds are used).
4. We keep exactly the same split files for all models for a paired comparison.
5. We report overall EER, the score direction, the number of Real/Fake, and decision metrics at the Validation threshold.

**Risk:** a speaker may appear in two datasets under different identifiers; without verification, a full Speaker-Disjoint cannot be declared. A Test split containing only one class will not suffice for computing EER.

### 6.3 Protocol P1 — LOSO, Unseen Systems

**Definition:** Leave-One-System-Out, not Leave-One-Speaker-Out. Before preparing a Split we will identify a candidate Generator `g`, and the matching Real recordings that will be included in the test. All the Fake of `g` will be held out of Train **and from any selection of Hyperparameters, layer, Pooling, and threshold**.

**Strict LOSO (the default for a strict generalization claim):** when parent-recording identifiers are known, **every derivative of every recording source found in Test must be outside Train/Validation**, even if it was created in a different Generator. This is in addition to non-exposure to system `g`. We will verify this by means of a connected-components check. If a claim is also made for Speaker Generalization, we will *additionally* require separation of speaker identities. Moving a Codec A derivative of source X to Train and a Codec B derivative of the same X to Test **will not pass Strict LOSO**.

**Limited Generator-Held-Out:** if there are no identifiers that allow verifying independence at the source level, a conditional result can still be published that system `g` itself was not seen in training, but with a `source independence unverified` label and without a Strict LOSO or Speaker-Disjoint claim.

**Real Controls:** we will choose Real in a pre-defined manner, preferably from the same dataset and under matching conditions, while preventing overlap of source families. We will not create a situation in which the Fake of a new Generator is tested against Real from another dataset without an explicit notice of Dataset–Label Confounding. For each Fold we will record `n_real`, `n_fake`, `n_speakers`, `n_derivation_groups`, `generator_id`, and the split version.

**Nested Selection / Evaluation:** for each Generator held out, model selection will be carried out only on Train/Inner Validation from the permitted systems; the data of `g` will not be used for any adaptation. A fixed threshold comes from Validation, not from the outer Fold. If the test set does not contain both classes or is too small, we will report Recall/the limitation and avoid an EER that is undefined or unstable.

**Condition for execution:** a feasibility check of Generator, derivative, speaker, and size identifiers in the EDA; we will not assume that identifiers from the full paper (such as A09–A16) are automatically found in the course sample.

### 6.4 Protocol P2 — Cross-Dataset

**A high-priority evaluation requirement derived from the course:** subject to valid source data, we will carry out both directions:

1. Training + model selection on ASVspoof 5 only; a reserved external evaluation on CodecFake.
2. Training + model selection on CodecFake only; a reserved external evaluation on ASVspoof 5.

For each direction there is a target set with Real and Fake, and therefore EER is defined when both classes are actually represented. All the recordings of the target dataset remain outside training, design decisions, Hyperparameter selection, and Threshold. **M-AILABS or an external dataset must not be incorporated into the training of the experiment and described as Train-on-Source-Only**; a separate addition experiment under a different name can be planned. If unresolvable source/speaker overlaps are discovered, we will fix the experiment or mark the limitation and raise the issue with the instructor — we will not silently cancel a Cross-Dataset requirement.

**Claim boundaries:** the transition involves Generator, speaker, source, and channel; the difference is not a causal effect of Generator alone. Each direction will be reported separately, without automatic summing of Scores or comparing them as if they were the same population.

**M-AILABS:** a Real-only Audit at a fixed threshold on a set held out of training; or Real added to training in a different experiment. There is no independent EER for a real-only dataset and no use of the same clips simultaneously in two roles.

### 6.5 Protocol P3 — Acoustic/Channel Shift

On a reserved Test we create **documented copies** of the same recordings with processing such as MP3/Opus compression, resampling, noise/reverberation, loudness changes, or Replay *only if a suitable environment exists*. Test derivatives are intended **for Robustness evaluation only**; not for training or choosing an Augmentation policy. If the same clip is changed in several ways, the statistical unit remains **the source recording**, not each copy as independent.

The same transformations and the distribution of loudness/noise must be kept in Real and in Fake in order not to create a class shortcut. Physical Replay is not equivalent to a software codec simulation, and we will not claim that we tested real Replay if we only carried out compression. Clean vs Perturbed differences will be presented with uncertainty and at the condition level.

### 6.6 The Place of the Competition Test

The course's competition set **is not** an Internal Test for research and tuning. After choosing a configuration by means of the permitted data, we will carry out a `Final Model Freeze` before the test files are released: Hash of weights, Encoder, Preprocessing, Feature Order, Scaler/Normalizer, Threshold if one exists, Score Direction, software and Dependencies, Config, and Commit SHA. If we decide to carry out a *Final Refit* on Train+Validation, the policy and configuration will be determined in advance, and the training will end **before the test clips are published** and in accordance with the course guidelines.

After the Test is published: Inference only; a format/file-integrity check is permitted and not model adaptation. An `id,score` deliverable with a high Score = more Spoof, one row per ID. We do not carry out Pseudo-Labeling, searching for original examples, analysis intended to guess labels, or retraining following the check; the single submission is planned in advance.

### 6.7 Choosing the Primary Evaluation Protocol and Test Governance — A Decision before Models

**A Decision Gate after EDA and before training/viewing Scores:** we will lock an `evaluation_contract.yaml` containing: (1) the primary research protocol; (2) Folds/Groups and Hash lists; (3) the primary `EER` endpoint and the computation definition; (4) Aggregation and Uncertainty rules; (5) the comparison matrix M0–M3; (6) the permitted dates for exposing Test results.

**The selection hierarchy:** `P1 Strict LOSO` if a split exists with sufficient source/systems and Real+Fake examples, and the required independence can be guaranteed; otherwise `P2 Cross-Dataset` as the primary endpoint when it is feasible and free of substantive overlaps, with both directions reported separately and a primary direction determined in advance; otherwise `P0 Grouped Internal Evaluation` only, with a notice that the unseen-generator claim was not tested. **Regardless of the primary endpoint, P2 remains a high-priority evaluation target according to the course requirements**. The feasibility failure is documented without replacing the protocol after seeing the models' results.

| Data layer | Permitted actions | What is forbidden |
|---|---|---|
| Train | Fitting learned features, Scaling, training models | Exposure to Eval clips/their derivatives |
| Inner Validation | Choosing Hyperparameters/Architecture/Layer/Pooling, Calibration | Participating in the final EER as if it had not been used for selection |
| A fixed Internal Test or Outer Fold | **Measuring only configurations and a selection procedure determined in advance** | Choosing a new model/Prompt/Threshold following Test performance |
| Competition Test | Inference in a frozen pipeline | Training, model selection, calibration, Pseudo-labeling |

**One evaluation alternative:** one can choose `Train + Validation + Locked Internal Test` or `Nested Grouped CV` according to the number of training groups, not both together without reason. In Nested CV every parameter selection is carried out within Inner Folds; Outer Folds are intended for evaluating the selection process. If comparing models on the Internal Test reveals a need for a research change, the insight can be recorded as *Exploratory* and tuning carried out only on training/Validation data; a later improvement on the same Test should not be reported as independent confirmation. For new verification a Holdout/external experiment that did not influence the decision is required.

**Pre-registration status:** after EDA a `PRIMARY_PROTOCOL_LOCKED` record will be produced before the M0–M3 results. Any later change receives a `protocol_deviation` with a reason and an effect on the validity of the inference.

## 7. Metrics, Thresholds, Statistics, and Fair Comparison

### 7.1 Primary Metric: Equal Error Rate

For each clip the system returns a continuous Spoof score. We will define `FPR_spoof(t)` as the ratio of Real classified as Fake and `FNR_spoof(t)` as the ratio of Fake classified as Real. EER is the error rate around a threshold at which the two rates are equal, according to an interpolation rule or a pre-defined threshold choice uniform for all models. **A lower EER is better**. The precision of the interpolation threshold is less important than consistency of computation; we will check this in Unit Tests and on known examples.

### 7.2 Complementary Decision Metrics

- `Macro-F1 = (F1_Real + F1_Fake)/2`, where the threshold is chosen **only on Validation**.
- `Fake Recall = TP_fake / N_fake`, that is the rate of forgeries detected.
- `Real Recall = TN_real / N_real`, that is the rate of real recordings preserved as real.
- `False Alarm on Real = 1 - Real Recall`; for M-AILABS this is a valid Real-only metric.
- Precision, Confusion Matrix, Score distribution, and Balanced Accuracy as needed.

Macro-F1 depends on the threshold and on class frequencies and is not identical to EER. We will not numerically compare AT-ADD's 90.71% Macro-F1 with the EER of another model. `minDCF` and `min t-DCF` are relevant for understanding the ASV literature but will not replace the EER of the course task, unless valid costs and probabilities are defined in advance.

### 7.3 Threshold Design and Score Preservation

For each model we will define the Score Direction, and only then choose a Threshold on Validation for metrics that require a decision. We will freeze the Validation threshold for all Test sets, including OOD. We will save continuous scores, labels, and local group identifiers (not in a prohibited publication) in order to compute ROC/EER and failure analysis. An OOD threshold must not be chosen retrospectively according to a Macro-F1 improvement.

### 7.4 Uncertainty and Statistical Stability

- For each Fold and each Generator separately: `n_real`, `n_fake`, source groups, EER, FPR/FNR at the Validation threshold, Generator and source data. A metric that is not defined in a single-class test will remain `NA`, and will not be replaced with Accuracy.
- The primary reporting over a number of Folds is **EER per Fold and a mean/median and spread between Folds**, while presenting sizes. An unweighted mean gives equal weight to Folds; therefore we will report the weight and the definition explicitly.
- **We do not merge Scores of different models between Outer Folds into a global EER without justifying calibration and a shared scale**, since even if each model's score is ranked well, the score scale may change between trainings.
- We will compare models on the same clips in the same Fold by means of `ΔEER = EER(candidate) − EER(reference)`; a negative value is better, but without CI/stability we do not claim significance. The number of Seeds and Repeats will be determined in the Experiment Contract before a run.
- A Bootstrap at the Group/speaker/source level according to the appropriate unit when the number of groups allows it; we will verify that both classes exist in every resample. For a sparse sample we will report substantial uncertainty and not hide it behind a CI that is too narrow.
- Drawing conclusions will distinguish between Data Splits variance, Training Seeds variance, and Generator-sampling variance. These are three different sources of uncertainty; we will not use the SD between Seeds alone as a CI of generalization.
- If the computational cost differs significantly, we will report extraction/training/inference time and memory alongside quality, and will not automatically choose a large model because of a tiny improvement.

### 7.5 Prohibiting Data Leakage and Correctly Classifying Protocol Mismatch

**Leakage:** using Test for Selection, crossing source derivatives, Feature Scaling on all the data, using Test Labels, or calibration on an evaluation sample. **Protocol Mismatch:** a valid test within the same Generator that is mistakenly described as generalization to a Generator not seen. **Confounding:** a combined change of Generator, speaker, source, and channel even when the split is valid. The distinctions will appear in every experiment report.

### 7.6 Primary Endpoint, Decision Criterion, and Choosing the Competition Model

**Primary Research Endpoint:** EER in the primary generalization protocol locked in Section 6.7. H1 comparison: M2 versus M0; H2 comparison: M3 versus M2. M1 versus M0 is a planned secondary representation analysis. Since a number of directions/Generator instances may differ in their difficulty, we will report per-Fold and avoid choosing the favorable Fold retrospectively.

**Secondary Endpoints:** P0 in-domain EER, both P2 directions (if they are not Primary), Real Recall on a held-out M-AILABS, Fake Recall by Generator, Macro-F1 at the Validation threshold, Confidence/stability, and the distribution of computational costs.

**A qualitative decision rule, without an arbitrary threshold invented:** (1) Does the direction of the difference on the Primary Endpoint fit the hypothesis? (2) What are its size and spread across Folds/Repeated Sampling? (3) Is the improvement accompanied by a significant worsening in Real Recall or in other OOD conditions? (4) Is the comparison valid according to the Split Audit? (5) What is the model's cost? We will summarize `supports / does not support / inconclusive`, and will not pick one pleasant result from a series of results.

**Choosing the model for the competition is a separate decision:** it is carried out on a Validation that represents the course data/the goal of the competition, before Test, and may prefer a model that does not have the best generalization EER. Both choices and results will appear openly in the report; competitive success should not be presented as proof of the same generalization hypothesis.

## 8. A Staged Model Plan

### 8.1 The Model Matrix

| ID | Input/Encoder | Classifier | Role | Status |
|---|---|---|---|---|
| M0 | MFCC, temporal statistics | Logistic Regression | Baseline; representation comparison | **Binding core** |
| M1 | CQCC, matching Pooling | Logistic Regression | Classical representation comparison | **Binding core** |
| M2 | Frozen wav2vec 2.0 Base, layer/Pooling defined | Logistic Regression | SSL representation and comparison to M0 | **Binding core** |
| M3 | The same Frozen wav2vec 2.0 | One-Class SVM | Examining RQ2 on the same Encoder | **A planned core; explicit Gate/Stop** |
| M4 | Frozen WavLM | Logistic Regression | Encoder comparison | Extension |
| M5 | SSL + a different Pooling/Layer | A light head | Local information/layers | Extension |
| M6 | AASIST-L / Deep SVDD | Dedicated | A deep model | Extension |
| M7 | Feature Fusion / Reconstruction / Ensemble | Combined | Isolating a new component | Extension |

The triple M0–M2 fulfills the requirement of a Baseline + two additional approaches. **M3 is the planned experiment for the core question RQ2**, since the Embeddings have already been computed; giving it up would be a documented Stop decision due to a validity, data, or resources problem, and RQ2 will not be reported as examined in such a case. M4–M7 are not a commitment.

### 8.2 M0 — MFCC + Logistic Regression

Pipeline: WAV → checking 16kHz/4s/Mono → MFCC (initial configuration: 20 coefficients; Frame ~25ms; Hop ~10ms) → Mean+Std Pooling over time → StandardScaler on Train only → Logistic Regression → a continuous Spoof Score. The proposed values are not proven optimal. We will initially choose a single simple configuration in order to determine a first EER, and will not open a Hyperparameter search before the Pipeline's validity.

**Acceptance:** a Notebook runnable from the start; an EER measured in practice; a Confusion Matrix at the Validation threshold; a split file and Config; library versions and Seed; absence of using Test for configuration choice.

### 8.3 M1 — CQCC versus MFCC

We will replace the features with CQCC, using Logistic Regression and the same Splits and Endpoint. For reproduction, the following must be fixed in the Config: the CQT/CQCC implementation version, the frequency range, bins-per-octave, the number of coefficients, handling of C0, Delta/Delta-Delta, Frame/Hop or unit time, Preprocessing, Mean/Std Pooling, the output dimension, and libraries. Values not yet chosen will be settled on Validation and not invented in the document.

**Fairness:** we will keep the same classifier type, the same Budget for Hyperparameter search (for example the same grid of `C` values), the same Inner CV, and the same selection metric — **not necessarily the same `C` value chosen**, because the dimensions and distributions of the representation differ. We will document the scope of the features and the additional cost.

### 8.4 M2 — Frozen wav2vec 2.0 + Logistic Regression

The wav2vec 2.0 Base Checkpoint will be set explicitly (`model_id`, revision/hash, Processor, and library versions), and loaded in Eval Mode with **frozen** weights. The following will be recorded: Sample Rate, Waveform normalization, handling of Padding/Attention Mask, Hidden State extraction from which layer, the time mask entering the Pooling, Mean or Mean+Std, Embeddings dimension, Chunking configuration, and length-cropping logic. **For the core comparison RQ2 (M2 versus M3-OC-Pure), the Checkpoint, layer, and Pooling will be set before the classification experiment according to an unsupervised rule or a decision documented in advance, without selection by Fake labels or labeled EER.** The shared representation values will be locked in the Experiment Contract before fitting the Downstream. It is permitted to conduct *separately* a representation-improvement experiment for M2 only, in which the layer/Pooling are chosen on a labeled Inner Validation; its results will not retroactively change the RQ2 representation and will not be called OC-Pure if passed to M3. Any search will be considered a Hyperparameter Search and documented.

We will extract Embeddings over 4 seconds with a local Cache whose key is `clip hash + checkpoint revision + feature config`, and train Logistic Regression with **the same tuning budget** as M0/M1. Scaling is fit on Train only. The layer or Training Seed must not be chosen according to Test. Computing Embeddings on Apple Silicon will be documented with Device, Batch Size, RAM, and extraction time.

### 8.5 M3 — Binary versus One-Class

**Core goal:** comparing M2 to M3 on the same Encoder, the same Embeddings configuration **chosen in advance without Fake labels** and the same Evaluation groups — but under deliberately different information budgets. The OC-Pure designation applies to **the entire chain of representation choice, fitting, tuning, and threshold** (except general Pretraining of an Encoder that exists beforehand and will be documented separately), and not only to the classifier's `fit()`.

| Stage | M2 Binary | M3 `OC-Pure` | M3 `OC-Supervised-Val` (secondary analysis) |
|---|---|---|---|
| Checkpoint / Layer / Pooling | **Locked in advance for RQ2, without Fake-labelled selection** | **The same locked representation, without Fake-labelled selection** | The same locked representation in order to isolate the effect of tuning; a supervised choice of the representation would require a separate experiment that is not OC-Pure |
| `StandardScaler.fit`, PCA, Feature Selection if learned | Train Real+Fake | **Train Real only** | Train Real only, as long as our goal is to isolate the effect of Validation and not to change the training |
| Classifier | LR on Real+Fake Train | One-Class SVM on Real Train only | The same One-Class SVM on Real only |
| Hyperparameters (`nu`, `gamma`) | LR `C` from labeled Inner Val | Fixed in advance / Real-only Inner Validation | Labeled in Inner Validation with Fake; this must be written |
| Threshold in hard classification | Labeled Inner Val | A Real-only rule, for example a pre-defined quantile | Labeled Inner Val |
| Model Selection | Labeled | **Without access to Fake labels, also not in learned preliminary stages** | Fake labels accessible only in Validation |
| Test/Eval | The same Manifest | The same Manifest | The same Manifest |

**Score Direction:** `OneClassSVM.decision_function` is higher for an Inlier; we will define `spoof_score = -decision_function` for all the EER checks. Reversing the direction is not a learned variable. For deviation from the Pretraining of a general Encoder, the early-training data will be documented separately and will not be presented as supervised One-Class training.

**Choosing `nu` and `gamma` in OC-Pure:** the default is to fix *in advance* `nu` and a `gamma` policy (for example a rule computed from Real Train only) before viewing Fake scores or Test results, and to document the values or the exact function in the Config file. Alternatively, it is permitted to use a **non-trivial** Real-only criterion that is registered in advance and measured on a Real Validation that is not used for fitting; it must be explicitly stated what the criterion is and how it is separated from threshold calibration. **One must not choose `nu`/`gamma` according to Real Recall when for each candidate a threshold for a fixed percentile is calibrated on the same Real Validation set**, because the rejection rate will be almost constant by definition and therefore does not distinguish between the candidates. An operating threshold, if required, will be set according to a pre-defined Real-only rule; EER will then be computed retrospectively on Eval for all the models, without using it in OC-Pure tuning. In OC-Supervised-Val one can choose parameters and a threshold according to a labeled Validation, but the result must be marked as a One-Class version with supervised selection, and not as OC-Pure.

**Permitted interpretation:** a comparison between a *labeled binary protocol* and a *one-class protocol without supervised selection on Fake throughout the entire Downstream-fitting chain and the choice of the locked representation*, which includes the difference in the Scaler and the Classifier. It is not an Ablation isolating only the classification function. We will also check False Alarms on Real from a new source in order to identify whether One-Class classifies authentic variance as forgery.

**Stop:** if there is not enough independent Real in Train/Inner Validation or the Scores are degenerate, we will document non-feasibility; we will not change the definition of OC-Pure merely in order to improve a result.

### 8.6 WavLM, AASIST, and Local Pooling as Extensions

WavLM provides a competitor on the SSL representation, not a promise of improvement. AASIST-L is possible if there is a justification for a dedicated experiment and computational capability. PhonemeDF points to variance of artifacts by phoneme; hence **our hypothesis** that Temporal Mean Pooling may weaken local forgery signs. An experiment between Mean and Max/Attention Pooling can be examined later, but one should not claim that the PhonemeDF paper already proved this at the recording level. Long recording windows/Sliding Windows are not a priority when every course clip is four seconds.

## 9. A New Protocol: Controlled Training Expansion by Means of MLAAD and PhonemeDF

### 9.1 The Role of the Sources and the Access Decision

| Source | What it contributes | A prominent risk | Usage decision |
|---|---|---|---|
| MLAAD (version v11 described) | A synthetic dataset mainly TTS, 205 models, 54 languages, metadata | No Real in the distribution itself; an M-AILABS source; licenses and speaker/text dependence | Conditional GO for a small pilot only |
| PhonemeDF | 4 TTS + 3 VC, 28,539 source families from LibriSpeech, parallel recordings/TextGrid | Derivatives from the same recording; licensing of derivatives and phoneme boundaries | Conditional GO for a small pilot; priority for Record-Level examples |
| AT-ADD Track 1 | An evaluation protocol for Unseen Generators and Channel Shift | No verified practical access; licensing terms not checked | **Not** for training and not for a direct Test at this stage |

The results reported on MLAAD do not verify that version v11 improves generalization compared with v1. The phonetic results of PhonemeDF do not verify an EER improvement in training expansion. Therefore every integration decision is conditional on **our experiment** and on the Gates of Section 9.2.

### 9.2 Dataset Admission Gates — Before Downloading Audio at a Significant Scale

**G1 — Access:** URL, download permissions, file scope, and version documentation can be verified. **G2 — License:** the usage, distribution, and derivative rights of the Audio, the model, the Real files, and the sources are verified separately; academic research does not exempt one from checking terms. For MLAAD, CC BY-NC 4.0 was declared on the dataset page that was examined; it should be verified at the time of download and the Real sources checked separately. For PhonemeDF one should not assume that all synthesis derivatives are automatically permitted under the LibriSpeech license. **G3 — Provenance:** Source IDs, speakers, texts, Generator/Family, reference files, and source associations are available and understood. **G4 — Overlap:** there is no prohibited overlap with course clips held in Test or with Negatives intended for external evaluation; M-AILABS/MLAAD and LibriSpeech/LibriVox are checked in particular. **G5 — Compute:** a small pilot can be processed locally and leaves time for running the main experiments. **G6 — Balance:** Real+Fake sets can be created with a controlled source composition and Eval data that does not leak into Train. **G7 — Reproducibility:** identifiers, version, selection script, list of examples, and seed are saved.

Each Gate will be recorded as `PASS`, `FAIL`, or `UNKNOWN`, with evidence. **UNKNOWN is not PASS**. If G2/G3/G4 fail, the dataset should not be included in a main experiment and a diversity conclusion should not be presented. If only Fake can be used and a matching Real cannot be created, we will report that the experiment is exposed to Dataset–Label Confounding, and will not claim that we neutralized it.

### 9.3 Source Risks and Class Balancing

MLAAD is based on recordings/texts related to M-AILABS. Therefore **expanding Fake from MLAAD against a fixed Real from another source** may cause the classifier to learn source instead of Fake. PhonemeDF allows a matching Real from the same LibriSpeech, but all 7 derivatives of a source must be kept in the same split, and choosing TTS versus VC may change the speaker set, the conditioning method, and the channel. If we use only a particular Fake and Real from another dataset, this must be presented as a limited condition; the experimental priority is **paired/matched-source** when licensing and data allow it.

The internal competition problem: 320 M-AILABS examples are Real only. One should not automatically choose these Real examples as a "half-balanced" counterpart for all the external Fake and call the result controlled; this may increase Shortcut Learning. We will prefer a matching Real for each source, and if it is unavailable we will consider the possibility of postponing the expansion experiment.

### 9.4 The Experiment Matrix: Size × Diversity

We will denote by `N` the number of **external Fake examples** chosen in addition to the course's fixed Train; `R` the number of **external Real examples**; `K` the number of unique Generator systems; `F` the number of Generator families (TTS/VC/Codec, when available). We will document separately the source, text, language, number of independent source families, and the **final** class ratio within the whole Train. **In Contrast S (E1 versus E2) N and R will grow together proportionally**, so that the class ratio and the overall mix are preserved as far as possible. It is not possible to keep both R constant and a constant class ratio when N changes. In contrast, **in Contrast D (E3 versus E4) both N and R will remain constant**, in order to examine allocating the same budget to a diversity of Generators. **N and R do not include Validation/Test**; derivatives of the same source must not be passed between the splits.

| Experiment | Course Train | External Fake | External Real | Diversity | The question examined | Permitted interpretation |
|---|---|---:|---:|---|---|---|
| E0 — Course Only | Fixed | 0 | 0 | Base | A performance anchor | EER without training expansion |
| E1 — Size Low | Identical to E0 | `N_low` | `R_low` | `K=K0` | The effect of increasing quantity in a composition fixed as far as possible | A trend by volume, when the class ratio is checked and controlled |
| E2 — Size High | Identical to E0 | `N_high` | `R_high` | The same `K0` and proportions weighting | Changing the quantity of Real and Fake together | Size under mix conditions, not Diversity |
| E3 — Diversity Low | Identical to E0 | `N_high` | `R_high` | `K0` systems | A control set at fixed N/R | A basis for the diversity comparison |
| E4 — Diversity High | Identical to E0 | **The same `N_high`** | **The same `R_high`** | `K1>K0` and/or `F1>F0` | Allocating the same quantity of examples to more Generators | The effect of allocating a fixed N between more Generators, subject to controls |
| E5 — Both Sources | Identical to E0 | A pre-defined budget | Matching Real per Gate | MLAAD + PhonemeDF | Transfer between sources/families | A combined experiment, not isolation of a single component |

Note: E2 and E3 can use **the same experimental arm**; they appear in two analytical roles. One should not claim "six independent arms" if some of the data is identical. The values `N_low`, `N_high`, `K0`, `K1` will not be set until the Gates and EDA. One must ensure that the number of source families itself does not change deliberately when trying to isolate only K, and that comparisons do not move from TTS only to TTS+VC while claiming that only the number of Generators was measured. **The number of Generators and the number of families are two different levels of diversity.**

### 9.5 Primary Comparisons and How Confounding Is Prevented

**Contrast S — Size Effect:** E1 versus E2, with approximately the same Generator list, the same Real families and sources, the same TTS/VC ratios, and the same processing methods. We will increase **`N_low → N_high` and `R_low → R_high` by the same growth factor**, as far as the availability of matching Real sources allows, and verify the class rate **in the whole Train after adding the course's fixed base**, and not only in the external part. Since the base ratio is 920 Real versus 600 Fake, adding at a 1:1 ratio will not necessarily preserve the base ratio. One can choose an addition ratio that matches the course base or an identical declared sampling/balancing policy in all arms; if the final composition is not preserved, we will report that the comparison also includes a Class Balance change and will not attribute the result to Size alone. We will set in advance the source/speaker/language mix, proportional sampling for each Generator, and a fixed Balance/Weights policy, and document the number of **independent recordings at the source level** alongside the number of files. We will prefer a small arm that is a grouped subsample of the large arm, without using Eval results for selection.

**Contrast D — Diversity Allocation:** E3 versus E4 with **exactly the same N and the same R**, the same overall class ratio, and the same size/Pooling policy. One can compare `K0=2` versus `K1=6` only if each group has at least enough independent examples; these are **numerical examples**, not set values. We will maintain a matched Real representation. If E4 introduces VC and E3 only TTS, the result measures *family diversity*, not only the number of models, and this must be declared.

**Contrast Source:** if MLAAD alone, PhonemeDF alone, and a combination are examined, this is also a change of **source/language/speaker**, not only a change of Diversity. We will not conclude from this what caused the improvement without additional controls.

**The conditional expansion metric:** EER on **the same fixed Holdout groups** set before the experiments; secondary: Real/Fake Recall and Macro-F1 at the Validation threshold. If a Holdout group includes only systems already in training, it tests In-domain; if new external systems are held out, an Unseen-Generator claim can be made only according to the verified separation. External data will never include examples of the Eval intended for OOD.

### 9.6 Replications, Sampling, and Dependence on Examples

Since PhonemeDF produces several derivatives per source, **the number of files is not the number of independent examples**. We will manage `derivation_group_id` (or connected components of source recordings) and carry out Subsampling at the source level before choosing synthetic versions, as far as possible. For Diversity we will try to also compare the number of independent speech sources, and not only the N of Fake files. **Necessarily, for a fixed N and a growing K, the mean number of examples per Generator decreases; this is a feature of comparing budget-allocation policies and is not an isolated causal effect of K.** We will run several Seeds for subset selection **and also a number of different Generator compositions for each K** if the dataset allows it; we will present spread separately across compositions/samples and model trainings; when the computational budget is limited, we will prefer more independence between sources over duplicating files.

### 9.7 Pilot Check and Stopping Rules

We will carry out a **Small Data First** pilot: verifying 100–300 examples/metadata (an estimated working number, not a research requirement), Hash/source checks, creating a grouped split, extracting Features, and checking Scores' validity. If there is no clear licensing, if the matching Real is missing, if an Overlap with Test is found, or if creating the comparisons requires introducing several changing factors simultaneously without the possibility of control — we will stop RQ3 and leave it as *Not Feasible Under Verified Constraints*. This is a legitimate design result and not a project failure.

### 9.8 What Must Not Be Done in the Expansion Experiments

- Adding only external Fake from a particular source and then attributing the improvement to "forgery diversity" without control over source/class.
- Mixing PhonemeDF's original Real with a derivative of it on the other side of Train/Test.
- Downloading 82GB and more of material before verifying licensing, access, and the ability to fit; a pilot first.
- Choosing K, N, systems, or a threshold on the basis of the Test results intended to verify them.
- Counting seven derivatives of the same sentence as seven independent source families.
- Concluding from PhonemeDF's KLD findings that the EER in the course will necessarily improve.
- Presenting an improvement from MLAAD v11 as if it had already been measured in the paper on this version.
- Including AT-ADD as a direct training/test experiment without verified access and licensing.

## 10. Augmentation, Robustness, and Control Experiments

### 10.1 A Separate Policy for a Training Experiment and a Robustness Test

**Training Augmentation** will be applied only on Train, with the same probability rule and processing range for Real and for Fake, unless an explicit hypothesis about asymmetry is being tested. **Robustness Evaluation** will be applied on a reserved Test fixed in advance, and only after freezing the training policy. The results of that same Robustness Test set must not be used to re-tune the Augmentation policy; if one wishes to compare Policies, an independent Robustness-Validation from Train/Validation only is required.

### 10.2 A Controlled Augmentation Experiment

| Arm | Changing feature | Fixed features | Validity claim |
|---|---|---|---|
| A0 | No Augmentation | Dataset/Encoder/Classifier/Split | Clean baseline |
| A1 | Codec/Resampling | Everything else | Robustness to similar codec conditions only |
| A2 | Noise/RIR | Everything else | Robustness to similar acoustic disturbances only |
| A3 | A combined policy | The other components remain | Measures a mixture of processing, not a single component |

There is no obligation to carry out all four arms; we will choose at most one experiment with a justification from the EDA, and carry out an Ablation if time allows. We will also check whether the Augmentation harms Clean EER. Following AT-ADD we will need to report **Real Recall under Shift** — not only how many forgeries were caught.

### 10.3 Score Consistency and Extensions

Inspired by NKU-HLT in AT-ADD, one can later encourage similar scores for a clean clip and for a version that underwent a change that does not change the label. This is a **hypothesis for future research**; it is not a condition for the course stage. If it is implemented, it is necessary to compare an identical model with and without a consistency component and also to examine side effects: erasing forgery traces sensitive to change.

## 11. Error Analysis, Shortcut Learning, and Causality

### 11.1 One Must Report More Than a Single Overall Metric

Inspired by AT-ADD, for each model we will report overall EER, EER by dataset when two classes exist, Fake Recall by Generator as far as there are examples, Real Recall by Real source, the Score distribution, and the decision threshold set on Validation. The BigVGAN and Replay findings in AT-ADD justify examining targeted weaknesses, and not assuming that every Generator is equivalent to another. Even a model with a good EER may classify Real from a new source as Fake.

### 11.2 Shortcut Probes

- **Dataset probe:** can the speech source be predicted from Features on Real only? If so — the information exists; this is not proof that the Detector uses it.
- **Silence/Loudness/Bandwidth probes:** are Scores especially sensitive to silence at the beginning/end, DC Offset, loudness, or frequency cropping?
- **Matched transformations:** we choose the same recording and apply a known change while preserving its label; if the decision changes, there is evidence of channel sensitivity, not necessarily proof of the cause of the general decision.
- **Source-matched fake/real:** when there is Pairing, we check whether the classifier's advantage is preserved without trivial source differences.
- **Shared errors:** for two models we can compute Jaccard between error sets, but the level of complementarity does not guarantee that combining them will improve the results.

### 11.3 The Inference Boundary

Cross-Dataset and LOSO experiments show **where the model struggles**. In order to claim **why** it struggles, an experiment is needed that holds the other variables constant as far as possible. EER differences between Domain A and Domain B may include Generator, Speaker, language, Source, and Channel in parallel. We will not write that a model "learned noise" merely because it failed on M-AILABS; at most that the result is consistent with a dependence on source features, and we will propose a control check.

## 12. Resources, Implementation, and Reproducibility

### 12.1 Compute Principles

The available computer is a MacBook Pro with an M3 Pro; therefore we will document RAM/memory constraints and prefer **Frozen SSL Feature Extraction** in batches that allow memory management, a local Cache, and small models. One should not assume that all CUDA-based research code will run without adaptation on Apple Silicon. AASIST-Full/XLSR Fine-Tuning/Ensemble will be considered only after Base Experiments, and not according to their success on an external Benchmark alone.

### 12.2 Structured Experiment Registration

**Experiment Contract — mandatory before every research run:**

| Field | What is locked in advance |
|---|---|
| `experiment_id`, `research_question`, `hypothesis` | Identifier, question, approved hypothesis |
| `train_manifest_hash`, `validation_manifest_hash`, `test_manifest_hash` | The split files, a sample to prevent retrospective changes |
| `grouping_rule`, `held_out_conditions` | The source/speaker/Generator unit and what was held out |
| `representation`, `checkpoint_revision`, `preprocessing_fit_scope` | Feature config, Pretraining, Real-only or Real+Fake fit; for RQ2 also `representation_selection_scope` and evidence of locking without Fake-labelled selection |
| `classifier`, `search_space`, `search_budget`, `seed` | Tuning policy and comparison budget |
| `primary_endpoint`, `secondary_metrics`, `threshold_rule` | How we measure and at what threshold |
| `contrast`, `interpretation_limit`, `stop_rule` | What was compared and what should not be concluded; for Contrast S also `n_fake_external`, `n_real_external`, `final_class_ratio`, `matching_policy`; for Contrast D the same N/R in both arms |
| `git_sha`, `environment`, `compute_budget` | Code, run environment, and cost |
| `result_status`, `deviations`, `audit_evidence` | Commitments checked and deviations |

Alongside the Contract, for each run we will save local Scores and predictions for the purpose of reproducing EER/ROC, verifying Test scope, and errors; only summarized results will be uploaded to the repo when permitted. We will not change a contract following Test: a new experiment will be registered as Exploratory and its result will require a new reserved confirmation.

### 12.3 Test Suite and Code Hygiene

- Unit Tests for a single EER function: positive Spoof direction, sorted examples, ties, single-class input (should fail with a message), Interpolation, and consistent Rate computation.
- **Split Invariant Tests:** no shared `derivation_group_id` or original recording identity between Train/Validation/Test in a Strict protocol; no overlapping Speaker when Speaker-Disjoint is claimed; no Generator held out at any stage of `fit`/`select`.
- **Learned Preprocessing Scope:** M0/M1/M2 fit on Train only; M3 OC-Pure fits Scaler/PCA/Feature Selection on Real Train only; the RQ2 representation (Checkpoint/Layer/Pooling) is locked without Fake-labelled selection; `nu`/`gamma` are set without Fake according to a non-degenerate rule; no learned component trains on Test.
- **Test Access Audit:** the number of Internal Test exposures and the code that created a final report are documented; no architecture change after exposure.
- **Cross-Dataset Tests:** target lists do not appear in Train; Hash/source overlap is checked; the sets include Real+Fake for measuring EER.
- **External Data Admission:** Gates with evidence; Unknown will not be counted as PASS; licensing, source pairs, and Metadata will be checked before training.
- **Competition Smoke Test:** a CSV `id,score` with the exact column order, a single ID, a numerical score, and a row-count check — without Test labels or reusing the test for tuning.

### 12.4 Code and Data Policy

Audio, `train.csv`, Test files, Embeddings, personal Metadata, labels, or lists that could reveal protected information will not be uploaded to the public repo. Code, configurations, and aggregate results will be published only subject to the guidelines and licenses. We will record the source/version/license of the Audio data, models, noise/music for Augmentation use, and Pretraining.

**AI Prompt Log — an appendix required for submission:** from the planning stage we will keep a Prompt record with the date, tool/model, task, prompt wording, output/code files affected, and the human verification carried out; we will verify that the appendix contains no personal information or course data that must not be shared. Before each Stage a Prompt Log appendix file will be prepared according to the requirements of the guidelines.

## 13. Execution Track, Gates, and Stopping Criteria

### 13.1 Stage 1 — Literature Review + EDA + Baseline

**The goal of the submission:** a 2–3 page document and a notebook. At least five papers will be derived from the review; the distribution of the data by source, speaker, and system, listening and spectrograms, and a real EER result of M0 will be presented. **Exit Gate:** the course file was loaded and examined; a valid split (or its limitation) was documented; the Notebook reproduces the EER; no models were chosen according to Test.

### 13.2 Stage 2 — Experimental Design

**Deliverable:** a two-page design document and a feedback meeting. It will include H1/H2 and a description of the conditional RQ3, M0 as the Baseline and M1/M2 as the two additional approaches, **M3 as a planned core experiment**, a primary evaluation protocol that will be locked after EDA, Cross-Dataset at high priority, Strict LOSO rules, Ablations, metrics, Stop Rules, and inference boundaries. If the EDA has not yet been completed, a Metadata-dependent Gate will be explicitly noted instead of presenting an invented split.

**Exit:** an `evaluation_contract` and basic Experiment Contracts ready before running the deciding results; a two-page document derived from the master document and not copied from it.

### 13.3 Stage 3 — Experiments, Results & Competition

**Deliverable:** a 6–8 page report, code allowing reproduction, at least M0–M2, **M3 as the core of RQ2 if the Gate is valid**, Cross-Dataset in accordance with the course requirements or an explicit explanation of a feasibility problem raised with the instructor, P0/P1 results as far as possible, Real/Fake error analysis, and uncertainty. Negative results are part of the report.

**Internal Test:** will be exposed only after the selection protocol is closed; any check that moves a new model is marked Exploratory and is not confirming evidence on that same Test. **Competition:** Final Model Freeze before the competition test is published; after the publication inference only, an `id,score` integrity check, and a single submission according to the guidelines. **Prompt Log:** we will attach the required prompt documentation.

### 13.4 Staged Progress — The Work Order

| Order | Deliverable | Transition Gate |
|---|---|---|
| 0 | EDA, Provenance graph, Metadata Schema, Split Manifest, EER tests | Group/Real+Fake conditions and defining independence units |
| 1 | **Protocol Lock**: choosing P1/P2/P0 as Primary, detailing the mandatory P2, and freezing Test Governance | Without viewing models' Scores |
| 2 | M0 + Notebook: a first EER | Validation only for model selection |
| 3 | M1 + M2: Representations comparison, a uniform tuning budget | The same Splits, EER Scores, and Model Contracts |
| 4 | **M3 OC-Pure** and optionally OC-Supervised-Val | Real-only fit, Stop Rule, comparison against M2 |
| 5 | P1 Strict/limited LOSO and P2 Cross-Dataset as determined in the protocol | Source derivatives/two Classes/no Test Tuning |
| 6 | A conditional MLAAD/PhonemeDF pilot | G1–G7 PASS |
| 7 | A conditional E0–E5 Size × Diversity | N/K and Generator compositions locked in advance |
| 8 | Augmentation, WavLM, Fusion, or Pooling only if there is evidence and budget | Experiment Contract and a separate Validation |
| 9 | Final Model Freeze, Prompt Log, Competition Inference | No training after the test is exposed; a valid CSV |

Stages 6–8 are conditional; the execution of the committed Stage 1–3 must not be harmed in order to carry out data expansion. If M3 cannot be carried out for a proven methodological reason, RQ2 will be explicitly marked 'not tested'.

## 14. Risk Register and Solutions in Advance

| Risk | Effect | Warning sign | Response / Stop decision |
|---|---|---|---|
| Few examples per Generator | Unstable EER | A very low number in LOSO | Do not present a seemingly precise per-Generator EER; attach n and CI or give up |
| Non-unique speaker identity | Unidentified Overlap | Contradictory Speaker IDs | A manual/source Audit; do not claim full Speaker-Disjoint |
| Real/Fake derivatives crossing a split | Leakage | The same `derivation_group_id` or a derivative relation on both sides | A strict Group split; disqualifying the experiment if there is no solution |
| Real speech from a single dataset only | Shortcut | Source predicts label | Control/Real matching; changing the experiment and not only improving the Score |
| Lack of matching external Real for MLAAD | Confounding | External Fake unique to a source | Postponing RQ3 or limiting interpretation |
| PhonemeDF licensing not verified | Unauthorized use | UNKNOWN in G2 | Do not include examples in the experiment |
| Train/Test mixing in Pretraining | Partial non-independence | An undocumented shared source | Provenance disclosure; do not claim complete independence |
| Computational load | Delay in the course requirements | Slow Feature extraction/insufficient memory | Frozen features, pilot, Cache, canceling extensions |
| Tuning on Test | Result bias | Changing a Threshold after Eval | Freezing Config; a new Test if verification is required |
| Erosion of the Internal Test through research decisions | Selection Bias | A new model following an earlier Test | A locked protocol, a one-time Test, marking Exploratory / a new Holdout |
| Fake leaking into OC-Pure through Scaler/PCA | A comparison that is not pure One-Class | `fit()` on two classes | Automatic enforcement of Real-only in M3 |
| Different models without a decision rule | A retrospective choice of the convenient metric | A contradiction between In-domain and OOD | A locked Primary endpoint, full Secondary reporting, and a separate Competition choice |
| Mix of Generators and Channels | Unclear causality | All the variables change together | Reporting on combined Shift only |
| Overfitting to audio changes | A decline in Clean performance | A1/A2 harm Clean | Checking both conditions and preferring a stable model |
| Scoring errors | Misleading results | A good model with an anomalous EER | Unit Tests, uniform Score direction, Audit |

## 15. Decision Log — Approved, Conditional, Open

### 15.1 Decisions Approved within the Planning

1. The project remains **Binary Speech Deepfake Detection**; EER is the central metric.
2. The course data base: 1,520 clips; M-AILABS serves as Real only.
3. M0 MFCC+LR; two additional mandatory approaches M1 CQCC+LR and M2 Frozen wav2vec2+LR.
4. M3 One-Class SVM on a **shared representation fixed in advance without Fake-labelled selection** is a **planned core experiment** after completing the initial triple; if not feasible, RQ2 will be marked as not tested.
5. All the models will be compared on the same verified splits and with a uniform Score direction; Trial/Model Selection will be carried out only by means of Inner Validation.
6. Separation between training, Validation, Internal Test, and the competition Test; preventing Test erosion through repeated choices.
7. AT-ADD is a methodological **Research Paper 10**; it is not Dataset 03 in the list of training datasets.
8. MLAAD and PhonemeDF are Dataset candidates only, and subject to Gates.
9. There is no advance determination that One-Class/SSL/Augmentation/Ensemble are superior — these are hypotheses to test.
10. The evaluation will separate In-Domain, Unseen System, Cross-Dataset, and Channel Shift.

### 15.2 Decisions That Cannot Yet Be Fixed

- The number of Folds and the split ratio; will be determined after an EDA of speakers and sources.
- Whether LOSO is valid for the specific Generator identifiers in the course file.
- Whether a full Speaker-Disjoint and also Source-Disjoint can be carried out for every experiment.
- The licensing of the expansion, the overlap of datasets, and the matching of external Real.
- The values of N and K, the ratio between TTS/VC, languages, and the number of Seeds in the RQ3 experiments.
- The choice of checkpoint/layer/Pooling for the supervised M2 experiments, without affecting the representation locked in advance for the RQ2 comparison.
- Whether there is sense in adding WavLM, AASIST-L, or Score Consistency.
- A framework for optimizing runtime on Apple Silicon.

### 15.3 Explicit Conditions We Will Not Promise before Measurement

There is here no EER of the course, no proof of generalization ability to a new Generator, no result of a Size/Diversity comparison, no declaration of full Speaker-Disjoint, and no confirmation that the licensing of every external dataset is valid. These will be completed by means of EDA, Gates, and experiments, or marked as inapplicable.

## 16. Expected Contributions and Reporting Boundaries

At the end of the project we aspire to present: (1) a transparent Baseline and a real EER; (2) a comparison of representations with control over the classifier and the split; (3) a Binary/One-Class comparison if M3 is feasible; (4) at least one generalization test whose validity was proven against the Metadata; (5) a Real/Fake error breakdown; (6) positive and negative findings with uncertainty; (7) reproducible code and a final model in the competition format. If RQ3 meets the Gates, we will add an empirical contribution on the difference between **increasing the training volume** and **expanding the diversity of generation systems**; if not, we will document the reasons for non-feasibility and will not create a conclusion without control.

**A summarizing principle:** success is not only the lowest EER on a single set. Research success is the ability to say which decision caused a change *up to the validity boundary the experiment allows*, which domains were tested, under what conditions the system fails, and how this can be reproduced.

---

## Appendix A — An Example Experiment Contract: M3 versus M2

| Component | A binding decision in the design |
|---|---|
| Research question | RQ2 — Does One-Class improve generalization relative to Binary on the same Frozen wav2vec 2.0? |
| Split unit | By `derivation_group_id` and, to the extent of the claim, also speaker, from an Audit |
| Representation | Checkpoint, layer, and Pooling identical **and chosen in advance without using Fake labels**; Validation-chosen representation experiments for M2 will be kept outside the RQ2 contract |
| Training | M2: Real+Fake; M3-Pure: Real only, including Scaler/PCA and every learned transformation; `nu` and a `gamma` policy fixed in advance or chosen according to a non-degenerate Real-only rule |
| Validation | M2: labeled for choosing LR; M3-Pure: Real-only, without choosing Layer/Pooling by Fake and without choosing `nu`/`gamma` on Real Recall dictated by a fixed-percentile calibration; OC-Supervised-Val is examined separately if chosen |
| Primary Metric | The EER difference in the locked Primary Research Protocol |
| Secondary Metrics | Real Recall, Fake Recall, Generator groups, extraction/training time |
| Cannot be concluded | That replacing the classifier alone explains a gap; that every future forgery will be detected |
| Stop | Lack of independent Real sets / unresolvable Source Leakage / unsuitable Eval data |

## Appendix B — Pre-EDA → Locked Protocol Checklist

- [ ] `train.csv` was loaded and the fields actually existing, the labels, and the numbers were checked.
- [ ] original recording / derivation / speaker groups were defined, including Unknowns.
- [ ] P0/P1/P2 have a count of Real/Fake in each Fold and source families.
- [ ] A primary alternative was chosen from the hierarchy, without viewing model results.
- [ ] The Inner Validation policy, Test exposure times, and the Validation threshold were defined.
- [ ] The EER per-fold reporting method, spread, Aggregation, and uncertainty were locked.
- [ ] Experiment Contracts for M0–M3 were approved, including a fair tuning budget.
- [ ] Tests ensuring `OC-Pure` Real-only fitting were created.
- [ ] The Cross-Dataset constraints from the course were checked and a plan for handling overlaps was defined.
- [ ] A Final Refit/Freeze policy and a Prompt Log were prepared from the start of the work.

- [ ] For RQ2 the Checkpoint, layer, and Pooling were locked before using Fake labels for representation choice, and the supervised representation experiments of M2 were separated.
- [ ] In OC-Pure `nu`/the `gamma` policy were set without Fake, and it was shown that the Real-only rule does not degenerate after threshold calibration.
- [ ] In Contrast S `N_low/R_low` and `N_high/R_high` were set, the final Real:Fake ratio in each Train was documented, and the effect of Class Balance was checked; in Contrast D the same N and the same R were locked.

**The planning completion rule:** the document fixes *the decision-making method*, not EDA results that have not been carried out. Identifiers, Folds, N/K values, external models, and diversity components will be documented only after an empirical check, and in any case before they are used for deciding on Test.

---

## Bibliography — The 12 Sources Read

[1] Wang et al. (2024). *ASVspoof 5: Crowdsourced Speech Data, Deepfakes, and Adversarial Attacks at Scale*. arXiv:2408.08739. https://arxiv.org/abs/2408.08739  
[2] Wu, H., Tseng, Y., & Lee, H.-y. (2024). *CodecFake: Enhancing Anti-Spoofing Models Against Deepfake Audios from Codec-Based Speech Synthesis Systems*. Interspeech 2024. https://arxiv.org/abs/2406.07237  
[3] Todisco, M., Delgado, H., & Evans, N. (2017). *Constant Q cepstral coefficients: A spoofing countermeasure for automatic speaker verification*. Computer Speech & Language, 45, 516–535. https://doi.org/10.1016/j.csl.2017.01.001  
[4] Jung et al. (2022). *AASIST: Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks*. ICASSP 2022. https://doi.org/10.1109/ICASSP43922.2022.9747766  
[5] Baevski et al. (2020). *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations*. NeurIPS. https://arxiv.org/abs/2006.11477  
[6] Chen et al. (2022). *WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing*. IEEE JSTSP, 16(6), 1505–1518. https://doi.org/10.1109/JSTSP.2022.3188113  
[7] Wu, S., Cheng, Y., Wang, R., & Yan, D. (2026). *Robust Speech Forgery Detection via Enhanced Forensic Trace Generation*. Signal, Image and Video Processing. https://doi.org/10.1007/s11760-026-05167-y  
[8] Izrailov, K. E., Kotenko, I. V., & Chechulin, A. A. (2026). *Intelligent Voice Fraud Detection Methods in Authentication Systems*. Pattern Recognition and Image Analysis. https://doi.org/10.1134/S1054661826700203  
[9] Yin, J., & Lei, S. (2026). *A Novel Attack-Resistant Speech Forgery Detection Method Integrating One-Class Learning and Wav2vec2*. CNML 2026. https://doi.org/10.1109/CNML68938.2026.11452384  
[10] Müller et al. (2024). *MLAAD: The Multi-Language Audio Anti-Spoofing Dataset*. IJCNN 2024. https://doi.org/10.1109/IJCNN60899.2024.10650962; v11 (2026): https://arxiv.org/abs/2401.09512  
[11] Nallaguntla et al. (2026). *PhonemeDF: A Synthetic Speech Dataset for Audio Deepfake Detection and Naturalness Evaluation*. LREC 2026, 5905–5915. https://aclanthology.org/2026.lrec-1.469/  
[12] Xie et al. (2026). *AT-ADD: A Benchmark and Challenge for Robust and All-Type Audio Deepfake Detection*. arXiv:2608.23437v2. https://arxiv.org/abs/2608.23437

**Source for the course requirements definition:** *Voice Deepfake Detection: Real or Fake?*, HIT, October 2026; it is not counted as one of the 12 research papers.
