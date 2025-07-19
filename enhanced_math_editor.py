"""
增强版数学笔记编辑器 - 集成文本选择和搜索功能
"""
import streamlit as st
import os
from datetime import datetime
from math_search.ui_components.ui_manager import UIManager
from math_search.models.search_result import SearchResult
from math_search.models.search_history import SearchHistory


def main():
    """主应用程序"""
    # 页面配置
    st.set_page_config(
        page_title="数学笔记智能编辑器",
        page_icon="🧮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 应用标题
    st.title("🧮 数学笔记智能编辑器")
    st.markdown("*支持文本选择搜索和数学内容识别*")
    
    # 初始化UI管理器
    ui_manager = UIManager()
    
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

---
*在上面选择任意文本，然后点击搜索按钮来查找相关资料！*
"""
    
    # 创建主布局
    main_col, sidebar_col = st.columns([3, 1])
    
    with main_col:
        # 渲染编辑器和文本选择功能
        content, selected_text = ui_manager.render_editor_with_selection(default_content)
        
        # 保存笔记功能
        save_col1, save_col2, save_col3 = st.columns([1, 1, 2])
        
        with save_col1:
            if st.button("💾 保存笔记", type="primary"):
                try:
                    with open(note_file, "w", encoding="utf-8") as f:
                        f.write(content)
                    st.success("✅ 笔记已保存！")
                except Exception as e:
                    st.error(f"❌ 保存失败: {str(e)}")
        
        with save_col2:
            if st.button("📄 新建笔记"):
                st.session_state.clear()
                st.rerun()
        
        # Markdown预览
        st.markdown("---")
        st.subheader("📖 Markdown预览")
        
        # 预览选项
        preview_col1, preview_col2 = st.columns([1, 3])
        with preview_col1:
            show_preview = st.checkbox("显示预览", value=True)
        
        if show_preview and content:
            try:
                st.markdown(content)
            except Exception as e:
                st.error(f"预览渲染错误: {str(e)}")
                st.code(content)
    
    with sidebar_col:
        st.markdown("### 🔍 搜索面板")
        
        # 获取搜索状态
        search_state = ui_manager.get_search_state()
        
        if search_state['search_triggered'] and search_state['selected_text']:
            st.success(f"🎯 搜索查询: {search_state['selected_text'][:30]}...")
            
            # 模拟搜索结果（实际实现中会调用搜索管理器）
            mock_results = generate_mock_search_results(search_state['selected_text'])
            ui_manager.render_search_panel(mock_results)
            
            # 重置搜索状态按钮
            if st.button("🔄 新搜索"):
                ui_manager.reset_search_state()
                st.rerun()
        
        else:
            st.info("👆 在编辑器中选择文本并点击搜索按钮")
        
        # 搜索历史面板
        st.markdown("---")
        mock_history = generate_mock_history()
        ui_manager.render_history_panel(mock_history)
        
        # 使用说明
        st.markdown("---")
        with st.expander("📖 使用说明"):
            st.markdown("""
            **文本选择搜索:**
            1. 在编辑器中选择要搜索的文本
            2. 复制并粘贴到"选中的文本"输入框
            3. 点击"🔍 搜索"或"🧮 数学搜索"按钮
            4. 在右侧查看搜索结果
            
            **快捷功能:**
            - 点击常用数学术语快速搜索
            - 使用"数学搜索"获得更精准的数学内容
            - 查看搜索历史并重新搜索
            
            **支持格式:**
            - Markdown文本
            - LaTeX数学公式 ($...$, $$...$$)
            - 数学符号和术语
            """)
    
    # 页面底部信息
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "🧮 数学笔记智能编辑器 | 支持LaTeX公式和智能搜索"
        "</div>",
        unsafe_allow_html=True
    )


def generate_mock_search_results(query: str) -> list[SearchResult]:
    """
    生成模拟搜索结果（用于演示）
    
    Args:
        query: 搜索查询
        
    Returns:
        List[SearchResult]: 模拟搜索结果
    """
    # 根据查询内容生成相关的模拟结果
    is_math_query = any(term in query.lower() for term in [
        '数学', '微积分', '导数', '积分', '矩阵', '线性代数', 
        '概率', '统计', '几何', '代数', 'math', 'calculus'
    ])
    
    base_results = [
        SearchResult(
            title=f"关于'{query}'的数学解释",
            url="https://zh.wikipedia.org/wiki/数学",
            snippet=f"这是关于{query}的详细数学解释和定义，包含了基本概念、性质和应用实例。",
            source="Wikipedia",
            relevance_score=0.95,
            timestamp=datetime.now(),
            math_content_detected=is_math_query
        ),
        SearchResult(
            title=f"{query} - 数学百科",
            url="https://mathworld.wolfram.com/",
            snippet=f"Wolfram MathWorld提供的{query}完整数学定义，包含公式、定理和证明。",
            source="Wolfram MathWorld",
            relevance_score=0.88,
            timestamp=datetime.now(),
            math_content_detected=is_math_query
        ),
        SearchResult(
            title=f"学习{query}的最佳资源",
            url="https://www.khanacademy.org/",
            snippet=f"Khan Academy提供的{query}免费在线课程，包含视频讲解和练习题。",
            source="Khan Academy",
            relevance_score=0.82,
            timestamp=datetime.now(),
            math_content_detected=is_math_query
        )
    ]
    
    if is_math_query:
        # 为数学查询添加更多专业结果
        base_results.extend([
            SearchResult(
                title=f"{query} - arXiv论文",
                url="https://arxiv.org/",
                snippet=f"arXiv上关于{query}的最新研究论文和学术文献。",
                source="arXiv",
                relevance_score=0.90,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title=f"{query}的应用实例",
                url="https://www.mathworks.com/",
                snippet=f"MATLAB文档中{query}的实际应用案例和代码示例。",
                source="MathWorks",
                relevance_score=0.75,
                timestamp=datetime.now(),
                math_content_detected=True
            )
        ])
    
    return base_results


def generate_mock_history() -> list[SearchHistory]:
    """
    生成模拟搜索历史（用于演示）
    
    Returns:
        List[SearchHistory]: 模拟搜索历史
    """
    return [
        SearchHistory(
            id=1,
            query_text="导数定义",
            search_keywords=["导数", "定义", "微积分"],
            timestamp=datetime.now(),
            results_count=5,
            top_result_url="https://zh.wikipedia.org/wiki/导数"
        ),
        SearchHistory(
            id=2,
            query_text="矩阵乘法",
            search_keywords=["矩阵", "乘法", "线性代数"],
            timestamp=datetime.now(),
            results_count=8,
            top_result_url="https://mathworld.wolfram.com/MatrixMultiplication.html"
        ),
        SearchHistory(
            id=3,
            query_text="积分基本定理",
            search_keywords=["积分", "基本定理", "微积分"],
            timestamp=datetime.now(),
            results_count=6,
            top_result_url="https://www.khanacademy.org/math/calculus"
        )
    ]


if __name__ == "__main__":
    main()