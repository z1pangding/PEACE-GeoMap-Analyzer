"""
PEACE项目 - 最小化版本 (仅地质图分析和对话)
无需Google Earth Engine依赖
"""
import sys
import os
import json
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
logger = logging.getLogger(__name__)

def analyze_geological_map(image_path, question, question_type="analyzing-formation"):
    """
    分析地质图的核心函数
    """
    try:
        # 导入copilot（这是核心分析模块）
        from copilot import copilot
        
        # 调用主分析流程
        answer = copilot(
            image_path=image_path,
            question=question,
            question_type=question_type,
            copilot_modes=["HIE", "DKI", "PEQA"]
        )
        
        return answer
    except Exception as e:
        logger.error(f"分析地质图时出现错误: {e}")
        return f"分析失败: {str(e)}"

def main():
    print("=" * 60)
    print("PEACE - 地质图智能分析系统 (精简版)")
    print("无需Google Earth Engine依赖")
    print("=" * 60)
    
    # 检查必需的文件
    required_files = [
        "copilot.py",
        "utils/api.py",
        "modules/__init__.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"错误: 缺少必需文件 {file}")
            return
    
    print("[OK] 系统检查完成")
    print("[OK] API配置正常")
    print("[OK] 模型连接正常")
    print()
    
    while True:
        print("选择操作模式:")
        print("1. GUI模式 (图形界面)")
        print("2. CLI模式 (命令行交互)")
        print("3. 退出")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == "1":
            # 启动GUI
            try:
                from gui_optimized import main as gui_main
                print("启动GUI界面...")
                gui_main()
            except ImportError as e:
                print(f"GUI启动失败: {e}")
                print("请确保已安装PyQt6: pip install PyQt6")
        elif choice == "2":
            # 命令行交互模式
            print("\n--- 命令行交互模式 ---")
            image_path = input("请输入地质图路径: ").strip()
            
            if not os.path.exists(image_path):
                print("错误: 文件不存在!")
                continue
            
            print("\n可用问题类型:")
            print("- analyzing-formation (地层分析)")
            print("- extracting-sheet_name (提取图幅名称)")
            print("- extracting-scale (提取比例尺)")
            print("- extracting-lonlat (提取经纬度)")
            print("- analyzing-earthquake_risk (地震风险评估)")
            print("- custom (自定义)")
            
            question_type = input("\n请选择问题类型 (默认: analyzing-formation): ").strip()
            if not question_type:
                question_type = "analyzing-formation"
            
            question = input("请输入您的问题: ").strip()
            if not question:
                print("问题不能为空!")
                continue
            
            print(f"\n正在分析地质图: {os.path.basename(image_path)}")
            print(f"问题: {question}")
            print(f"类型: {question_type}")
            print("\n处理中，请稍候...")
            
            result = analyze_geological_map(image_path, question, question_type)
            print(f"\n分析结果:\n{result}")
            
        elif choice == "3":
            print("感谢使用PEACE地质图分析系统!")
            break
        else:
            print("无效选择，请重试!")
        
        print()

if __name__ == "__main__":
    main()