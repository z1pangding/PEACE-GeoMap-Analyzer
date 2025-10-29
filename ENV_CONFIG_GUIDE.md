# 环境变量配置指南

## API密钥配置

本项目使用阿里云DashScope API，需要配置环境变量才能正常运行。

### 1. 获取API密钥

1. 访问阿里云官网: https://www.aliyun.com/
2. 登录并进入DashScope控制台
3. 在API-KEY管理中创建新的API密钥

### 2. 环境变量设置

#### Windows系统
```cmd
# 设置API密钥（永久）
setx DASHSCOPE_API_KEY "your-api-key-here"

# 设置模型名称（可选，默认为qwen-vl-max）
setx MODEL_NAME "qwen3-vl-plus"
```

#### Linux/macOS系统
```bash
# 添加到~/.bashrc或~/.zshrc文件中
echo 'export DASHSCOPE_API_KEY="your-api-key-here"' >> ~/.bashrc
echo 'export MODEL_NAME="qwen3-vl-plus"' >> ~/.bashrc

# 重新加载配置
source ~/.bashrc
```

#### 使用.env文件
你也可以创建一个`.env`文件来配置：

```bash
# .env文件内容
DASHSCOPE_API_KEY=your-api-key-here
MODEL_NAME=qwen3-vl-plus
```

然后在Python代码中加载：
```python
import os
from dotenv import load_dotenv

load_dotenv()  # 加载.env文件

api_key = os.getenv("DASHSCOPE_API_KEY")
model_name = os.getenv("MODEL_NAME", "qwen-vl-max")
```

### 3. 验证配置

运行以下Python代码验证环境变量是否正确设置：

```python
import os

api_key = os.getenv("DASHSCOPE_API_KEY")
model_name = os.getenv("MODEL_NAME", "qwen-vl-max")

if api_key:
    print("✓ API密钥已配置")
    print(f"模型: {model_name}")
else:
    print("✗ 未找到API密钥，请设置DASHSCOPE_API_KEY环境变量")
```

### 4. 支持的模型

- `qwen-vl-max` - 最强视觉语言模型
- `qwen3-vl-plus` - 新一代视觉语言模型  
- `qwen-vl-plus` - 平衡性能的视觉语言模型

### 5. 安全建议

1. **不要**将API密钥硬编码到代码中
2. **不要**将包含API密钥的文件上传到公共仓库
3. 定期轮换API密钥
4. 限制API密钥的使用范围和权限

### 6. 故障排除

如果遇到API连接问题：

1. 检查环境变量是否正确设置
2. 确认API密钥是否有效
3. 检查网络连接
4. 验证API配额是否充足