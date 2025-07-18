# 常见问题解答 (FAQ)

## 🚨 安装和环境问题

### Q1: 安装依赖时出现错误
**问题**: `pip install -r requirements.txt` 失败

**解决方案**:
```bash
# 1. 升级pip
python -m pip install --upgrade pip

# 2. 如果是网络问题，使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 3. 如果是特定包问题，逐个安装
pip install streamlit requests python-dotenv
pip install sympy latex2mathml pandas numpy
pip install pytest black flake8 mypy
```

### Q2: Python版本兼容性问题
**问题**: 代码在旧版本Python上运行失败

**解决方案**:
- 确保使用Python 3.8或更高版本
- 检查Python版本: `python --version`
- 如果需要多版本管理，推荐使用pyenv或conda

### Q3: 虚拟环境问题
**问题**: 虚拟环境创建或激活失败

**解决方案**:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# 如果权限问题
sudo python3 -m venv .venv
```

## 🔧 配置问题

### Q4: 环境变量配置错误
**问题**: API密钥配置不生效

**解决方案**:
1. 确保`.env`文件在项目根目录
2. 检查文件格式，不要有多余空格
3. 重启应用以加载新配置
```env
# 正确格式
GOOGLE_API_KEY=your_actual_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id

# 错误格式（有空格）
GOOGLE_API_KEY = your_actual_api_key
```

### Q5: 数据库文件权限问题
**问题**: SQLite数据库创建失败

**解决方案**:
```bash
# 检查目录权限
ls -la

# 修改权限（Linux/Mac）
chmod 755 .
chmod 644 *.db

# Windows - 以管理员身份运行
```

## 💾 数据库问题

### Q6: 数据库连接错误
**问题**: `sqlite3.OperationalError: database is locked`

**解决方案**:
1. 确保没有其他进程占用数据库
2. 检查数据库文件权限
3. 使用连接池管理连接
```python
# 正确的连接管理
with DatabaseConnection() as db:
    # 执行操作
    pass
```

### Q7: 搜索历史数据丢失
**问题**: 重启应用后搜索历史消失

**解决方案**:
1. 检查数据库文件是否存在
2. 验证数据库表结构
```bash
# 检查数据库
sqlite3 math_search.db ".tables"
sqlite3 math_search.db ".schema search_history"
```

### Q8: 中文数据存储问题
**问题**: 中文关键词保存后显示乱码

**解决方案**:
- 确保数据库连接使用UTF-8编码
- 检查JSON序列化设置
```python
# 正确的中文处理
json.dumps(keywords, ensure_ascii=False)
```

## 🧪 测试问题

### Q9: 测试运行失败
**问题**: `pytest` 命令找不到模块

**解决方案**:
```bash
# 1. 确保在项目根目录
cd shuxuewang

# 2. 安装测试依赖
pip install pytest pytest-cov pytest-mock

# 3. 设置Python路径
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 4. 运行测试
python -m pytest tests/ -v
```

### Q10: 临时文件清理问题
**问题**: 测试后留下临时数据库文件

**解决方案**:
- 测试会自动清理临时文件
- 如果手动清理: `rm -f *.db test_*.db`
- 检查测试代码中的`teardown_method`

## 📊 数据验证问题

### Q11: 数据模型验证错误
**问题**: `ValueError: 相关度评分必须在0-1之间`

**解决方案**:
```python
# 检查数据范围
search_result = SearchResult(
    title="标题",
    url="https://example.com",
    snippet="摘要",
    source="来源",
    relevance_score=0.85,  # 确保在0-1之间
    timestamp=datetime.now(),
    math_content_detected=True
)
```

### Q12: 空值验证问题
**问题**: `ValueError: 标题和URL不能为空`

**解决方案**:
- 确保必填字段不为空
- 在创建对象前进行数据验证
```python
# 数据验证示例
if not title or not url:
    raise ValueError("标题和URL不能为空")
```

## 🔍 搜索功能问题

### Q13: API配额超限
**问题**: Google搜索API返回配额错误

**解决方案**:
1. 检查API使用量
2. 配置多个API密钥轮换
3. 实现缓存减少API调用
4. 考虑使用免费的arXiv API作为补充

### Q14: 搜索结果为空
**问题**: 搜索返回0个结果

**解决方案**:
1. 检查网络连接
2. 验证API密钥有效性
3. 检查搜索关键词是否合理
4. 查看API响应日志

## 🎨 界面问题

### Q15: Streamlit应用启动失败
**问题**: `streamlit run` 命令报错

**解决方案**:
```bash
# 1. 检查Streamlit版本
streamlit --version

# 2. 重新安装Streamlit
pip uninstall streamlit
pip install streamlit>=1.28.0

# 3. 使用完整路径
streamlit run "import streamlit as st.py"
```

### Q16: 页面显示异常
**问题**: 界面布局错乱或组件不显示

**解决方案**:
1. 清除浏览器缓存
2. 检查Streamlit版本兼容性
3. 重启Streamlit服务
4. 检查控制台错误信息

## 🔧 开发问题

### Q17: 代码格式化问题
**问题**: `black` 格式化后代码风格不一致

**解决方案**:
```bash
# 统一格式化
black --line-length 88 math_search/ tests/

# 检查格式
black --check math_search/ tests/

# 配置文件 pyproject.toml
[tool.black]
line-length = 88
target-version = ['py38']
```

### Q18: 类型检查错误
**问题**: `mypy` 报告类型错误

**解决方案**:
```python
# 添加类型注解
from typing import List, Optional, Dict

def process_results(results: List[SearchResult]) -> Dict[str, int]:
    return {"count": len(results)}

# 忽略特定错误
# type: ignore
```

## 📈 性能问题

### Q19: 数据库查询慢
**问题**: 搜索历史查询响应缓慢

**解决方案**:
1. 检查数据库索引
2. 限制查询结果数量
3. 定期清理旧数据
```sql
-- 检查索引
.indices search_history

-- 创建索引
CREATE INDEX idx_search_history_timestamp ON search_history(timestamp);
```

### Q20: 内存使用过高
**问题**: 应用占用内存过多

**解决方案**:
1. 实现结果分页
2. 清理不需要的缓存
3. 优化数据结构
4. 定期重启应用

## 🛠️ 故障排除步骤

### 通用排查流程
1. **检查日志**: 查看控制台输出和错误信息
2. **验证环境**: 确认Python版本、依赖版本
3. **测试连接**: 验证数据库和API连接
4. **重现问题**: 使用最小示例重现问题
5. **查看文档**: 参考相关模块的文档和测试用例

### 获取帮助
如果以上解决方案都无法解决问题：

1. **查看测试用例**: `tests/` 目录下的示例代码
2. **运行演示脚本**: `python tests/demo_*.py`
3. **创建Issue**: 提供详细的错误信息和环境信息
4. **查看开发指南**: `DEVELOPMENT_GUIDELINES.md`

---

**提示**: 遇到问题时，首先查看相关的测试文件，它们通常包含正确的使用示例。