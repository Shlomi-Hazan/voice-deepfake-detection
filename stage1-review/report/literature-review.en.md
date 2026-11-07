# Integrated Literature Review: Voice Deepfake Detection and Generalization to Unseen Attacks

**Project:** Fake or Real: Voice Deepfake Detection  
**Researchers:** Shlomi Hazan & Mayan Adler  
**Course:** Advanced Topics in Machine Learning, HIT  
**Scope of the review:** 12 research papers read and analyzed within the project, 2017–2026  
**Document status:** Revised edition following research critique — Document A | November 7, 2026

---

## Abstract

The development of speech synthesis (Text-to-Speech) technologies, Voice Conversion, and Neural Audio Codecs makes it possible to produce high-quality synthetic voice recordings, which challenge voice authentication systems and forgery detection mechanisms. Although advanced models for voice forgery detection show high performance on known evaluation datasets, the research literature points to a persistent difficulty in generalizing to new forgery methods, to speakers not seen in training, and to different recording conditions. This difficulty raises a central question: to what extent does the model detect signs related to the creation of synthetic speech, and to what extent does its performance depend on the data source and on the conditions observed during training? Error patterns may indicate a possible dependence on the source, but do not by themselves reveal the model's decision mechanism.

This review integratively analyzes twelve core studies dealing with voice forgery detection, speech representation, and generalization between attacks and datasets. The studies are examined along five central directions: pre-computed acoustic features, deep architectures for artifact detection, speech representations based on Self-Supervised Learning, improving representations by means of guided reconstruction, and One-Class Learning. In addition, ASVspoof 5 and CodecFake are examined as evaluation frameworks, MLAAD and PhonemeDF as candidate external sources for data expansion, and AT-ADD as a study on robustness and generalization.

The literature shows that the choice of representation, the classification architecture, and the learning paradigm affect detection performance, but it cannot be assumed that an improvement on a particular dataset will be preserved when moving to a different data source or forgery method. In particular, feature combination, the use of pre-trained models, and learning the distribution of real speech offer promising directions, but each is accompanied by methodological limitations and risks of overfitting or shortcut learning.

Based on these findings, the review proposes examining the effect of the speech representation, the learning paradigm, and the composition of the training data on the ability to generalize to forgeries not seen in training, by means of a controlled comparison of classical models, SSL representations, and one-class classifiers. In addition, a research framework is proposed that distinguishes between increasing the number of training examples and expanding the diversity of forgery systems, and between Leave-One-System-Out experiments and Cross-Dataset Evaluation. The evaluation should distinguish between generalization to new attacks and sensitivity to differences in source, speaker, and recording conditions, while using a consistent data-splitting protocol and appropriate detection metrics.

**Keywords:** Audio Deepfake Detection, Speech Anti-Spoofing, Unseen Attacks, Cross-Dataset Generalization, Speaker Generalization, Channel Robustness, MLAAD, PhonemeDF, AT-ADD, ASVspoof 5, CodecFake, CQCC, AASIST, wav2vec 2.0, WavLM, One-Class Learning, Deep SVDD, EER.

---

## 1. Introduction: The Problem of Voice Forgery Detection

Voice recognition and authentication systems are used in a variety of applications, including remote identity verification, banking systems, voice user interfaces, and biometric security measures. Alongside the advancement of these systems, the ability of technologies to produce synthetic speech resembling human speech has improved significantly. Text-to-Speech (TTS) technologies make it possible to generate speech from text, while Voice Conversion (VC) technologies make it possible to change the features of an existing voice while preserving part of its content. Further developments in the field of Neural Audio Codecs make it possible to encode and reconstruct speech signals by means of representations learned by neural networks, and sometimes also serve as a component in synthetic generation systems. However, processing a signal by means of a neural codec does not by itself indicate that the speech source is synthetic; the authenticity label depends on the task and on the protocol of the dataset.

These capabilities raise a significant security challenge: a synthetic recording can preserve features perceived as authentic and even resemble a particular speaker, without having been created by means of the natural speech of that person. For this reason, two related but non-identical tasks must be distinguished. Speaker Verification examines the match between the recording's voice and the claimed identity of the speaker, whereas Speech Anti-Spoofing examines whether the recording itself is authentic or was created by means of manipulation. The present study focuses on the second task: classifying speech into Bona Fide and Spoof, without the need to decide on the speaker's identity.

One of the central challenges in forgery detection is the generalization gap between training data and evaluation data. A supervised model may learn patterns characterizing particular attacks and achieve low error rates when tested on similar data. However, when the synthesis algorithm, the codec, the recording features, or the speaker population changes, those same patterns may no longer appear. As a result, the model's performance may deteriorate even when the task ostensibly remains the same: distinguishing between real and fake speech.

This problem is at the center of two studies dealing directly with evaluation datasets and modern forgery methods: ASVspoof 5 by Wang et al. (2024) [1] and CodecFake by Wu et al. (2024) [2]. The first emphasizes the diversity in speech conditions and the threat of sophisticated attacks, while the second demonstrates how moving to a different family of generation technologies may expose the limitations of existing detection systems.

Accordingly, the research question is not reduced to identifying the model with the lowest error rate on a given dataset. One must also examine how error patterns vary between attacks and sources, and to what extent the findings are consistent with a dependence on source features or on processing conditions. Causal attribution of the model's decisions to a particular feature requires additional control checks, and cannot be derived directly from an overall EER metric.

---

## 2. Evaluation Datasets, Distribution Shifts, and the Challenge of Unseen Attacks

### 2.1 ASVspoof 5: A Move to Complex Forgery and Recording Conditions

The ASVspoof series of challenges has contributed to the development of the forgery detection field by means of creating datasets, evaluation protocols, and shared reference systems. ASVspoof 5 constitutes a significant advancement relative to previous versions, both in terms of the source of the speech examples and in terms of the attack features included in the dataset (Wang et al., 2024) [1].

The dataset is based on speech data collected from a large number of speakers and under more diverse acoustic conditions than those characterizing earlier datasets. Alongside TTS and VC attacks, it includes mechanisms intended to improve the ability of attacks to deceive authentication and forgery-detection systems, including the use of Surrogate models and Adversarial attacks. In addition, the evaluation data includes various compression and coding conditions, including neural codecs.

The authors distinguish between two evaluation tracks: Track 1 deals with standalone detection of real versus fake speech, and Track 2 deals with Spoofing-Robust Automatic Speaker Verification. This distinction is essential because the two tracks examine different problems, and therefore the metrics and protocols are not identical. In particular, the primary metric of Track 1 in the challenge is minDCF, with EER reported as an additional metric. In the present study, EER was chosen as the central metric in accordance with the requirements of the course project, but this does not make it the primary metric of the original ASVspoof 5 challenge.

The paper emphasizes the importance of separating speakers and attack methods within the training and evaluation splits. In the original protocol, attacks A01–A08 are assigned to the training split, A09–A16 to the development split, and A17–A32 to the evaluation split. This distinction is also relevant to the present study, which uses a subset of attacks A09–A16: the mere use of this subset does not guarantee that the test attacks will be unknown to the model. In order to examine generalization to attacks not seen in training, a dedicated split must be created that keeps certain forgery systems out of training.

The central contribution of ASVspoof 5 to the literature review is not only presenting a more advanced dataset, but sharpening the requirement for an evaluation that reflects the complexity of the real world. Success on examples with known features does not provide evidence of the ability to cope with every future combination of speaker, recording channel, codec, and synthesis system.

### 2.2 CodecFake: Generalization to New Forgery Families

Wu et al. (2024) [2] examine the ability of Anti-Spoofing systems to detect speech created by means of synthesis systems based on Neural Audio Codecs. The researchers point out that detection systems trained on traditional forgery datasets are not necessarily adapted to the artifacts characterizing neural encoding and reconstruction processes.

For the study, the CodecFake dataset was built, based on six families of neural codecs and 15 models in total. A significant methodological aspect is that the forgery examples in the dataset are created by means of a Codec Resynthesis process: encoding existing speech into a discrete representation and reconstructing it by means of the codec's decoder. This process makes it possible to examine the effect of the encoding and reconstruction mechanism itself, without being dependent on all the components of a full TTS system.

The researchers use VCTK data, separating speakers between the training, development, and testing sets. Subsequently, models trained on different CodecFake subsets are examined, and their generalization ability is tested between codec families and relative to recordings created by means of other synthesis systems. The study's findings indicate a significant decline in the performance of systems trained on ASVspoof 2019 LA when they are tested on CodecFake examples. Conversely, training using data including certain Codec reconstructions improves the detection ability for some of the codec-based synthesis systems.

