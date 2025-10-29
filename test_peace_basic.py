# test_peace_basic.py
import os
import sys

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Testing PEACE project basic functionality...")

# 测试导入
try:
    from utils import common, api
    print("SUCCESS: Utils imported successfully")
    print(f"Current model: {common.model_name}")
    print(f"Dataset source: {common.dataset_source}")
except ImportError as e:
    print(f"ERROR importing utils: {e}")
    sys.exit(1)

# 测试模块导入
try:
    from modules.HIE import hierarchical_information_extraction
    print("SUCCESS: HIE module imported successfully")
except ImportError as e:
    print(f"ERROR importing HIE: {e}")

try:
    from modules.DKI import domain_knowledge_injection
    print("SUCCESS: DKI module imported successfully")
except ImportError as e:
    print(f"ERROR importing DKI: {e}")

try:
    from modules.PEQA import prompt_enhanced_QA
    print("SUCCESS: PEQA module imported successfully")
except ImportError as e:
    print(f"ERROR importing PEQA: {e}")

# 测试 API 功能
try:
    if hasattr(api, 'client'):
        print("SUCCESS: API client configured")
    else:
        print("WARNING: API client not configured")
except Exception as e:
    print(f"ERROR testing API: {e}")

# 测试常用函数
try:
    date = common.today_date()
    print(f"SUCCESS: Date function works, today's date: {date}")
except Exception as e:
    print(f"ERROR with date function: {e}")

print("Basic functionality test completed.")