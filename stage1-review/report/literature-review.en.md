# Integrated Literature Review: Voice Deepfake Detection and Generalization to Unseen Attacks

**סקירת ספרות אינטגרטיבית: זיהוי זיופים קוליים והכללה למתקפות לא מוכרות**

**Project:** Fake or Real: Voice Deepfake Detection
**Researchers:** Shlomi Hazan & Mayan Adler
**Course:** Advanced Topics in Machine Learning, HIT
**Scope of the review:** Nine research papers, 2017–2026
**Document status:** Foundational research document for the literature review and for formulating the research question

---

## Abstract

The development of speech synthesis (Text-to-Speech) technologies, Voice Conversion, and Neural Audio Codecs makes it possible to produce high-quality synthetic voice recordings, which challenge voice authentication systems and forgery detection mechanisms. Although advanced models for voice forgery detection show high performance on known evaluation datasets, the research literature points to a persistent difficulty in generalizing to new forgery methods, to speakers not seen in training, and to different recording conditions. This difficulty raises a central question: does a model learn features that are essential to forgery, or does it rely on patterns that depend on the generation technology and the data source on which it was trained?

This review integratively analyzes nine studies dealing with voice forgery detection, speech representation, and generalization between attacks and datasets. The studies are examined along five central directions: pre-computed acoustic features, deep architectures for artifact detection, speech representations based on Self-Supervised Learning, improving representations by means of guided reconstruction, and One-Class Learning. In addition, the ASVspoof 5 and CodecFake datasets are examined as evaluation frameworks that emphasize the variance between attacks and the limitations of generalization.

The literature shows that the choice of representation, the classification architecture, and the learning paradigm affect detection performance, but it cannot be assumed that an improvement on a particular dataset will be preserved when moving to a different data source or forgery method. In particular, feature combination, the use of pre-trained models, and learning the distribution of real speech offer promising directions, but each is accompanied by methodological limitations and risks of overfitting or shortcut learning.

Based on these findings, the review proposes examining the effect of speech representation and learning paradigm on the ability to generalize to forgeries not seen in training, by means of a controlled comparison of classical models, SSL representations, and one-class classifiers. The evaluation should distinguish between generalization to new attacks and sensitivity to differences in source, speaker, and recording conditions, while using a consistent data-splitting protocol and appropriate detection metrics.

**Keywords:** Audio Deepfake Detection, Speech Anti-Spoofing, Generalization, Unseen Attacks, ASVspoof 5, CodecFake, CQCC, AASIST, wav2vec 2.0, WavLM, One-Class Learning, Deep SVDD, EER.

---

## 1. Introduction: The Problem of Voice Forgery Detection

Voice recognition and authentication systems are used in a variety of applications, including remote identity verification, banking systems, voice user interfaces, and biometric security measures. Alongside the advancement of these systems, the ability of technologies to produce synthetic speech resembling human speech has improved significantly. Text-to-Speech (TTS) technologies make it possible to generate speech from text, while Voice Conversion (VC) technologies make it possible to change the features of an existing voice while preserving part of its content. Further developments in the field of Neural Audio Codecs make it possible to encode, reconstruct, and generate speech signals by means of discrete representations learned by neural networks.

These capabilities raise a significant security challenge: a synthetic recording can preserve features perceived as authentic and even resemble a particular speaker, without having been created by means of the natural speech of that person. For this reason, two related but non-identical tasks must be distinguished. Speaker Verification examines the match between the recording's voice and the claimed identity of the speaker, whereas Speech Anti-Spoofing examines whether the recording itself is authentic or was created by means of manipulation. The present study focuses on the second task: classifying speech into Bona Fide and Spoof, without the need to decide on the speaker's identity.

One of the central challenges in forgery detection is the generalization gap between training data and evaluation data. A supervised model may learn patterns characterizing particular attacks and achieve low error rates when tested on similar data. However, when the synthesis algorithm, the codec, the recording features, or the speaker population changes, those same patterns may no longer appear. As a result, the model's performance may deteriorate even when the task ostensibly remains the same: distinguishing between real and fake speech.

This problem is at the center of two studies dealing directly with evaluation datasets and modern forgery methods: ASVspoof 5 by Wang et al. (2024) [1] and CodecFake by Wu et al. (2024) [2]. The first emphasizes the diversity in speech conditions and the threat of sophisticated attacks, while the second demonstrates how moving to a different family of generation technologies may expose the limitations of existing detection systems.

