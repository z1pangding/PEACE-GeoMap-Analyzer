# PEACE - 地质图理解系统

## 项目概述

PEACE (Empowering Geologic Map Holistic Understanding with MLLMs) 是一个基于多模态大语言模型的地质图理解系统。本系统通过HIE（分层信息提取）、DKI（领域知识注入）和PEQA（增强提示问答）三个模块，实现对地质图的智能分析。

## 系统特点

- **无需Google Earth Engine**：完全移除GEE依赖，仅保留核心的地质图分析功能
- **中文支持**：完整支持中文界面和地质图分析
- **多模态能力**：结合图像理解和领域知识进行地质图分析

## 安装要求

1. **Python版本**：Python 3.10及以上
2. **必需依赖**：
   ```bash
   pip install -r requirements.txt
   ```
3. **可选依赖**（用于GUI）：
   ```bash
   pip install PyQt6
   ```

## 必需模型文件

系统需要以下模型文件才能运行：

1. `dependencies/models/det_component/weights/best.pt` - 组件检测模型
2. 其他YOLOv10相关模型文件

**注意**：由于模型文件较大，未包含在项目中。您需要从官方渠道下载。

## 使用方法

### 1. GUI模式（推荐）

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

系统已配置为使用阿里云Qwen API：

- **模型**: qwen3-vl-plus
- **API密钥**: 已在代码中配置
- **端点**: dashscope.aliyuncs.com

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

## 注意事项

1. **首次运行**：可能需要几分钟时间加载模型
2. **模型文件**：确保下载了必需的模型文件
3. **API限制**：注意API调用频率限制
4. **图像格式**：支持主流图像格式 (JPG, PNG, TIF, BMP等)

## 系统架构

```
GUI界面 ←→ Copilot核心 ←→ HIE/DKI/PEQA模块 ←→ 阿里云Qwen API
     ↓
  进度显示 ←→ 结果展示
```

## 故障排除

- **模型加载失败**：检查模型文件是否存在
- **API连接失败**：确认API密钥和网络连接
- **GUI启动失败**：安装PyQt6依赖
- **中文显示问题**：确认系统支持中文字体

## 许可证

本项目遵循原项目的许可证协议。