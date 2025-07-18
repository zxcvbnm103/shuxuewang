# 项目结构说明
# Project Structure Documentation

## 目录结构
```
shuxuewang/
├── math_search/                    # 主要功能模块
│   ├── __init__.py                # 模块入口
│   ├── models/                    # 数据模型
│   │   ├── __init__.py
│   │   ├── search_result.py       # 搜索结果模型
│   │   ├── search_history.py      # 搜索历史模型
│   │   └── math_term.py           # 数学术语模型
│   ├── interfaces/                # 核心接口定义
│   │   ├── __init__.py
│   │   ├── text_processor.py      # 文本处理器接口
│   │   ├── search_manager.py      # 搜索管理器接口
│   │   ├── relevance_calculator.py # 相关度计算器接口
│   │   └── ui_manager.py          # UI管理器接口
│   ├── database/                  # 数据库模块
│   │   ├── __init__.py
│   │   ├── connection.py          # 数据库连接管理器
│   │   └── history_repository.py  # 搜索历史数据仓库
│   ├── text_processing/           # 文本处理模块
│   │   └── __init__.py
│   ├── search_management/         # 搜索管理模块
│   │   └── __init__.py
│   ├── relevance_calculation/     # 相关度计算模块
│   │   └── __init__.py
│   ├── ui_components/             # 用户界面组件模块
│   │   └── __init__.py
│   └── config/                    # 配置模块
│       ├── __init__.py
│       └── settings.py            # 应用设置
├── tests/                         # 测试文件
│   ├── __init__.py
│   ├── test_models.py
│   └── demo_models.py
├── requirements.txt               # 项目依赖
├── .env.example                   # 环境变量模板
├── import streamlit as st.py      # 主应用文件
└── README.md                      # 项目说明
```

## 模块说明

### 数据模型 (models/)
- **SearchResult**: 搜索结果数据类，包含标题、URL、摘要、相关度等信息
- **SearchHistory**: 搜索历史数据类，记录查询文本、关键词、时间戳等
- **MathTerm**: 数学术语数据类，包含术语、LaTeX表示、分类、置信度等

### 核心接口 (interfaces/)
- **ITextProcessor**: 文本处理器接口，定义文本提取、数学术语识别等方法
- **ISearchManager**: 搜索管理器接口，定义网页搜索、学术搜索等方法
- **IRelevanceCalculator**: 相关度计算器接口，定义相关度计算和结果排序方法
- **IUIManager**: UI管理器接口，定义界面渲染和交互处理方法

### 数据库模块 (database/)
- **DatabaseConnection**: SQLite数据库连接管理器，提供线程安全的数据库连接和基础操作
- **HistoryRepository**: 搜索历史数据仓库，实现搜索历史记录的CRUD操作和查询功能

### 功能模块
- **text_processing/**: 文本处理功能实现（待后续任务实现）
- **search_management/**: 搜索管理功能实现（待后续任务实现）
- **relevance_calculation/**: 相关度计算功能实现（待后续任务实现）
- **ui_components/**: 用户界面组件实现（待后续任务实现）

### 配置模块 (config/)
- **Settings**: 应用配置类，包含搜索API、UI、缓存、数学处理等配置

## 依赖说明

### 核心依赖
- **streamlit**: Web应用框架
- **requests**: HTTP请求库
- **python-dotenv**: 环境变量管理

### 数学处理
- **sympy**: 符号数学库
- **latex2mathml**: LaTeX解析库

### 数据处理
- **pandas**: 数据分析库
- **numpy**: 数值计算库
- **scikit-learn**: 机器学习库（用于文本相似度计算）

### 开发工具
- **pytest**: 测试框架
- **black**: 代码格式化
- **flake8**: 代码检查
- **mypy**: 类型检查

## 配置说明

### 环境变量
复制 `.env.example` 为 `.env` 并配置以下变量：
- `GOOGLE_API_KEY`: Google Custom Search API密钥
- `GOOGLE_SEARCH_ENGINE_ID`: Google搜索引擎ID
- `BING_API_KEY`: Bing搜索API密钥（可选）

### 应用配置
通过 `Settings` 类可以配置：
- 搜索API参数
- UI界面参数
- 缓存设置
- 数学处理参数

## 设计原则

1. **模块化设计**: 各功能模块独立，便于维护和扩展
2. **接口驱动**: 通过接口定义规范，支持不同实现
3. **配置化**: 关键参数可配置，适应不同使用场景
4. **可测试性**: 清晰的模块划分便于单元测试和集成测试