Accordingly, the research question is not reduced to identifying the model with the lowest error rate on a given dataset. One must also examine the nature of the information the model exploits, the degree of its dependence on known forgery examples, and its ability to distinguish between signs essential to forgery and differences unrelated to the recording's authenticity.

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

From a research perspective, CodecFake highlights the difference between generalization within a forgery family and generalization between forgery families. A model may successfully detect reconstructions created by means of a known codec, but struggle to detect reconstructions from a system with a different encoding mechanism. It follows that reporting an overall EER is not sufficient; it is necessary to examine how the results change according to the type of forgery system.

### 2.3 Three Different Aspects of Generalization

Combining the findings of ASVspoof 5 and CodecFake makes it possible to distinguish between three types of distribution shifts:

**Attack Generalization:** the model's ability to detect TTS, VC, or forgery systems not included in training.

**Cross-Dataset Generalization:** the ability to maintain performance when the data source changes, including speaker features, content, and recording conditions.

**Channel and Codec Robustness:** the ability to distinguish between forgery features and changes created due to compression, bandwidth changes, or signal processing.

The three aspects are related to each other, but are not equivalent. When a model shows a decline in performance when moving from one dataset to another, this cannot be automatically attributed only to new attacks. Part of the decline may stem from source differences not directly related to forgery.

This distinction forms a central basis for formulating a valid evaluation protocol in the present study.

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
| Intelligent Voice Fraud [8] | Combining MFCC, PLP, GMM–UBM, and CNN | Additional evaluation on TED-LIUM | Absence of full Ablation and implementation detail |
| One-Class + wav2vec 2.0 [9] | Modeling real speech by means of Deep SVDD | Improved performance on ASVspoof 2021 DF | Sensitivity to Domain Shift and ambiguity in the tuning protocol |

The table is used for a conceptual and methodological comparison between the studies. It does not constitute a numerical performance ranking, since the papers were examined on different datasets, tasks, and protocols.

### 8.2 Four Shared Insights

**First, the choice of representation affects the ability to detect forgeries.** CQCC demonstrates the importance of spectral structure, AASIST learns temporal and spectral relations, and SSL provides pre-trained speech representations. However, none of the representations alone guarantees robustness to every type of attack.

**Second, an improvement in discriminative ability is not necessarily equivalent to an improvement in generalization.** A model may achieve a low EER on a known dataset, but show a significant decline when the forgery-generation mechanism changes. The CodecFake findings demonstrate this problem directly.

**Third, there are different ways to reduce dependence on known forgery examples.** Using SSL representations seeks to exploit knowledge learned from a broad scope of speech, guided reconstruction seeks to highlight discriminative information, and One-Class Learning seeks to define the real-speech region instead of learning all forms of forgery.

**Fourth, the usefulness of added complexity is not guaranteed.** Feature Fusion, VQ-VAE, and Multi-Model Fusion may improve performance, but also increase computational cost, sensitivity to tuning, and the risk of overfitting. In order to determine their value, their contribution must be examined by means of controlled experiments, and not relied upon only on the basis of the overall performance of a complex system.

### 8.3 The Tension between a Rich Representation and a Robust Representation

One of the insights arising from the synthesis is that there is a possible tension between enriching the speech representation and reducing its sensitivity to variance unrelated to forgery.

A rich representation may preserve more details, including subtle artifacts created in synthesis processes. However, it may also preserve information about the speaker, language, recording channel, or dataset source. If the model relies on this information, an improvement in performance on the training data does not guarantee generalization ability.

On the other hand, a representation whose purpose is to learn general and environment-robust features may suppress some of the acoustic details required for distinguishing between natural and fake speech.

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

When the number of examples is small, even a computed EER may be sensitive to a small number of wrong decisions. Therefore the size of the evaluation sets must be reported, and one must be cautious about drawing strong conclusions from results based on few recordings.

### 9.4 Preventing Data Leakage

The validity of the evaluation also depends on how the data is split.

If recordings of the same speaker appear both in training and in evaluation, the model may exploit speaker features instead of learning patterns related to forgery. Similarly, if examples related to the same generation system or the same content appear in both sets, the result may be optimistic relative to true generalization.

