# -*- coding: utf-8 -*-
"""
配置管理模块
用于加载和管理OpenAI API配置
"""

import json
import os
from openai import OpenAI


def load_config(config_path='config.json'):
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError("配置文件 {} 不存在".format(config_path))
    except json.JSONDecodeError:
        raise ValueError("配置文件 {} 格式错误".format(config_path))


def init_openai_client(config):
    """初始化OpenAI客户端"""
    try:
        client = OpenAI(api_key=config['openai']['api_key'])
        model = config['openai']['model']
        return client, model
    except KeyError as e:
        raise KeyError(f"配置文件缺少必要字段: {e}")


def setup_environment():
    """设置项目环境，创建必要的文件夹"""
    folders = ['word_lists', 'articles', 'translations', 'translation_results']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    
    return folders
