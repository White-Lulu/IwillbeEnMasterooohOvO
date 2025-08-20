# -*- coding: utf-8 -*-
"""
English2 学习系统模块包

包含以下模块:
- config_manager: 配置管理和API客户端初始化
- word_manager: 单词列表管理
- article_generator: AI文章生成
- translation_evaluator: AI翻译评估
- file_manager: 文件管理工具
"""

__version__ = "1.0.0"
__author__ = "English2 Learning System"

# 导入主要模块
from .config_manager import load_config, init_openai_client, setup_environment
from .word_manager import get_available_word_lists, display_word_lists, select_word_list
from .article_generator import generate_articles_with_ai, parse_and_save_articles, display_generated_articles
from .translation_evaluator import (
    get_available_articles, get_available_translations, 
    evaluate_translation_with_ai, generate_evaluation_report
)
from .file_manager import ensure_directory, check_project_structure, display_project_status

__all__ = [
    'load_config', 'init_openai_client', 'setup_environment',
    'get_available_word_lists', 'display_word_lists', 'select_word_list', 
    'generate_articles_with_ai', 'parse_and_save_articles', 'display_generated_articles',
    'get_available_articles', 'get_available_translations',
    'evaluate_translation_with_ai', 'generate_evaluation_report',
    'ensure_directory', 'check_project_structure', 'display_project_status'
]
