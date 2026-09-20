# Echo-Sync

> **Edge-Optimized Real-Time Sign Language Translation Platform**

[![Documentation & Site](https://img.shields.io/badge/Live_Site-Astro_%2B_Starlight-059669.svg?logo=astro&logoColor=white)](https://sriramxdev.github.io/Echo-Sync/)
[![Environment: Pixi](https://img.shields.io/badge/Environment-Pixi-blue.svg)](https://pixi.sh)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

---

## 🌐 Live Platform & Documentation

Explore the official project website, interactive architecture visualizers, and module API specifications:

🔗 **[Echo-Sync Documentation & Portal](https://sriramxdev.github.io/Echo-Sync/)**

* **Interactive Showcase:** High-level problem statement, model benchmarks, and hardware targets.
* **Technical Docs:** Canonical 75-joint skeletal schema, spatial-temporal normalization pipelines, and ST-GCN stage specifications.
* **Edge Engine Specs:** Zero-copy DynaPrune Rust decimation engine details and latency metrics.

---

## 📌 Project Overview

**Echo-Sync** is an engineering project focused on high-performance, real-time edge processing and neural inference for accessibility systems. The platform bridges low-latency computer vision pipelines with localized AI models to enable efficient continuous translation directly on consumer edge hardware without depending on heavy cloud compute resources.

This repository serves as the core development codebase for the **B.Tech Final Year Capstone Major Project**.

---

## 👥 Project Team

* **Sri Ram Sharma** — *Team Lead & Architecture*
* **Yusuf Mushtaq** — *Core Engineering & Development*
* **Ujjawal Kesarwani** — *Core Engineering & Development*
* **Shubhanshu Singh** — *Core Engineering & Development*

---

## 🛠️ Developer Setup & Environment

This repository uses **[Pixi](https://pixi.sh)** for deterministic, multi-platform environment management.

### 1. Install Pixi
* **Linux / macOS:**
  ```bash
  curl -fsSL [https://pixi.sh/install.sh](https://pixi.sh/install.sh) | sh