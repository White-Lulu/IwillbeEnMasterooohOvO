# -*- coding: utf-8 -*-
"""
文件管理工具模块
用于管理项目文件和目录
"""

import shutil
import time
from pathlib import Path


def clean_directory(directory_path):
    """清空指定目录"""
    if Path(directory_path).exists():
        shutil.rmtree(directory_path)
    Path(directory_path).mkdir(exist_ok=True)
    print(f"已清空目录: {directory_path}")


def ensure_directory(directory_path):
    """确保目录存在，不删除现有文件"""
    Path(directory_path).mkdir(exist_ok=True)
    print(f"已确保目录存在: {directory_path}")


def backup_existing_files(directory_path, backup_suffix="_backup"):
    """备份现有文件"""
    if not Path(directory_path).exists():
        return
    
    files = list(Path(directory_path).glob('*'))
    if files:
        backup_dir = Path(directory_path + backup_suffix)
        backup_dir.mkdir(exist_ok=True)
        
        for file in files:
            if file.is_file():
                backup_path = backup_dir / file.name
                # 如果备份文件已存在，添加时间戳
                if backup_path.exists():
                    timestamp = time.strftime('%Y%m%d_%H%M%S')
                    backup_path = backup_dir / f"{file.stem}_{timestamp}{file.suffix}"
                
                shutil.copy2(file, backup_path)
        
        print(f"已备份 {len(files)} 个文件到 {backup_dir}")


def check_project_structure():
    """检查项目文件结构完整性"""
    results = {}
    
    # 检查各个文件夹的文件
    results['word_lists'] = len(list(Path('word_lists').glob('*.txt')))
    results['articles'] = len(list(Path('articles').glob('*.md')))
    results['translations'] = len(list(Path('translations').glob('*.txt')))
    results['translation_results'] = len(list(Path('translation_results').glob('*.md')))
    results['config'] = Path('config.json').exists()
    
    return results


def display_project_status(results):
    """显示项目状态"""
    print("📊 项目文件统计:")
    print(f"   📝 单词列表文件: {results['word_lists']} 个")
    print(f"   📖 生成的文章: {results['articles']} 个")
    print(f"   ✍️ 翻译文件: {results['translations']} 个")
    print(f"   📋 评估报告: {results['translation_results']} 个")
    
    print("\n✅ 项目结构完整性:")
    print(f"   - 配置文件: {'✓' if results['config'] else '✗'}")
    print(f"   - 单词列表: {'✓' if results['word_lists'] > 0 else '✗'}")
    print(f"   - 生成文章: {'✓' if results['articles'] > 0 else '✗'}")
    print(f"   - 用户翻译: {'✓' if results['translations'] > 0 else '✗'}")
    print(f"   - AI评估报告: {'✓' if results['translation_results'] > 0 else '✗'}")
    
    return all([
        results['config'],
        results['word_lists'] > 0,
        results['articles'] > 0,
        results['translations'] > 0,
        results['translation_results'] > 0
    ])


def list_files_in_directory(directory_path, pattern='*'):
    """列出目录中的文件"""
    try:
        files = list(Path(directory_path).glob(pattern))
        return files
    except Exception as e:
        print(f"列出文件时出错: {e}")
        return []


def extract_title_from_article(article_path):
    """从文章文件中提取标题"""
    try:
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取第一行的标题（去掉#标记）
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                title = line.strip().lstrip('#').strip()
                return title
        
        # 如果没有找到标题，使用文件名
        return article_path.stem
    except Exception:
        return article_path.stem
