# PEACE地质图分析系统 - EXE分发版

## 项目概述

PEACE (Empowering Geologic Map Holistic Understanding with MLLMs) 是一个基于多模态大语言模型的地质图理解系统。本项目已打包为EXE可执行文件，方便在没有Python环境的计算机上使用。

## 版权信息

**项目基于微软研究院PEACE项目二次开发**  
原项目地址: https://github.com/microsoft/PEACE

**二次开发单位**: 浙江省水文地质工程地质大队（浙江省宁波地质院）  
**二次开发人**: 基础地质调查研究中心-丁正鹏  
**邮箱**: zhengpengding@outlook.com

```
@article{huang2025peace,
  title={PEACE: Empowering Geologic Map Holistic Understanding with MLLMs},
  author={Huang, Yangyu and Gao, Tianyi and Xu, Haoran and Zhao, Qihao and Song, Yang and Gui, Zhipeng and Lv, Tengchao and Chen, Hao and Cui, Lei and Li, Scarlett and others},
  journal={arXiv preprint arXiv:2501.06184},
  year={2025}
}
```

## 包含的文件

- `PEACE_GeoMap_Analyzer.exe` - 主程序EXE文件
- `使用指南.txt` - 详细安装和使用说明
- `requirements.txt` - 依赖包列表
- `INSTALLATION_GUIDE.md` - 完整安装教程

## 打包优化说明

为了最小化EXE文件大小，我们进行了以下优化：

1. **精简依赖**：移除了非必要的大型依赖包如geopandas、transformers、paddleocr等
2. **优化GUI**：使用优化后的GUI界面，保留完整功能但减少依赖
3. **配置文件**：集成API配置功能，无需手动修改代码
4. **错误处理**：增强错误处理和用户体验

## 系统要求

- **操作系统**: Windows 7/8/10/11 (64位)
- **内存**: 至少 8GB RAM
- **存储空间**: 至少 2GB 可用空间
- **Python**: 运行时需要Python 3.10+环境

## 使用方法

### 1. 安装Python环境
请参考 `使用指南.txt` 中的Python安装步骤

### 2. 安装依赖库
```bash
pip install -r requirements.txt
```

### 3. 运行程序
双击 `PEACE_GeoMap_Analyzer.exe` 启动程序

### 4. 配置API密钥
首次使用需要配置阿里云通义千问API密钥：
- 点击菜单栏"设置" -> "API配置"
- 输入您的API密钥
- 选择合适的模型
- 点击"保存"

## 功能特性

- **完整GUI界面**：包含图像上传、问题输入、结果展示等所有功能
- **智能问题检测**：自动识别问题类型
- **多模块分析**：HIE(分层信息提取)、DKI(领域知识注入)、PEQA(增强提示问答)
- **实时进度显示**：显示各模块处理状态
- **中文支持**：完整的中文界面和分析能力

## 注意事项

1. **API密钥**：需要阿里云通义千问API密钥才能使用
2. **网络连接**：需要稳定的网络连接以调用API
3. **图像大小**：单个图像文件不要超过50MB
4. **首次运行**：可能需要几分钟时间加载模型

## 打包脚本

如果需要重新打包，可以使用以下文件：
- `create_dist_package.py` - 分发包创建脚本
- `build_exe.py` - 完整打包脚本
- `gui_optimized_for_dist.py` - 优化的GUI界面

## 技术支持

如遇到问题，请参考 `INSTALLATION_GUIDE.md` 或联系技术支持。

## 版权信息

本项目基于PEACE开源项目，详情请参考原项目的LICENSE文件。