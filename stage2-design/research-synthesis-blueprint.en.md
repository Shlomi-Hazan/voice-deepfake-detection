# Document B — Research Synthesis & Experimental Blueprint

## Research and Experiment Plan for Voice Deepfake Detection and Evaluating Generalization to Unseen Attacks

**Project:** Fake or Real: Voice Deepfake Detection
**Researchers:** Shlomi Hazan & Mayan Adler
**Course:** Advanced Topics in Machine Learning, HIT
**Research foundation:** Nine academic papers, 2017–2026
**Version:** 1.0 — 2 November 2026
**Document status:** Proposed Research Design — Before Empirical Evaluation

---

# Executive Summary

The purpose of this document is to translate the conclusions obtained from the integrated literature review into an executable and reproducible research and experiment plan for the voice deepfake detection project.

The central research problem is the generalization ability of voice forgery detection models to attacks and data sources not included in training. The literature indicates that models may show high performance under known evaluation conditions, but struggle when the forgery-generation mechanism, the speaker's identity, the recording source, or the channel conditions change.

The present study will seek to examine two central factors that may affect the generalization ability:

1. **Feature Representation:** a comparison between pre-computed acoustic features and deep representations produced by Self-Supervised Learning models.
2. **Learning Paradigm:** a comparison between supervised binary classification and anomaly detection by means of One-Class Learning.

The experiments will be based on 1,520 four-second recordings, originating from three datasets: ASVspoof 5, CodecFake, and M-AILABS. The evaluation will focus on the Equal Error Rate (EER) metric, alongside error analysis by source, forgery type, and speaker, according to metadata availability.

The study will be carried out in a staged approach. First, a simple Baseline based on MFCC and Logistic Regression will be built. Subsequently, at least two additional approaches will be examined: an alternative acoustic representation by means of CQCC, and a pre-trained SSL representation with a lightweight classifier. Afterwards, according to the results and resources, one-class learning by means of a One-Class SVM on the same SSL representations will be examined.

More complex architectures, such as AASIST-L, Deep SVDD, Feature Reconstruction, and Multi-Model Fusion, are defined as extension options and not as initial implementation commitments.

The guiding principle is to prefer experiments that allow drawing valid research conclusions over increasing the system's complexity without control. In particular, model comparison will be carried out on shared data splits, while preventing leakage between sets, separating model selection from its evaluation, and distinguishing between general classification performance and true generalization ability.

---

# 1. The Purpose and Scope of the Document

This document constitutes the basis for the project's research and experiment planning.

It is intended to fulfill four roles:

**A. To connect the literature review to the empirical research.** To show how the conclusions from the papers lead to the choice of research questions, models, metrics, and experiments.

**B. To define a valid experimental process.** To describe in advance the manner of data splitting, model comparison, generalization evaluation, and prevention of biases.

**C. To distinguish between required experiments and extensions.** To ensure the work meets the course requirements, without committing in advance to complex implementations that are not required.

**D. To support reproducibility.** To document decisions, versions, Seeds, training settings, and results, so that the findings can be reproduced and interpreted critically.

This document does not replace the data-analysis notebook, the model code, or the submission reports. It serves as a master plan from which those deliverables will be derived.

## 1.1 Distinguishing between Types of Information

In order to maintain academic precision, throughout the project we will distinguish between three types of claims:

| Type | Meaning | Example |
|---|---|---|
| A finding from the literature | Data or a claim reported in a research paper | CodecFake found a decline in generalization for certain models trained on ASVspoof |
| A research hypothesis | A claim we want to test but has not yet been verified by us | SSL representations will improve EER compared with MFCC |
| Our own empirical finding | A result obtained from an experiment we conducted and documented | The EER of the Baseline on a defined split |

We will not turn a hypothesis into a finding without an experiment, and we will not attribute to a paper conclusions it did not explicitly test.

---

# 2. Course Requirements and the Connection to the Research Plan

## 2.1 Project Stages

| Stage | Date | Weight | Central requirements |
|---|---|---:|---|
| Stage 1 — Review | Week 4 | 15% | Literature review, data analysis, Baseline with EER |
| Stage 2 — Experiment Design | Week 7 | 15% | Research question, hypotheses, at least two additional approaches, protocol and risks |
| Stage 3 — Results | Week 12 | 30% | Experiments, comparisons, error analysis, report and reproduction code |
| Presentation | Last class | 20% | Presentation of the problem, method, findings, and conclusions |
| Competition | Before the presentations | 20% | EER on a hidden test set and the quality of the research process |

## 2.2 Deliverables by Stage

**Stage 1:** A 2–3 page document and a Notebook. The review will be based on at least five sources, the data analysis will include a distribution by dataset, speaker, and forgery system alongside listening checks and spectrograms, and the Baseline will present an actually measured EER.

**Stage 2:** A two-page design document and a feedback meeting. It must present a focused research question, hypotheses, at least two approaches beyond the Baseline, an evaluation protocol, generalization experiments, Ablations, and methodological risks.

**Stage 3:** A 6–8 page report, code allowing reproduction of the results, and a competition file. A fair comparison, error analysis, a discussion of generalization, and reporting also of results that do not support the hypotheses will be required.

The present document is an extended working document. It is not itself subject to Stage 2's two-page limit.

---

# 3. The Evidence Map: What Do the Nine Papers Contribute to the Planning?