For example, the researchers report an EER of 0.40% in detecting VALL-E examples for a model trained under a particular CodecFake condition. However, this result refers to a defined experimental configuration and does not represent the performance of all CodecFake models or the generalization ability to every Codec-based attack.

One must distinguish between **a Neural Codec as processing or as a signal-transmission channel**, and **Codec Resynthesis as defined in CodecFake as a Spoof condition**. Within CodecFake, the reconstructed examples are labeled as fake in order to examine the ability to detect artifacts stemming from the reconstruction process [2]; in other protocols, such as the coding conditions in ASVspoof 5 [1] and the signal processing in AT-ADD [12], coding can apply to both Real and Fake without changing the label of the speech source. Therefore success on CodecFake does not prove that the model distinguishes well between synthetic speech and legitimate human speech that underwent coding, and the label definition in each Benchmark should be reported separately.

From a research perspective, CodecFake highlights the difference between generalization within a forgery family and generalization between forgery families. A model may successfully detect reconstructions created by means of a known codec, but struggle to detect reconstructions from a system with a different encoding mechanism. It follows that reporting an overall EER is not sufficient; it is necessary to examine how the results change according to the type of forgery system.

### 2.3 A Map of the Generalization Dimensions

The four dimensions relevant to the study are **Unseen Attack Generalization** (generation systems or families not observed in training), **Cross-Dataset Generalization** (moving between datasets), **Speaker Generalization** (new speaker identities), and **Acoustic/Channel Robustness** (changes in processing or recording conditions that are not supposed to change authenticity). They are not equivalent: in one protocol a single dimension may change, and in another several dimensions together. The definitions, limitations, and the protocol matrix are detailed in Section 2.4.

### 2.4 Cross-Domain Benchmarking and Evaluation Validity

The foundational conclusion arising from ASVspoof 5 [1] and CodecFake [2] is that the term *Generalization* should not be treated as a single property of a model. Each experimental protocol determines which factor is held constant and which factor changes, and accordingly which conclusions can be attributed to the results. AT-ADD by Xie and colleagues (2026) [12] deepens this distinction by evaluating attacks not seen in training alongside changing recording conditions, processing, and Replay. Combined with the findings of MLAAD [10] on transitions between datasets, these studies illustrate that different protocols may expose different generalization difficulties, but do not necessarily isolate the cause of the decline in performance.

#### 2.4.1 Unseen Attack Generalization: Generalization to New Generation Systems

In an experiment aimed at *Unseen Attack Generalization*, the evaluation set includes TTS, VC, Vocoder, or Codec systems that were not used in training. For example, in a Leave-One-System-Out (LOSO) design, a particular generation system is removed from the training set and it is tested whether the detector detects examples produced by means of it. A stricter definition may remove an entire architecture family, since the names of different systems do not necessarily indicate independent generation mechanisms. The experiment tests generalization to the system or family left out, *within the other protocol conditions that were defined*. If the same speakers and sources appear in Train and in Test, the result should not be interpreted as proof of generalization also to new speakers or sources.

CodecFake [2] provides an empirical justification for separation between Codec families, while ASVspoof 5 [1] separates attack identifiers according to its original splits. AT-ADD Track 1 [12] extends this by means of 20 generation conditions in Train/Dev versus 27 forgery conditions in Eval, which also include two synthetic-speech Replay conditions. It follows that it is not correct to describe all 27 conditions as independent synthesis systems or to conclude that every change in performance stems from architectural novelty alone.

#### 2.4.2 Cross-Dataset Generalization: Moving between Data Sources

In *Cross-Dataset Generalization*, a model trained on one data source is tested against examples from another source, for example training on ASVspoof 5 and evaluating on CodecFake. Such a transition may change simultaneously the forgery classes, speakers, languages, microphone features, audio duration, and processing procedures. Therefore a higher EER when moving between datasets is evidence of a difficulty in *overall Domain Shift*, but is not exclusive evidence of a failure to detect a new attack. The distinction is also essential when the external dataset includes real and fake examples from different sources.

MLAAD [10] demonstrates that Cross-Dataset performance depends on the training dataset and on the evaluation dataset; there is no single training dataset that dominated all the comparison scenarios examined. CodecFake [2] adds evidence that moving to examples created in neural codecs may expose transfer failures from systems trained on other forgery datasets. Both findings reinforce the need to report the training source and the evaluation source, but do not by themselves isolate the effect of changing the generation system from the effect of changes in speakers and recording conditions.

#### 2.4.3 Speaker Generalization: Separation between Speaker Identities

*Speaker Generalization* examines whether a detector identifies authenticity for speakers who did not appear in training. For this purpose the speaker must be identified and the data split at the Speaker ID level, and not only at the file level. When source recordings and synthetic versions derived from them exist, preserving source groups is also required in order to prevent almost identical content or source signal from passing between splits. Speaker separation does not replace separation between forgery systems, and vice versa.

AT-ADD [12] reports a planned speaker separation but documents 18 Common Voice identities overlapping between chosen sets. It follows that the dataset is not fully Speaker-Disjoint. Also in PhonemeDF [11], where parallel synthetic versions are derived from the same LibriSpeech recordings, evaluation validity requires keeping the families of source recordings in the same split. The two examples illustrate that one should not conclude from the title *Cross-Domain* or *Unseen Attack* that full separation between speakers and sources was guaranteed; each condition must be verified by means of metadata and the splitting protocol.

#### 2.4.4 Acoustic and Channel Robustness: Robustness to Signal and Channel Changes

*Acoustic and Channel Robustness* refers to preserving performance after changes that are not supposed to change the authenticity label: compression, filtering, Resampling, noise, reverberation, changing the recording or playback device, or playback and re-recording. This definition differs from detecting Replay as an attack in its own right in certain biometric tasks. In AT-ADD Track 1 [12], for example, human speech that was re-recorded remains Real and TTS speech that was re-recorded remains Fake. In this way the protocol emphasizes a distinction between the speech source and the channel the signal passed through.

In order to evaluate robustness as cleanly as possible, it is advisable to apply the same signal change to the same recordings — or to matched sets — in both authenticity classes. When a certain change is more common in one class, the model may learn a shortcut through the processing features. AT-ADD provides evidence for the difficulties of BigVGAN and Replay and also for the wrong identification of Real from the 3D-Speaker source in some of the systems, but does not isolate in a uniform experiment the effect of each channel condition.

#### 2.4.5 The Protocol Matrix: What Claim Can the Study Support?

| Protocol | What is held out of training | What can be claimed | What cannot be claimed without further checking |
|---|---|---|---|
| Within-Dataset Speaker-Disjoint | Speakers and source groups | Generalization to new speakers within the dataset | Generalization to a new attack or dataset |
| Leave-One-System-Out | A forgery system / a system family | Generalization to the system that was excluded | Generalization to new sources and channels if they overlap |
| Cross-Dataset Held-Out | An entire dataset | Ability to transfer to a different data source | Identifying the causal factor for the decline in performance |
| Controlled Channel Perturbation | A defined processing condition | Robustness to the signal change tested | Robustness to all forms of Replay or to every device |
| Joint Cross-Domain | Speakers, systems, and sources together | Generalization under combined distribution shift | Separating the contribution of each dimension to the error |

This distinction sharpens the need to separate two questions: *Does the model fail when the domain changes?* versus *Which factor in the new domain is responsible for the failure?* The first question is examined by means of an external Benchmark; the second requires suitable controls or Ablation experiments. Accordingly, in the present project Leave-One-System-Out and Cross-Dataset are not substitutes but complementary experiments with different interpretive boundaries.

### 2.5 MLAAD and PhonemeDF: Expanding Data versus Expanding Diversity

Alongside improving the architecture, another possible path for coping with generalization gaps is changing the composition of the training data. MLAAD [10] and PhonemeDF [11] offer two resources that differ in the diversity of speech and the diversity of generation systems. In both, the mere availability of many synthesis files does not prove that adding them will improve generalization; one must distinguish between the number of examples, the number of systems, the identity of the speech sources, and the speaker composition.

#### 2.5.1 MLAAD: A Wide Variety of TTS Systems and Languages

Müller and colleagues [10] present MLAAD, a multilingual synthetic-speech dataset based on texts and source recordings related to M-AILABS. In version v11 described in the paper, about 1,153.6 hours of synthetic speech from 205 TTS models in 54 languages are included. The dataset includes metadata such as language, model architecture, generation-system name, transcript, and a link to the source file; information on the reference speaker is documented starting from later versions. This scope makes it a candidate for increasing synthesis diversity, although it distributes synthetic Fake files only, and the Real examples must be matched from a licensed source such as M-AILABS; it focuses mainly on TTS and does not structurally provide the same VC coverage as PhonemeDF.

