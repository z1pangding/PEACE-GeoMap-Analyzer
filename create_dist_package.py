"""
PEACE项目 - EXE分发包创建脚本
用于为同事创建最小化的可执行文件
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
import zipfile

def main():
    print("PEACE地质图分析系统 - EXE分发包创建工具")
    print("=" * 50)
    
    # 检查必要文件
    print("1. 检查必要文件...")
    required_files = [
        'gui_optimized_for_dist.py',
        'copilot.py',
        'utils/__init__.py',
        'modules/__init__.py',
        'agents/__init__.py',
        'tool_pool/__init__.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"[ERROR] 缺少以下必要文件: {missing_files}")
        return
    
    print("[OK] 所有文件检查通过")
    
    # 创建打包脚本
    print("\n2. 生成打包命令...")
    
    build_script = '''
import os
import subprocess
import sys

def build():
    print("开始打包PEACE地质图分析系统...")
    
    # 使用PyInstaller打包
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=PEACE_GeoMap_Analyzer',
        '--onefile',  # 打包成单个EXE文件
        '--windowed',  # 创建GUI窗口应用（无控制台）
        '--icon=',  # 可以指定图标
        '--clean',
        '--noconfirm',
        # 排除大体积但非必需的依赖
        '--exclude-module=matplotlib',
        '--exclude-module=geopandas', 
        '--exclude-module=shapely',
        '--exclude-module=transformers',
        '--exclude-module=sentence_transformers',
        '--exclude-module=paddleocr',
        '--exclude-module=deep-translator',
        'gui_optimized_for_dist.py'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] 打包成功！")
            print("EXE文件位置: dist/PEACE_GeoMap_Analyzer.exe")
            return True
        else:
            print(f"[ERROR] 打包失败:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[ERROR] 执行打包命令时出错: {e}")
        return False

if __name__ == "__main__":
    build()
'''
    
    with open('build_for_dist.py', 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    print("[OK] 打包脚本已生成")
    
    # 创建安装说明
    install_guide = '''PEACE地质图分析系统使用指南
============================

## 版权信息
项目基于微软研究院PEACE项目二次开发
原项目地址: https://github.com/microsoft/PEACE

二次开发单位: 浙江省水文地质工程地质大队（浙江省宁波地质院）
二次开发人: 基础地质调查研究中心-丁正鹏
邮箱: zhengpengding@outlook.com

## 第一步：安装Python
1. 访问 https://www.python.org/ 下载Python 3.10或更高版本
2. 安装时务必勾选 "Add Python to PATH"
3. 安装完成后重启电脑

## 第二步：安装依赖
1. 打开命令提示符（按 Win+R，输入 cmd，回车）
2. 进入程序所在文件夹（例如：cd C:\\PEACE）
3. 运行以下命令安装依赖：
   pip install PyQt6 openai dashscope pandas numpy pillow opencv-python

## 第三步：运行程序
1. 双击 PEACE_GeoMap_Analyzer.exe 运行程序
2. 首次使用需要配置API密钥：
   - 点击菜单栏"设置" -> "API配置"
   - 输入阿里云通义千问API密钥
   - 选择模型后点击"保存"

## 注意事项
- 确保网络连接正常
- 首次运行可能较慢，因为需要加载模型
- 支持的图片格式：JPG, PNG, BMP, TIF
- 单个图片文件不超过50MB
'''
    
    with open('使用指南.txt', 'w', encoding='utf-8') as f:
        f.write(install_guide)
    
    print("[OK] 使用指南已生成")
    
    # 创建最小依赖列表
    requirements = '''PyQt6>=6.4.0
openai>=1.0.0
dashscope
pandas>=2.0.0
numpy>=1.20.0
pillow>=9.0.0
opencv-python>=4.5.0
'''
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print("[OK] 依赖列表已生成")
    
    print("\n3. 准备完成！")
    print("\n要创建EXE文件，请执行以下命令：")
    print("   python build_for_dist.py")
    print("\n要分发给同事，请提供以下文件：")
    print("   - PEACE_GeoMap_Analyzer.exe (打包后生成)")
    print("   - 使用指南.txt")
    print("   - requirements.txt")
    
    print("\n[!] 重要提示：")
    print("- 您需要先安装PyInstaller: pip install pyinstaller")
    print("- 打包过程可能需要几分钟时间")
    print("- 打包后的EXE文件会出现在 dist/ 文件夹中")

if __name__ == "__main__":
    main()