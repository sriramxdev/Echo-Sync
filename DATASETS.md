# 📊 Sign Language Datasets Registry

> Curated datasets for Indian Sign Language (ISL) continuous translation, kinematic benchmark baselines, and reference corpora.

---

## 🇮🇳 Category A: Continuous Indian Sign Language (ISL)
* **Assigned To:** Shubhanshu Singh
* **Focus:** Continuous ISL sentence-level video/skeletal datasets (e.g., INCLUDE, ISL-CSLR, or regional corpora).

## Continuous Indian Sign Language (ISL) Datasets

| Dataset Name | Source / Repository Link | Format (RGB / Skeletal / 3D) | Size / Vocab Count | Notes |
|---|---|---|---|---|
| **iSign / ISLTranslate** | [Official iSign Website](https://exploration-lab.github.io/iSign/) | RGB Video + Skeletal/Pose | 31K+ ISL-English sentence/phrase pairs | Large-scale continuous ISL dataset for ISL-to-English translation. Supports both video-to-text and pose-to-text tasks. |
| **ISL-CSLTR** | [Mendeley Data](https://data.mendeley.com/datasets/kcmpdxky7p/1) | RGB Video | 700 videos, 100 sentences, 7 signers, 18,863 sentence-level frames, 1,036 word-level images | Sentence-level continuous ISL dataset with annotations, signer variants, and time boundaries. Publicly available under CC BY 4.0. |
| **ISL-FS** | [Official ISL-Fingerspelling Website](https://kirandevraj.github.io/ISL-Fingerspelling/) | RGB Video | 1,308 segments, 499 source videos, 14,814 characters, 3 signers | Continuous ISL fingerspelling dataset with aligned text and temporal annotations. Research use under CC BY-NC 4.0. |

---

## 🌍 Category B: Standard / Global Continuous SLR Benchmarks
* **Assigned To:** Yusuf Mushtaq
* **Focus:** Standard academic benchmark datasets used for baseline comparisons (e.g., PHOENIX-Weather, CSL-Daily, WLASL).

| Dataset Name | Source / Repository Link | Format (RGB / Skeletal / 3D) | Size / Vocab Count | Notes |
| :--- | :--- | :--- | :--- | :--- |
| *Example* | `https://example.com/phoenix` | RGB + Annotations | 1,000+ signs | Baseline comparative metric |

---

## 📖 Category C: Lexicon, Grammatical Rulebooks & Isolated Sign Corpora
* **Assigned To:** Ujjawal Kesarwani
* **Focus:** Official ISL dictionary/lexicon corpora (e.g., ISLRTC official sign bank, isolated signs).

| Dataset Name | Source / Repository Link | Format (RGB / Skeletal / 3D) | Size / Vocab Count | Notes |
| :--- | :--- | :--- | :--- | :--- |
| *Example* | `https://example.com/islrtc` | Video clips / Dictionary | Standard vocabulary | Syntax & rule verification |

---

## ⚙️ Ingestion & Verification Engine
* **Assigned To:** Sri Ram Sharma
* **Module:** `src/pipeline/validator.py` (Validates video decode integrity and executes MediaPipe skeletal sanity tests on incoming dataset samples)

---

## 📌 Submission Rules
1. Every entry **must** contain a working direct link (Kaggle, Zenodo, Hugging Face, GitHub, or institutional repository).
2. **Zero duplicates allowed:** Check existing entries before adding.
3. Submit a minimum of **2–3 unique datasets** in your assigned category via a GitHub Pull Request.