For this reason, a random split of recordings without regard to speakers and forgery systems is not sufficient for testing generalization ability.

Strict adherence to an appropriate data split, to separation between training and tuning, and to preventing the use of test data for model selection is a fundamental condition for a valid interpretation of the results.

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

Therefore, success on a particular split of the course data will not by itself be sufficient to prove that the model learned forgery features with generalization ability.

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

---

## 11. The Research Gap Emerging from the Literature

The studies reviewed provide evidence for the importance of acoustic representations, deep architectures, pre-trained models, and anomaly-detection methods. However, a significant practical question remains regarding the relationship between the quality of the speech representation, the learning paradigm, and the generalization ability.

The literature points to several limitations that are not resolved uniformly:

**First gap — distinguishing between detecting known attacks and generalizing to new attacks.** High results on a known dataset do not guarantee similar performance when moving to a different forgery family, as emerges from the CodecFake study and from generalization analyses in other studies.

**Second gap — the difficulty of isolating the contribution of the representation from the classifier.** Certain studies present an improvement stemming from a system including several new components, without an experiment that allows unambiguously identifying the contribution of each component.

**Third gap — dependence on the data source.** When different datasets also differ in speakers, recording conditions, and class frequencies, it is difficult to determine whether the model learned forgery features or source features.

**Fourth gap — evaluating One-Class Learning.** One-class learning offers the possibility of detecting attacks without direct training on forgery examples, but may be sensitive to natural variance in speech. In addition, one must distinguish between training without forgery labels and model selection relying on such labels.

**Fifth gap — the relationship between complexity and generalization ability.** Methods including Reconstruction, Feature Fusion, or multiple sub-networks may improve performance, but it is necessary to check whether the advantage is preserved under a fair protocol and whether it justifies the additional resources.

Based on these gaps, the present study does not seek to assume in advance that a particular architecture is the best. Its purpose is to examine, within the course dataset, which features and learning strategies show more stable performance when the recording source or the forgery-generation method changes.

It is important to emphasize that the gap described is an **empirical and practical gap relative to the research question and the current data protocol**. It should not be concluded from the nine papers that comparisons between all these approaches have never been made in the broader literature.

---

## 12. Deriving the Research Question

From the synthesis arises a need to examine separately two central components of a forgery-detection system: the speech representation on which it is based and the learning paradigm it uses.

The choice of speech representation may affect the type of artifacts the model is able to detect. The learning paradigm may affect the degree of its dependence on known forgery examples and the way it copes with anomalies.

Accordingly, the following central research question is proposed:

**To what extent do the choice of speech representation and the learning paradigm affect the ability of a voice forgery detection system to generalize to attacks and data sources not included in training, under a controlled evaluation protocol?**

From this question, several sub-questions are derived:

**RQ1 — Speech representation:** How do classical acoustic features, such as MFCC and CQCC, differ from pre-trained SSL representations, such as wav2vec 2.0 and WavLM, in terms of detection and generalization performance?

**RQ2 — Learning paradigm:** Does a one-class classifier based on real speech alone show an advantage over a supervised binary classifier in detecting attacks not included in training?

**RQ3 — Sensitivity to the data source:** How do error rates change when moving between ASVspoof 5, CodecFake, and M-AILABS, and to what extent may the changes indicate dependence on source features instead of forgery features?

**RQ4 — Complexity versus benefit:** Do extensions such as Feature Fusion or learning complex anomaly representations improve performance in a stable manner that justifies their additional cost?

These questions do not predetermine the study's results. They provide a conceptual framework from which measurable hypotheses and an experimental protocol can be derived at the research-planning stage.

---

## 13. Conclusions of the Literature Review

The integrative review of the nine studies points to significant progress in methods for voice forgery detection, but also to a central limitation that has persisted across different approaches: high detection performance under known evaluation conditions does not guarantee generalization ability to new conditions.

Classical acoustic features provide a simple and analyzable reference point, but their effectiveness may vary according to the attack's features. Deep architectures such as AASIST make it possible to learn complex relations between temporal and spectral regions, but their ability to cope with new forgery families also depends on the training data.

Self-Supervised Learning models, including wav2vec 2.0 and WavLM, offer the use of pre-trained speech representations, which may be especially useful when the scope of labeled data is limited. However, success in other speech tasks is not direct evidence of robustness in forgery detection.