The work was originally published at IJCNN 2024, while the dataset-scope figures of v11 refer to the 2026 arXiv update. A critical limitation for interpreting the results is that the Cross-Dataset experiments reported in the paper were carried out on **MLAAD v1**, and were not automatically repeated on all the later versions of the dataset. The authors report that MLAAD and ASVspoof 2019 complement each other, with each leading in four of the eight evaluation settings; this is not empirical proof that version v11 will necessarily achieve better performance, or that increasing the quantity is by itself the cause of the improvement. Likewise, since the dataset was built on the basis of M-AILABS — a source that appears as Real only also in the course data — there is a practical need to check the overlap of source files, texts, and speakers before integrating it into training.

#### 2.5.2 PhonemeDF: Source Matching and Phonetic Analysis

Nallaguntla and colleagues [11] present PhonemeDF, a parallel dataset based on 28,539 real speech recordings from LibriSpeech and on 199,773 synthetic versions created in four TTS systems and three VC systems. The data is accompanied by phoneme boundaries computed by means of the Montreal Forced Aligner and by TextGrid files. This design makes it possible to compare acoustic features of matching phonetic units and to examine whether artifacts appear non-uniformly throughout the speech.

In an analysis on a subset of 1,000 source recordings, the researchers use LFCC, LogSpec, wav2vec 2.0, and WavLM, together with KLD, LR/SVM classifiers, and Pearson correlations. They find notable differences between phonemes, synthesis systems, and representations. However, the relationship between the size of KLD and Accuracy is not consistent between Handcrafted Features and SSL representations, and may even be negative. Therefore the paper does not prove that a high KLD entails an EER improvement at the recording level or that PhonemeDF necessarily improves generalization to systems not seen in training.

For the present study, the dataset has a possible dual role: expanding training by means of additional TTS and VC systems, and phonetic error analysis as an advanced stage. Since each source recording gives rise to many synthetic versions, *the entire family of recordings derived from the same source* must be kept within the same split. Otherwise, classification may be aided by content or source signals that crossed between Train and Test. Licensing, Speaker Metadata, and sources should also be verified before practical use.

#### 2.5.3 Why Are "More Data" and "More Diversity" Different Hypotheses?

Adding 10,000 synthetic recordings from the same TTS system may increase the number of training examples without broadening the coverage of forgery mechanisms. In contrast, adding 10,000 recordings divided among several TTS and VC systems may also increase diversity. If the two interventions are compared without controlling the number of examples, there is no way to know whether the improvement stems from the training volume, from the diversity of generation systems, from the speech sources, or from a combination of them.

Therefore the conceptual recommendation is to distinguish between a **Size-Controlled Comparison** — changing the amount of data while keeping a similar composition — and a **Diversity-Controlled Comparison** — keeping the same number of examples while changing the number of generation systems or their families. In both cases, a consistent speaker and source split, class balancing, an equal processing policy, and a model-selection process that does not use Test must be maintained. These are *proposed research implications based on the sources*, and not experiments that the papers jointly proved.

### 2.6 Synthesis: An External Benchmark Is Not a Substitute for a Causal Experiment

The body of ASVspoof 5 [1], CodecFake [2], MLAAD [10], PhonemeDF [11], and AT-ADD [12] supports building a research plan on two levels: (a) **controlled experiments**, which isolate as much as possible the roles of the representation, the training volume, and the diversity of attacks; (b) **external-validity experiments**, which evaluate how the model performs under combined changes in the data source. Reporting separately on the two types of experiments prevents the error whereby a good result on an external test by itself reveals which component caused the improvement, or a good result in a LOSO experiment proves general robustness to every channel and dataset change.

---

## 3. Classical Acoustic Features: Between Computational Efficiency and Sensitivity to Attacks

### 3.1 Acoustic Representation as a Means for Artifact Detection

Early approaches to voice forgery detection relied largely on extracting pre-computed acoustic features (Handcrafted Features), such as MFCC, LFCC, and CQCC, and subsequently on using statistical classifiers such as Gaussian Mixture Models.

The underlying assumption of these approaches is that synthesis and voice-conversion processes may leave spectral or temporal signs in the speech signal that distinguish it from natural speech. An appropriate choice of acoustic representation may highlight these signs even when they are not noticeable in ordinary listening.

The advantage of classical features is that they are defined by means of a known computational process, which can be reproduced and analyzed. They can serve as a basis for relatively simple models, and are therefore especially suited to Baseline experiments whose purpose is to examine in a controlled manner the contribution of the feature-extraction stages and of the classifiers.

However, features defined by means of a fixed formula limit the types of information preserved in the representation. In a situation where a forgery mechanism succeeds in well imitating certain features of real speech, a classifier based on those same features may fail to notice the manipulation.

### 3.2 CQCC and the Importance of Spectral Resolution

Todisco, Delgado and Evans (2017) [3] propose using Constant Q Cepstral Coefficients (CQCC) for detecting attacks against speaker verification systems. The method combines a Constant-Q Transform with Cepstral processing, with the aim of preserving spectral information suited to detecting artifacts created in forgery attacks.

Unlike analysis based on a linear frequency division, the Constant-Q Transform uses a logarithmic division of the frequency domain, which makes it possible to achieve higher frequency resolution at low frequencies and higher temporal resolution at high frequencies. These features may provide sensitivity to patterns that are not preserved in the same way in other acoustic representations.

The authors examine CQCC on three datasets including different forgery scenarios: ASVspoof 2015, AVspoof, and RedDots Replayed. Beyond demonstrating the effectiveness of the representation, the study presents an important insight regarding generalization: CQCC configurations suited to a particular dataset or type of attack are not necessarily the configurations best suited to a different dataset.

Therefore the contribution of CQCC to the present study is not only in proposing an additional acoustic feature, but in illustrating the importance of choosing a representation according to the nature of the attacks and the evaluation conditions. The fact that a particular feature achieves good performance in a defined scenario does not guarantee that it will be robust against a distribution shift.

### 3.3 Feature Fusion and Combining Statistical and Neural Models

An additional direction is presented by Izrailov, Kotenko and Chechulin (2026) [8], who propose a system for voice forgery detection in a biometric authentication environment by means of combining MFCC, Perceptual Linear Prediction (PLP), GMM–UBM, and a CNN network.

The logic of the method is that different acoustic features may describe complementary aspects of the speech signal. While MFCC is based on an analysis of the spectral envelope on the Mel scale, PLP combines assumptions related to auditory perception and Linear Predictive Coding. The combination is intended to allow detection of patterns that may not be well represented by means of a single type of feature.

GMM–UBM is used for statistical modeling of the feature distribution, while the CNN is intended to learn relations within the combined representation. On ASVspoof 2019 LA, the researchers report an EER of 4.79% for the hybrid approach, compared with 6.27% for CQCC+GMM and 7.44% for LFCC+GMM. In an additional experiment on TED-LIUM data, an EER of about 5.1% was reported, under more limited evaluation conditions.

These results indicate potential for improvement by means of combining features and classification approaches. However, the paper does not include Ablation experiments that fully isolate the contribution of MFCC, PLP, GMM–UBM, and the CNN. It follows that it cannot be concluded that adding PLP alone is the cause of the improvement, or that a complex CNN is necessarily better than a simple classifier in the same feature space.

In addition, the paper proposes a decision-making framework with four categories, combining speaker verification with different levels of suspicion of forgery, while the central results table does not present a separate evaluation of all four categories. Therefore one must distinguish between the description of the proposed system and the scope of the experimental evidence supporting it.

### 3.4 An Integrative Conclusion: Choosing a Representation before Increasing Complexity

The findings of CQCC and the hybrid approach offer two complementary directions. The first emphasizes the importance of acoustic features with different properties, and the second proposes combining features and models in order to exploit complementary information.

However, neither direction proves that increasing the number of features or the complexity of the system necessarily leads to an improvement. Combining features may also increase the dimension of the data, add duplicate information, or increase sensitivity to irrelevant features.

In the context of a limited training dataset, there is a research justification to start with simple models with a small number of features, and to examine in a controlled manner whether the addition of information actually improves performance and generalization.

---

## 4. End-to-End Deep Learning: Detecting Spectral and Temporal Relations

Beyond the approaches based on pre-computed features, many studies propose deep networks that themselves learn representations relevant to forgery detection from the speech signal.

One of the central approaches in this direction is AASIST — Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks, presented by Jung et al. (2022) [4].

