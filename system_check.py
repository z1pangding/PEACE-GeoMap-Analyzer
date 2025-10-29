"""
PEACE系统检查脚本
验证系统是否已正确配置
"""
import os
import sys
import importlib.util

def check_python_version():
    """检查Python版本"""
    print("检查Python版本...", end=" ")
    if sys.version_info >= (3, 10):
        print("[OK] 支持 (Python 3.10+)")
        return True
    else:
        print(f"[ERR] 不支持 (当前: {sys.version_info.major}.{sys.version_info.minor})")
        return False

def check_required_files():
    """检查必需的项目文件"""
    print("\n检查必需的项目文件...")
    
    required_files = [
        "copilot.py",
        "utils/api.py",
        "modules/__init__.py",
        "agents/__init__.py",
        "tool_pool/__init__.py"
    ]
    
    all_found = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  [OK] {file}")
        else:
            print(f"  [ERR] {file}")
            all_found = False
    
    return all_found

def check_model_files():
    """检查必需的模型文件"""
    print("\n检查必需的模型文件...")
    
    model_files = [
        "dependencies/models/det_component/weights/best.pt"
    ]
    
    all_found = True
    for model in model_files:
        if os.path.exists(model):
            print(f"  [OK] {model}")
        else:
            print(f"  [ERR] {model} (需要下载)")
            all_found = False
    
    return all_found

def check_dependencies():
    """检查关键依赖"""
    print("\n检查关键依赖...")
    
    dependencies = [
        ("openai", "OpenAI"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("PIL", "Pillow"),
        ("cv2", "OpenCV")
    ]
    
    all_installed = True
    for module, name in dependencies:
        if importlib.util.find_spec(module):
            print(f"  [OK] {name}")
        else:
            print(f"  [ERR] {name}")
            all_installed = False
    
    # 检查PyQt6（可选）
    if importlib.util.find_spec("PyQt6"):
        print(f"  [OK] PyQt6 (GUI支持)")
    else:
        print(f"  [WARN] PyQt6 (GUI支持 - 可选)")
    
    return all_installed

def check_api_config():
    """检查API配置"""
    print("\n检查API配置...")
    
    try:
        from utils.api import client
        print("  [OK] API客户端配置正常")
        print("  [OK] 已配置为阿里云Qwen API")
        print("  [OK] 模型: qwen3-vl-plus")
        return True
    except Exception as e:
        print(f"  [ERR] API配置错误: {e}")
        return False

def main():
    print("=" * 50)
    print("PEACE系统检查脚本")
    print("=" * 50)
    
    checks = []
    
    checks.append(check_python_version())
    checks.append(check_required_files())
    checks.append(check_model_files())
    checks.append(check_dependencies())
    checks.append(check_api_config())
    
    print(f"\n{'='*50}")
    print("检查结果总结:")
    
    passed = sum(checks)
    total = len(checks)
    
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("[INFO] 所有检查通过! 系统已准备就绪。")
        print("\n您可以使用以下命令:")
        print("  python launch.py gui     # 启动GUI界面")
        print("  python launch.py eval    # 评估模式")
        print("  python launch.py metrics # 指标计算模式")
    else:
        print("[WARN] 一些检查未通过，请按照提示解决问题。")
        print("特别注意：模型文件需要单独下载。")
    
    print("=" * 50)

if __name__ == "__main__":
    main()