| No. | Paper | The central knowledge we take | The resulting experimental decision |
|---|---|---|---|
| 01 | ASVspoof 5 | Generalization, unknown attacks, separation between speakers, and evaluation metrics | A controlled split and analysis by attack |
| 02 | CQCC | The effect of the choice of spectral representation on forgery detection | An additional Baseline with CQCC |
| 03 | AASIST | Learning temporal and spectral relations by means of Graph Attention | A candidate for an advanced deep model |
| 04 | wav2vec 2.0 | Learning pre-trained speech representations | A Frozen SSL Encoder with a classifier |
| 05 | WavLM | General speech representations, including information related to the speaker and the environment | An alternative Encoder to wav2vec 2.0 |
| 06 | CodecFake | Difficulty in generalizing to forgeries based on Neural Audio Codecs | Cross-Codec and Cross-Dataset experiments |
| 07 | Enhanced Forensic Trace Generation | Guided reconstruction can highlight artifacts | A conditional Feature Reconstruction extension |
| 08 | Intelligent Voice Fraud Detection | Combining acoustic features with statistical and deep models | An Ablation of Feature Fusion, if examined |
| 09 | One-Class Learning + wav2vec 2.0 | Modeling real speech instead of learning known attacks | Comparing Binary Classification to One-Class |

## 3.1 Planning Conclusions

Five principles emerge from the literature:

1. One should not infer generalization ability from a low EER on a single dataset alone.
2. The choice of features may be no less important than the complexity of the classifier.
3. Pre-trained representations may be suited to a small labeled dataset, but their contribution to forgery detection requires testing.
4. One-Class Learning offers the possibility of detecting unknown attacks, but may identify natural variance in speech as an anomaly.
5. Every additional component should be examined by means of a controlled comparison, taking into account the computational cost and the stability of the results.

## 3.2 Evidentiary Limitations That Must Be Preserved

**AASIST:** Its strong results on ASVspoof 2019 LA do not prove robustness to ASVspoof 5 or to CodecFake. In addition, one must distinguish between the best run and the average across Seeds.

**wav2vec 2.0 and WavLM:** ASR or Speaker Verification performance are not Anti-Spoofing metrics. The justification for using them is their quality as representation models, not a result proven in advance on our dataset.

**Enhanced Forensic Trace Generation:** The improvement following guided reconstruction is not uniform between feature types, and comes with an increase in the system's complexity.

**Intelligent Voice Fraud Detection:** Without a detailed Ablation, it cannot be determined which addition is responsible for the improvement.

**One-Class Learning + wav2vec 2.0:** There is ambiguity in the description of model selection by means of EER and there are inconsistencies in the Ablation table. Therefore we will not base planning on an unverified attribution of every improvement to a particular component.

**Significance:** The results matrix from the literature is a tool for building hypotheses, not a ranking table from which the best model is automatically chosen.

---

# 4. Defining the Research Problem

## 4.1 The Task

The task is Binary Audio Classification:

- Bona Fide — real speech.
- Spoof — fake speech.

Given a recording x, the system returns a continuous score s(x) representing how much the recording is suspected of being fake.

The convention in the project is:

**A higher Score = a higher likelihood of forgery.**

The evaluation will be carried out primarily by means of EER.

## 4.2 The Problem beyond Classification

The research problem is not only to learn a classification function that distinguishes between the two classes in given data.

We want to test whether the distinction learned is preserved when the recordings' features or the forgery-generation mechanism change.

In particular, we will try to distinguish between three scenarios:

- Performance on speakers not seen in training, within the same sources.
- Performance on forgery systems not included in training.
- Performance on a different data source, including a possible change also in speaker, recording, and forgery features.

## 4.3 The Central Research Question

**How do the speech representation and the learning paradigm affect the generalization ability of voice forgery detection models, when the type of forgery attack or the data source changes, while maintaining a controlled evaluation protocol?**

This is the study's overarching question. In order to answer it, we will narrow the experiments to a number of defined comparisons.

## 4.4 Sub-Questions

**RQ1 — Representation:** Do pre-trained SSL representations improve detection and generalization performance compared with classical features?

**RQ2 — Learning Paradigm:** Does One-Class Learning provide an advantage in detecting attacks not seen in training, compared with a binary classifier using the same speech representation?

**RQ3 — Domain Shift:** To what extent are model performances affected by source and speaker differences not directly related to forgery?

**RQ4 — Complexity:** Does an improvement obtained from an additional representation, classifier, or Fusion mechanism justify its complexity and resources?

For the purpose of completing the course requirements on time, RQ1 and RQ2 will be central, RQ3 will mainly serve for validity control and interpretation, and RQ4 will be examined only for extensions actually implemented.

---

# 5. Research Data

## 5.1 The Composition of the Dataset

In accordance with the course guidelines:

| Source | Real | Fake | Total | Nature of the data |
|---|---:|---:|---:|---|
| ASVspoof 5 | 300 | 300 | 600 | TTS / VC, systems A09–A16 |
| CodecFake | 300 | 300 | 600 | Reconstruction and encoding by means of Neural Codecs |
| M-AILABS | 320 | 0 | 320 | Real speech from audiobooks |
| **Total** | **920** | **600** | **1,520** | |

Each recording is supposed to be 4 seconds long, at a sampling rate of 16kHz and in a mono channel.

The `train.csv` file is supposed to include a label, source, speaker identifier, and forgery system. Before building the processing pipeline, the column names and values in the file itself must be checked, and field names must not be assumed in advance.

## 5.2 Known Features

The three datasets differ in the nature of the recordings and in the forgery-generation mechanisms.

In addition, M-AILABS includes only real examples. This fact creates an association between the data source and the class and requires caution in evaluating the models.

## 5.3 Features Not Yet Empirically Verified

Before determining the splits, the following must be checked:

- The number of unique speakers in each source.
- The number of examples per speaker.
- The number of examples per forgery system.
- The combination of source, speaker, and class.
- The existence of speakers or recordings appearing in more than one source.
- The existence of source and forgery recordings produced from the same sentence or the same recording.
- The distribution of loudness, silence, bandwidth, and other acoustic properties.
- The validity of the labels and example counts.

