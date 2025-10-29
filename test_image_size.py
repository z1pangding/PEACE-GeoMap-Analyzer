"""
测试图像大小限制的脚本
"""
import os
from utils.api import local_image_to_data_url

def test_file_size_check():
    # 创建一个测试文件以验证大小限制
    test_file_path = "test_size_limit.txt"
    
    # 创建一个超过原8MB但小于新50MB限制的测试文件
    test_size = 20 * 1024 * 1024  # 20MB
    
    with open(test_file_path, 'wb') as f:
        f.write(b'0' * test_size)  # 创建20MB文件
    
    try:
        # 测试大小检查函数
        print(f"测试文件大小: {os.path.getsize(test_file_path) / (1024*1024):.2f} MB")
        result = local_image_to_data_url(test_file_path)
        print("[OK] 文件大小检查通过 - 20MB文件被接受")
    except ValueError as e:
        print(f"[ERROR] 文件大小检查失败: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

if __name__ == "__main__":
    test_file_size_check()