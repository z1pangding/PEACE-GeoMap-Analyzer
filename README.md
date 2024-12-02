# PEACE: Empowering Geologic Map Holistic Understanding with MLLMs

<div align="center">
![](https://img.shields.io/badge/Task-GeologicMap_Understanding-blue)
![](https://img.shields.io/badge/Data-Released-orange)
![](https://img.shields.io/badge/Code_License-MIT-green)
</div>

<p align="center">
  <a href="https://arxiv.org/abs/"><b>[📜 Paper]</b></a> •
  <a href="https://huggingface.co/microsoft/"><b>[🤗 HF Dataset]</b></a> •
  <a href="https://github.com/microsoft/PEACE"><b>[🐱 GitHub]</b></a>
</p>

## Introduction
Geologic map, as a fundamental diagram in geology science, provides critical insights into the structure and composition of Earth's subsurface and surface. These maps are indispensable in various fields, including disaster detection, resource exploration, and civil engineering.

Despite their significance, current Multimodal Large Language Models (MLLMs) often fall short in geologic map understanding.
To bridge this gap, we introduce GeoMap-Agent, the inaugural agent designed for geologic map understanding, which features three modules: Hierarchical Information Extraction (HIE), Domain Knowledge Injection (DKI), and Prompt-enhanced Question Answering (PEQA).

## Quick Start

 - Step1: Clone Repo
```
git clone https://github.com/microsoft/PEACE.git
```

 - Step2: Download Layout Detection [Model](https://github.com/microsoft/PEACE/releases/download/layout_model/models.zip)
```
wget https://github.com/microsoft/PEACE/releases/download/layout_model/models.zip
unzip models.zip
```

 - Step3: Install Dependencies
```
pip install -r requirements.txt
```

 - Step4: Configure API endpoint and key in utils/api.py

## Evaluation
```
python eval.py --copilot_mode HIE,DKI,PEQA --dataset_source usgs
```

## Citation
```
TBD
```

## License
```
This code repository is licensed under the MIT License. The use of Ultralytics library is subject to the its [License](https://github.com/ultralytics/ultralytics/blob/main/LICENSE).
```
