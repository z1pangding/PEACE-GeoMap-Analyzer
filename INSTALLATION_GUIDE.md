# PEACE地质图分析系统 - 完整安装教程

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

## 项目版权信息

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

---

## 目录
1. [系统要求](#系统要求)
2. [Python安装](#python安装)
3. [项目依赖安装](#项目依赖安装)
4. [API密钥配置](#api密钥配置)
5. [运行程序](#运行程序)
6. [常见问题](#常见问题)

---

## 系统要求

- **操作系统**: Windows 7/8/10/11 (64位)
- **内存**: 至少 8GB RAM
- **存储空间**: 至少 2GB 可用空间
- **Python版本**: Python 3.10 或更高版本

---

## Python安装

### 1. 下载Python
1. 访问Python官方网站: https://www.python.org/
2. 点击页面上的 "Download Python" 按钮
3. 选择适合Windows的最新版本（3.10或更高）
4. 下载完成后，双击安装文件

### 2. 安装Python
1. 运行下载的Python安装程序
2. **重要**: 勾选 "Add Python to PATH" 选项
3. 选择 "Install Now" 进行标准安装
4. 等待安装完成

### 3. 验证安装
1. 按 `Windows键 + R` 打开运行对话框
2. 输入 `cmd` 并按回车打开命令提示符
3. 输入以下命令并确认版本:
```cmd
python --version
```
输出应显示Python 3.10或更高版本，例如：`Python 3.10.11`

---

## 项目依赖安装

### 1. 创建项目文件夹
1. 在电脑任意位置创建一个新文件夹，命名为 `PEACE`
2. 将 `requirements_minimal.txt` 文件复制到此文件夹中

### 2. 打开命令提示符
1. 进入 `PEACE` 文件夹
2. 按住 `Shift` 键，同时在文件夹空白处右键
3. 选择 "在此处打开PowerShell窗口" 或 "在此处打开命令窗口"

### 3. 安装依赖
在打开的命令窗口中输入以下命令：

```cmd
pip install -r requirements_minimal.txt
```

如果上述命令失败，请尝试：
```cmd
pip install PyQt6 openai dashscope pandas numpy pillow opencv-python
```

### 4. 等待安装完成
- 依赖安装可能需要5-10分钟
- 请耐心等待直到安装完成
- 安装完成后，命令提示符会返回到输入状态

---

## API密钥配置

### 1. 获取阿里云API密钥
1. 访问阿里云官方网站: https://www.aliyun.com/
2. 注册并登录账户
3. 进入 "通义千问" 控制台
4. 在 "API-KEY管理" 中创建新的API密钥

### 2. 查看API密钥
1. 登录阿里云控制台
2. 搜索 "通义千问"
3. 进入 "模型服务" -> "API-KEY管理"
4. 复制您的API密钥（以 `sk-` 开头）

---

## 运行程序

### 1. 下载程序文件
将 `PEACE_GeoMap_Analyzer.exe` 文件保存到 `PEACE` 文件夹中

### 2. 运行程序
1. 双击 `PEACE_GeoMap_Analyzer.exe` 文件
2. 程序将启动PEACE地质图分析系统

### 3. 初次使用配置
1. 程序启动后，点击菜单栏的 `设置` -> `API配置`
2. 输入您的阿里云API密钥
3. 选择合适的模型（推荐使用 `qwen3-vl-plus`）
4. 点击 `保存` 按钮

### 4. 使用程序
1. 点击 `📁 选择图片` 按钮上传地质图
2. 在问题描述框中输入您想了解的问题
3. 选择问题类型（或使用自动检测）
4. 点击 `🔍 开始分析` 按钮
5. 查看分析结果和详细日志

---

## 功能说明

### 支持的问题类型
- **提取类**: 图幅名称、比例尺、经纬度等信息提取
- **分析类**: 地层分析、地震风险评估
- **推理类**: 区域对比、断层存在性推理
- **定位类**: 标题、主图、图例等位置定位
- **指代类**: 根据颜色识别岩石类型

### 智能检测功能
- 选择 "auto-detect" 可让系统自动识别问题类型
- 系统会根据问题内容智能选择最适合的分析方法

---

## 常见问题

### Q1: 程序无法启动
**可能原因**: 缺少必要的依赖或Python版本不兼容
**解决方法**: 
1. 确保Python版本为3.10或更高
2. 重新运行依赖安装命令:
```cmd
pip install -r requirements_minimal.txt
```

### Q2: API配置失败
**可能原因**: API密钥格式错误或网络连接问题
**解决方法**:
1. 确认API密钥以 `sk-` 开头
2. 检查网络连接是否正常
3. 确认阿里云账户状态正常

### Q3: 图片上传失败
**可能原因**: 图片格式不支持或文件过大
**解决方法**:
1. 确认图片格式为JPG、PNG、BMP或TIF
2. 检查图片文件大小不超过50MB
3. 确认图片路径没有中文字符

### Q4: 分析结果为空
**可能原因**: 图片质量不高或问题描述不清晰
**解决方法**:
1. 使用清晰度较高的地质图
2. 问题描述尽量具体明确
3. 确认API密钥有调用权限

### Q5: 程序运行缓慢
**可能原因**: 网络速度慢或地质图分辨率过高
**解决方法**:
1. 检查网络连接速度
2. 适当降低地质图分辨率
3. 选择较小的地质图进行分析

---

## 故障排除

### 检查Python环境
在命令提示符中运行:
```cmd
python --version
pip --version
```

### 检查依赖安装
```cmd
pip list | findstr -i "pyqt openai pandas numpy pillow opencv"
```

### 重新安装依赖
```cmd
pip uninstall PyQt6 openai dashscope pandas numpy pillow opencv-python
pip install PyQt6 openai dashscope pandas numpy pillow opencv-python
```

---

## 技术支持

如果遇到问题，请检查:
1. 确保按照上述步骤正确安装
2. 检查是否有管理员权限
3. 确认防火墙和杀毒软件没有阻止程序运行

如仍有问题，可联系技术支持提供以下信息:
- 操作系统版本
- Python版本
- 具体错误信息截图
- 已执行的安装步骤