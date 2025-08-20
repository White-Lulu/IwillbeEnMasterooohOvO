# IwllbeEnMasterooohOvO - 英语学习系统

一个基于AI的英语学习系统，包含文章生成和翻译评估功能。

## 项目结构

```
English2/
├── 📁 modules/              # 核心Python模块文件夹
│   ├── 🐍 __init__.py       # 模块包初始化文件
│   ├── 🐍 config_manager.py # 配置管理模块
│   ├── 🐍 word_manager.py   # 单词列表管理模块  
│   ├── 🐍 article_generator.py # 文章生成模块
│   ├── 🐍 translation_evaluator.py # 翻译评估模块
│   └── 🐍 file_manager.py   # 文件管理工具模块
├── 📁 word_lists/           # 单词列表文件夹
├── 📁 articles/             # 生成的文章文件夹
├── 📁 translations/         # 用户翻译文件夹
├── 📁 translation_results/  # AI评估报告文件夹
├── 📄 config.json          # AI配置文件
├── 📓 article_generation.ipynb      # 文章生成系统
├── 📓 translation_evaluation.ipynb  # 翻译评估系统
└── 📖 README.md            # 项目说明文件
```

## 功能特点

### 文章生成系统
- 📝 基于完整单词列表生成定制化英语文章
- 🎯 支持自定义主题、体裁和难度
- 🔄 可设定每个目标单词最少出现次数（min_occurrences）
- ✨ 生成的文章中目标单词会自动加粗显示（**word**）
- 💾 自动保存为markdown格式，带时间戳避免文件覆盖

### 翻译评估系统
- 🤖 AI逐句评估翻译质量
- 📊 提供1-10分的详细评分
- 💡 标准翻译和流畅翻译对比
- 📋 生成完整的评估报告和改进建议

## 使用说明

### 1. 环境配置

确保安装了以下依赖：
```bash
pip install openai pathlib
```

### 2. 配置文件设置

在 `config.json` 中设置您的OpenAI API信息：
```json
{
    "openai": {
        "api_key": "your-openai-api-key",
        "model": "gpt-4o"
    }
}
```

### 3. 文章生成

1. 打开 `article_generation.ipynb`
2. 在参数设置部分修改：
   - `article_count`: 生成文章篇数
   - `article_topic`: 文章主题
   - `article_genre`: 文章体裁
   - `article_difficulty`: 文章难度
   - `word_list_index`: 选择的单词列表索引
   - `min_occurrences`: 每个单词最少出现次数
3. 依次运行所有单元格
4. 查看 `articles/` 文件夹中生成的文章

### 4. 翻译评估

1. 准备翻译文件：在 `translations/` 文件夹中创建 `.txt` 文件，每行一句翻译
2. 打开 `translation_evaluation.ipynb`
3. 在参数设置部分修改：
   - `article_filename`: 要评估的文章文件名关键词
   - `translation_filename`: 翻译文件名关键词（可选，留空自动匹配）
4. 依次运行所有单元格
5. 查看 `translation_results/` 文件夹中的评估报告

## 示例文件

### 单词列表文件格式 (word_lists/academic_words.txt)
```
abundant
accomplish
acquire
adapt
analyze
...
```

### 翻译文件格式 (translations/my_translation.txt)
```
技术创新依赖于当今世界丰富的资源。
利用这些资源，个人和公司可以取得显著成就。
为了从技术进步中获益，仔细分析趋势和数据是关键的。
...
```

## 技术支持

如有问题，请检查：
1. OpenAI API Key是否正确配置
2. 网络连接是否正常
3. 文件路径和格式是否正确
4. Python环境和依赖是否安装完整
