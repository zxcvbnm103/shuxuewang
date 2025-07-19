"""
搜索结果展示面板演示
Demo for Search Results Display Panel
"""

import streamlit as st
from datetime import datetime, timedelta
import random

from math_search.ui_components.ui_manager import UIManager
from math_search.models.search_result import SearchResult


def create_demo_results() -> list[SearchResult]:
    """创建演示用的搜索结果"""
    demo_data = [
        {
            "title": "微积分基础教程 - 导数与积分",
            "url": "https://zh.wikipedia.org/wiki/微积分",
            "snippet": "微积分是数学的一个分支，研究函数的导数、积分以及相关概念。本教程详细介绍了导数的定义、计算方法和几何意义，以及积分的基本定理和应用。",
            "source": "Wikipedia",
            "relevance_score": 0.95,
            "math_content": True
        },
        {
            "title": "线性代数入门 - 矩阵与向量空间",
            "url": "https://www.khanacademy.org/math/linear-algebra",
            "snippet": "线性代数是数学的重要分支，研究向量、向量空间、线性映射和有限维线性方程组。本课程涵盖矩阵运算、行列式、特征值和特征向量等核心概念。",
            "source": "Khan Academy",
            "relevance_score": 0.92,
            "math_content": True
        },
        {
            "title": "概率论与数理统计",
            "url": "https://mathworld.wolfram.com/Probability.html",
            "snippet": "概率论是研究随机现象数量规律的数学分支。本资源介绍了概率的基本概念、条件概率、贝叶斯定理以及常见的概率分布。",
            "source": "Wolfram MathWorld",
            "relevance_score": 0.89,
            "math_content": True
        },
        {
            "title": "数学建模方法与应用",
            "url": "https://arxiv.org/abs/math.GM/0001001",
            "snippet": "数学建模是运用数学方法解决实际问题的过程。本论文讨论了常用的数学建模方法，包括微分方程模型、优化模型和统计模型等。",
            "source": "arXiv",
            "relevance_score": 0.87,
            "math_content": True
        },
        {
            "title": "数学史 - 从古代到现代",
            "url": "https://example.com/math-history",
            "snippet": "数学的发展历程从古代文明开始，经历了希腊数学、中世纪数学、文艺复兴时期数学，直到现代数学的各个分支。本文回顾了数学发展的重要里程碑。",
            "source": "数学百科",
            "relevance_score": 0.75,
            "math_content": False
        },
        {
            "title": "拓扑学基础概念",
            "url": "https://mathworld.wolfram.com/Topology.html",
            "snippet": "拓扑学是研究空间性质的数学分支，关注在连续变形下保持不变的性质。本资源介绍了拓扑空间、连续映射、同胚等基本概念。",
            "source": "Wolfram MathWorld",
            "relevance_score": 0.84,
            "math_content": True
        },
        {
            "title": "数值分析方法",
            "url": "https://www.mathworks.com/help/matlab/numerical-analysis.html",
            "snippet": "数值分析是用数值方法求解数学问题的学科。本指南介绍了数值积分、微分方程求解、插值和拟合等常用数值方法。",
            "source": "MathWorks",
            "relevance_score": 0.81,
            "math_content": True
        },
        {
            "title": "抽象代数导论",
            "url": "https://example.com/abstract-algebra",
            "snippet": "抽象代数研究代数结构，如群、环、域等。本教程从基本概念开始，逐步介绍群论、环论和域论的核心内容。",
            "source": "数学教育网",
            "relevance_score": 0.78,
            "math_content": True
        },
        {
            "title": "数学软件应用指南",
            "url": "https://example.com/math-software",
            "snippet": "现代数学研究离不开计算机软件的辅助。本指南介绍了Mathematica、MATLAB、Python等常用数学软件的使用方法和应用场景。",
            "source": "技术博客",
            "relevance_score": 0.68,
            "math_content": False
        },
        {
            "title": "复分析理论与应用",
            "url": "https://mathworld.wolfram.com/ComplexAnalysis.html",
            "snippet": "复分析是研究复变函数的数学分支。本资源详细介绍了复数、解析函数、留数定理等重要概念，以及它们在物理和工程中的应用。",
            "source": "Wolfram MathWorld",
            "relevance_score": 0.86,
            "math_content": True
        }
    ]
    
    results = []
    for i, data in enumerate(demo_data):
        # 随机化时间戳
        timestamp = datetime.now() - timedelta(hours=random.randint(1, 72))
        
        result = SearchResult(
            title=data["title"],
            url=data["url"],
            snippet=data["snippet"],
            source=data["source"],
            relevance_score=data["relevance_score"],
            timestamp=timestamp,
            math_content_detected=data["math_content"]
        )
        results.append(result)
    
    return results


def main():
    """主演示程序"""
    st.set_page_config(
        page_title="搜索结果展示面板演示",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 搜索结果展示面板演示")
    st.markdown("*展示增强的搜索结果显示功能*")
    
    # 创建演示数据
    demo_results = create_demo_results()
    
    # 初始化UI管理器
    ui_manager = UIManager()
    
    # 模拟搜索状态
    if 'search_triggered' not in st.session_state:
        st.session_state.search_triggered = True
    
    # 创建布局
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🔧 演示控制")
        
        # 结果数量控制
        result_count = st.slider(
            "显示结果数量",
            min_value=1,
            max_value=len(demo_results),
            value=len(demo_results),
            help="选择要显示的搜索结果数量"
        )
        
        # 模拟搜索查询
        search_query = st.text_input(
            "模拟搜索查询",
            value="数学 微积分 线性代数",
            help="这是模拟的搜索查询文本"
        )
        
        # 重新生成结果按钮
        if st.button("🔄 重新生成结果"):
            st.rerun()
        
        # 功能说明
        st.markdown("---")
        st.subheader("✨ 功能特点")
        st.markdown("""
        **搜索结果展示面板包含:**
        - 📊 结果统计信息
        - 🔧 筛选和排序选项
        - 📄 分页显示
        - 🎨 美观的结果卡片
        - 🔗 点击跳转功能
        - 📋 链接复制功能
        - 📤 结果分享功能
        - ⭐ 收藏功能
        """)
        
        # 测试数据信息
        st.markdown("---")
        st.subheader("📋 测试数据")
        math_count = sum(1 for r in demo_results if r.math_content_detected)
        st.metric("总结果数", len(demo_results))
        st.metric("数学内容", math_count)
        st.metric("普通内容", len(demo_results) - math_count)
        
        # 来源分布
        sources = {}
        for result in demo_results:
            sources[result.source] = sources.get(result.source, 0) + 1
        
        st.markdown("**来源分布:**")
        for source, count in sources.items():
            st.write(f"- {source}: {count}")
    
    with col2:
        st.subheader("🎯 搜索结果展示")
        
        # 显示当前搜索查询
        st.info(f"🔍 搜索查询: {search_query}")
        
        # 渲染搜索结果面板
        selected_results = demo_results[:result_count]
        ui_manager.render_search_panel(selected_results)
    
    # 页面底部信息
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "🎯 搜索结果展示面板演示 | 实现需求 2.2, 2.3, 3.1, 3.2"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()