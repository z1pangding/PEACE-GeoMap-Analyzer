# PEACE项目全面概览

## 项目简介
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

## 项目特点
- **无需Google Earth Engine**: 完全移除GEE依赖，仅保留核心的地质图分析功能
- **中文支持**: 完整支持中文界面和地质图分析
- **多模态能力**: 结合图像理解和领域知识进行地质图分析
- **模块化设计**: 采用清晰的模块化架构，便于扩展和维护
- **安全配置**: 通过环境变量而非硬编码配置API密钥

## 系统架构

### 三个核心模块
1. **HIE (Hierarchical Information Extraction) - 分层信息提取模块**
   - 负责地质图的数字化和结构化解析
   - 使用YOLOv10模型检测地图组件（如标题、主图、图例、比例尺等）
   - 提取图例信息、基本地图信息等

2. **DKI (Domain Knowledge Injection) - 领域知识注入模块**
   - 注入地质学相关领域知识
   - 模拟地理空间数据查询
   - 结合地震学和地理学知识

3. **PEQA (Prompt-enhanced Question Answering) - 增强提示问答模块**
   - 构建增强提示词
   - 调用大语言模型生成答案
   - 根据问题类型选择适当的图像组件

### 项目文件结构
```
PEACE/
├── agents/                 # 智能体模块
│   ├── geographer.py      # 地理学智能体
│   ├── geologist.py       # 地质学智能体
│   └── seismologist.py    # 地震学智能体
├── modules/               # 核心模块
│   ├── HIE.py            # 分层信息提取模块
│   ├── DKI.py            # 领域知识注入模块
│   └── PEQA.py           # 增强提示问答模块
├── tool_pool/             # 工具池
│   ├── map_component_detector.py    # 地图组件检测器
│   ├── map_legend_detector.py       # 图例检测器
│   └── ...               # 其他工具
├── utils/                 # 工具函数
│   ├── api.py            # API调用接口
│   ├── prompt.py         # 提示词管理
│   ├── vision.py         # 计算机视觉功能
│   └── common.py         # 通用函数
├── data/                  # 数据目录
├── models/                # 模型目录
├── dependencies/          # 依赖项
├── gui_*.py              # GUI界面文件
├── launch.py             # 启动脚本
├── copilot.py            # 核心分析接口
├── eval.py               # 评估脚本
├── calc_metrics.py       # 指标计算脚本
└── ...
```

### 主要功能模块

#### 1. 图像处理和分析 (`utils/vision.py`)
- 图像尺寸获取
- 图像裁剪和保存
- 颜色计算和识别
- 经纬度区域检测
- 岩石区域分割

#### 2. API接口 (`utils/api.py`)
- 集成阿里云Qwen API
- 支持多模态请求
- 错误处理和重试机制
- 图像编码为base64数据URL

#### 3. 提示词管理 (`utils/prompt.py`)
- 支持中英文双语提示
- 按问题类型分类的提示模板
- 支持多种问题格式（选择题、填空题、问答题等）

#### 4. GUI界面
- `gui_right_log.py` - 带日志的完整版界面
- `gui_chinese_support.py` - 修复中文编码问题的版本
- `gui_simple.py` - 简洁版界面
- `gui_optimized.py` - 优化版界面

### 问题类型支持
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

### 运行模式
1. **GUI模式**：`python launch.py gui`
2. **评估模式**：`python launch.py eval`
3. **指标计算模式**：`python launch.py metrics`

### 依赖管理
- 使用`requirements.txt`管理Python依赖
- 模型文件需单独下载
- 支持YOLOv10模型用于地质图组件检测

### API配置
- 使用阿里云Qwen API
- 支持qwen-vl-max和qwen3-vl-plus模型
- 具备错误处理和重试机制

## 使用方法
1. 安装依赖：`pip install -r requirements.txt`
2. 下载模型文件（需从官方渠道获取）
3. 配置API密钥
4. 运行GUI界面：`python launch.py gui`

## 注意事项
- 首次运行可能需要几分钟加载模型
- 需要有效的API密钥才能使用在线模型
- 支持主流图像格式（JPG, PNG, TIF, BMP等）
- 具备内容过滤功能，避免敏感内容