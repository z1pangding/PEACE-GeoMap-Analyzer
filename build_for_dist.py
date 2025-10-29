
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