### 4.1 The AASIST Architecture

AASIST uses an Encoder based on RawNet2 for extracting representations from the speech, and subsequently graph mechanisms describing relations in the time domain and the frequency domain.

The model's central novelty is the use of a Heterogeneous Stacking Graph Attention Layer (HS-GAL), which makes it possible to learn relations between different temporal and spectral representations. In this way the model is not limited to examining each domain separately, but can learn relations between artifacts appearing at different positions along the recording and in different frequency domains.

In addition, the model includes a Max Graph Operation (MGO), which combines two processing branches by means of a Maximum operation, and a Readout mechanism using, among other things, a Stack Node for pooling information relevant to classification.

The research assumption is that different forgeries may leave signs in different regions of the signal, and therefore an Attention mechanism capable of focusing on diverse relations may be more effective than a simple global representation.

### 4.2 Results and the Contribution of the Components

On ASVspoof 2019 LA, the authors report an EER of 0.83% and a min t-DCF of 0.0275 for AASIST's best result. It is important to note that these results are of the best run, while the averages reported across three Seeds are an EER of 1.13% and a min t-DCF of 0.0347.

The researchers also present a lightweight version, AASIST-L, including about 85 thousand parameters and achieving an EER of 0.99% in the best run. This finding demonstrates that competitive performance can be achieved by means of a relatively compact architecture, although a small number of parameters is not necessarily equivalent to low computational cost in every hardware environment.

In Ablation experiments it was found that removing the HS-GAL, MGO, or Readout mechanism components has a negative effect on performance, with the Heterogeneous Attention mechanism showing the most significant contribution among the components examined.

### 4.3 Generalization Limitations of a Dedicated Architecture

Despite its achievements, the central evaluation in the AASIST paper is carried out on ASVspoof 2019 LA. These results alone do not indicate an ability to detect more recent attacks, and in particular forgeries based on Neural Audio Codecs.

In this context, the CodecFake findings [2] are especially significant: they indicate that models with strong performance on the ASVspoof 2019 LA dataset may show a considerable decline when they are tested on forgeries from a different Codec family.

Combining the two studies teaches that an architecture capable of learning complex spectral and temporal relations is not necessarily immune to a shift in the distribution of attacks. The quality of the artifact representation is an important factor, but the diversity and features of the training data may also determine which artifacts the model learns to detect.

Therefore, AASIST serves in this review as an example of a dedicated deep architecture with high discriminative abilities, but not as proof of unlimited generalization ability.

---

## 5. Self-Supervised Learning: Pre-Trained Speech Representations as an Alternative to Training from Scratch

An additional approach for coping with data limitations is the use of speech models that underwent Pre-training on large amounts of unlabeled audio.

Unlike models that train all the representation components directly on the forgery dataset, Self-Supervised Learning (SSL) makes it possible to learn general speech features, and subsequently to use the learned representations for additional tasks.

### 5.1 wav2vec 2.0: Learning Representations by Means of a Contrastive Task

Baevski et al. (2020) [5] present wav2vec 2.0, an architecture for learning speech representations from the Raw Waveform.

The model combines a Convolutional Feature Encoder, a Transformer Context Network, and a Quantization mechanism used at the self-training stage. During Pre-training, segments of the continuous representation are masked, and the model is required to identify the corresponding discrete representation by means of Contrastive Learning, distinguishing between the correct representation and negative examples.

This mode of training allows the model to learn representations describing temporal and contextual relations in speech, without needing a transcription for every recording during Pre-training.

The authors demonstrate the method's effectiveness mainly in Automatic Speech Recognition (ASR) tasks, including situations where there is a limited amount of labeled data. However, the central metrics in the paper, such as Word Error Rate (WER), are not metrics for voice forgery detection.

Therefore the contribution of wav2vec 2.0 to the present study is in presenting an efficient mechanism for learning pre-trained speech representations, and not in direct proof that these representations detect forgeries better than other acoustic features.

### 5.2 WavLM: Extending Speech Representations to Diverse Tasks

Chen et al. (2022) [6] present WavLM, an SSL model intended to produce representations suited to a wide range of speech processing tasks, and not only for detecting the verbal content.

The model combines Masked Speech Prediction with Denoising during Pre-training, and uses a Gated Relative Position Bias for modeling temporal relations. The WavLM Large version was trained on about 94 thousand hours of audio from different sources.

One of the central aspects of the study is the distinction between the types of information present in speech representations. While ASR tasks focus mainly on the content spoken, other tasks require information about the speaker's identity, intonation, acoustic environment, or relations between speakers.

The authors demonstrate the model's effectiveness in a variety of tasks within SUPERB and additional evaluation datasets, including Speaker Verification, Speaker Diarization, and Speech Separation.

However, the EER results appearing in the paper for Speaker Verification refer to verifying the speaker's identity, and not to classifying real versus fake speech. They should not be interpreted as Deepfake Detection metrics.

### 5.3 The Relevance of SSL Representations to Forgery Detection

Both studies offer the possibility of using knowledge learned from extensive speech data for a task with a relatively small labeled dataset.

From an applied perspective, wav2vec 2.0 and WavLM can be used as frozen Encoders, Embeddings can be extracted from them, and the representations can be passed to a simple classifier. This approach makes it possible to examine the quality of the representation without retraining the millions of parameters of the original model.

However, there is a tension between learning general representations and preserving the subtle signs required for forgery detection. A representation well suited to detecting speech content or identifying a speaker does not necessarily preserve the same spectral artifacts that indicate artificial synthesis.

Furthermore, different layers of an SSL model may preserve different types of information. Therefore the choice of Layer, the Pooling method, and the manner of adapting the classifier may affect detection performance.

It follows that using a Pre-trained Encoder is a reasonable research hypothesis, but not a guaranteed solution to the generalization problem. Its contribution should be examined empirically, under a protocol identical to that of the comparison methods.

In addition, **the source of the Pre-training data is part of the validity protocol**. Since SSL models may be trained on broad corpora, the exact Checkpoint version and the known sources of the pre-training should be documented, and possible overlaps with the evaluation recordings and their source files should be checked. Prior exposure to unlabeled audio is not necessarily equivalent to leakage of Test labels during supervised training, but it may reduce the degree of independence of the evaluation; in the absence of sufficient information, the uncertainty should be reported, and the complete absence of overlap should not be claimed.

---

## 6. Improving Representations by Means of Guided Reconstruction and Highlighting Forensic Traces

The studies reviewed so far focus mainly on the choice of speech representation or on the classification architecture. In contrast, Wu et al. (2026) [7], in the paper *Robust Speech Forgery Detection via Enhanced Forensic Trace Generation*, propose improving the information passed to the classifier by means of a guided reconstruction process.

### 6.1 The Central Idea: Reconstruction as a Way to Highlight Discriminative Information

The researchers use a Vector-Quantized Variational Autoencoder (VQ-VAE) for reconstructing spectral features, and subsequently combine the reconstructed representation with the original representation.

The goal of the process is not only to faithfully reconstruct the speech signal, but to improve the classifier's ability to distinguish between real and fake speech. Accordingly, the generative model is trained by means of supervisory signals coming from the Encoder of a pre-trained forgery classifier whose parameters remain frozen at the reconstruction-guidance stage.

The researchers propose several Loss components that guide the reconstruction process. True Speech Consistency Loss is intended to preserve the closeness between representations of real speech and their reconstructions, while Dual-Margin Triplet Loss also uses fake examples to increase the distinction between real and fake speech in the feature space.

An important point is that the approach is not One-Class Learning in its full sense. Although the reconstruction is directed at real speech, forgery examples serve as a supervisory signal during training, and therefore the method also relies on explicit information regarding the fake class.

### 6.2 Results and Generalization Ability

The study was examined on ASVspoof 2019 LA and on ASVspoof 2021 LA, by means of different acoustic features and a classifier based on ResNet.

For Log-Power Spectrum (LPS), the system based on the original features achieved an EER of 1.22% on ASVspoof 2019 LA and 22.64% on ASVspoof 2021 LA. After combining the original features with the guided reconstruction, EERs of 1.02% and 14.04% were obtained, respectively.

That is, the improvement on ASVspoof 2021 LA was more significant than the improvement on the 2019 dataset, and demonstrated potential for improving performance under a shift in evaluation conditions.

However, the improvement was not uniform across all representations. For example, for CQCC a certain worsening in EER was obtained on ASVspoof 2019 LA after adding the reconstruction process, alongside an improvement on ASVspoof 2021 LA. This finding reinforces the need to evaluate the improvement process according to the representation and the dataset, rather than assuming that Feature Reconstruction is beneficial in every situation.

