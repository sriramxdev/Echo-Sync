# 📊 Sign Language Datasets Registry

> Curated datasets for Indian Sign Language (ISL) continuous translation, kinematic benchmark baselines, and reference corpora.

---

## 🇮🇳 Category A: Continuous Indian Sign Language (ISL)
* **Assigned To:** Shubhanshu Singh
* **Focus:** Continuous ISL sentence-level video/skeletal datasets (e.g., INCLUDE, ISL-CSLR, or regional corpora).

| Dataset Name | Source / Repository Link | Format (RGB / Skeletal / 3D) | Size / Vocab Count | Notes |
| :--- | :--- | :--- | :--- | :--- |
| *Example* | `https://example.com/isl-dataset` | Video / Skeletal | ~5,000 samples | Verified working link |

---

## 🌍 Category B: Standard / Global Continuous SLR Benchmarks
* **Assigned To:** Yusuf Mushtaq
* **Focus:** Standard academic benchmark datasets used for baseline comparisons (e.g., PHOENIX-Weather, CSL-Daily, WLASL).

| Dataset Name | Source / Repository Link | Format (RGB / Skeletal / 3D) | Size / Vocab Count | Notes |

| RWTH-PHOENIX-Weather 2014-T | [RWTH-PHOENIX-2014-T](https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX-2014-T/) | RGB + Gloss + Translation | 39 GB / 1,085 signs | Continuous German Sign Language benchmark |

| How2Sign | [How2Sign](https://how2sign.github.io/#download) | RGB + Depth + 2D/3D Skeleton | 16,609 vocabulary / 80+ hours | Large-scale continuous American Sign Language benchmark |

| LSA-T | [LSA-T](https://github.com/midusi/LSA-T) | RGB + Skeletal Keypoints | 8,459 clips / 14,239-word vocabulary | First continuous Argentinian Sign Language dataset |

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