We will not choose in advance a number of Folds or a final percentage split before we know whether the number of speakers and systems allows it.

---

# 6. Preliminary Data Review — Data Audit

The data review is a mandatory part of Stage 1 and also a precondition for valid experiment planning.

## 6.1 Structural Checks

The first checks will be:

1. The total number of recordings.
2. The number of recordings from each source.
3. The real/fake distribution.
4. The number of forgery systems and the examples of each system.
5. The number of speakers and the number of examples per speaker.
6. The duration of the recordings, the Sample Rate, and the number of channels.
7. Identifying corrupted files, missing records, and duplicates by Metadata.

## 6.2 Acoustic Checks

We will examine representative examples of real and fake speech by means of listening and presenting Waveforms and Spectrograms.

Alongside this, we will measure features such as RMS Energy, silence rate, peak loudness, DC Offset, and energy-distribution features in frequencies.

The purpose of the checks is not to visually determine whether a recording is fake, but to identify differences between sources or classes that may affect the model's behavior.

## 6.3 An Important Rule in Data Analysis

Statistical descriptions can be computed for the purpose of understanding the dataset, but every stage learned from the data and used as part of a model — for example StandardScaler, PCA, Feature Selection, or threshold choice — will be fit on the training set alone within each Fold.

Feature Selection will not be performed on the entire dataset before the split.

---

# 7. The Data-Splitting Protocol

This is one of the most important parts of the plan, because the evaluation results will be valid only if we prevented information leakage.

## 7.1 A Basic Principle: Speaker-Disjoint Split

Recordings of the same speaker will not appear both in training and in evaluation.

We will examine using StratifiedGroupKFold or another grouped split, according to the number of speakers and the class composition.

The goal is to preserve, as much as possible, the representation of both classes and the sources, without violating the speaker separation.

If the speaker identifiers are not unique between sources, their meaning will need to be checked and we will not settle for a technical concatenation of the dataset name and the identifier.

## 7.2 The Separation of Three Sets

We will use the distinction between:

**Training:** fitting the model, computing normalization features, and learning the parameters.

**Validation:** choosing hyperparameters and models, and calibrating decision thresholds when required.

**Internal Evaluation:** a reserved evaluation of the chosen model, without changing the model based on its results.

The course's official competition set will remain separate from all of these.

If the data structure does not allow a valid three-way split while separating speakers, we will consider Grouped Cross-Validation for model selection and evaluation, with explicit documentation of the limitation.

## 7.3 The Same Split for All Models

All approaches will be examined on the same Training, Validation, and Evaluation sets as much as possible.

One model tested on an easy split should not be compared with another model tested on a difficult split.

The split-definition files will be kept in a manner allowing reproduction, without exposing the course data in the public repository.

## 7.4 Preventing Additional Leakage

In addition to separating speakers, it must be checked whether different examples share a source recording, text, or almost identical content.

This is especially significant for Codec Resynthesis, in which a fake example may be a reconstruction of a real recording.

If such associations can be identified by means of Metadata, linked examples must be kept in the same Fold. If not possible, we will document the risk and will not claim that we fully prevented leakage at the level of the original recording.

---

# 8. The Evaluation Protocols

We will define three levels of evaluation, in order of priority.

## P1 — Speaker-Disjoint In-Domain Evaluation

**Goal:** to measure performance when the training and evaluation sets are separated by speakers, but still represent the same data families.

**Method:** a grouped split by speaker, while preserving as much as possible both classes and the source distribution.

**Primary metric:** overall EER.

**Complementary metrics:** EER by source with two classes, errors by forgery system, and False Rejection by real source.

This is the base protocol for comparing the models.

## P2 — Leave-One-Attack/System-Out

**Goal:** to examine detection of attacks not included in training.

**Proposed method:** to keep a forgery system or group of systems out of training, and evaluate the model on them.

In ASVspoof 5 we will examine using the A09–A16 identifiers. In CodecFake we will use the Codec system identifiers found in the Metadata.

**Necessary control:** the Spoof examples of the held-out system will not be used for training or model selection. In addition, speaker separation must be maintained relative to the training data, or a limitation must be explicitly reported if this is not feasible.

**Condition for execution:** the existence of a sufficient number of systems, speakers, and examples to build a valid split.

**Reservation:** if the remaining set is too small for a stable EER computation, we will prefer to report the sample and the limitation instead of presenting a seemingly precise estimate.

## P3 — Cross-Dataset Evaluation

**Goal:** to examine the model's behavior when the data source changes.

A first possible experiment: training on ASVspoof 5 and evaluating on CodecFake.

A second possible experiment: training on CodecFake and evaluating on ASVspoof 5.

In each of them we will keep the evaluation source out of training and out of hyperparameter selection.

Since both sources include real and fake examples, EER can be computed for each direction separately.

**An important limitation:** a result in this experiment entangles source changes and forgery-mechanism changes. Accordingly, it does not measure in isolation only generalization to new attacks.

### The Role of M-AILABS

M-AILABS contains only real examples, and therefore an independent EER cannot be computed for it.

We can use it for examining the wrongful rejection of real speech (Bona Fide False Rejection), using a threshold set on Validation and not on M-AILABS itself.

We will examine two options separately:

- Using M-AILABS as a real source not included at all in training, for an external Audit.
- Including examples from it in training to test the effect of the diversity of real-speech sources.

The same M-AILABS recordings will not be used both for improving the model and for presenting them as an independent external evaluation.

---

# 9. The Evaluation Metrics

## 9.1 Primary Metric — EER

EER is the central metric in accordance with the course requirements.

The score the model returns will be continuous, with the direction:

**Label 1 = Spoof; higher score = more likely Spoof.**