In addition, the method adds computational cost relative to the original classifier. The researchers report an increase from a system including about 2.34 million parameters and about 1.25 billion MACs to a system including about 5.67 million parameters and about 3.12 billion MACs. Accordingly, the improvement in EER comes with an increase in the system's complexity.

### 6.3 Research Significance

The study demonstrates that an improvement in detection ability does not have to stem from replacing the entire classifier. One can also change the representation passed to the classifier, with the aim of highlighting information related to forgery.

However, it should not be concluded that the process will work to the same degree on the CodecFake or ASVspoof 5 datasets, which were not directly tested in the paper. In addition, since the method relies on generative components and additional loss functions, the ratio between its contribution to performance and the cost and complexity it adds must be examined.

In the context of the present study, this method provides a possible direction for future extension, but does not require implementation at the initial stage of the study.

---

## 7. One-Class Learning: Modeling Real Speech Instead of Learning Known Attacks

The approaches discussed so far mainly use supervised learning of the difference between real and fake speech, or highlighting features by means of examples from both classes. A different approach is proposed by Yin and Lei (2026) [9], in the paper *A Novel Attack-Resistant Speech Forgery Detection Method Integrating One-Class Learning and Wav2vec2*.

### 7.1 A Change in the Learning Paradigm

The authors argue that one of the factors harming generalization is dependence on labeled forgery examples, which represent only part of the possible technologies. In order to cope with this limitation, they propose learning the distribution of authentic speech alone, and defining examples deviating from it as suspicious.

The method is based on Deep Support Vector Data Description (Deep SVDD), within which a neural network maps real examples to a representation space and learns a compact region around them. The region is represented by means of a Hypersphere, and the distance from its center serves as the basis for the anomaly score of a new recording.

The possible advantage of this approach is that the model is not required to learn the unique features of every forgery technology. Instead, it examines whether the recording matches the distribution of real speech learned in training.

### 7.2 Combining Deep SVDD with wav2vec 2.0

The proposed system uses wav2vec 2.0 Base representations and LFCC features. Sub-networks including Bi-LSTM and LCNN components produce representations used for learning the Deep SVDD boundaries.

In addition, the researchers propose a Weighted Fusion mechanism combining the scores of four sub-networks. The combination weights are chosen by means of Optuna, with the aim of reducing EER on the Validation set.

In this way, the study combines two different ideas: using pre-trained speech representations, and changing the classification paradigm from binary learning to anomaly learning.

### 7.3 Results on Known and Unknown Attacks

The authors report an EER of 2.13% on ASVspoof 2019 LA and of 6.89% on ASVspoof 2021 DF.

For comparison, a wav2vec 2.0 model with a supervised binary classifier achieved an EER of 2.35% on ASVspoof 2019 LA and of 18.45% on ASVspoof 2021 DF.

The results indicate a notable advantage of the combined system on the ASVspoof 2021 DF evaluation set, in accordance with the reported protocol.

However, one must distinguish between this result and general proof of the superiority of One-Class Learning. The proposed method differs from the binary classifier not only in the learning paradigm; it also includes several sub-networks, a combination of scores, and a different representation method. Therefore the entire improvement cannot be attributed to Deep SVDD alone.

In addition, the transition between ASVspoof 2019 LA and ASVspoof 2021 DF includes a change in the dataset and the evaluation conditions, and not only a replacement of the attack type. Accordingly, the finding constitutes a certain piece of evidence for the ability to cope with different evaluation data, but does not fully isolate generalization to new attacks.

### 7.4 Methodological Limitations of the Method

The paper presents the method as one that does not require labeled forgery examples. However, alongside training Deep SVDD on real speech, the authors describe using EER for Early Stopping and for choosing the Fusion weights by means of Optuna.

Since computing EER in a forgery-detection task requires labeled examples from both classes, the description does not fully establish the claim that the complete system is not at all dependent on forgery examples. One must distinguish between training the anomaly classifier itself and the model and hyperparameter-selection process.

Likewise, in the paper's Ablation table there are inconsistencies between the configuration names and the values and verbal explanations. These inconsistencies limit the possibility of precisely attributing the improvement to each component.

### 7.5 A Deviation from the Distribution Is Not Necessarily a Forgery

The most important fundamental limitation of One-Class Learning stems from the distinction between detecting a deviation and detecting a forgery.

A real recording may be a deviation from the data on which the model was trained due to differences in speaker, language, microphone, background noise, or data source. In such a case the model may identify authentic speech as a forgery.

Conversely, an especially high-quality forgery may produce a representation similar enough to the real-speech distribution, and therefore not be detected as a deviation.

It follows that the success of One-Class Learning depends not only on the quality of the decision boundary, but also on how representative the real-speech examples are and on how the feature space distinguishes between natural changes and forgery artifacts.

Therefore this method requires a dedicated evaluation of the rate of wrongly rejecting real speech, especially when the recordings come from different sources.

---

## 8. A Comparative Synthesis of the Research Directions

The studies reviewed represent different approaches to forgery detection and to coping with the generalization problem. The differences between them are not reduced to architecture or number of parameters, but relate to the question of what information is considered relevant to forgery and how the model learns to use it.

### 8.1 A Map of the Studies

| Study | Central contribution | Evidence of generalization | Significant limitation |
|---|---|---|---|
| ASVspoof 5 [1] | A dataset and protocol including diverse attacks and conditions | Attack, speaker, and channel splits | Does not prove the generalization of a particular model |
| CodecFake [2] | A forgery dataset based on Neural Codecs | Cross-Codec and Cross-Dataset | Performance depends on the Codec family and the training configuration |
| CQCC [3] | A spectral representation with variable resolution | Evaluation on several datasets | Sensitivity of the representation to the attack type and evaluation conditions |
| AASIST [4] | Deep learning of spectral and temporal relations | Strong performance on ASVspoof 2019 LA | Generalization to new Codec attacks is not guaranteed |
| wav2vec 2.0 [5] | Speech representations by means of SSL | Generalization to ASR tasks with few labels | No direct proof of forgery detection in the original paper |
| WavLM [6] | SSL for a variety of speech tasks | Performance on various speech tasks | Speaker Verification metrics are not Spoof EER |
| Enhanced Forensic Trace [7] | Guided spectral reconstruction for highlighting artifacts | Improvement on ASVspoof 2021 LA | Added complexity and an improvement that is not uniform between features |
| Intelligent Voice Fraud [8] | Combining MFCC, PLP, GMM–UBM, and CNN | Additional evaluation on TED-LIUM | Absence of Ablation and full implementation detail |
| One-Class + wav2vec 2.0 [9] | Modeling real speech by means of Deep SVDD | Improved performance on ASVspoof 2021 DF | Sensitivity to Domain Shift and ambiguity in the tuning protocol |
| MLAAD [10] | Expanding TTS systems and languages in training | Cross-Dataset experiments on v1 | v11 performance should not be inferred from v1 evaluations; overlaps with M-AILABS require checking |
| PhonemeDF [11] | A parallel TTS/VC dataset with phoneme labeling | Analysis of phonetic separation between Real and Fake | No direct evidence of an EER improvement or generalization to Unseen Generators |
| AT-ADD [12] | A robustness and generalization protocol under changing recording conditions | Generator Shift, Replay, channel, and error analysis | Combined domain changes; access to Track 1 data not verified |

The table is used for a conceptual and methodological comparison between the studies. It does not constitute a numerical performance ranking, since the papers were examined on different datasets, tasks, and protocols.

### 8.2 Empirical Evidence Anchors and Interpretive Boundaries

The following table presents **internal comparisons only**: the numbers are intended to anchor particular claims in the original studies, not to rank all models across different datasets and metrics.

| Study | Reported empirical comparison | What can be concluded — and what cannot |
|---|---|---|
| CodecFake [2] | For the VALL-E example an EER of 0.40% is reported under training on a particular CodecFake subset; training on a traditional dataset harms performance in the scenarios examined | The composition of training examples is relevant to transfer between Codec families; the value should not be generalized to all methods |
| AASIST [4] | A mean EER of 1.13% across three runs on ASVspoof 2019 LA; best run 0.83% | Strong performance on a defined dataset; no automatic proof of generalization between datasets |
| Enhanced Forensic Trace [7] | In the LPS representation, a move from 22.64% to 14.04% EER on ASVspoof 2021 LA | Guided reconstruction may help under the conditions tested; there is no uniform improvement in all representations |
| One-Class + wav2vec 2.0 [9] | 6.89% versus 18.45% EER for a binary comparison system on ASVspoof 2021 DF | The combined system has an advantage in the reported experiment; it cannot be attributed to Deep SVDD alone |
| MLAAD [10] | In Cross-Dataset tests on v1, MLAAD and ASVspoof 2019 each lead in four of eight evaluation configurations | Complementary training datasets; no controlled proof of improvement due to the move to v11 was carried out |
| PhonemeDF [11] | Differences in KLD and Accuracy between phonemes and representations, including negative correlations in some SSL representations | There is phonetic variance in the discriminative signals; there is no direct evidence of an EER improvement at the recording level |
| AT-ADD Track 1 [12] | 76.73% Macro-F1 for the leading official Baseline versus 90.71% for the winning system; BigVGAN and Replay are relatively difficult | The winners' complete system has superior performance in this protocol; there is no causal isolation of each component or ability to compare numerically with EER |