Methods based on guided reconstruction or Feature Fusion propose enriching the representation and improving discriminative ability, but require examining the contribution of the components and the additional computational cost. At the same time, One-Class Learning proposes reducing dependence on known forgery examples, but requires coping with the fact that a deviation from the real-speech distribution is not necessarily a result of forgery.

From the studies it emerges, then, that there is no single solution proven to be superior across every dataset, forgery family, and recording condition. This conclusion reinforces the need for a controlled comparison, in which the models' performance is examined on the same data splits, with separation between speakers and forgery systems and error analysis according to the data source.

In the context of the present study, the significance is that the aspiration is not only to achieve the lowest possible EER, but to understand **which features allow a model to detect forgery, under what conditions this ability is preserved, and when it is harmed as a result of a change in the data distribution**.

From this arises a justification for starting with simple and interpretable models, comparing them to SSL representations, and subsequently examining one-class learning approaches, while maintaining methodological consistency and full reporting of positive and negative results.

The literature review thus provides the theoretical basis for the experiment-planning stage, in which the hypotheses, splitting methods, evaluation metrics, and comparison criteria will be defined in a manner that allows examining the generalization question and not only the classification performance on a single dataset.

---

## Bibliographic Sources

**[1]** Wang, X., Delgado, H., Tak, H., Jung, J., Shim, H., Todisco, M., et al. (2024). *ASVspoof 5: Crowdsourced Speech Data, Deepfakes, and Adversarial Attacks at Scale*. arXiv:2408.08739. https://arxiv.org/abs/2408.08739

**[2]** Wu, H., Tseng, Y., & Lee, H.-y. (2024). *CodecFake: Enhancing Anti-Spoofing Models Against Deepfake Audios from Codec-Based Speech Synthesis Systems*. Interspeech 2024. https://arxiv.org/abs/2406.07237

**[3]** Todisco, M., Delgado, H., & Evans, N. (2017). *Constant Q Cepstral Coefficients: A Spoofing Countermeasure for Automatic Speaker Verification*. https://www.eurecom.fr/en/publication/5146

**[4]** Jung, J.-w., Heo, H.-S., Tak, H., Shim, H.-j., Chung, J. S., Lee, B.-J., Yu, H.-J., & Evans, N. (2022). *AASIST: Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks*. ICASSP 2022. https://doi.org/10.1109/ICASSP43922.2022.9747766

**[5]** Baevski, A., Zhou, H., Mohamed, A., & Auli, M. (2020). *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations*. Advances in Neural Information Processing Systems. https://arxiv.org/abs/2006.11477

**[6]** Chen, S., Wang, C., Chen, Z., Wu, Y., Liu, S., et al. (2022). *WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing*. IEEE Journal of Selected Topics in Signal Processing. https://arxiv.org/abs/2110.13900

**[7]** Wu, S., Cheng, Y., Wang, R., & Yan, D. (2026). *Robust Speech Forgery Detection via Enhanced Forensic Trace Generation*. Signal, Image and Video Processing, 20, Article 130. https://doi.org/10.1007/s11760-026-05167-y

**[8]** Izrailov, K. E., Kotenko, I. V., & Chechulin, A. A. (2026). *Intelligent Voice Fraud Detection Methods in Authentication Systems*. Pattern Recognition and Image Analysis, 36(2), 391–399. https://doi.org/10.1134/S1054661826700203

**[9]** Yin, J., & Lei, S. (2026). *A Novel Attack-Resistant Speech Forgery Detection Method Integrating One-Class Learning and Wav2vec2*. 2026 International Conference on Communication Networks and Machine Learning (CNML), 415–419. IEEE. https://doi.org/10.1109/CNML68938.2026.11452384

### Source for the Task Definition and Research Data

The course requirements document, *Voice Deepfake Detection: Real or Fake?*, Advanced Topics in Machine Learning, HIT, October 2026. This source is used to describe the dataset, the project requirements, and the required evaluation protocol; it is not included as a tenth research paper in the literature review.

---

**Note on the scope of the review:** This is an integrative review document based on nine sources chosen for their relevance to the research question. It is not an exhaustive systematic review of all publications in the field. The numerical results presented in the document are results reported in the original studies, and not results of an experiment conducted within the course project. The research questions and their implications for the present dataset are our own research synthesis and interpretation, and not conclusions jointly verified by the papers' authors.
