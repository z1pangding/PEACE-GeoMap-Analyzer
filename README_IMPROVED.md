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

## 系统特点

- **无需Google Earth Engine**: 完全移除GEE依赖，仅保留核心的地质图分析功能
- **中文支持**: 完整支持中文界面和地质图分析
- **多模态能力**: 结合图像理解和领域知识进行地质图分析
- **安全配置**: 通过环境变量而非硬编码配置API密钥
- **模块化设计**: 采用清晰的模块化架构，便于扩展和维护

## 安装要求

1. **Python版本**: Python 3.10及以上
2. **必需依赖**:
   ```bash
   pip install -r requirements.txt
   ```
3. **可选依赖**（用于GUI）:
   ```bash
   pip install PyQt6
   ```

## 使用方法

### 1. GUI模式（推荐）

```bash
python gui_main.py
```

或

```bash
python launch.py gui
```

### 2. 命令行模式

```bash
python launch.py eval        # 评估模式
python launch.py metrics     # 计算指标模式
```

### 3. 直接调用API

```python
from copilot import copilot

result = copilot(
    image_path="your_geological_map.jpg",
    question="您的问题",
    question_type="analyzing-formation",
    copilot_modes=["HIE", "DKI", "PEQA"]
)
```

## API配置

通过环境变量配置API（推荐方式）：

```bash
export DASHSCOPE_API_KEY="your-api-key-here"
export MODEL_NAME="qwen3-vl-plus"
```

或通过GUI配置对话框设置。

## 功能模块

1. **HIE (Hierarchical Information Extraction)**
   - 层次化信息提取
   - 地质图数字化

2. **DKI (Domain Knowledge Injection)**
   - 领域知识注入
   - 模拟地理空间数据查询

3. **PEQA (Prompt-enhanced Question Answering)**
   - 增强提示问答
   - 智能回答生成

## 支持的问题类型

- 地层分析 (analyzing-formation)
- 图幅名称提取 (extracting-sheet_name)
- 比例尺提取 (extracting-scale)
- 经纬度提取 (extracting-lonlat)
- 地震风险分析 (analyzing-earthquake_risk)
- 区域对比推理 (reasoning-area_comparison)
- 断层存在性推理 (reasoning-fault_existence)
- 岩石颜色识别 (referring-rock_by_color)
- 标题定位 (grounding-title_by_name)
- 主图定位 (grounding-main_map_by_name)

## 二次开发信息

- **开发单位**: 浙江省水文地质工程地质大队（浙江省宁波地质院）
- **开发人员**: 基础地质调查研究中心-丁正鹏
- **邮箱**: zhengpengding@outlook.com
- **开发时间**: 2025年10月

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

## 注意事项

1. **首次运行**: 可能需要几分钟时间加载模型
2. **模型文件**: 确保下载了必需的模型文件
3. **API限制**: 注意API调用频率限制
4. **图像格式**: 支持主流图像格式 (JPG, PNG, TIF, BMP等)
5. **安全配置**: 建议使用环境变量而非硬编码方式配置API密钥

## 系统架构

```
GUI界面 ←→ Copilot核心 ←→ HIE/DKI/PEQA模块 ←→ 阿里云Qwen API
     ↓
  进度显示 ←→ 结果展示
```

## 故障排除

- **模型加载失败**: 检查模型文件是否存在
- **API连接失败**: 确认API密钥和网络连接
- **GUI启动失败**: 安装PyQt6依赖
- **中文显示问题**: 确认系统支持中文字体

## 许可证

本项目遵循原项目的MIT许可证协议。