We will use a shared EER function for all the models, and test it by means of Unit Tests.

The function will handle the definition of the positive class, the score direction, thresholds, and tied Scores in a documented and consistent manner.

## 9.2 Complementary Metrics

| Metric | Why do we use it? |
|---|---|
| Overall EER | The primary comparison metric |
| EER by source | Checking performance differences between ASVspoof 5 and CodecFake |
| EER by forgery system | Identifying difficult attacks, when there is a comparable real-speech set |
| Bona Fide FPR / False Rejection | Checking the wrongful rejection of real speech |
| Spoof Miss Rate | Identifying forgeries the model wrongly accepts |
| ROC / Score Distributions | Analyzing the behavior of the model's scores |
| Runtime / Memory | Evaluating the computational cost of extensions |

For terminological precision: when a high Score represents forgery, a wrongful rejection of real speech is equivalent to a False Positive relative to the Spoof class. In the report we will use well-defined terms and note the direction of the classes.

## 9.3 EER by Forgery System

For a particular forgery system, EER will be computed by means of its forgery examples against a suitable set of real examples.

We will prefer using real examples from the same source, and, to the extent possible, matched to speakers or evaluation conditions.

We will always report the number of forgery examples and the number of real examples used for the computation.

EER will not be computed from forgery examples alone.

## 9.4 Separating EER from the Operating Threshold

EER is a retrospective metric based on changing the decision threshold.

A practical system requires a fixed threshold. If we report errors at an operating threshold, the threshold will be chosen on the Validation set and kept unchanged during the evaluation of the test set.

A threshold will not be chosen based on the results of the test set.

## 9.5 Variance and Uncertainty

Where feasible, we will run several splits or Seeds fixed in advance and report the mean and spread.

We will consider confidence intervals that take into account grouping by speaker, when the number of groups allows it.

We will not interpret small differences in EER as significant without appropriate support. In particular, a result based on few examples may change due to a small number of wrong decisions.

---

# 10. The Model Plan

## 10.1 The Comparison Principle

Every new model should answer a clear question.

We want to distinguish between a change in representation, a change in classifier, and a change in learning paradigm. Therefore we will avoid, as much as possible, adding several components at once without a suitable Baseline.

## 10.2 The Model Matrix

| ID | Representation | Classifier | Paradigm | Status |
|---|---|---|---|---|
| M0 | MFCC | Logistic Regression | Binary | Required — Baseline |
| M1 | CQCC | Logistic Regression | Binary | Additional approach 1 |
| M2 | Frozen wav2vec 2.0 | Logistic Regression | Binary | Additional approach 2 |
| M3 | Frozen wav2vec 2.0 | One-Class SVM | One-Class | Central research experiment, conditional on feasibility |
| M4 | Frozen WavLM | Logistic Regression | Binary | Alternative / extension |
| M5 | Frozen WavLM | One-Class SVM | One-Class | Controlled extension |
| M6 | AASIST-L | Neural Binary Classifier | Binary | Advanced extension |
| M7 | SSL + Deep SVDD | Deep One-Class | One-Class | Advanced extension |
| M8 | Feature Fusion / Reconstruction | A suitable classifier | According to the configuration | Extension only |

The research minimum commitment is M0, M1, and M2.

M3 is the next preferred experiment because it makes it possible to examine the One-Class question while using the same Encoder as M2.

M4 and M5 will be examined if there is research value and resources to compare wav2vec 2.0 to WavLM.

M6–M8 are not a condition for research success and are not required for the first stage.

---

# 11. Defining the First Baseline

## M0 — MFCC + Logistic Regression

### 11.1 The Goal of the Experiment

To build a simple, transparent, and reproducible system, which will serve as the reference point for all the following experiments.

### 11.2 Proposed Pipeline

Audio WAV

→ Feature Extraction: MFCC

→ Temporal Statistical Pooling

→ StandardScaler

→ Logistic Regression

→ Continuous Spoof Score

→ EER.

### 11.3 Proposed Opening Configuration

- Sampling rate: 16kHz.
- Frame length: about 25ms.
- Hop Length: about 10ms.
- Initial number of MFCC coefficients: 20.
- Pooling: mean and standard deviation over time.
- Classifier: Logistic Regression.
- Use of StandardScaler fit on Training only.
- Setting a Random Seed and library versions.

The values are proposed implementation decisions, not parameters required by the guidelines or proven to be optimal.

At the first stage we will prefer a single simple configuration. Tuning will be carried out only after the Pipeline is working and the result is measured properly.

### 11.4 Required Results

- A first actual EER.
- The distribution of Bona Fide and Spoof scores.
- Performance by source.
- A preliminary error analysis.
- Documentation of the data split.
- Documentation of the approximate training and inference time.

### 11.5 Completion Criterion

The Baseline is considered complete only when the notebook can be run from start to finish, the same experimental settings obtained, and the EER result reproduced.

---

# 12. The Two Additional Approaches Required for Stage 2

## M1 — CQCC + Logistic Regression

### The Experimental Question

Does replacing the acoustic representation from MFCC to CQCC improve detection and generalization?

### Planning

We will use the same classifier and the same protocol as M0.

Only the feature-extraction component will change, as much as possible.

For a fair comparison we will keep the same Train/Validation/Evaluation mechanism and a suitable and documented Pooling method.

### What Will We Learn?

If an improvement is obtained, it will be evidence that the acoustic representation has a contribution beyond the choice of classifier.

If no improvement is obtained, we can discuss the fact that a different spectral resolution does not guarantee an advantage on the present data.

**Research source:** Todisco et al. (2017) — CQCC [3].

## M2 — Frozen wav2vec 2.0 + Logistic Regression

### The Experimental Question