These findings reinforce the conclusion that a system's success depends on the composition of the data, the representation, the training process, and the manner of evaluation. However, **no row is a joint experiment for all twelve studies**; the inference boundaries of each source are preserved separately.

### 8.3 Six Integrative Insights

**First, the choice of representation affects the ability to detect forgeries.** CQCC demonstrates the importance of spectral structure, AASIST learns temporal and spectral relations, and SSL provides pre-trained speech representations. However, none of the representations alone guarantees robustness to every type of attack.

**Second, an improvement in discriminative ability is not necessarily equivalent to an improvement in generalization.** A model may achieve a low EER on a known dataset, but show a significant decline when the forgery-generation mechanism changes. The CodecFake findings demonstrate this problem directly.

**Third, there are different ways to reduce dependence on known forgery examples.** Using SSL representations seeks to exploit knowledge learned from a broad scope of speech, guided reconstruction seeks to highlight discriminative information, and One-Class Learning seeks to define the real-speech region instead of learning all forms of forgery.

**Fourth, the usefulness of added complexity is not guaranteed.** Feature Fusion, VQ-VAE, and Multi-Model Fusion may improve performance, but also increase computational cost, sensitivity to tuning, and the risk of overfitting. In order to determine their value, their contribution must be examined by means of controlled experiments, and not relied upon only on the basis of the overall performance of a complex system.

**Fifth, training diversity is an experimental variable separate from training volume.** MLAAD [10] and PhonemeDF [11] offer an opportunity to expand the forgery sources, but do not prove that increasing the quantity of files by itself explains an improvement in generalization. The addition of quantity and the addition of TTS/VC families should be examined separately, while controlling for the source and the number of examples.

**Sixth, evaluation validity depends on the exact definition of the change.** AT-ADD [12] and CodecFake [2] offer strict protocols that take into account Generator, Speaker, Dataset, and Channel changes. However, performance under combined Shift does not identify the source of the failure without an additional controlled experiment.

### 8.4 The Tension between a Rich Representation and a Robust Representation

One of the insights arising from the synthesis is that there is a possible tension between enriching the speech representation and reducing its sensitivity to variance unrelated to forgery.

A rich representation may preserve more details, including subtle artifacts created in synthesis processes. However, it may also preserve information about the speaker, language, recording channel, or dataset source. If the model relies on this information, an improvement in performance on the training data does not guarantee generalization ability.

On the other hand, a representation whose purpose is to learn general and environment-robust features may suppress some of the acoustic details required for distinguishing between natural and fake speech.

An additional finding from PhonemeDF [11] is that discriminative ability varies between phonemes: signs of forgery do not have to be distributed uniformly in time. This gives rise to **an additional but non-binding research hypothesis**: Temporal Mean Pooling of Embeddings at the recording level may dilute local artifacts, while Aggregation that preserves information of certain segments may preserve them. The paper does not prove an advantage of a different Pooling method for the course data, and therefore this is a possibility for future analysis or Ablation, and not a proven conclusion.

The balance between the two directions is not unambiguously resolved in the literature reviewed. It requires an empirical evaluation that examines not only the quality of the classification but also the type of information on which the model's decisions are based.

---

## 9. Evaluation Metrics and Methodological Validity

### 9.1 Equal Error Rate

EER is a central metric in Speech Anti-Spoofing studies. It is obtained at the threshold point at which the rate of fake examples wrongly accepted and the rate of real examples wrongly rejected are equal.

A lower EER value indicates a better ability to distinguish between the classes within the given evaluation set.

The advantage of the metric is that it is based on the model's scores and on examining different thresholds, and not on Accuracy at a single decision threshold. However, EER alone does not provide full information about the costs of errors in a particular application or about the quality of score calibration.

For the purpose of the present study, a uniform score convention is required: a higher Score value should indicate a higher likelihood of forgery. In models where a higher score represents real speech, the score direction must be reversed before computing EER.

### 9.2 Cost Metrics and Differences between Protocols

Alongside EER, the literature uses metrics such as minDCF, actDCF, and min t-DCF. These metrics are intended to take into account decision costs, assumptions about class frequencies, or the interaction between the Anti-Spoofing mechanism and the Speaker Verification system.

It is important to emphasize that minDCF and min t-DCF values are not necessarily comparable between studies using different cost-function definitions and different evaluation protocols.

Similarly, EER numbers reported for ASVspoof 2019 LA, ASVspoof 2021 LA, ASVspoof 2021 DF, or CodecFake datasets do not allow a direct ranking between models as long as they were not examined on the same data and under the same protocol.

### 9.3 Evaluation by Attack Type and Data Source

An overall EER may hide significant differences between attacks. A particular model may detect one type of forgery well and struggle greatly with another type, with the overall average hiding the gap.

Therefore, to the extent the data allows, further analysis by type of forgery system and by data source is required.

Computing EER for a particular forgery system requires including alongside it a suitable set of real examples. EER cannot be computed from a set containing only fake examples or only real examples.

In particular, **M-AILABS in the course subset contains only Real**, and therefore an independent EER cannot be computed for it. One can measure Real Recall, the rate of wrongful rejection at a threshold chosen in advance on Validation, and the distribution of authenticity scores, in addition to the number of recordings. Similarly, if a Generator is examined in which only Fake examples appear, Fake Recall should be computed or a suitable Real set should be explicitly defined in order to compute EER.

When the number of examples is small, even a computed EER may be sensitive to a small number of wrong decisions. Therefore the size of the evaluation sets must be reported, and one must be cautious about drawing strong conclusions from results based on few recordings.

### 9.4 Data Leakage, Protocol Mismatch, and Pre-Training Overlaps

Two different failures must be distinguished. **Data Leakage** occurs when prohibited information passes from the evaluation processes to training or tuning: the same source recording and a derived version of it appear in different splits; windows from the same file are scattered between Train and Test; Threshold adjustment or Checkpoint selection is carried out based on Test; or information from the evaluation labels reaches the model in another way. When one source produces many synthetic versions (as in PhonemeDF), the splitting unit must take the source family into account.

By contrast, **Protocol Mismatch** occurs when the split itself is valid but the result is presented as evidence for a claim that was not tested. For example, using the same TTS system in training and testing may be entirely valid for a *Known-Generator / Within-Distribution* experiment if the files are independent and there are no prohibited overlaps. It does not prove generalization to a TTS system not seen. Similarly, Speaker-Disjoint does not guarantee Generator-Disjoint. Therefore the Shift dimension each experiment examines must be defined in advance.

An additional type of partial non-independence may exist between the **Pre-training data of a pre-trained Encoder** and the evaluation recordings. The Checkpoint, the known Pre-training sources, and the Provenance of the Test recordings should be documented, as far as possible. Exposure to unlabeled audio in earlier training is not necessarily leakage of test labels, but it limits strong claims about data never seen by the system. The inability to verify overlap will be noted as a research limitation.

### 9.5 Feasibility and Validity of the Generalization Protocols

The theoretical distinction between **Leave-One-System-Out**, **Speaker-Disjoint**, and **Cross-Dataset** is detailed in Section 2.4. In practice, the validity of each experiment depends on the availability of system, speaker, and source-file identifiers, the number of examples in each subset, the representation of both classes, and the absence of derivatives crossing splits. The full term *Leave-One-System-Out* is preferable here to the abbreviation LOSO, which might also be interpreted as Leave-One-Speaker-Out.

One should not assume in advance that the course data allows a strict test of all types of generalization. An EDA and Metadata check is a precondition for approving feasibility; when there are not enough examples or valid source identifiers, the scope of the claim should be reduced and the protocol should not be presented as if it were fully implemented.

### 9.6 Metrics, Thresholds, and Error Analysis at Different Levels

