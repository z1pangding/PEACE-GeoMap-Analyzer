# 🗺️ PEACE: Em**p**owering G**e**ologic M**a**p Holisti**c** Und**e**rstanding with MLLMs

<div align="center">

![](https://img.shields.io/badge/Task-GeoMap-orange)
![](https://img.shields.io/badge/Data-Released-green)
![](https://img.shields.io/badge/Code_License-MIT-blue)

</div>

<p align="center">
  <a href="https://arxiv.org/abs/"><b>[📜 Paper]</b></a> •
  <a href="https://huggingface.co/microsoft/GeoMap-Bench"><b>[🤗 HF Dataset]</b></a> •
  <a href="https://github.com/microsoft/PEACE"><b>[🐱 GitHub Code]</b></a>
</p>

<p align="center">
    <img src="./images/Cover_v8.png" width="800">
</p>

## 📢 News and Updates
- 2024/12/3: Benchmark and Agent released. 
## 📖 Table of Contents

- [Overview](#introduction)
- [GeoMap-Bench](#geoMap-bench)
- [GeoMap-Agent](#geomap-agent)
- [Quickstart](#quick-start)
- [Citation](#citation)

## 🌟 Introduction
Geologic map, as a fundamental diagram in geology science, provides critical insights into the structure and composition of Earth's subsurface and surface. These maps are indispensable in various fields, including disaster detection, resource exploration, and civil engineering.

To quantify this gap, we construct **GeoMap-Bench**, the first-ever bench mark for evaluating MLLMs in geologic map understand ing, which assesses the full-scale abilities in extracting, re ferring, grounding, reasoning, and analyzing. To bridge this gap, we introduce **GeoMap-Agent**, the inaugural agent designed for geologic map understanding.

## 🧭 GeoMap-Bench
We present GeoMap-Bench, a new benchmark consisting of 124 geologic maps and 3,864 multimodal multiple-choice questions with diverse annotations. The distribution of questions in the GeoMap-Bench. It consists of 25 task types that measure critical geological map interpretation abilities across **five** aspects: *grounding, extracting, referring, reasoning, and analyzing*.

<p align="center">
    <img src="./images/GeoMap_Bench.png" width="600">

</p>

## 🛠️ GeoMap-Agent

<p align="center">
    <img src="./images/GeoMap_Agent_Framework_v2.png" width="800">
</p>

## 🧮 Leaderboard

| Method               | Extracting | Grounding | Referring | Reasoning | Analyzing | Overall |
|----------------------|------------|-----------|-----------|-----------|-----------|---------|
| Random               | 0          | 0         | 0.250     | 0.250     | 0         | 0.100   |
| GPT-4o               | 0.219      | 0.128     | 0.378     | 0.507     | 0.612     | 0.369   |
| GeoMap-Agent         | 0.832      | 0.920     | 0.886     | 0.588     | 0.831     | 0.811   |


## ⏩ Quick Start
<details open>
<summary>Installation</summary>

 - Step1: Clone repository
```
git clone https://github.com/microsoft/PEACE.git
```

 - Step2: Download layout detection [models](https://github.com/microsoft/PEACE/releases/download/layout_model/models.zip)
```
wget https://github.com/microsoft/PEACE/releases/download/layout_model/models.zip
unzip models.zip
```

 - Step3: Install dependencies
```
pip install -r requirements.txt
```

 - Step4: Configure API endpoint and key in utils/api.py

</details>

<details open>
<summary>Evaluation</summary>

```
python eval.py --copilot_mode HIE,DKI,PEQA --dataset_source usgs
```

</details>

## Disclaimer
Due to the inherent limitations of large language models, there may be issues such as hallucinations.


## Citation
```
TBD
```

## License
This repository is licensed under the [MIT](https://github.com/microsoft/PEACE/blob/main/LICENSE) License.
The use of Ultralytics library is subject to the [AGPL-3.0](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) License.