Does a pre-trained speech representation provide an advantage over pre-computed acoustic features, when the classifier remains simple?

### Planning

We will use wav2vec 2.0 Base as a frozen Encoder.

We will extract Embeddings from a predefined layer, perform Pooling along the time axis, and train a Logistic Regression on the representations.

There is no need to start with Full Fine-Tuning of the model.

### Experimental Control

In order to isolate the contribution of the representation, we will prefer to keep the same classifier used in M0 and M1.

The changes in the feature dimension and in the extraction cost will be documented, since the representations are not identical in size.

### What Will We Learn?

We will be able to evaluate whether SSL representations improve EER and generalization, or whether they mainly preserve other information not useful for forgery detection on the course data.

**Research sources:** Baevski et al. (2020) [5]; Chen et al. (2022) [6].

---

# 13. The One-Class Learning Experiment

## M3 — Frozen wav2vec 2.0 + One-Class SVM

### 13.1 The Goal of the Experiment

To examine whether changing the learning paradigm from binary classification to anomaly detection improves the detection ability of attacks not seen in training.

### 13.2 The Comparison Principle

We will use the same wav2vec 2.0 Encoder and the same representation-extraction method used by M2.

The main difference will be the classifier:

**M2:** a binary classifier trained on real and fake examples.

**M3:** a One-Class SVM trained only on the real speech examples in the training set.

This way we can compare the effect of the learning paradigm without also replacing the Encoder at the same time.

### 13.3 Hyperparameter Selection

We will distinguish between two possible protocols.

**Pure One-Class:** choosing the classifier's settings without using the labels of forgery examples, by means of a predefined configuration or a distribution control on real speech alone.

**One-Class with Supervised Validation:** training the classifier on real speech alone, but choosing hyperparameters according to EER on a Validation set including both classes.

Both protocols are legitimate as different experimental questions, but the second should not be presented as an approach that does not use forgery labels at all.

The distinction stems from the critique of the selection protocol described in Yin and Lei (2026).

### 13.4 Evaluation

The experiment will be examined under the same Internal Evaluation and the same generalization scenarios as M2.

We will measure EER, and in addition examine the behavior of the scores of real speech from different sources.

### 13.5 Central Research Risk

A One-Class SVM may identify real recordings from a new source as anomalies.

Therefore success in forgery detection must be examined together with the rate of wrongful rejection of Bona Fide.

### 13.6 Why Not Start with Deep SVDD?

A One-Class SVM makes it possible to test the central research hypothesis without first adding an additional learned network, a complex loss function, and a sensitive training process.

If the results indicate potential, we can proceed to Deep SVDD. If not, we will still obtain a significant research result regarding the limitations of One-Class Learning on our data.

**Research source:** Yin and Lei (2026) [9].

---

# 14. Research Hypotheses

The hypotheses are formulated in advance to allow falsification and not only confirmation.

| ID | Hypothesis | Comparison | Central metric | What would refute it? |
|---|---|---|---|---|
| H1 | SSL representations will provide better generalization than classical features | M2 versus M0/M1 | EER on held-out attacks | A similar or higher EER for M2 |
| H2 | One-Class Learning may improve the detection of unknown attacks relative to Binary Classification | M3 versus M2 | Unseen-Attack EER | M3 does not improve EER or shows a worsening |
| H3 | One-Class Learning may be more sensitive to a change in the source of real speech | M3 versus M2 | Bona Fide False Rejection by source | No substantial difference, or M3 is more stable |
| H4 | Combining classical and deep representations may add complementary information | Fusion versus the components separately | EER and ablation | Fusion does not improve or harms |
| H5 | Additional complexity will not necessarily lead to a stable improvement that justifies its cost | A complex model versus a simple one | EER, variance, and cost | A large, consistent improvement at a reasonable cost |

H1–H3 are the desired central hypotheses.

H4–H5 will be examined only if we decide to carry out advanced extensions.

The hypotheses are not a predetermined statement about the results. Their purpose is to define exactly what will be considered support or non-support for the research direction.

---

# 15. Ablation Experiments

Ablation is intended to isolate the effect of a particular component and allow an explanation of the change in performance.

## 15.1 Basic Ablation — Representation

We will compare:

- MFCC + Logistic Regression.
- CQCC + Logistic Regression.
- Frozen wav2vec 2.0 + Logistic Regression.

In all three experiments we will keep the same evaluation protocol.

This is a comparison between representations, and not a full comparison of their computational cost, since SSL extraction may be more expensive.

## 15.2 Ablation of the Learning Paradigm

We will compare:

- Frozen wav2vec 2.0 + Binary Classifier.
- Frozen wav2vec 2.0 + One-Class SVM.

This comparison is especially significant because it keeps the same Encoder.

However, it must be recognized that the number of labels and class examples used for training deliberately differs between the two approaches. This is part of the research question, and not a state of an identical label budget.

## 15.3 Ablation of Preprocessing

If significant differences in silence or loudness levels are found in the data analysis, we can examine the effect of silence removal or loudness normalization.

A possible hypothesis is that such operations will reduce dependence on source features.

Conversely, they may remove information useful for forgery detection.

Therefore we will not perform them as an automatic step without documenting their effect.

## 15.4 Advanced Ablations — Conditional

If we reach more complex models, we will define a suitable Ablation for each component:

- wav2vec 2.0 versus WavLM.
- A single layer versus Weighted Layer Pooling.
- LFCC/SSL separately versus Feature Fusion.
- One-Class SVM versus Deep SVDD.
- Feature Reconstruction with and without reconstruction.
- A single-classifier system versus Multi-Model Fusion.

We will not carry out all the experiments just because they are possible. We will choose them according to the research question, the time, and the expected contribution.

---

# 16. Checks for Shortcut Learning and Data Leakage