AT-ADD Track 1 [12] uses Macro-F1, while the research question in the course project is focused on EER. The metrics are complementary but not equivalent: EER is computed from a threshold sweep over continuous scores, while Macro-F1 reflects decisions at a particular threshold and also depends on the class composition. Therefore the model scores should be saved, a Threshold chosen only on Validation, and Real/Fake Recall reported separately. In the case of a single forgery system without a matching Real, Fake Recall can be computed, but not a valid EER for that subset without defining a Real comparison set.

AT-ADD's error analysis found difficult conditions such as BigVGAN and Replay, and high rates of wrongful rejection of Real speech from certain sources. It also showed that complementary error patterns do not guarantee that Majority Voting will improve the best model. Accordingly, a valid research comparison should combine overall EER with reporting by dataset and forgery system, a check of Real/Fake errors, and uncertainty metrics or confidence intervals when the number of evaluation examples allows it. For clips with a shared speaker or source, it is advisable to consider a group-based Bootstrap and not to assume full independence between all the files.

### 9.7 Validity of Results in Data-Expansion Experiments

One should ask whether the observed improvement reflects **more examples**, **more forgery systems**, **more speakers**, **more languages**, or **a change in the source/quality of the recordings**. For this reason, one should not naively compare training on a small base dataset to training on a large external dataset and attribute the difference specifically to Generator diversity. The correct experiment for separating the explanations includes, as far as possible, size-matched training conditions, class balancing, non-leaking speakers/sources, consistent Augmentation, and several repeated runs. The detailed design will appear in Document B; here the research logic and the principle of isolating variables are emphasized.

---

## 10. Connection to the Present Study: The Dataset and the Unique Challenges

### 10.1 The Composition of the Project's Data

The present study is based on a dataset including 1,520 four-second voice recordings, at a sampling rate of 16kHz and in a mono channel, in accordance with the course specification.

The data comes from three sources:

| Source | Real speech | Fake speech | Total |
|---|---:|---:|---:|
| ASVspoof 5 | 300 | 300 | 600 |
| CodecFake | 300 | 300 | 600 |
| M-AILABS | 320 | 0 | 320 |
| **Total** | **920** | **600** | **1,520** |

ASVspoof 5 includes, in the subset chosen, TTS and VC examples from systems A09–A16. CodecFake includes speech that underwent encoding and reconstruction processes by means of neural codecs, while M-AILABS contains only real speech, originating from audiobook recordings.

It follows that the project's dataset includes not only two classes, but also fundamental differences between the data sources.

### 10.2 The Risk of Shortcut Learning

A central methodological aspect stems from the fact that the M-AILABS source is represented by means of real examples only.

As a result, the model may learn that features identified with M-AILABS indicate real speech, instead of learning general features of authenticity. Similarly, it may learn to identify patterns related to the ASVspoof 5 or CodecFake source and not to the forgery mechanism itself.

This problem is sometimes called Shortcut Learning: the model achieves a good fit to the data by means of available statistical associations, but these associations do not necessarily reflect the mechanism one seeks to detect.

A further example is the use of recording features, such as loudness level, background noise, silence duration, bandwidth, or artifacts related to coding. Some of these features may be related to the recording source and not to the fact of it being fake.

Therefore, success on a particular split of the course data will not by itself be sufficient to prove that the model learned forgery features with generalization ability. A suitable principled analysis would examine the score distribution for Real recordings by source, Fake Recall by forgery system, and the sensitivity of the predictions to silence, loudness, and bandwidth when matched controls can be carried out. Such checks may reveal problematic dependence, but do not by themselves prove which internal feature the model uses for its decision.

### 10.3 The Challenge of One-Class Learning in This Data

The structure of the dataset creates an opportunity to examine the one-class learning idea presented by Yin and Lei (2026) [9], but also illustrates its limitation.

In principle, one can train an anomaly classifier on real speech examples alone. However, if the training examples do not well represent the variety of sources, the model may reject real speech from a new source.

For example, a model trained on real recordings from ASVspoof 5 may struggle to accept real speech from M-AILABS, not due to forgery but due to differences in speakers, speaking style, and recording conditions.

Therefore, a positive result of One-Class Learning will need to be interpreted alongside a dedicated analysis of the real-speech examples, and not only according to the overall EER.

### 10.4 The Significance of the Dataset-Size Limitation

A dataset of 1,520 recordings is relatively small compared with the amounts of data on which large SSL models were trained. This fact does not preclude the use of deep learning, but it reinforces the importance of choosing the training strategy.

Training a large model from scratch may be sensitive to overfitting and to variance between data splits. In contrast, using a pre-trained Encoder and a simple classifier makes it possible to exploit representations learned from a large amount of speech data, without needing to retrain all the components of the model.

However, even frozen representations can preserve information related to the data source, and therefore do not automatically solve the Shortcut Learning problem.

The decision on the model's complexity should, therefore, be based on empirical comparison and on examining the stability of the performance, and not only on the number of parameters or on the architecture's success in a different study.

### 10.5 The Competition Test versus Generalization Experiments

According to the course requirements document, the final competition set will be sampled from the same three data sources. However, this does not guarantee that all the attack types in the test set will be new relative to training.

For this reason, two evaluation goals must be distinguished:

**Competition performance:** the ability to classify recordings not used for training, from the data sources defined in the course.

**Research generalization ability:** the ability to detect attacks, systems, or conditions not included in training, in a controlled manner.

Both goals are important, but they do not fully overlap. A model can achieve a good result in the competition and still struggle with a new attack, and vice versa.

It follows that there is a need to examine the generalization question in a dedicated experiment, even when the competition evaluation does not isolate this variable.

### 10.6 External Datasets as Training Candidates: Decisions and Reservations

The new review adds two candidate training datasets, but does not turn their full scope into a binding usage plan. **MLAAD [10]** may expand the number of TTS systems and the diversity of languages. The public distribution page notes a **CC BY-NC 4.0** license for non-commercial academic use; before practical integration, one must also check the terms of use of the source data, the dataset version, the source files, and the possible overlap with M-AILABS, which is used by the course. **PhonemeDF [11]** may add TTS and VC examples from a parallel setup; verification is required that use of the synthetic audio files is permitted, and that the separation between splits is maintained at the source and speaker level and not only at the file level.

**AT-ADD [12]** is classified here as *Research Paper 10*, and not as an applicable external training source: its evaluation protocol is important, but there is no verified access for us to the Track 1 dataset and its terms of use are not verified for the project's purposes. This classification decision preserves the distinction between a dataset we are considering actually integrating and a paper used for building a valid evaluation protocol.

### 10.7 Feasibility Boundaries and Course Deliverables

The guidelines document requires a Baseline with EER, a comparison of additional approaches, analysis by forgery system, and a discussion of generalization between datasets; the final competition set is expected to be sampled from the same three sources and undergo similar processing. Accordingly, the official evaluation examines performance on new examples from defined sources, while strict Shift experiments require dedicated splits that will be approved only after an EDA of speakers, systems, and sources. One cannot assume in advance the feasibility of full Leave-One-System-Out, Speaker-Disjoint, and Cross-Dataset on the limited subset. Document A provides a scientific justification, and Document B will detail the applicable experiment plan in accordance with the findings of the data audit.

---

## 11. The Research Gap Emerging from the Literature

Despite progress in acoustic features, dedicated architectures, and SSL representations, it is sometimes difficult to separate the effect of the **speech representation**, the **learning paradigm**, and the **composition of the training data** on the generalization ability. Studies report improvements in full configurations tested on different datasets, but differences in data, classifier, tuning, and evaluation conditions limit attributing an improvement to a single component [2], [4], [7], [9], [12].

At the same time, moving between datasets may change together the generation method, the source speakers, the language, and the recording conditions. Therefore an external performance metric makes it possible to identify **that a generalization problem exists**, but does not by itself show **why it occurs**. Error analysis by source or Generator provides diagnostic signals, while a causal explanation requires suitable controls. The difficulty is especially prominent in the course data, where M-AILABS provides Real examples only, and the separation of systems and speakers in the subset requires a Metadata check.

Expanding data by means of MLAAD [10] and PhonemeDF [11] raises a complementary question: does a possible improvement stem from more examples, from a diversity of generation systems, or from a change in the speech source? The literature chosen justifies the check, but does not resolve this distinction under our project's conditions. Moreover, some of the generalization results in MLAAD refer to an early version and not to the scope of v11, and PhonemeDF mainly analyzes the phoneme level and does not prove an EER improvement at the recording level.

