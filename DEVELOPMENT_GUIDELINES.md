# 开发规范和流程指南

## 📋 目录
- [代码规范](#代码规范)
- [项目结构](#项目结构)
- [开发流程](#开发流程)
- [测试规范](#测试规范)
- [文档规范](#文档规范)
- [版本控制](#版本控制)
- [部署规范](#部署规范)

## 🎯 代码规范

### Python代码风格

#### 1. 基础规范
- **PEP 8**: 严格遵循Python官方代码风格指南
- **行长度**: 最大88字符（Black默认）
- **缩进**: 4个空格，不使用Tab
- **编码**: UTF-8，文件头部声明编码

```python
# -*- coding: utf-8 -*-
"""
模块文档字符串
Module docstring
"""

import os
from typing import List, Optional, Dict
from datetime import datetime
```

#### 2. 命名规范
```python
# 类名：大驼峰命名
class SearchResultManager:
    pass

# 函数和变量：小写+下划线
def calculate_relevance_score():
    search_results = []
    
# 常量：全大写+下划线
MAX_SEARCH_RESULTS = 100
API_TIMEOUT_SECONDS = 30

# 私有方法：前缀下划线
def _internal_helper_method():
    pass
```

#### 3. 类型注解
```python
from typing import List, Optional, Dict, Union

def process_search_results(
    results: List[SearchResult], 
    max_count: Optional[int] = None
) -> Dict[str, Union[int, float]]:
    """
    处理搜索结果
    
    Args:
        results: 搜索结果列表
        max_count: 最大结果数量
        
    Returns:
        处理统计信息
    """
    pass
```

#### 4. 文档字符串
```python
def calculate_relevance(query: str, result: SearchResult) -> float:
    """
    计算搜索结果的相关度评分
    
    Args:
        query: 用户查询文本
        result: 搜索结果对象
        
    Returns:
        相关度评分，范围0-1
        
    Raises:
        ValueError: 当输入参数无效时
        
    Example:
        >>> result = SearchResult(...)
        >>> score = calculate_relevance("数学", result)
        >>> assert 0 <= score <= 1
    """
    pass
```

### 代码质量工具

#### 1. 格式化工具
```bash
# 安装Black
pip install black

# 格式化代码
black math_search/ tests/

# 检查格式（CI中使用）
black --check math_search/ tests/
```

#### 2. 代码检查
```bash
# 安装flake8
pip install flake8

# 检查代码
flake8 math_search/ tests/

# 配置文件 .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,.venv
```

#### 3. 类型检查
```bash
# 安装mypy
pip install mypy

# 类型检查
mypy math_search/

# 配置文件 mypy.ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

## 🏗️ 项目结构

### 目录组织原则
1. **按功能模块划分**: 每个功能独立目录
2. **接口与实现分离**: interfaces/ 定义接口，具体模块实现
3. **测试代码对应**: 每个模块都有对应测试文件
4. **配置集中管理**: config/ 目录统一配置

### 新模块添加流程
```bash
# 1. 创建模块目录
mkdir math_search/new_module

# 2. 创建必要文件
touch math_search/new_module/__init__.py
touch math_search/new_module/implementation.py

# 3. 定义接口（如果需要）
touch math_search/interfaces/new_module_interface.py

# 4. 创建测试文件
touch tests/test_new_module.py
touch tests/demo_new_module.py

# 5. 更新文档
# 更新 PROJECT_STRUCTURE.md
# 更新 README.md
```

### 文件命名规范
```
math_search/
├── models/
│   ├── __init__.py           # 模块导出
│   ├── search_result.py      # 单一职责类
│   └── base_model.py         # 基础模型类
├── interfaces/
│   ├── __init__.py
│   └── text_processor.py     # 接口定义
├── text_processing/
│   ├── __init__.py
│   ├── processor.py          # 主要实现
│   └── utils.py              # 辅助工具
└── tests/
    ├── test_models.py        # 单元测试
    ├── demo_models.py        # 演示脚本
    └── conftest.py           # pytest配置
```

## 🔄 开发流程

### Git工作流

#### 1. 分支策略
```bash
# 主分支
main                    # 生产环境代码
develop                 # 开发环境代码

# 功能分支
feature/search-api      # 新功能开发
feature/ui-improvement  # 界面改进

# 修复分支
hotfix/critical-bug     # 紧急修复
bugfix/minor-issue      # 一般修复
```

#### 2. 提交规范
```bash
# 提交消息格式
<type>(<scope>): <subject>

<body>

<footer>

# 示例
feat(search): add relevance calculation algorithm

Implement TF-IDF based relevance scoring for search results.
- Add RelevanceCalculator class
- Include math domain boost functionality
- Add comprehensive unit tests

Closes #123
```

#### 3. 提交类型
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

### 开发步骤

#### 1. 功能开发流程
```bash
# 1. 创建功能分支
git checkout -b feature/new-feature

# 2. 开发前准备
# - 阅读相关文档
# - 理解需求和设计
# - 查看相关测试用例

# 3. 编写代码
# - 先写接口定义
# - 再写实现代码
# - 遵循TDD原则

# 4. 运行测试
pytest tests/ -v
black math_search/ tests/
flake8 math_search/ tests/
mypy math_search/

# 5. 提交代码
git add .
git commit -m "feat(module): add new feature"

# 6. 推送并创建PR
git push origin feature/new-feature
```

#### 2. 代码审查清单
- [ ] 代码符合规范（Black + Flake8 + MyPy通过）
- [ ] 有完整的单元测试
- [ ] 测试覆盖率 > 80%
- [ ] 有适当的文档字符串
- [ ] 错误处理完善
- [ ] 性能考虑合理
- [ ] 向后兼容性

## 🧪 测试规范

### 测试结构

#### 1. 测试文件组织
```
tests/
├── __init__.py
├── conftest.py              # pytest配置和fixtures
├── test_models.py           # 数据模型测试
├── test_database.py         # 数据库操作测试
├── test_search_manager.py   # 搜索管理测试
├── demo_models.py           # 演示脚本
└── integration/             # 集成测试
    └── test_full_workflow.py
```

#### 2. 测试命名规范
```python
class TestSearchResult:
    """SearchResult 数据模型测试"""
    
    def test_valid_creation(self):
        """测试有效对象创建"""
        pass
    
    def test_invalid_relevance_score_raises_error(self):
        """测试无效相关度评分抛出异常"""
        pass
    
    def test_serialization_roundtrip(self):
        """测试序列化往返转换"""
        pass
```

#### 3. 测试数据管理
```python
# conftest.py
import pytest
import tempfile
from math_search.database import DatabaseConnection

@pytest.fixture
def temp_db():
    """临时数据库fixture"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    db = DatabaseConnection(db_path)
    yield db
    
    db.close_connection()
    os.unlink(db_path)

@pytest.fixture
def sample_search_result():
    """示例搜索结果fixture"""
    return SearchResult(
        title="测试标题",
        url="https://example.com",
        snippet="测试摘要",
        source="测试源",
        relevance_score=0.8,
        timestamp=datetime.now(),
        math_content_detected=True
    )
```

### 测试类型

#### 1. 单元测试
```python
def test_calculate_relevance_basic():
    """测试基础相关度计算"""
    calculator = RelevanceCalculator()
    result = SearchResult(...)
    
    score = calculator.calculate_relevance("数学", result)
    
    assert 0 <= score <= 1
    assert isinstance(score, float)
```

#### 2. 集成测试
```python
def test_full_search_workflow():
    """测试完整搜索流程"""
    # 1. 创建搜索管理器
    manager = SearchManager()
    
    # 2. 执行搜索
    results = manager.search("线性代数")
    
    # 3. 验证结果
    assert len(results) > 0
    assert all(isinstance(r, SearchResult) for r in results)
    
    # 4. 验证历史记录
    history = manager.get_search_history()
    assert len(history) > 0
```

#### 3. 性能测试
```python
import time

def test_search_performance():
    """测试搜索性能"""
    manager = SearchManager()
    
    start_time = time.time()
    results = manager.search("数学")
    end_time = time.time()
    
    # 搜索应在5秒内完成
    assert end_time - start_time < 5.0
    assert len(results) > 0
```

### 测试运行

#### 1. 本地测试
```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_models.py -v

# 运行特定测试方法
pytest tests/test_models.py::TestSearchResult::test_valid_creation -v

# 生成覆盖率报告
pytest tests/ --cov=math_search --cov-report=html
```

#### 2. CI/CD测试
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=math_search --cov-report=xml
    
    - name: Code quality
      run: |
        black --check math_search/ tests/
        flake8 math_search/ tests/
        mypy math_search/
```

## 📚 文档规范

### 文档类型

#### 1. 代码文档
- **模块文档**: 每个模块的`__init__.py`包含模块说明
- **类文档**: 类的用途、属性、方法说明
- **函数文档**: 参数、返回值、异常、示例

#### 2. 项目文档
- **README.md**: 项目概述、安装、使用
- **FAQ.md**: 常见问题和解决方案
- **DEVELOPMENT_GUIDELINES.md**: 开发规范
- **PROJECT_STRUCTURE.md**: 项目结构说明

#### 3. API文档
```python
def search_math_content(
    query: str, 
    sources: List[str] = None,
    max_results: int = 10
) -> List[SearchResult]:
    """
    搜索数学相关内容
    
    这个函数会在多个数据源中搜索与查询相关的数学内容，
    并返回按相关度排序的结果列表。
    
    Args:
        query: 搜索查询字符串，支持中英文和数学术语
        sources: 搜索源列表，默认使用所有可用源
            可选值: ['google', 'bing', 'arxiv']
        max_results: 最大返回结果数，默认10个
    
    Returns:
        搜索结果列表，按相关度降序排列
        每个结果包含标题、URL、摘要等信息
    
    Raises:
        ValueError: 当query为空或max_results无效时
        APIError: 当所有搜索源都不可用时
        
    Example:
        >>> results = search_math_content("线性代数", max_results=5)
        >>> len(results) <= 5
        True
        >>> all(r.relevance_score >= 0 for r in results)
        True
        
    Note:
        - 函数会自动识别查询中的数学术语
        - 结果会根据数学领域相关性进行加权
        - 搜索历史会自动保存到数据库
    """
    pass
```

### 文档更新流程

#### 1. 代码变更时
- 更新相关的文档字符串
- 更新README中的功能列表
- 更新API文档

#### 2. 新功能添加时
- 在README中添加功能说明
- 创建使用示例
- 更新项目结构文档

#### 3. 问题修复时
- 在FAQ中添加相关问题
- 更新故障排除指南

## 🔒 版本控制

### 版本号规范

#### 语义化版本 (Semantic Versioning)
```
MAJOR.MINOR.PATCH

例如: 1.2.3
- MAJOR: 不兼容的API修改
- MINOR: 向后兼容的功能性新增
- PATCH: 向后兼容的问题修正
```

#### 版本标签
```bash
# 创建版本标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 查看版本历史
git tag -l
```

### 变更日志

#### CHANGELOG.md格式
```markdown
# 变更日志

## [1.2.0] - 2024-01-15

### 新增
- 添加相关度计算算法
- 支持arXiv搜索源
- 新增搜索历史统计功能

### 修改
- 优化数据库查询性能
- 改进错误处理机制

### 修复
- 修复中文关键词存储问题
- 解决并发访问数据库的bug

### 移除
- 移除已废弃的旧API接口
```

## 🚀 部署规范

### 环境配置

#### 1. 开发环境
```bash
# 本地开发配置
cp .env.example .env.dev
# 编辑开发环境配置

# 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 2. 测试环境
```bash
# 测试环境配置
cp .env.example .env.test
# 配置测试API密钥和数据库

# 运行测试套件
pytest tests/ --cov=math_search
```

#### 3. 生产环境
```bash
# 生产环境配置
cp .env.example .env.prod
# 配置生产API密钥和优化参数

# 性能优化设置
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
export STREAMLIT_SERVER_ENABLE_CORS=false
```

### 部署检查清单

#### 部署前检查
- [ ] 所有测试通过
- [ ] 代码质量检查通过
- [ ] 文档更新完成
- [ ] 环境变量配置正确
- [ ] 数据库迁移脚本准备
- [ ] 性能测试通过

#### 部署后验证
- [ ] 应用正常启动
- [ ] 核心功能可用
- [ ] 数据库连接正常
- [ ] API接口响应正常
- [ ] 日志记录正常

---

## 📞 支持和反馈

如果对开发规范有疑问或建议：

1. 查看现有代码示例
2. 参考测试用例
3. 创建Issue讨论
4. 提交改进建议

**记住**: 好的代码不仅要能工作，还要易于理解、维护和扩展。