This is a necessary component of the research plan and not an optional appendix.

## 16.1 The Risk of Identifying the Source Instead of the Forgery

Since M-AILABS includes only real speech, a model can exploit the association between the data source and the class.

In order to detect this risk we will carry out:

**A check of the Score distribution by source:** we will check whether real examples from M-AILABS consistently receive different scores from real examples in the other two sources.

**A Dataset Probe:** we will examine whether the recording source can be predicted from the features or the Embeddings, especially when using only real examples from all the sources.

A high ability to identify the source does not prove that the final classifier uses this information, but it indicates that the information is available in the feature space.

**Comparing Pooled versus Cross-Dataset:** we will check whether good performance in a mixed evaluation is also preserved when moving between sources.

## 16.2 Artifacts Not Related to Forgery

We will check whether the model's scores are abnormally affected by:

- Loudness.
- DC Offset.
- The rate of silence at the beginning or end of the recording.
- Bandwidth Cutoff.
- Padding or processing features of fixed-length segments.
- Compression and Codec Fingerprints.
- Features related to the recording source.

Not every association between these features and forgery is illegitimate: some of the artifacts may be a genuine result of the forgery process. The question is whether the model relies on signs that generalize reasonably or on an incidental association specific to the dataset.

## 16.3 Negative Controls

Simple control experiments can be used, such as a source classifier or a check of a single feature, in order to evaluate whether trivial associations explain a significant part of the performance.

These results will be used for diagnosis, not as a substitute for the evaluation of the central model.

---

# 17. Error Analysis

We will not be content with reporting an overall EER.

## 17.1 Two Types of Errors

**Missed Spoof:** a fake recording accepted as real.

**False Alarm / Bona Fide Rejection:** a real recording classified as fake.

The two types of errors have different significance in applied systems, and therefore should be analyzed separately.

## 17.2 A Breakdown by Forgery System

We will check which systems are more difficult for each model, and whether the failures are concentrated in a particular family of attacks.

## 17.3 A Breakdown by Source

We will check whether a particular model shows good performance mainly on one of the datasets.

In such a case we will need to distinguish between a lack of forgery generalization and sensitivity to source features.

## 17.4 Analysis of Scores

We will present distributions of Bona Fide and Spoof scores, and check the degree of overlap between them.

For One-Class Learning we will especially examine whether real examples from a new source receive high anomaly scores.

## 17.5 Careful Interpretation

We will not attribute an error to a particular acoustic feature without supporting evidence. If it cannot be determined whether the source of the error is a Codec, a speaker, noise, or a type of attack, we will present this as a limitation and not as a proven explanation.

---

# 18. Reproducibility and Experiment Documentation

## 18.1 Principles

Every experiment must be reproducible by means of documented code, settings, and versions.

For every run, at least the following will be recorded:

- Experiment ID.
- Model name and version.
- Data source and split.
- Seed.
- Feature-extraction configuration.
- Hyperparameters.
- Pre-trained model version, if relevant.
- EER and complementary metrics.
- Training and inference time, if measured.
- Git version / Commit SHA.
- Notes on problems or limitations.

## 18.2 Configuration Documentation

We will prefer a separate Config for each experiment, for example YAML or JSON.

Each configuration will define the data, the model, the parameters, and the metrics, in order to prevent undocumented manual changes between runs.

## 18.3 Shared Evaluation Code

A single EER function will serve all the models, with Unit Tests verifying score direction and behavior in edge cases.

We will not use different EER implementations for different models.

## 18.4 Working with SSL Models

The weights of the pre-trained model will be kept outside the repo.

Embeddings will be computed by means of a separate script and can be saved in a local Cache in order to prevent unnecessary repeated extraction.

The Cache will not be saved in the public repo.

## 18.5 Documentation of External Sources

For every pre-trained model, library, or research code, we will record the source, version, and relevant license.

We will also examine the source of the Pre-training data to the extent possible, in order to document a possible risk of overlap between the earlier training data and the evaluation data.

## 18.6 Course Privacy Requirements

We will not upload to the public repo audio files, `train.csv`, test files, or individual data derived from them.

Code, methodological documentation, configurations, and summarized results permitted according to the course guidelines can be kept.

## 18.7 Use of AI Tools

In accordance with the course guidelines, we will maintain documentation of the prompts in which AI tools were used.

The documentation will make it possible to distinguish between our own research decisions, information taken from the sources, and assistance received from AI tools.

---

# 19. Risk Management

| Risk | Possible effect | Mitigation measure |
|---|---|---|
| Speaker Leakage | An optimistic and unrepresentative EER | Grouped Split |
| An association between source and forgery | The model identifies the dataset instead of the forgery | Source Audit and Cross-Dataset |
| Few examples per attack | An unstable EER | Reporting counts, limiting interpretation |
| Overfitting | An improvement in training but not in evaluation | Simple models, Validation, regularization |
| Codec and channel changes | A decline in generalization | Cross-Codec Analysis |
| One-Class sensitive to source | A wrongful rejection of real speech | Real-Only Audit |
| An SSL model that is too large | A high computational cost | A Frozen Encoder and Cache |
| Unnecessary Feature Fusion | Complexity without an advantage | Ablation |
| Tuning on the Test set | Biased results | Model selection on Validation only |
| Inability to reproduce | Harm to scientific validity | Configs, Seeds, and an Experiment Log |
| Overlap in Pre-training | A possibly optimistic evaluation | Checking the source of the weights and documenting the limitation |

## 19.1 A Methodological Stop Gate

If a split preventing leakage at the speaker level or at the level of the original recording cannot be built, we will not present the result as a reliable estimate of generalization.

We will prefer to fix the protocol, narrow the scope of the experiment, or note an explicit limitation.

## 19.2 A Complexity Stop Gate

