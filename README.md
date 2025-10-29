# PEACE - 地质图智能分析系统

## 项目概述

**PEACE (Empowering Geologic Map Holistic Understanding with MLLMs)** 是一个基于多模态大语言模型的地质图理解系统。本项目在微软研究院原PEACE项目基础上，由浙江省水文地质工程地质大队（浙江省宁波地质院）基础地质调查研究中心进行二次开发。

**原项目地址**: https://github.com/microsoft/PEACE  
**原论文**: @article{huang2025peace, title={PEACE: Empowering Geologic Map Holistic Understanding with MLLMs}, author={Huang, Yangyu and Gao, Tianyi and Xu, Haoran and Zhao, Qihao and Song, Yang and Gui, Zhipeng and Lv, Tengchao and Chen, Hao and Cui, Lei and Li, Scarlett and others}, journal={arXiv preprint arXiv:2501.06184}, year={2025} }

## 二次开发改进

### 主要改进内容

1. **GUI界面优化**
   - 重新设计了用户友好的图形界面
   - 添加了实时进度显示
   - 集成了模块状态指示器
   - 优化了用户交互体验

2. **EXE分发包**
   - 创建了完整的EXE打包流程
   - 最小化依赖以减小文件大小
   - 提供一键安装和使用指南

3. **中文支持**
   - 完整的中文界面支持
   - 优化了中文环境下的显示效果

4. **API配置优化**
   - 安全的API配置方式
   - 支持环境变量配置
   - 避免了硬编码敏感信息

## 系统架构

### 三个核心模块
1. **HIE (Hierarchical Information Extraction)** - 分层信息提取模块
2. **DKI (Domain Knowledge Injection)** - 领域知识注入模块
3. **PEQA (Prompt-enhanced Question Answering)** - 增强提示问答模块

## 软件界面展示

![软件界面示例](屏幕截图 2025-10-29 164134.png)
*图1: 主界面展示*

![问题配置界面](屏幕截图 2025-10-29 164252.png)
*图2: 问题配置界面*

![分析过程显示](屏幕截图 2025-10-29 164814.png)
*图3: 分析过程实时显示*

![结果展示界面](屏幕截图 2025-10-29 165113.png)
*图4: 分析结果展示*

![模块状态监控](屏幕截图 2025-10-29 165317.png)
*图5: HIE/DKI/PEQA模块状态监控*

## 功能特性

- 🎯 **智能问题检测**: 自动识别问题类型并选择最优分析策略
- 📊 **实时进度监控**: 可视化显示HIE、DKI、PEQA三大模块的处理状态
- 🌍 **多语言支持**: 支持中文界面和地质图分析
- 📈 **模块化设计**: 采用清晰的模块化架构，便于扩展和维护
- 🔐 **安全API配置**: 通过环境变量配置API密钥，避免泄露风险

## 支持的问题类型

1. **提取类 (extracting)**
   - 图幅名称提取
   - 比例尺提取
   - 经纬度提取
   - 索引图提取

2. **定位类 (grounding)**
   - 标题定位
   - 主图定位
   - 比例尺定位
   - 图例定位

3. **指代类 (referring)**
   - 根据颜色指代岩石

4. **推理类 (reasoning)**
   - 区域对比推理
   - 断层存在性推理

5. **分析类 (analyzing)**
   - 地层分析
   - 地震风险评估

## 安装指南

### 依赖安装

```bash
pip install -r requirements.txt
```

### 环境变量配置

```bash
# 设置API密钥
export DASHSCOPE_API_KEY="your-api-key-here"

# 设置模型名称（可选，默认为qwen-vl-max）
export MODEL_NAME="qwen3-vl-plus"
```

## 使用方法

1. 启动GUI界面：
   ```bash
   python gui_main.py
   ```

2. 上传地质图文件
3. 输入或选择问题类型
4. 配置API密钥（首次使用）
5. 点击"开始分析"按钮
6. 查看分析结果和详细日志

## 二次开发信息

- **开发单位**: 浙江省水文地质工程地质大队（浙江省宁波地质院）
- **开发人员**: 基础地质调查研究中心-丁正鹏
- **邮箱**: zhengpengding@outlook.com
- **开发时间**: 2025年10月

## 许可证

本项目遵循原项目的MIT许可证协议。

## 致谢

感谢微软研究院提供的原PEACE项目作为基础。