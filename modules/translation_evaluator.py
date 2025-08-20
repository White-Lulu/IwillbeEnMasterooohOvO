# -*- coding: utf-8 -*-
"""
翻译评估模块
使用AI对用户翻译进行评估和反馈
"""

import re
import time
from pathlib import Path


def get_available_articles(articles_dir='articles'):
    """获取所有可用的文章文件"""
    article_files = list(Path(articles_dir).glob('*.md'))
    return article_files


def get_available_translations(translations_dir='translations'):
    """获取所有可用的翻译文件"""
    translation_files = list(Path(translations_dir).glob('*.txt'))
    return translation_files


def display_available_files(articles, translations):
    """显示可用的文章和翻译文件"""
    print("可用的文章文件：")
    if not articles:
        print("  没有找到文章文件")
    else:
        for i, article in enumerate(articles, 1):
            print(f"  {i}. {article.name}")
    
    print("\n可用的翻译文件：")
    if not translations:
        print("  没有找到翻译文件")
    else:
        for i, translation in enumerate(translations, 1):
            print(f"  {i}. {translation.name}")


def extract_article_content(article_path):
    """从文章文件中提取正文内容"""
    try:
        with open(article_path, 'r', encoding='utf-8') as f:
            article_content = f.read()
        
        # 提取英文正文
        content_match = re.search(r'## 正文\s*\n(.*?)(?=\n---|\Z)', article_content, re.DOTALL)
        if not content_match:
            raise ValueError("无法提取文章正文")
        
        english_text = content_match.group(1).strip()
        english_sentences = re.split(r'[.!?]+', english_text)
        english_sentences = [s.strip() for s in english_sentences if s.strip() and len(s.strip()) > 5]
        
        return english_sentences
    except Exception as e:
        raise Exception(f"读取文章文件时出错: {e}")


def read_user_translation(translation_path):
    """读取用户翻译文件"""
    try:
        with open(translation_path, 'r', encoding='utf-8') as f:
            user_translations = [line.strip() for line in f.readlines() if line.strip()]
        return user_translations
    except Exception as e:
        raise Exception(f"读取翻译文件时出错: {e}")


def evaluate_translation_with_ai(client, model, english_sentences, user_translations):
    """使用AI评估翻译质量"""
    
    print(f"原文句数: {len(english_sentences)}")
    print(f"翻译句数: {len(user_translations)}")
    
    # 构建评估提示词
    evaluation_pairs = []
    for i, (eng, trans) in enumerate(zip(english_sentences, user_translations), 1):
        evaluation_pairs.append(f"""
句子 {i}:
英文原文: {eng}
用户翻译: {trans}
""")
    
    prompt = f"""请作为专业的英语翻译评估专家，对以下英中翻译进行详细评估：

{chr(10).join(evaluation_pairs)}

请严格按照以下格式对每个句子（如果发现用户很可能只是漏了/多了一个句子/句子错位请自行调整）进行评估，并在重点内容使用markdown格式强调：

## **SENTENCE 1**

**原文**: [英文原文]
**用户翻译**: [用户的中文翻译]
**标准翻译**: [您认为的标准中文翻译]
***流畅翻译***: [更加流畅自然的中文翻译]
**评分**: [1-10分的评分]
**评价**: [详细的评价和改进建议，包括***词汇***、~~语法~~、*流畅度*等方面]

## **SENTENCE 2**

[继续同样格式...]

最后请提供整体评估：

## **整体评估**

**整体评分**: [1-10分]
**总体评价**: [整体翻译质量的综合评价]
***主要优点***: [列出翻译的主要优点]
~~主要问题~~: [列出需要改进的主要问题]
***改进建议***: [具体的改进建议]

**评分标准**：
- **9-10分**：翻译准确，语言流畅，完全符合中文表达习惯
- **7-8分**：翻译基本准确，语言较流畅，有轻微不当之处
- **5-6分**：翻译大意正确，但有明显的词汇或语法问题
- **3-4分**：翻译部分正确，存在较多错误
- **1-2分**：翻译错误较多，严重影响理解

请确保使用markdown格式对重点内容进行强调：**粗体**、***斜体加粗***、~~删除线~~、*斜体*。"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一位资深的英语翻译评估专家，具有丰富的翻译教学经验。请客观公正地评估翻译质量，并提供有建设性的改进建议。输出时请严格使用markdown格式对重点内容进行强调。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"评估翻译时出错: {e}")


def generate_evaluation_report(evaluation_result, article_title, translation_filename, model, results_dir='translation_results'):
    """生成评估报告并保存"""
    
    if not evaluation_result:
        raise ValueError("没有评估结果可生成报告")
    
    # 构建报告内容
    report_content = f"""# AI翻译评估报告

## 基本信息
- **原文章标题**: {article_title}
- **翻译文件**: {translation_filename}
- **评估时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **评估模型**: {model}

## 详细评估结果

{evaluation_result}

## 使用说明
本报告由AI自动生成，评估了您的英文翻译质量。请参考以下建议继续改进：

1. **词汇选择**: 注意英文单词的准确对应和语境适配
2. **语法结构**: 确保中文表达符合语法规范
3. **语言流畅度**: 让翻译读起来自然流畅
4. **文化适应**: 考虑中英文表达习惯的差异

继续练习，您的翻译水平会不断提高！

---
*本报告由IwillbeEnMasteroooh学习系统自动生成*
"""
    
    # 保存报告
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    report_filename = f"AI_translation_evaluation_{timestamp}.md"
    report_path = Path(results_dir) / report_filename
    
    # 确保目录存在
    Path(results_dir).mkdir(exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return report_path, report_content


def display_evaluation_preview(report_content, char_limit=500):
    """显示评估报告预览"""
    print("\n=== 报告预览 ===")
    preview = report_content[:char_limit] + "..." if len(report_content) > char_limit else report_content
    print(preview)


def find_matching_files(article_filename, translation_filename=None, articles_dir='articles', translations_dir='translations'):
    """根据文件名查找匹配的文章和翻译文件"""
    
    # 查找文章文件
    article_path = None
    articles = get_available_articles(articles_dir)
    
    for article in articles:
        if article_filename.lower() in article.name.lower() or article.name.lower() in article_filename.lower():
            article_path = article
            break
    
    if not article_path:
        raise FileNotFoundError(f"未找到匹配的文章文件: {article_filename}")
    
    # 查找翻译文件
    translation_path = None
    translations = get_available_translations(translations_dir)
    
    if translation_filename:
        # 指定了翻译文件名
        for translation in translations:
            if translation_filename.lower() in translation.name.lower() or translation.name.lower() in translation_filename.lower():
                translation_path = translation
                break
    else:
        # 自动查找匹配的翻译文件
        article_stem = article_path.stem
        for translation in translations:
            if article_stem.lower() in translation.name.lower():
                translation_path = translation
                break
    
    if not translation_path:
        raise FileNotFoundError(f"未找到匹配的翻译文件: {translation_filename or '自动匹配'}")
    
    return article_path, translation_path
