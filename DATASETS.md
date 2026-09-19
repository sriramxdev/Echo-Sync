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
|---|---|---|---|---|
| RWTH-PHOENIX-Weather 2014-T | [RWTH-PHOENIX-2014-T](https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX-2014-T/) | RGB + Gloss + Translation | 39 GB / 1,085 signs | Continuous German Sign Language benchmark |
| How2Sign | [How2Sign](https://how2sign.github.io/#download) | RGB + Depth + 2D/3D Skeleton | 16,609 vocabulary / 80+ hours | Large-scale continuous American Sign Language benchmark |
| LSA-T | [LSA-T](https://github.com/midusi/LSA-T) | RGB + Skeletal Keypoints | 8,459 clips / 14,239-word vocabulary | First continuous Argentinian Sign Language dataset |

---

## 📖 Category C: Lexicon, Grammatical Rulebooks & Isolated Sign Corpora
* **Assigned To:** Ujjawal Kesarwani
* **Focus:** Official ISL dictionary/lexicon corpora (e.g., ISLRTC official sign bank, isolated signs).

### Official Indian Sign Language Corpora Directory

| Dataset Name | Source / Repository Link | Format (RGB / Skeletal / 3D) | Size / Vocab Count | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **ISLRTC National Dictionary** | `https://islrtc.nic.in` | Video clips (RGB) / Dictionary | **10,000+ standardized terms** | Official national corpus spanning academic, legal, medical, and agricultural categories. Signed by native Deaf experts. |
| **Sign Learn Mobile Database** | `https://islrtc.nic.in` | Video clips (RGB) | Mobile lookup application | Pocket repository for Android/iOS sync to track isolated word searches natively. |
| **FDMSE General Dictionary** | `https://indiansignlanguage.org` | Video clips (RGB) & Images | Comprehensive general vocabulary | Cross-mapped to **11 regional Indian languages** with structural tracking by C-DAC. |
| **INCLUDE Dataset** | https://www.kaggle.com/datasets/prathumarikeri/indian-sign-language-isl | Video clips (RGB) & Landmarked coordinates | **4,287 videos** (263 isolated word signs) | Public machine learning dataset spanning 15 distinct categories for word-level recognition. |
| **ISL-CSLTR Corpus** | `https://mendeley.com` | Annotated continuous video frames (RGB) | Time-bounded sequences | Specifically engineered for **continuous sign language translation (SLT)** research. |




---

## ⚙️ Ingestion & Verification Engine
* **Assigned To:** Sri Ram Sharma
* **Module:** `src/pipeline/validator.py` (Validates video decode integrity and executes MediaPipe skeletal sanity tests on incoming dataset samples)

---

## 📌 Submission Rules
1. Every entry **must** contain a working direct link (Kaggle, Zenodo, Hugging Face, GitHub, or institutional repository).
2. **Zero duplicates allowed:** Check existing entries before adding.
3. Submit a minimum of **2–3 unique datasets** in your assigned category via a GitHub Pull Request.