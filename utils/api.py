import os
import cv2
import time
import random
import base64
import common
import logging
from io import BytesIO
from PIL import Image
from mimetypes import guess_type
import openai
from openai import OpenAI

# 从环境变量获取API配置
api_key = os.getenv("DASHSCOPE_API_KEY", "")  # 从环境变量获取API密钥
if not api_key:
    # 如果环境变量未设置，提示用户设置
    print("警告: 未找到DASHSCOPE_API_KEY环境变量。请设置您的API密钥。")
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"  # 阿里云兼容OpenAI格式的API端点
model_name = os.getenv("MODEL_NAME", "qwen-vl-max")  # 使用环境变量或默认模型

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def answer_wrapper(messages, max_tks=2048, temperature=0.0, structured=False, tools=None):
    models = [model_name]  # 直接使用配置的模型名称
    max_trial = len(models)
    current = 0  # 直接使用第一个模型
    answer = None
    for i in range(max_trial):
        try:
            response = None
            if tools is not None:
                response = client.chat.completions.create(
                    model=models[current],
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tks,
                    response_format={"type": "json_object" if structured else "text"},
                    tools = tools,
                    tool_choice = "auto",
                )
                answer = response.choices[0].message
            else:
                response = client.chat.completions.create(
                    model=models[current],
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tks,
                    response_format={"type": "json_object" if structured else "text"},
                )
                answer = response.choices[0].message.content
        # https://github.com/openai/openai-python/blob/main/openai/error.py
        except openai.RateLimitError as e:
            logging.warning(f"RateLimitError: {e}. Retrying...")
            time.sleep(2)
        except openai.BadRequestError as e:
            if e.code == "content_filter":
                logging.warning(f"BadRequestError:content_filter: {e}. Skipping...")
                break
            elif e.code == "context_length_exceeded":
                logging.warning(f"BadRequestError:context_length_exceeded: {e}. Skipping...")
                break
            else:
                logging.warning(f"BadRequestError: {e}. Skipping...")
                break
        except openai.APITimeoutError as e:
            logging.warning(f"APITimeoutError: {e}. Retrying...")
            time.sleep(2)
        except openai.APIConnectionError as e:
            logging.warning(f"Connection aborted: {e}.")
            time.sleep(2)
        except Exception as e:
            if response is not None and response.choices[0].finish_reason == "content_filter":
                print(messages)
                print(response.choices[0].content_filter_results)
                logging.warning(f"{type(e).__name__}:content_filter: {e}. Skipping...")
                break
            else:
                logging.warning(f"{type(e).__name__}: {e}. Retrying...")
                time.sleep(2)
        if answer is not None:
            break
    return answer

def input_image_to_data_url(image_rgb_array, image_format="PNG") :
    # Convert numpy array to PIL Image
    image = Image.fromarray(image_rgb_array)
    # Convert the image to a bytes object
    buffered = BytesIO()
    image.save(buffered, format=image_format)
    # Guess the MIME type from the image format
    mime_type, _ = guess_type(f"dummy.{image_format.lower()}")
    if mime_type is None:
        mime_type = "application/octet-stream"  # Default MIME type if none is found
    # Encode the image to base64
    base64_encoded_data = base64.b64encode(buffered.getvalue()).decode("utf-8")
    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

def local_image_to_data_url(image_path):
    api_image_size_limit = 50 * 1024 * 1024  # 50MB limit (增加到50MB以支持更大的地质图文件)
    
    # Check file size
    file_size = os.path.getsize(image_path)
    if file_size >= api_image_size_limit:
        raise ValueError(f"图像文件太大 ({file_size/1024/1024:.1f}MB)，请使用小于50MB的图像文件")
    
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = "application/octet-stream"  # Default MIME type if none is found
    
    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode("utf-8")
    
    # Double check the encoded size
    encoded_size = len(base64_encoded_data)
    if encoded_size >= api_image_size_limit * 4/3:  # Base64 encoding increases size by ~33%
        raise ValueError(f"图像编码后太大，请使用更小的图像文件")
    
    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"