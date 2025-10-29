"""
PEACE项目打包脚本
用于将PEACE GUI界面打包成最小的EXE文件
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_spec_file():
    """创建PyInstaller的spec文件，用于优化打包"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
sys.setrecursionlimit(5000)  # 增加递归限制

block_cipher = None

# 需要包含的文件和路径
a = Analysis(
    ['gui_optimized_for_dist.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # 包含必要的数据文件
        ('utils', 'utils'),
        ('modules', 'modules'),
        ('agents', 'agents'),
        ('tool_pool', 'tool_pool'),
        ('data', 'data'),
        ('models', 'models'),
        ('dependencies', 'dependencies'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        # 隐式导入的模块
        'utils.api',
        'utils.prompt', 
        'utils.vision',
        'utils.common',
        'modules.HIE',
        'modules.DKI', 
        'modules.PEQA',
        'agents.geologist',
        'agents.geographer',
        'agents.seismologist',
        'tool_pool.map_component_detector',
        'tool_pool.map_legend_detector',
        'tool_pool.rock_type_and_age_db',
        'tool_pool.k2_knowledge_db',
        'copilot',
        'PIL',
        'cv2',
        'numpy',
        'openai',
        'dashscope',
        'PyQt6.sip',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不必要的大依赖以减小文件大小
        'tkinter',
        'matplotlib.backends',
        'matplotlib.pyplot',
        'geopandas',
        'shapely',
        'sentence_transformers',
        'transformers',
        'torchvision.models',
        'torch.nn',
        'torch.optim',
        'torch.utils',
        'paddleocr',
        'paddle',
        'paddle.fluid',
        'paddleseg',
        'paddlenlp',
        'deep-translator',
        'tqdm',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PEACE_GeoMap_Analyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为False以创建GUI应用程序
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标路径
)
'''
    with open('peace_gui.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

def create_minimal_requirements():
    """创建用于EXE分发的最小依赖列表"""
    minimal_req = '''PyQt6>=6.4.0
openai==1.45.0
dashscope
pandas==2.2.2
numpy==1.26.4
pillow==11.0.0
opencv-python==4.10.0.84
'''
    with open('requirements_minimal.txt', 'w', encoding='utf-8') as f:
        f.write(minimal_req)

def build_exe():
    """执行打包命令"""
    try:
        # 创建spec文件
        create_spec_file()
        
        # 创建最小依赖文件
        create_minimal_requirements()
        
        print("开始打包PEACE项目...")
        print("这可能需要几分钟时间，请耐心等待...")
        
        # 执行PyInstaller打包命令
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            'peace_gui.spec',
            '--clean',
            '--noconfirm'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 打包成功！")
            print("EXE文件位置: dist/PEACE_GeoMap_Analyzer.exe")
            return True
        else:
            print(f"❌ 打包失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 打包过程中出现错误: {str(e)}")
        return False

def create_distribution_package():
    """创建可分发的完整包"""
    try:
        print("创建完整分发包...")
        
        # 创建分发目录
        dist_dir = Path("PEACE_Distribution")
        dist_dir.mkdir(exist_ok=True)
        
        # 复制EXE文件
        exe_src = Path("dist/PEACE_GeoMap_Analyzer.exe")
        exe_dst = dist_dir / "PEACE_GeoMap_Analyzer.exe"
        if exe_src.exists():
            shutil.copy2(exe_src, exe_dst)
            print(f"✅ 已复制EXE文件到: {exe_dst}")
        
        # 复制必要文件
        files_to_copy = [
            "requirements_minimal.txt",
            "README.md",
            "LICENSE"
        ]
        
        for file_path in files_to_copy:
            src = Path(file_path)
            if src.exists():
                dst = dist_dir / src.name
                shutil.copy2(src, dst)
                print(f"✅ 已复制: {src.name}")
        
        # 创建文档
        readme_content = """PEACE 地质图分析系统
===================

这是一个基于多模态大语言模型的地质图智能分析系统。

使用说明：
1. 确保已安装Python 3.10+
2. 安装所需依赖（见requirements_minimal.txt）
3. 运行 PEACE_GeoMap_Analyzer.exe

首次使用需要配置阿里云通义千问API密钥。
"""
        readme_path = dist_dir / "README_DIST.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ 分发包已创建: {dist_dir.absolute()}")
        return True
        
    except Exception as e:
        print(f"❌ 创建分发包时出现错误: {str(e)}")
        return False

def main():
    print("PEACE项目EXE打包工具")
    print("=====================")
    
    # 检查PyInstaller是否已安装
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
    except ImportError:
        print("❌ 未找到PyInstaller，请先安装: pip install pyinstaller")
        return
    
    # 检查是否在项目根目录
    required_files = [
        'gui_optimized_for_dist.py',
        'copilot.py',
        'utils/api.py',
        'modules/HIE.py',
        'modules/DKI.py',
        'modules/PEQA.py'
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ 缺少必要文件: {file}")
            return
    
    print("✅ 所有必要文件检查通过")
    
    # 执行打包
    success = build_exe()
    if success:
        create_distribution_package()
        print("\\n🎉 打包完成！")
        print("分发包已创建，请查看 'PEACE_Distribution' 目录")
    else:
        print("\\n❌ 打包失败，请检查错误信息")

if __name__ == "__main__":
    main()