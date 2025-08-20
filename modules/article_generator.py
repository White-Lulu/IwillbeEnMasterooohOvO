# -*- coding: utf-8 -*-
"""
文章生成模块
使用AI生成基于单词列表的英语文章，支持单词标粗
"""

import re
import time
from pathlib import Path


def generate_articles_with_ai(client, model, words, count, topic, genre, difficulty, min_occurrences=2):
    """使用AI生成文章，支持单词标粗和最小出现次数设置"""
    
    prompt = f"""Please write {count} English articles based on the following requirements:

Target words that MUST be included: {', '.join(words)}
Topic: {topic}
Genre: {genre}
Difficulty: {difficulty}

Requirements:
1. Across ALL {count} articles, each target word must appear at least {min_occurrences} times total
2. Write in clear, educational English
3. Make the target words BOLD using **word** format in the content
4. Ensure incorporating all target words

Output format (VERY IMPORTANT):
Please use this EXACT format for each article:

=== ARTICLE 1 ===
Title: [Article title here]
Abstract: [Brief summary in 30-50 words]
---
[Article content here with **target words** in bold]
=== END ARTICLE 1 ===

=== ARTICLE 2 ===
Title: [Article title here] 
Abstract: [Brief summary in 30-50 words]
---
[Article content here with **target words** in bold]
=== END ARTICLE 2 ===

Make sure to use **bold** formatting for all target words when they appear in the content."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert English teacher. Create educational articles that naturally incorporate the specified vocabulary words with bold formatting. Follow the exact format requested."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.6
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"生成文章时出错: {e}")
        return None


def parse_and_save_articles(ai_output, word_list_name, articles_dir='articles'):
    """解析AI输出并保存为独立的markdown文件"""
    
    if not ai_output:
        print("没有AI输出内容可解析")
        return []
    
    print("\n=== AI输出内容预览 ===")
    preview = ai_output[:500] + "..." if len(ai_output) > 500 else ai_output
    print(preview)
    print("=" * 50)
    
    saved_articles = []
    
    # 方法1: 使用=== ARTICLE X ===格式
    pattern1 = r'=== ARTICLE (\d+) ===(.*?)=== END ARTICLE \1 ==='
    matches1 = re.findall(pattern1, ai_output, re.DOTALL | re.IGNORECASE)
    
    if matches1:
        print(f"使用格式1解析到 {len(matches1)} 篇文章")
        for num, content in matches1:
            article_info = _parse_single_article(content, num, word_list_name, articles_dir)
            if article_info:
                saved_articles.append(article_info)
    
    # 如果格式1失败，尝试其他方法
    if not saved_articles:
        print("格式1解析失败，尝试备用方法...")
        saved_articles = _fallback_parse_articles(ai_output, word_list_name, articles_dir)
    
    return saved_articles


def _parse_single_article(content, num, word_list_name, articles_dir):
    """解析单篇文章"""
    # 解析标题和摘要
    title_match = re.search(r'Title:\s*(.*?)(?:\n|Abstract:)', content, re.IGNORECASE)
    abstract_match = re.search(r'Abstract:\s*(.*?)(?:\n|---)', content, re.IGNORECASE | re.DOTALL)
    
    title = title_match.group(1).strip() if title_match else f"Article {num}"
    abstract = abstract_match.group(1).strip() if abstract_match else "AI generated article"
    
    # 提取正文（---后的内容）
    content_match = re.search(r'---\s*(.*)', content, re.DOTALL)
    article_content = content_match.group(1).strip() if content_match else content.strip()
    
    # 清理内容
    article_content = re.sub(r'Title:.*?\n', '', article_content, flags=re.IGNORECASE)
    article_content = re.sub(r'Abstract:.*?\n', '', article_content, flags=re.IGNORECASE)
    article_content = re.sub(r'---+', '', article_content).strip()
    
    # 保存文章
    safe_title = re.sub(r'[^\w\s-]', '', title).strip()
    safe_title = re.sub(r'[-\s]+', '-', safe_title)[:50]  # 限制长度
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filename = f"{word_list_name}-{safe_title}-{timestamp}.md"
    
    markdown_content = f"""# {title}

## 摘要
{abstract}

## 正文
{article_content}

---
*本文基于单词列表 "{word_list_name}" 生成*
"""
    
    file_path = Path(articles_dir) / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"已保存文章: {filename}")
    
    return {
        'title': title,
        'abstract': abstract,
        'filename': filename,
        'path': file_path
    }


def _fallback_parse_articles(ai_output, word_list_name, articles_dir):
    """备用解析方法"""
    saved_articles = []
    
    # 按段落分割并创建文章
    paragraphs = [p.strip() for p in ai_output.split('\n\n') if p.strip()]
    if len(paragraphs) >= 2:
        # 将段落分组为文章
        mid = len(paragraphs) // 2
        article_groups = [
            ('\n\n'.join(paragraphs[:mid]), "Technology and Innovation Article 1"),
            ('\n\n'.join(paragraphs[mid:]), "Technology and Innovation Article 2")
        ]
        
        for i, (content, title) in enumerate(article_groups, 1):
            safe_title = re.sub(r'[^\w\s-]', '', title).strip()
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"{word_list_name}-{safe_title}-{timestamp}.md"
            
            markdown_content = f"""# {title}

## 摘要
AI生成的关于技术创新的文章

## 正文
{content}

---
*本文基于单词列表 "{word_list_name}" 生成*
"""
            
            file_path = Path(articles_dir) / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            saved_articles.append({
                'title': title,
                'abstract': "AI生成的关于技术创新的文章",
                'filename': filename,
                'path': file_path
            })
            
            print(f"已保存文章 {i}: {filename}")
    
    return saved_articles


def display_generated_articles(saved_articles):
    """显示生成的文章预览"""
    if not saved_articles:
        print("暂无已生成的文章")
        return
    
    print("\n=== 文章预览 ===")
    for i, article in enumerate(saved_articles, 1):
        print(f"\n📖 文章 {i}: {article['title']}")
        print(f"摘要: {article['abstract']}")
        print(f"文件: {article['filename']}")
        print("-" * 50)


def check_word_coverage(saved_articles, target_words, min_occurrences=2):
    """检查目标单词的覆盖情况"""
    print("\n=== 单词覆盖检查 ===")
    word_counts = {word.lower(): 0 for word in target_words}
    
    for article in saved_articles:
        try:
            with open(article['path'], 'r', encoding='utf-8') as f:
                content = f.read().lower()
                for word in target_words:
                    count = content.count(word.lower())
                    word_counts[word.lower()] += count
        except Exception as e:
            print(f"检查文章 {article['filename']} 时出错: {e}")
    
    print(f"目标出现次数: {min_occurrences}")
    print("单词覆盖情况:")
    
    insufficient_words = []
    for word, count in word_counts.items():
        status = "✅" if count >= min_occurrences else "❌"
        print(f"  {status} {word}: {count} 次")
        if count < min_occurrences:
            insufficient_words.append(word)
    
    if insufficient_words:
        print(f"\n⚠️ 以下单词出现次数不足: {insufficient_words}")
        return False
    else:
        print(f"\n🎉 所有单词都满足最少出现 {min_occurrences} 次的要求！")
        return True
