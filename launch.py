"""
PEACE项目启动脚本
用于启动GUI界面或命令行工具
"""
import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="PEACE地质图理解系统启动器")
    parser.add_argument("mode", nargs="?", default="gui", choices=["gui", "eval", "metrics"], 
                        help="运行模式: gui (GUI界面), eval (评估模式), metrics (计算指标)")
    parser.add_argument("--copilot_mode", type=str, default="HIE,DKI,PEQA", 
                        help="协作模式: HIE,DKI,PEQA")
    parser.add_argument("--dataset_source", type=str, default="usgs", 
                        help="数据集来源: usgs, cgs")
    
    args = parser.parse_args()
    
    if args.mode == "gui":
        # 启动GUI
        try:
            from gui_right_log import main as gui_main
            print("启动PEACE地质图理解系统GUI...")
            gui_main()
        except ImportError as e:
            print(f"右侧日志版GUI启动失败: {e}")
            print("尝试启动简洁版GUI...")
            try:
                from gui_simple import main as gui_main
                gui_main()
            except ImportError as e2:
                print(f"简洁版GUI也启动失败: {e2}")
                print("尝试启动优化版GUI...")
                try:
                    from gui_optimized import main as gui_main
                    gui_main()
                except ImportError as e3:
                    print(f"优化版GUI也启动失败: {e3}")
                    print("尝试启动主版GUI...")
                    try:
                        from gui_main import main as gui_main
                        gui_main()
                    except ImportError as e4:
                        print(f"主版GUI也启动失败: {e4}")
                        print("尝试启动测试版GUI...")
                        try:
                            from gui_app_demo import main as demo_main
                            demo_main()
                        except ImportError as e5:
                            print(f"所有GUI版本均启动失败: {e5}")
                            print("请确保已安装PyQt6: pip install PyQt6")
    elif args.mode == "eval":
        # 启动评估模式
        from eval import main as eval_main
        eval_main()
    elif args.mode == "metrics":
        # 启动指标计算模式
        from calc_metrics import main as metrics_main
        metrics_main()
    else:
        print("未知模式，请使用 gui, eval 或 metrics")

if __name__ == "__main__":
    main()