We will not add a complex model just because it was presented in a paper.

We will require at least one of the following:

- A measurable and consistent improvement in results.
- The ability to answer a research question that cannot be tested with a simpler model.
- A clear advantage in a particular error profile.
- A clear computational or applied justification.

A negligible or unstable improvement does not automatically justify added complexity.

---

# 20. The Execution Plan by Course Stage

## Stage 1 — Review

**The goal of the stage:** to become familiar with the data, establish the research choices, and produce a first empirical reference point.

### Required Actions

1. Completing the abbreviated literature review from Document A.
2. Loading `train.csv` and checking its actual structure.
3. Reviewing distributions by class, source, speaker, and forgery system.
4. Listening to examples and presenting representative spectrograms.
5. Identifying Leakage and shortcut risks.
6. Determining an initial controlled split by speakers.
7. Implementing MFCC + Logistic Regression.
8. Computing EER and documenting the experiment.
9. An initial formulation of the findings and limitations.

### Stage 1 Deliverables

**Report:** A 2–3 page document containing a literature review, data analysis, a Baseline, and preliminary findings.

**Notebook:** A runnable notebook presenting the checks and the EER measurement.

**Completion condition:** a real EER result exists, with a clear description of the data and the split on which it was measured.

---

## Stage 2 — Experiment Design

**The goal of the stage:** to define in advance what is being tested, how it is tested, and what will be considered evidence for the hypotheses.

### Required Actions

1. A final formulation of the research question.
2. Choosing the central hypotheses.
3. Approving M1 and M2 as the two additional approaches.
4. Deciding whether M3 will be included in the central experiments.
5. Defining the Speaker-Disjoint protocol.
6. Defining Cross-Dataset and Leave-One-System-Out according to feasibility.
7. Defining EER metrics and error analysis.
8. Setting the Ablations.
9. Documenting the risks and solutions.
10. Documenting the decisions before running the advanced experiments.

### Stage 2 Deliverable

A two-page design document, to be derived from the present document.

The abbreviated document will focus mainly on the research question, the hypotheses, the chosen models, the protocol, and the risks.

---

## Stage 3 — Results

**The goal of the stage:** to carry out the comparisons that were planned, explain the results, and reach a valid research conclusion.

### Required Actions

1. Running the chosen models on the same splits.
2. Documenting EER, complementary metrics, and run features.
3. Carrying out the generalization experiments.
4. Running the pre-chosen Ablations.
5. Analyzing errors by source and forgery system.
6. Checking the stability of the results to the extent the data allows.
7. A discussion of results that do not support the hypotheses.
8. Preparing a results report and reproduction code.
9. Choosing the final model by means of Validation alone.
10. Freezing the model and the Inference Pipeline before the competition test is published.

### Deliverables

- A 6–8 page report.
- Code for reproducing the experiments.
- Full documentation of the configurations and results.
- A competition submission file in accordance with the official format.

---

# 21. The Competition and Final-Model Plan

## 21.1 Separating Model Selection from Its Testing

Every decision on architecture, Hyperparameters, decision threshold, or Preprocessing method will be based on the permitted training and Validation data alone.

We will not use the competition set for model selection.

## 21.2 Final Training

After choosing the configuration, it will be possible to retrain the model on the available training data in accordance with the determined protocol, as long as this is done before the test data is released.

We will use the same Pipeline described in the report, without an undocumented substantive change.

## 21.3 Freeze

Before the competition data is published, we will freeze:

- The model's architecture.
- The final weights.
- The order of the Preprocessing stages.
- The feature-extraction parameters.
- The score-computation method.
- The Inference code version.

## 21.4 The Submission File

In accordance with the course document, the submission file will be a CSV including:

`id,score`

Each recording will receive one score, and a higher score will indicate a higher likelihood of forgery.

Training on the test data, Pseudo-Labeling, manually labeling it, or searching for the recordings in the original datasets to reveal the labels are not permitted.

---

# 22. The Research Decision Map

In order to avoid over-expanding the project, we will define what has already been decided and what still depends on the data and the experiments.

| Decision | Status | Explanation |
|---|---|---|
| Binary Anti-Spoofing task | Approved | A course requirement |
| Primary metric EER | Approved | A course requirement |
| High score = Spoof | Approved | The competition format |
| MFCC + Logistic Regression | Approved as Baseline | Simple, explainable, and reproducible |
| CQCC + Logistic Regression | Proposed as additional approach 1 | Testing Feature Representation |
| Frozen wav2vec 2.0 + Logistic Regression | Proposed as additional approach 2 | Testing SSL Representation |
| One-Class SVM on SSL | A preferred additional experiment | Testing the Learning Paradigm |
| WavLM as an alternative Encoder | Conditional | We will examine whether it contributes to the research question |
| AASIST-L | Optional | Higher complexity |
| Deep SVDD | Optional | Only after a simple One-Class experiment |
| VQ-VAE Reconstruction | Not a first priority | Additional complexity and computation |
| Multi-Model Fusion | Not a first priority | Requires proving complementary information |
| Number of Folds | Not yet determined | Depends on the actual number of speakers |
| Systems to be held out of training | Not yet determined | Depends on Metadata and counts |
| The Baseline's EER | Not yet measured | Requires running the experiment |

A "Approved" status refers to a framework already set in the project. A "Proposed" status refers to a research planning decision not yet verified by experiment.

---

# 23. A Minimal Track and an Extension Track

## 23.1 Minimum Viable Research

The minimal research track includes:

**M0:** MFCC + Logistic Regression.

**M1:** CQCC + Logistic Regression.

**M2:** Frozen wav2vec 2.0 + Logistic Regression.

**Evaluation:** Speaker-Disjoint Evaluation, EER by source, error analysis, and generalization by attack or source to the extent the data allows.

