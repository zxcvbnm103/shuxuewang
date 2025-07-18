# 🧮 数学笔记智能搜索系统

专为数学学习设计的智能笔记和搜索工具，支持LaTeX公式编辑、数学术语识别和多源搜索整合。

## ✨ 主要功能

- 📝 **数学笔记编辑器** - 支持Markdown和LaTeX公式的实时编辑预览
- 🔍 **智能搜索功能** - 多源搜索整合，自动识别数学内容
- 📊 **搜索历史管理** - 完整的搜索记录和统计分析
- 🧮 **数学内容识别** - 自动检测和处理数学术语、公式

## 🚀 快速体验

### 一键启动
```bash
# 克隆项目
git clone <repository-url>
cd shuxuewang

# 安装依赖
pip install -r requirements.txt

# 启动应用
streamlit run app.py
```

### 在线演示
启动后访问：http://localhost:8501

## 🛠️ 详细安装

### 环境要求
- Python 3.8+
- 现代浏览器 (Chrome, Firefox, Safari)

### 完整安装步骤

1. **创建虚拟环境**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量 (可选)**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件添加搜索API密钥以获得真实搜索结果
   ```

4. **启动应用**
   ```bash
   streamlit run app.py
   ```

### 环境变量配置

在 `.env` 文件中配置以下变量：

```env
# Google搜索API (必需)
GOOGLE_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id

# Bing搜索API (可选)
BING_API_KEY=your_bing_api_key
```

## 🧪 测试

### 运行所有测试
```bash
pytest tests/ -v
```

### 运行特定测试
```bash
# 测试数据模型
pytest tests/test_models.py -v

# 测试数据库操作
pytest tests/test_database.py -v

# 运行演示脚本
python tests/demo_models.py
python tests/demo_database.py
```

### 测试覆盖率
```bash
pytest tests/ --cov=math_search --cov-report=html
```

## 📁 项目结构

```
shuxuewang/
├── math_search/                    # 主要功能模块
│   ├── models/                    # 数据模型 ✅
│   │   ├── search_result.py       # 搜索结果模型
│   │   ├── search_history.py      # 搜索历史模型
│   │   └── math_term.py           # 数学术语模型
│   ├── database/                  # 数据库模块 ✅
│   │   ├── connection.py          # 数据库连接管理
│   │   └── history_repository.py  # 搜索历史仓库
│   ├── config/                    # 配置模块 ✅
│   │   └── settings.py            # 应用设置
│   ├── interfaces/                # 接口定义 ✅
│   │   ├── text_processor.py      # 文本处理接口
│   │   ├── relevance_calculator.py # 相关度计算接口
│   │   └── ...
│   ├── text_processing/           # 文本处理 🔄
│   ├── search_management/         # 搜索管理 🔄
│   ├── relevance_calculation/     # 相关度计算 🔄
│   └── ui_components/             # UI组件 🔄
├── tests/                         # 测试文件 ✅
│   ├── test_models.py            # 模型测试
│   ├── test_database.py          # 数据库测试
│   └── demo_*.py                 # 演示脚本
├── requirements.txt               # 项目依赖
├── .env.example                   # 环境变量模板
└── README.md                      # 项目说明
```

## 🔧 开发指南

### 代码规范
- 使用 `black` 进行代码格式化
- 使用 `flake8` 进行代码检查
- 使用 `mypy` 进行类型检查

```bash
# 格式化代码
black math_search/ tests/

# 检查代码
flake8 math_search/ tests/

# 类型检查
mypy math_search/
```

### 添加新功能
1. 在相应的接口文件中定义接口
2. 在对应模块中实现功能
3. 编写单元测试
4. 更新文档

## 📊 性能特性

- **数据库**: SQLite，支持并发访问和事务管理
- **缓存**: 可配置的搜索结果缓存机制
- **内存**: 优化的数据结构，支持大量搜索历史
- **响应**: 异步搜索和实时结果更新

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如果您遇到问题或有建议，请：
1. 查看 [FAQ文档](FAQ.md)
2. 创建 [Issue](../../issues)
3. 查看 [开发规范](DEVELOPMENT_GUIDELINES.md)

---

**状态说明**:
- ✅ 已完成
- 🔄 开发中
- ⏳ 计划中