**Our specific research gap** is therefore the need for a controlled comparison and documented evaluation of speech representations and learning methods under distribution shifts that can be defined and verified on a limited course dataset, and for examining the contribution of training-data diversity when the data allows suitable control. There is no claim here that such comparisons were never carried out; this is a justification for a focused empirical study on the task, the limitations, and the splits of the present project.

## 12. Deriving the Research Question and Prioritization

From the synthesis a central research question is derived:

**How do the choice of speech representation, the learning paradigm, and the composition of the training data affect the generalization ability of voice forgery detectors to systems and conditions not seen in training, within evaluation protocols that can be verified?**

For focus, the study is organized along three axes with a clear order of priority, and not as six independent tasks that must all be carried out in full:

**RQ1 — Representation (a core axis):** How do detection and generalization performance vary between classical features (for example MFCC/CQCC) and SSL representations (wav2vec 2.0/WavLM), when the classifier, the data split, and the comparison conditions are controlled as far as possible?

**RQ2 — Learning Paradigm (a core axis):** How does supervised binary classification compare to One-Class Learning on Real speech, when a parallel representation and evaluation protocol are used? The comparison will explicitly report whether Fake labels were used for Validation, Early Stopping, or calibration, so as not to present a system calibrated by means of Fake as fully independent of this class.

**RQ3 — Training Data Diversity (an axis conditional on feasibility):** Given a similar number of training recordings, does exposure to a larger number of TTS/VC systems or families improve generalization to systems not seen in training, beyond the effect of the number of examples? Testing this question depends on access and licensing, on verifying the source of the recordings, and on the ability to create sufficient splits without overlaps.

**A cross-cutting evaluation layer — not an independent research question:** For each axis, evaluation sets and reporting methods will be defined in advance as far as feasible: overall EER, Real/Fake metrics at a threshold chosen on Validation, analysis by Dataset and Generator, as well as Speaker-Disjoint, Leave-One-System-Out, or Cross-Dataset when the identifiers and the number of examples allow it. For M-AILABS (Real only) we will examine rates of wrongful acceptance/rejection and not an independent EER. Performance gaps between domains will not be interpreted as proof of the causal source of the failure.

**Possible extensions, not a commitment to the core of the study:** Feature Fusion, Pooling methods focused on local artifacts, Score Consistency, broader Fine-Tuning, Ensemble, and measuring computational cost. They will be considered according to resources, EDA findings, and their contribution to the core questions.

This framework preserves all the ideas that arose from the papers, but distinguishes between hypotheses for which binding experiments should be planned and possible directions that are not a condition for completing the project.

## 13. Conclusions of the Literature Review

The twelve studies reviewed demonstrate that voice forgery detection relies on a combination of the audio representation, the learning method, the composition of the training data, and the evaluation protocol. CQCC, AASIST, and SSL representations emphasize different levels of acoustic information, but none of the approaches guarantees generalization to every generation system or recording condition. Guided reconstruction, feature combination, and one-class learning offer alternatives, but their advantage depends on the experimental conditions and on being accompanied by suitable controls.

ASVspoof 5, CodecFake, and AT-ADD place evaluation validity at the center: success on known systems, on a Generator not included in training, when moving between datasets, or after a channel change are different claims. Differences between domains may expose weakness, but do not necessarily isolate its cause. Separate Real/Fake analysis, preserving continuous scores, thresholds chosen only on Validation, and reporting the limitations of the splits are conditions for a cautious interpretation of the findings.

MLAAD and PhonemeDF add the possibility of expanding the training diversity, but require control over dataset size, source associations, speakers, licensing, and overlaps. PhonemeDF even raises the possibility that local phonetic information is absorbed in global pooling, but this is a continuation hypothesis and not a proven result in the project's recording-level model. For the course data, in which M-AILABS is represented as Real only, explicit attention to Shortcut Learning and to the limitations of the metrics that can be computed by source is required.

Accordingly, a controlled comparison is proposed between acoustic representations and SSL representations and between binary classification and one-class learning, with a feasibility-conditional examination of the quantity of training data versus the diversity of attacks. **The purpose of the study is not only to reduce EER, but to determine under what conditions the improvement is preserved, what can be concluded from it, and what remains uncertain.** Document B will describe the design of the experiments and controls that will implement this research logic.

## Bibliographic Sources

**[1]** Wang, X., Delgado, H., Tak, H., Jung, J., Shim, H., Todisco, M., et al. (2024). *ASVspoof 5: Crowdsourced Speech Data, Deepfakes, and Adversarial Attacks at Scale*. arXiv:2408.08739. https://arxiv.org/abs/2408.08739

**[2]** Wu, H., Tseng, Y., & Lee, H.-y. (2024). *CodecFake: Enhancing Anti-Spoofing Models Against Deepfake Audios from Codec-Based Speech Synthesis Systems*. Interspeech 2024. https://arxiv.org/abs/2406.07237

**[3]** Todisco, M., Delgado, H., & Evans, N. (2017). *Constant Q cepstral coefficients: A spoofing countermeasure for automatic speaker verification*. Computer Speech & Language, 45, 516–535. https://doi.org/10.1016/j.csl.2017.01.001

**[4]** Jung, J.-w., Heo, H.-S., Tak, H., Shim, H.-j., Chung, J. S., Lee, B.-J., Yu, H.-J., & Evans, N. (2022). *AASIST: Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks*. ICASSP 2022. https://doi.org/10.1109/ICASSP43922.2022.9747766

**[5]** Baevski, A., Zhou, H., Mohamed, A., & Auli, M. (2020). *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations*. Advances in Neural Information Processing Systems. https://arxiv.org/abs/2006.11477

**[6]** Chen, S., Wang, C., Chen, Z., Wu, Y., Liu, S., et al. (2022). *WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing*. IEEE Journal of Selected Topics in Signal Processing, 16(6), 1505–1518. https://doi.org/10.1109/JSTSP.2022.3188113

**[7]** Wu, S., Cheng, Y., Wang, R., & Yan, D. (2026). *Robust Speech Forgery Detection via Enhanced Forensic Trace Generation*. Signal, Image and Video Processing, 20, Article 130. https://doi.org/10.1007/s11760-026-05167-y

**[8]** Izrailov, K. E., Kotenko, I. V., & Chechulin, A. A. (2026). *Intelligent Voice Fraud Detection Methods in Authentication Systems*. Pattern Recognition and Image Analysis, 36(2), 391–399. https://doi.org/10.1134/S1054661826700203

**[9]** Yin, J., & Lei, S. (2026). *A Novel Attack-Resistant Speech Forgery Detection Method Integrating One-Class Learning and Wav2vec2*. 2026 International Conference on Communication Networks and Machine Learning (CNML), 415–419. IEEE. https://doi.org/10.1109/CNML68938.2026.11452384

**[10]** Müller, N. M., Kawa, P., Choong, W. H., Casanova, E., Gölge, E., Müller, T., Syga, P., Sperl, P., & Böttinger, K. (2024). *MLAAD: The Multi-Language Audio Anti-Spoofing Dataset*. 2024 International Joint Conference on Neural Networks (IJCNN), 1–7. https://doi.org/10.1109/IJCNN60899.2024.10650962. **The updated dataset scope in the review is taken from the arXiv v11 version (2026)**: https://arxiv.org/abs/2401.09512

**[11]** Nallaguntla, V., Fursule, A., Kshirsagar, S., & Avila, A. R. (2026). *PhonemeDF: A Synthetic Speech Dataset for Audio Deepfake Detection and Naturalness Evaluation*. Proceedings of LREC 2026, 5905–5915. https://aclanthology.org/2026.lrec-1.469/

**[12]** Xie, Y., Cheng, H., Zhou, J., et al. (2026). *AT-ADD: A Benchmark and Challenge for Robust and All-Type Audio Deepfake Detection*. arXiv:2608.23437v2 (15 October 2026). The paper describes the ACM Multimedia 2026 Grand Challenge; this is not a determination that publication of the paper itself in the conference proceedings has been verified. https://arxiv.org/abs/2608.23437

### Source for the Task Definition and Research Data

The course guidelines document, *Voice Deepfake Detection: Real or Fake?*, Advanced Topics in Machine Learning, HIT, October 2026. This source is used to describe the dataset, the project requirements, and the required evaluation protocol; it is not counted as a research paper in the literature review.

---

**Note on the scope of the review:** This is an integrative review document based on the twelve papers we read and analyzed, chosen for their relevance to the research question. It is not an exhaustive systematic review of all publications in the field. The numerical results presented in the document are results reported in the original studies, and not results of an experiment conducted within the course project. The research questions and their implications for the present dataset are our own research synthesis and interpretation, and not conclusions jointly verified by the papers' authors.