This track meets the requirement of two additional approaches beyond the Baseline, and makes it possible to answer RQ1.

## 23.2 Preferred Research Extension

A preferred extension:

**M3:** Frozen wav2vec 2.0 + One-Class SVM.

This way RQ2 can be added and the effect of the learning paradigm examined while keeping the same Encoder.

This is an extension with a relatively high research value relative to its complexity, because it makes it possible to test a new idea from the literature without building a complex deep system from scratch.

## 23.3 Advanced Extensions

If the first experiments are stable and we remain with suitable resources, it will be possible to choose only one extension from among:

- WavLM as an alternative Encoder.
- Deep SVDD.
- AASIST-L.
- Feature Fusion.
- Feature Reconstruction.

The choice will be based on the research question the experiment will be able to answer, and not on the architecture's complexity in itself.

---

# 24. Expected Research Deliverables

At the end of the study we will want to present:

1. A literature review positioning the work relative to classical, deep, and one-class methods.
2. An analysis of the dataset and its methodological risks.
3. A first Baseline with a verified EER.
4. A comparison between at least three approaches under a uniform protocol.
5. A generalization experiment to attacks or sources not included in training.
6. An analysis of the effect of the speech representation on detection performance.
7. An examination of One-Class Learning, if included in the scope of the experiment.
8. An error analysis by source and forgery system.
9. An evaluation of the complexity and resources for the extensions implemented.
10. A research conclusion based on the results, including negative results.
11. Code and documentation allowing reproduction of the experiments.
12. A final model that meets the course's competition protocol.

There is no requirement that all the hypotheses be confirmed. Research success will also be measured by the ability to explain why a particular approach did not improve the results or failed to generalize.

---

# 25. Planning Conclusion

The literature review indicates that voice forgery detection is not only a classification problem, but also a generalization problem under distribution shifts.

The studies examined emphasize the importance of spectral features, deep learning, SSL representations, guided reconstruction, and one-class learning. However, the results reported in the papers are not sufficient to determine in advance which approach will achieve the best performance on the present project's dataset.

Therefore the study will adopt a staged strategy, starting with a simple Baseline and advancing to additional approaches according to defined research questions.

The first comparison will examine the effect of the speech representation by means of MFCC, CQCC, and wav2vec 2.0.

Subsequently, to the extent the resources and data allow, we will examine the effect of the learning paradigm by means of a comparison between Binary Classification and One-Class Learning on the same SSL representation.

At every stage we will place emphasis on preventing Data Leakage, on checking dependence on the data source, on separating training from evaluation, and on full reporting of positive and negative results.

**The central research principle is that a good model is not only a model that shows a low EER, but a model whose performance was measured validly, whose limitations are understood, and for which it can be explained under what conditions it is expected to generalize — and under what conditions it is not.**

This plan is intended to provide a consistent scientific basis for all the stages of the project, while balancing academic quality, experimental complexity, and the available execution resources.

---

# Appendix A — Direct Mapping to the Repository Documents

In accordance with the existing repo structure:

| Folder | Deliverables to be prepared |
|---|---|
| `literature/` | The nine research cards and summaries; Document A |
| `stage1-review/report/` | The Stage 1 Report |
| `stage1-review/notebooks/` | The Data Audit and Baseline Notebook |
| `stage2-design/` | The Stage 2 Design Report from Document B |
| `stage3-results/src/` | Model code, feature extraction, evaluation, and experiments |
| `stage3-results/report/` | The final results report |
| `stage3-results/competition/` | The competition submission file |
| `prompts/` | Prompt documentation in accordance with the guidelines |
| `data/` | Local data only, not uploaded to the repo |

Document B itself is an extended research document. Its final location will be determined according to the documentation structure we want to keep in the repo, without assuming new folders need to be created.

---

# Appendix B — Research Sources

[1] Wang et al. (2024). *ASVspoof 5: Crowdsourced Speech Data, Deepfakes, and Adversarial Attacks at Scale*. arXiv:2408.08739.

[2] Wu, H., Tseng, Y., & Lee, H.-y. (2024). *CodecFake: Enhancing Anti-Spoofing Models Against Deepfake Audios from Codec-Based Speech Synthesis Systems*. Interspeech 2024.

[3] Todisco, M., Delgado, H., & Evans, N. (2017). *Constant Q Cepstral Coefficients: A Spoofing Countermeasure for Automatic Speaker Verification*.

[4] Jung et al. (2022). *AASIST: Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks*. ICASSP 2022.

[5] Baevski et al. (2020). *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations*. NeurIPS.

[6] Chen et al. (2022). *WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing*. IEEE Journal of Selected Topics in Signal Processing.

[7] Wu, S., Cheng, Y., Wang, R., & Yan, D. (2026). *Robust Speech Forgery Detection via Enhanced Forensic Trace Generation*. Signal, Image and Video Processing.

[8] Izrailov, K. E., Kotenko, I. V., & Chechulin, A. A. (2026). *Intelligent Voice Fraud Detection Methods in Authentication Systems*. Pattern Recognition and Image Analysis.

[9] Yin, J., & Lei, S. (2026). *A Novel Attack-Resistant Speech Forgery Detection Method Integrating One-Class Learning and Wav2vec2*. CNML 2026.

**Requirements source:** *Voice Deepfake Detection: Real or Fake?* — course project guidelines, Advanced Topics in Machine Learning, HIT, 2026.

---

**Validity note:** This document was written before the data analysis and the experiments were carried out. It includes proposed planning decisions, hypotheses, and limitations known from the literature and the course requirements. Split definitions dependent on Metadata, EER results, stability metrics, and empirical conclusions will be determined and documented only after the experiments are actually run.
