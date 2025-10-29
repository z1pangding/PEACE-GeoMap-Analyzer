# PEACE地质图分析系统 - GitHub上传指南

## 上传的文件列表

### 根目录文件
- README.md - 项目主说明
- README_IMPROVED.md - 项目改进说明  
- README_DIST.md - 分发版说明
- PROJECT_OVERVIEW_CN.md - 项目中文概览
- LICENSE - 许可证文件
- CODE_OF_CONDUCT.md - 行为准则
- SECURITY.md - 安全政策
- SUPPORT.md - 支持说明
- NOTICE - 通知文件
- requirements.txt - 依赖列表
- .gitignore - Git忽略配置

### 源代码文件
- copilot.py - 核心分析接口
- launch.py - 启动脚本
- minimal_launch.py - 最小启动脚本
- system_check.py - 系统检查脚本
- calc_metrics.py - 指标计算脚本
- eval.py - 评估脚本

### GUI界面文件
- gui_main.py - 主GUI界面
- gui_optimized_for_dist.py - 优化版GUI（带版权信息）
- gui_optimized.py - 优化版GUI
- gui_right_log.py - 日志版GUI
- gui_simple.py - 简洁版GUI
- gui_chinese_support.py - 中文支持GUI
- api_config_dialog.py - API配置对话框

### 模块文件 (modules/)
- __init__.py
- HIE.py - 分层信息提取模块
- DKI.py - 领域知识注入模块
- PEQA.py - 增强提示问答模块

### 工具池文件 (tool_pool/)
- __init__.py
- active_fault_db.py
- history_earthquake_db.py
- k2_knowledge_db.py
- landcover_type_api.py
- map_component_detector.py
- map_legend_detector.py
- population_density_api.py
- rock_type_and_age_db.py

### 智能体文件 (agents/)
- __init__.py
- geographer.py - 地理学智能体
- geologist.py - 地质学智能体
- seismologist.py - 地震学智能体

### 工具函数 (utils/)
- __init__.py
- api.py - API接口（已移除硬编码密钥）
- common.py - 通用函数
- prompt.py - 提示词管理
- vision.py - 计算机视觉功能

### 测试文件
- test_peace_basic.py - 基础功能测试
- test_image_size.py - 图像尺寸测试
- test_api.py - API测试

### 文档文件
- INSTALLATION_GUIDE.md - 安装教程
- LICENSE_INFO.md - 许可证信息

## 上传步骤

### 1. 初始化Git仓库
```bash
git init
git add .
git commit -m "Initial commit: PEACE地质图分析系统"
```

### 2. 创建远程仓库
1. 在GitHub上创建新仓库
2. 添加远程源：
```bash
git remote add origin https://github.com/your-username/PEACE-GeoMap-Analyzer.git
git branch -M main
git push -u origin main
```

### 3. 环境变量配置说明
用户需要设置以下环境变量：

```bash
# 设置阿里云DashScope API密钥
export DASHSCOPE_API_KEY="your-api-key-here"

# （可选）设置模型名称，默认为qwen-vl-max
export MODEL_NAME="qwen3-vl-plus"
```

### 4. Windows环境变量设置
在Windows上：
```cmd
setx DASHSCOPE_API_KEY "your-api-key-here"
setx MODEL_NAME "qwen-vl-max"
```

## 仓库结构说明

```
PEACE-GeoMap-Analyzer/
├── README.md                 # 项目说明
├── requirements.txt          # 依赖文件
├── .gitignore              # Git忽略规则
├── LICENSE                 # 许可证
├── copilot.py              # 核心分析模块
├── launch.py               # 启动脚本
├── gui_main.py             # 主GUI界面
├── api_config_dialog.py    # API配置界面
├── modules/                # 核心模块
│   ├── HIE.py
│   ├── DKI.py
│   └── PEQA.py
├── agents/                 # 智能体模块
│   ├── geologist.py
│   ├── geographer.py
│   └── seismologist.py
├── tool_pool/              # 工具池
├── utils/                  # 工具函数
│   ├── api.py             # API接口
│   ├── common.py
│   ├── prompt.py
│   └── vision.py
└── docs/                   # 文档
```

## 重要说明

1. **安全考虑**：已移除所有硬编码的API密钥，使用环境变量替代
2. **.gitignore**：已配置忽略大型二进制文件、构建产物和敏感配置
3. **API配置**：用户需要自行获取API密钥并配置环境变量
4. **依赖管理**：通过requirements.txt管理包依赖
5. **版权信息**：保留了原微软PEACE项目的引用信息和许可证

## 后续维护

1. 定期更新依赖版本
2. 添加更多测试用例
3. 完善文档
4. 修复bug和添加新功能