#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阿里云Qwen API配置
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import api

def test_qwen_api():
    """测试Qwen API是否配置正确"""
    print("测试阿里云Qwen API配置...")
    print(f"使用模型: qwen-vl-max")
    print(f"API密钥: sk-08d3ac8e89f8445486c27a46b0456af3")
    
    # 测试简单文本对话
    test_messages = [
        {"role": "system", "content": "你是一个 helpful assistant。"},
        {"role": "user", "content": "请简单介绍一下地质地图的作用。"}
    ]
    
    try:
        response = api.answer_wrapper(test_messages)
        if response:
            print("✅ API连接成功!")
            print(f"回复: {response}")
            return True
        else:
            print("❌ API连接失败，未收到回复")
            return False
    except Exception as e:
        print(f"❌ API连接出错: {e}")
        return False

if __name__ == "__main__":
    success = test_qwen_api()
    if success:
        print("\n🎉 阿里云Qwen API配置成功，可以开始使用PEACE项目!")
    else:
        print("\n⚠️ 请检查API配置和网络连接")