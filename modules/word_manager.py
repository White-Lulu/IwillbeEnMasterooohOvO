# -*- coding: utf-8 -*-
"""
单词列表管理模块
用于读取和管理单词列表文件
"""

from pathlib import Path


def get_available_word_lists(word_lists_dir='word_lists'):
    """获取所有可用的单词列表文件"""
    word_list_files = list(Path(word_lists_dir).glob('*.txt'))
    return word_list_files


def read_word_list(file_path):
    """读取单词列表文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f.readlines() if line.strip()]
        return words
    except FileNotFoundError:
        raise FileNotFoundError(f"单词列表文件 {file_path} 不存在")
    except Exception as e:
        raise Exception(f"读取单词列表文件时出错: {e}")


def display_word_lists(word_lists):
    """显示可用的单词列表"""
    if not word_lists:
        print("没有找到单词列表文件")
        return None
    
    print("可用的单词列表：")
    for i, word_list in enumerate(word_lists, 1):
        print(f"{i}. {word_list.name}")
    
    return word_lists


def select_word_list(word_lists, index=0):
    """选择单词列表"""
    if not word_lists or index >= len(word_lists):
        return None
    
    selected = word_lists[index]
    words = read_word_list(selected)
    
    print(f"已选择单词列表: {selected.name}")
    print(f"包含 {len(words)} 个单词")
    print(f"单词列表: {words}")
    
    return selected, words
