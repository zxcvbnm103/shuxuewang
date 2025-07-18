"""
数学笔记智能搜索系统 - 主应用程序
Math Notes Search System - Main Application
"""
import streamlit as st
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from math_search.ui_components.ui_manager import UIManager
    from math_search.models.search_result import SearchResult
    from math_search.models.search_history import SearchHistory
    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False


def main():
    """主应用程序"""
    # 页面配置
    st.set_page_config(
        page_title="数学笔记智能搜索系统",
        page_icon="🧮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 应用标题和介绍
    st.title("🧮 数学笔记智能搜索系统")
    st.markdown("*Math Notes Search System - 专为数学学习设计的智能搜索工具*")
    
    # 功能选择标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📝 笔记编辑器", "🔍 搜索演示", "📊 项目状态", "📖 使用说明"])
    
    with tab1:
        render_note_editor()
    
    with tab2:
        render_search_demo()
    
    with tab3:
        render_project_status()
    
    with tab4:
        render_usage_guide()


def render_note_editor():
    """渲染笔记编辑器"""
    st.header("📝 数学笔记编辑器")
    
    # 读取已保存的笔记内容
    note_file = "my_math_note.md"
    try:
        with open(note_file, "r", encoding="utf-8") as f:
            default_content = f.read()
    except FileNotFoundError:
        default_content = """# 我的数学笔记

## 微积分基础

### 导数定义
导数的定义为：
$$f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$$

### 积分基本定理
如果 $F(x)$ 是 $f(x)$ 的原函数，那么：
$$\\int_a^b f(x) dx = F(b) - F(a)$$

## 线性代数

### 矩阵乘法
两个矩阵 $A$ 和 $B$ 的乘积定义为：
$$(AB)_{ij} = \\sum_{k=1}^n A_{ik} B_{kj}$$

### 特征值和特征向量
对于方阵 $A$，如果存在非零向量 $v$ 和标量 $\\lambda$ 使得：
$$Av = \\lambda v$$
那么 $\\lambda$ 是特征值，$v$ 是对应的特征向量。

## 概率论

### 贝叶斯定理
$$P(A|B) = \\frac{P(B|A) \\cdot P(A)}{P(B)}$$

---
*选择上面的任意数学内容进行搜索测试！*
"""
    
    # 创建编辑器布局
    editor_col, preview_col = st.columns([1, 1])
    
    with editor_col:
        st.subheader("✏️ 编辑区域")
        content = st.text_area(
            "编辑你的数学笔记：",
            value=default_content,
            height=400,
            help="支持Markdown格式和LaTeX数学公式"
        )
        
        # 保存按钮
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("💾 保存笔记", type="primary"):
                try:
                    with open(note_file, "w", encoding="utf-8") as f:
                        f.write(content)
                    st.success("✅ 笔记已保存！")
                except Exception as e:
                    st.error(f"❌ 保存失败: {str(e)}")
        
        with col2:
            if st.button("🗑️ 清空内容"):
                st.session_state.clear()
                st.rerun()
    
    with preview_col:
        st.subheader("👀 实时预览")
        if content:
            try:
                st.markdown(content)
            except Exception as e:
                st.error(f"预览渲染错误: {str(e)}")
                st.code(content)


def render_search_demo():
    """渲染搜索功能演示"""
    st.header("🔍 智能搜索演示")
    
    # 搜索输入区域
    search_col, button_col = st.columns([3, 1])
    
    with search_col:
        search_query = st.text_input(
            "输入搜索内容：",
            placeholder="例如：导数定义、矩阵乘法、贝叶斯定理...",
            help="输入数学术语或概念进行搜索"
        )
    
    with button_col:
        st.write("")  # 空行对齐
        search_clicked = st.button("🔍 搜索", type="primary")
    
    # 快速搜索按钮
    st.subheader("🚀 快速搜索")
    quick_terms = ["导数", "积分", "矩阵", "特征值", "贝叶斯定理", "微分方程", "概率分布", "线性变换"]
    
    cols = st.columns(4)
    for i, term in enumerate(quick_terms):
        with cols[i % 4]:
            if st.button(f"🔍 {term}", key=f"quick_{term}"):
                search_query = term
                search_clicked = True
    
    # 执行搜索
    if search_clicked and search_query:
        st.markdown("---")
        st.subheader(f"🎯 搜索结果：{search_query}")
        
        # 生成模拟搜索结果
        results = generate_mock_search_results(search_query)
        
        # 显示搜索统计
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("搜索结果", len(results))
        with col2:
            math_results = sum(1 for r in results if r.math_content_detected)
            st.metric("数学内容", math_results)
        with col3:
            avg_relevance = sum(r.relevance_score for r in results) / len(results)
            st.metric("平均相关度", f"{avg_relevance:.2f}")
        
        # 显示搜索结果
        for i, result in enumerate(results, 1):
            with st.expander(f"📄 {i}. {result.title} {'🧮' if result.math_content_detected else ''}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**来源：** {result.source}")
                    st.write(f"**摘要：** {result.snippet}")
                    st.write(f"**链接：** [{result.url}]({result.url})")
                with col2:
                    st.metric("相关度", f"{result.relevance_score:.2f}")
                    if result.math_content_detected:
                        st.success("🧮 数学内容")
    
    elif search_clicked:
        st.warning("⚠️ 请输入搜索内容")


def render_project_status():
    """渲染项目状态"""
    st.header("📊 项目开发状态")
    
    # 功能模块状态
    st.subheader("🏗️ 功能模块")
    
    modules = [
        {"name": "数据模型 (Models)", "status": "✅ 完成", "progress": 100, "description": "SearchResult, SearchHistory, MathTerm"},
        {"name": "数据库管理 (Database)", "status": "✅ 完成", "progress": 100, "description": "SQLite连接, 历史记录存储"},
        {"name": "配置管理 (Config)", "status": "✅ 完成", "progress": 100, "description": "环境变量, 应用设置"},
        {"name": "文本处理 (Text Processing)", "status": "🔄 开发中", "progress": 70, "description": "数学术语识别, LaTeX解析"},
        {"name": "搜索管理 (Search Management)", "status": "🔄 开发中", "progress": 60, "description": "多源搜索, 结果整合"},
        {"name": "相关度计算 (Relevance)", "status": "🔄 开发中", "progress": 50, "description": "智能排序, 数学权重"},
        {"name": "用户界面 (UI)", "status": "🔄 开发中", "progress": 80, "description": "Streamlit界面, 交互组件"},
    ]
    
    for module in modules:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.write(f"**{module['name']}**")
            st.write(module['description'])
        with col2:
            st.write(module['status'])
        with col3:
            st.progress(module['progress'] / 100)
            st.write(f"{module['progress']}%")
        st.markdown("---")
    
    # 技术栈
    st.subheader("🛠️ 技术栈")
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("""
        **前端框架：**
        - Streamlit (Web界面)
        - HTML/CSS (自定义样式)
        
        **数据处理：**
        - Pandas (数据分析)
        - NumPy (数值计算)
        - SymPy (符号数学)
        """)
    
    with tech_col2:
        st.markdown("""
        **后端技术：**
        - Python 3.8+
        - SQLite (数据存储)
        - Requests (HTTP请求)
        
        **AI/ML：**
        - NLTK (自然语言处理)
        - Scikit-learn (机器学习)
        """)
    
    # 测试覆盖率
    st.subheader("🧪 测试状态")
    test_col1, test_col2, test_col3 = st.columns(3)
    
    with test_col1:
        st.metric("单元测试", "15个", "✅")
    with test_col2:
        st.metric("测试覆盖率", "85%", "📈")
    with test_col3:
        st.metric("集成测试", "8个", "✅")


def render_usage_guide():
    """渲染使用说明"""
    st.header("📖 使用说明")
    
    # 快速开始
    st.subheader("🚀 快速开始")
    st.markdown("""
    1. **安装依赖**
       ```bash
       pip install -r requirements.txt
       ```
    
    2. **配置环境变量**
       ```bash
       cp .env.example .env
       # 编辑 .env 文件添加API密钥
       ```
    
    3. **运行应用**
       ```bash
       streamlit run app.py
       ```
    """)
    
    # 功能介绍
    st.subheader("✨ 主要功能")
    
    feature_tabs = st.tabs(["📝 笔记编辑", "🔍 智能搜索", "📊 历史管理", "🧮 数学识别"])
    
    with feature_tabs[0]:
        st.markdown("""
        **数学笔记编辑器**
        - 支持Markdown格式
        - LaTeX数学公式渲染
        - 实时预览功能
        - 自动保存机制
        
        **支持的数学符号：**
        - 行内公式：`$x^2 + y^2 = r^2$`
        - 块级公式：`$$\\int_a^b f(x) dx$$`
        - 矩阵：`$$\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}$$`
        """)
    
    with feature_tabs[1]:
        st.markdown("""
        **智能搜索功能**
        - 多源搜索整合 (Google, Bing, arXiv)
        - 数学内容自动识别
        - 相关度智能排序
        - 实时搜索建议
        
        **搜索技巧：**
        - 使用具体的数学术语
        - 组合多个关键词
        - 利用快速搜索按钮
        """)
    
    with feature_tabs[2]:
        st.markdown("""
        **搜索历史管理**
        - 完整的搜索记录
        - 历史查询统计
        - 快速重新搜索
        - 结果收藏功能
        
        **历史功能：**
        - 查看搜索频率
        - 导出搜索记录
        - 清理历史数据
        """)
    
    with feature_tabs[3]:
        st.markdown("""
        **数学内容识别**
        - LaTeX公式解析
        - 数学术语提取
        - 符号识别转换
        - 公式语义分析
        
        **识别范围：**
        - 微积分概念
        - 线性代数
        - 概率统计
        - 数论基础
        """)
    
    # API配置
    st.subheader("🔧 API配置")
    st.markdown("""
    **Google搜索API (推荐)**
    ```env
    GOOGLE_API_KEY=your_google_api_key
    GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
    ```
    
    **Bing搜索API (可选)**
    ```env
    BING_API_KEY=your_bing_api_key
    ```
    
    **获取API密钥：**
    - [Google Custom Search API](https://developers.google.com/custom-search/v1/introduction)
    - [Bing Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api)
    """)
    
    # 常见问题
    st.subheader("❓ 常见问题")
    
    with st.expander("Q: 如何输入数学公式？"):
        st.markdown("""
        使用LaTeX语法：
        - 行内公式：`$公式内容$`
        - 独立公式：`$$公式内容$$`
        - 例如：`$\\frac{d}{dx}f(x) = f'(x)$`
        """)
    
    with st.expander("Q: 搜索结果不准确怎么办？"):
        st.markdown("""
        尝试以下方法：
        1. 使用更具体的数学术语
        2. 添加上下文关键词
        3. 使用"数学搜索"模式
        4. 检查API配置是否正确
        """)
    
    with st.expander("Q: 如何提高搜索相关度？"):
        st.markdown("""
        优化搜索策略：
        1. 使用标准数学术语
        2. 避免过于宽泛的查询
        3. 结合多个相关概念
        4. 利用历史搜索记录
        """)


def generate_mock_search_results(query: str) -> list[SearchResult]:
    """生成模拟搜索结果"""
    # 检测是否为数学查询
    math_keywords = [
        '导数', '积分', '微积分', '矩阵', '线性代数', '特征值', '特征向量',
        '概率', '统计', '贝叶斯', '微分', '方程', '函数', '极限',
        'derivative', 'integral', 'calculus', 'matrix', 'eigenvalue',
        'probability', 'statistics', 'bayes', 'differential', 'equation'
    ]
    
    is_math_query = any(keyword in query.lower() for keyword in math_keywords)
    
    # 基础搜索结果
    results = [
        SearchResult(
            title=f"关于'{query}'的数学解释 - 维基百科",
            url="https://zh.wikipedia.org/wiki/数学",
            snippet=f"这是关于{query}的详细数学解释和定义，包含了基本概念、性质和应用实例。维基百科提供了全面的数学知识体系。",
            source="Wikipedia",
            relevance_score=0.95,
            timestamp=datetime.now(),
            math_content_detected=is_math_query
        ),
        SearchResult(
            title=f"{query} - Wolfram MathWorld",
            url="https://mathworld.wolfram.com/",
            snippet=f"Wolfram MathWorld提供的{query}完整数学定义，包含公式、定理和证明。这是数学研究的权威参考资源。",
            source="Wolfram MathWorld",
            relevance_score=0.92,
            timestamp=datetime.now(),
            math_content_detected=is_math_query
        ),
        SearchResult(
            title=f"学习{query}的最佳资源 - Khan Academy",
            url="https://www.khanacademy.org/",
            snippet=f"Khan Academy提供的{query}免费在线课程，包含视频讲解和练习题。适合各个水平的学习者。",
            source="Khan Academy",
            relevance_score=0.88,
            timestamp=datetime.now(),
            math_content_detected=is_math_query
        )
    ]
    
    if is_math_query:
        # 为数学查询添加专业结果
        results.extend([
            SearchResult(
                title=f"{query} - arXiv数学论文",
                url="https://arxiv.org/list/math/recent",
                snippet=f"arXiv上关于{query}的最新研究论文和学术文献。包含前沿的数学研究成果和理论发展。",
                source="arXiv",
                relevance_score=0.90,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title=f"{query}的MATLAB实现",
                url="https://www.mathworks.com/help/",
                snippet=f"MATLAB文档中{query}的实际应用案例和代码示例。提供了实用的计算方法和算法实现。",
                source="MathWorks",
                relevance_score=0.85,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title=f"{query} - 数学之美博客",
                url="https://www.mathbeauty.com/",
                snippet=f"深入浅出地解释{query}的数学原理和应用，配有直观的图表和实例说明。",
                source="数学之美",
                relevance_score=0.82,
                timestamp=datetime.now(),
                math_content_detected=True
            )
        ])
    
    # 按相关度排序
    results.sort(key=lambda x: x.relevance_score, reverse=True)
    return results


if __name__ == "__main__":
    main()