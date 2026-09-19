# 📊 Sign Language Datasets Registry

> Curated datasets for Indian Sign Language (ISL) continuous translation, kinematic benchmark baselines, and reference corpora.

---

## 🇮🇳 Category A: Continuous Indian Sign Language (ISL)
* **Assigned To:** Shubhanshu Singh
* **Focus:** Continuous ISL sentence-level video/skeletal datasets (e.g., INCLUDE, ISL-CSLR, or regional corpora).

| Dataset Name | Source / Repository Link | Format (RGB / Skeletal / 3D) | Size / Vocab Count | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **iSign** | [iSign Benchmark Project Page](https://exploration-lab.github.io/iSign/) | Video / Skeletal (3D) | **118,228 pairs** | Free for research use; supports native benchmarking for multi-modal tasks including *SignVideo2Text* and *SignPose2Text*. |
| **ISLTranslate** | [Exploration-Lab GitHub Repository](https://github.com/Exploration-Lab/ISLTranslate) | Video / Skeletal | **31,222 pairs** / 11,655 unique words | Largest translation dataset for continuous ISL; features a Baseline model using MediaPipe holistic poses. |
| **ISL-CSLTR** | [Kaggle Dataset Page](https://www.kaggle.com/datasets/drblack00/isl-csltr-indian-sign-language-dataset) | Video (RGB Frames) | **700 videos** / 18,863 sentence-level frames / 100 sentences | Fully annotated data recorded with 7 different signers across varied visual configurations. |
| **ISLVT** | [Mendeley Data Repository](https://data.mendeley.com/datasets/98mzk82wbb/1) | Video (Dual-View) | **152 videos** / 76 sentence pairs | Captures continuous English-Marathi-ISL gloss sentence pairs from front and side angles. |
| **INSIGNVID** | [Research Corpus References](https://arxiv.org/) | Video (RGB) | Varying custom configurations | Regional continuous configurations tailored for specialized sequence modelling. |

##### Note : Since delayed by Shubhanshu, added by Sri Ram.
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

| **ISLRTC National Dictionary** | https://drive.google.com/drive/folders/1U-Pr4r1-cupgNOOq9NH_uTsQnPSVEKco | Video clips (RGB) / Dictionary | **10,000+ standardized terms** | Official national corpus spanning academic, legal, medical, and agricultural categories. Signed by native Deaf experts. |
| **Sign Learn Mobile Database** | 'https://www.youtube.com/channel/UC3AcGIlqVI4nJWCwHgHFXtg' | Video clips (RGB) | Mobile lookup application | Pocket repository for Android/iOS sync to track isolated word searches natively. |
| **FDMSE General Dictionary** | https://www.data.gov.in/resource/number-registered-newspapers-and-periodicals-language-and-periodicity-language-wise-upto | Video clips (RGB) & Images | Comprehensive general vocabulary | Cross-mapped to **11 regional Indian languages** with structural tracking by C-DAC. |
| **INCLUDE Dataset** | https://www.kaggle.com/datasets/prathumarikeri/indian-sign-language-isl | Video clips (RGB) & Landmarked coordinates | **4,287 videos** (263 isolated word signs) | Public machine learning dataset spanning 15 distinct categories for word-level recognition. |
| **ISL-CSLTR Corpus** | `https://mendeley.com` | Annotated continuous video frames (RGB) | Time-bounded sequences | Specifically engineered for **continuous sign language translation (SLT)** research. |




<<<<<<< HEAD

=======
>>>>>>> origin/dataset/ECHO-15-ujjawal-lexicon

---

## ⚙️ Ingestion & Verification Engine
* **Assigned To:** Sri Ram Sharma
* **Module:** `src/pipeline/validator.py` (Validates video decode integrity and executes MediaPipe skeletal sanity tests on incoming dataset samples)

---

## 📌 Submission Rules
1. Every entry **must** contain a working direct link (Kaggle, Zenodo, Hugging Face, GitHub, or institutional repository).
2. **Zero duplicates allowed:** Check existing entries before adding.
3. Submit a minimum of **2–3 unique datasets** in your assigned category via a GitHub Pull Request.
