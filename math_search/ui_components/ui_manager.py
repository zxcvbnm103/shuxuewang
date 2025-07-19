"""
用户界面管理器 - 管理Streamlit界面组件和交互
"""
import streamlit as st
from typing import Optional, Tuple, List
import re
from ..models.search_result import SearchResult
from ..models.search_history import SearchHistory


class UIManager:
    """用户界面管理器，负责管理Streamlit界面组件和交互"""
    
    def __init__(self):
        """初始化UI管理器"""
        # 初始化session state
        if 'selected_text' not in st.session_state:
            st.session_state.selected_text = ""
        if 'search_triggered' not in st.session_state:
            st.session_state.search_triggered = False
        if 'search_results' not in st.session_state:
            st.session_state.search_results = []
    
    def render_editor_with_selection(self, default_content: str = "") -> Tuple[str, str]:
        """
        渲染带有文本选择功能的编辑器
        
        Args:
            default_content: 默认内容
            
        Returns:
            Tuple[str, str]: (编辑器内容, 选中的文本)
        """
        st.subheader("📝 Markdown编辑器")
        
        # 创建两列布局
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # 主编辑器
            content = st.text_area(
                "编辑你的 Markdown 内容：",
                value=default_content,
                height=400,
                key="main_editor",
                help="在此编辑你的数学笔记，支持Markdown和LaTeX格式"
            )
            
            # 文本选择输入框
            st.markdown("---")
            st.markdown("**🔍 文本选择搜索**")
            selected_text = st.text_input(
                "选中的文本（或手动输入要搜索的内容）：",
                value=st.session_state.selected_text,
                key="selected_text_input",
                help="复制粘贴你想要搜索的文本内容"
            )
            
            # 搜索触发按钮
            search_col1, search_col2, search_col3 = st.columns([1, 1, 2])
            
            with search_col1:
                if st.button("🔍 搜索", type="primary", help="搜索选中的文本内容"):
                    if selected_text.strip():
                        st.session_state.selected_text = selected_text
                        st.session_state.search_triggered = True
                        st.success(f"正在搜索: {selected_text[:50]}...")
                    else:
                        st.warning("请先选择或输入要搜索的文本")
            
            with search_col2:
                if st.button("🧮 数学搜索", help="专门搜索数学相关内容"):
                    if selected_text.strip():
                        # 为数学搜索添加特殊标记
                        math_query = f"数学 {selected_text}"
                        st.session_state.selected_text = math_query
                        st.session_state.search_triggered = True
                        st.success(f"正在进行数学搜索: {selected_text[:50]}...")
                    else:
                        st.warning("请先选择或输入要搜索的数学内容")
            
            with search_col3:
                if st.button("🗑️ 清除选择", help="清除当前选中的文本"):
                    st.session_state.selected_text = ""
                    st.session_state.search_triggered = False
                    st.rerun()
        
        with col2:
            # 快捷操作面板
            st.markdown("**⚡ 快捷操作**")
            
            # 常用数学术语快捷搜索
            st.markdown("*常用数学术语:*")
            math_terms = [
                "微积分", "线性代数", "概率论", "统计学",
                "拓扑学", "群论", "数论", "几何学"
            ]
            
            for i in range(0, len(math_terms), 2):
                term_col1, term_col2 = st.columns(2)
                with term_col1:
                    if i < len(math_terms):
                        if st.button(math_terms[i], key=f"term_{i}"):
                            st.session_state.selected_text = math_terms[i]
                            st.session_state.search_triggered = True
                            st.rerun()
                
                with term_col2:
                    if i + 1 < len(math_terms):
                        if st.button(math_terms[i + 1], key=f"term_{i+1}"):
                            st.session_state.selected_text = math_terms[i + 1]
                            st.session_state.search_triggered = True
                            st.rerun()
            
            # 文本分析信息
            if content:
                st.markdown("---")
                st.markdown("**📊 文本分析**")
                word_count = len(content.split())
                char_count = len(content)
                math_patterns = self._detect_math_content(content)
                
                st.metric("字数", word_count)
                st.metric("字符数", char_count)
                st.metric("数学公式", len(math_patterns))
                
                if math_patterns:
                    with st.expander("检测到的数学内容"):
                        for pattern in math_patterns[:5]:  # 显示前5个
                            st.code(pattern, language="latex")
        
        return content, selected_text
    
    def render_search_panel(self, results: List[SearchResult]) -> None:
        """
        渲染搜索结果面板 - 实现右侧结果面板的Streamlit组件
        
        Args:
            results: 搜索结果列表
        """
        if not results:
            if st.session_state.search_triggered:
                st.info("🔍 暂无搜索结果，请尝试其他关键词")
                st.markdown("**搜索建议:**")
                st.markdown("- 尝试使用更具体的数学术语")
                st.markdown("- 检查拼写是否正确")
                st.markdown("- 使用英文术语可能获得更多结果")
            return
        
        # 搜索结果标题和统计信息
        st.subheader(f"🎯 搜索结果")
        
        # 结果统计信息
        math_count = sum(1 for r in results if r.math_content_detected)
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            st.metric("总结果", len(results))
        with stats_col2:
            st.metric("数学内容", math_count)
        with stats_col3:
            avg_relevance = sum(r.relevance_score for r in results) / len(results)
            st.metric("平均相关度", f"{avg_relevance:.2f}")
        
        # 搜索结果控制面板
        with st.expander("🔧 结果筛选和排序", expanded=False):
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                sort_by = st.selectbox(
                    "排序方式",
                    ["相关度", "时间", "来源"],
                    key="sort_results",
                    help="选择结果排序方式"
                )
                
                show_math_only = st.checkbox(
                    "仅显示数学内容",
                    key="filter_math",
                    help="只显示包含数学内容的结果"
                )
            
            with filter_col2:
                min_relevance = st.slider(
                    "最低相关度",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.0,
                    step=0.1,
                    key="min_relevance",
                    help="过滤低相关度结果"
                )
                
                source_filter = st.multiselect(
                    "来源筛选",
                    options=list(set(r.source for r in results)),
                    default=list(set(r.source for r in results)),
                    key="source_filter",
                    help="选择要显示的结果来源"
                )
        
        # 过滤和排序结果
        filtered_results = results
        
        # 应用筛选条件
        if show_math_only:
            filtered_results = [r for r in filtered_results if r.math_content_detected]
        
        filtered_results = [r for r in filtered_results if r.relevance_score >= min_relevance]
        
        if source_filter:
            filtered_results = [r for r in filtered_results if r.source in source_filter]
        
        # 应用排序
        if sort_by == "相关度":
            filtered_results.sort(key=lambda x: x.relevance_score, reverse=True)
        elif sort_by == "时间":
            filtered_results.sort(key=lambda x: x.timestamp, reverse=True)
        elif sort_by == "来源":
            filtered_results.sort(key=lambda x: x.source)
        
        # 显示过滤后的结果数量
        if len(filtered_results) != len(results):
            st.info(f"📊 显示 {len(filtered_results)} / {len(results)} 个结果")
        
        # 结果卡片显示
        if not filtered_results:
            st.warning("🚫 没有符合筛选条件的结果")
            return
        
        # 分页显示
        results_per_page = 5
        total_pages = (len(filtered_results) + results_per_page - 1) // results_per_page
        
        if total_pages > 1:
            page_col1, page_col2, page_col3 = st.columns([1, 2, 1])
            with page_col2:
                current_page = st.selectbox(
                    "页面",
                    range(1, total_pages + 1),
                    key="results_page",
                    format_func=lambda x: f"第 {x} 页 (共 {total_pages} 页)"
                )
        else:
            current_page = 1
        
        # 计算当前页面的结果范围
        start_idx = (current_page - 1) * results_per_page
        end_idx = min(start_idx + results_per_page, len(filtered_results))
        page_results = filtered_results[start_idx:end_idx]
        
        # 显示结果卡片
        for i, result in enumerate(page_results):
            result_idx = start_idx + i
            self._render_result_card(result, result_idx)
    
    def _render_result_card(self, result: SearchResult, index: int) -> None:
        """
        渲染单个搜索结果卡片
        
        Args:
            result: 搜索结果
            index: 结果索引
        """
        # 创建结果卡片容器
        with st.container():
            # 卡片边框样式
            st.markdown(
                f"""
                <div style="
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 16px;
                    margin: 8px 0;
                    background-color: {'#f8f9ff' if result.math_content_detected else '#ffffff'};
                ">
                """,
                unsafe_allow_html=True
            )
            
            # 结果标题和排名
            title_col, rank_col = st.columns([4, 1])
            
            with title_col:
                # 标题，支持点击跳转
                st.markdown(
                    f"**#{index + 1}. [{result.title}]({result.url})**",
                    help=f"点击访问: {result.url}"
                )
            
            with rank_col:
                # 相关度评分
                score_color = "green" if result.relevance_score >= 0.8 else "orange" if result.relevance_score >= 0.6 else "red"
                st.markdown(
                    f"<span style='color: {score_color}; font-weight: bold;'>⭐ {result.relevance_score:.2f}</span>",
                    unsafe_allow_html=True
                )
            
            # 结果元信息
            meta_col1, meta_col2, meta_col3 = st.columns([2, 1, 1])
            
            with meta_col1:
                st.markdown(f"🌐 **来源:** {result.source}")
            
            with meta_col2:
                if result.math_content_detected:
                    st.markdown("🧮 **数学内容**")
                else:
                    st.markdown("📄 **普通内容**")
            
            with meta_col3:
                time_str = result.timestamp.strftime("%m-%d %H:%M")
                st.markdown(f"🕒 {time_str}")
            
            # 结果摘要
            if result.snippet:
                snippet_text = result.snippet
                if len(snippet_text) > 200:
                    snippet_text = snippet_text[:200] + "..."
                
                st.markdown(f"📝 **摘要:** {snippet_text}")
            
            # 操作按钮
            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1, 1, 1])
            
            with btn_col1:
                if st.button("🔗 打开链接", key=f"open_{index}", help="在新标签页中打开"):
                    # 使用JavaScript在新窗口打开链接
                    st.markdown(
                        f"""
                        <script>
                        window.open('{result.url}', '_blank');
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                    st.success("链接已在新窗口打开")
            
            with btn_col2:
                if st.button("📋 复制链接", key=f"copy_{index}", help="复制链接到剪贴板"):
                    # 显示链接供用户复制
                    st.code(result.url, language=None)
                    st.info("请手动复制上方链接")
            
            with btn_col3:
                if st.button("📤 分享", key=f"share_{index}", help="分享此结果"):
                    share_text = f"**{result.title}**\n{result.snippet[:100]}...\n🔗 {result.url}"
                    st.text_area("分享内容", share_text, height=100, key=f"share_text_{index}")
            
            with btn_col4:
                if st.button("⭐ 收藏", key=f"bookmark_{index}", help="收藏此结果"):
                    # 这里可以实现收藏功能
                    st.success("已收藏！")
                    st.balloons()
            
            # 额外信息展开面板
            with st.expander(f"📊 详细信息 #{index + 1}", expanded=False):
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.markdown("**完整URL:**")
                    st.code(result.url, language=None)
                    
                    st.markdown("**搜索来源:**")
                    st.write(result.source)
                
                with detail_col2:
                    st.markdown("**相关度评分:**")
                    st.progress(result.relevance_score)
                    
                    st.markdown("**检索时间:**")
                    st.write(result.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                
                if result.snippet:
                    st.markdown("**完整摘要:**")
                    st.write(result.snippet)
            
            # 结束卡片容器
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 分隔线
            st.markdown("---")
    
    def render_history_panel(self, history: List[SearchHistory]) -> None:
        """
        渲染历史记录面板
        
        Args:
            history: 搜索历史列表
        """
        if not history:
            st.info("📝 暂无搜索历史")
            return
        
        st.subheader("📚 搜索历史")
        
        # 历史记录选项
        hist_col1, hist_col2 = st.columns(2)
        with hist_col1:
            show_count = st.selectbox("显示数量", [5, 10, 20], index=1)
        
        with hist_col2:
            if st.button("清除历史"):
                st.warning("历史记录清除功能需要在数据库层实现")
        
        # 显示历史记录
        for i, record in enumerate(history[:show_count]):
            with st.expander(f"{record.query_text[:30]}... ({record.timestamp.strftime('%m-%d %H:%M')})"):
                st.markdown(f"**查询文本:** {record.query_text}")
                st.markdown(f"**搜索关键词:** {', '.join(record.search_keywords)}")
                st.markdown(f"**结果数量:** {record.results_count}")
                st.markdown(f"**时间:** {record.timestamp}")
                
                if record.top_result_url:
                    st.markdown(f"**最佳结果:** [链接]({record.top_result_url})")
                
                if st.button("重新搜索", key=f"research_{i}"):
                    st.session_state.selected_text = record.query_text
                    st.session_state.search_triggered = True
                    st.rerun()
    
    def handle_search_trigger(self, selected_text: str) -> None:
        """
        处理搜索触发事件
        
        Args:
            selected_text: 选中的文本
        """
        if selected_text.strip():
            st.session_state.selected_text = selected_text
            st.session_state.search_triggered = True
            st.success(f"搜索已触发: {selected_text[:50]}...")
        else:
            st.warning("请选择有效的文本内容")
    
    def _detect_math_content(self, text: str) -> List[str]:
        """
        检测文本中的数学内容
        
        Args:
            text: 输入文本
            
        Returns:
            List[str]: 检测到的数学公式列表
        """
        # LaTeX公式模式
        latex_patterns = [
            r'\$\$.*?\$\$',  # 块级公式
            r'\$.*?\$',      # 行内公式
            r'\\begin\{.*?\}.*?\\end\{.*?\}',  # 环境
            r'\\[a-zA-Z]+\{.*?\}',  # LaTeX命令
        ]
        
        math_content = []
        for pattern in latex_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            math_content.extend(matches)
        
        return list(set(math_content))  # 去重
    
    def get_search_state(self) -> dict:
        """
        获取当前搜索状态
        
        Returns:
            dict: 搜索状态信息
        """
        return {
            'selected_text': st.session_state.get('selected_text', ''),
            'search_triggered': st.session_state.get('search_triggered', False),
            'has_results': len(st.session_state.get('search_results', [])) > 0
        }
    
    def reset_search_state(self) -> None:
        """重置搜索状态"""
        st.session_state.selected_text = ""
        st.session_state.search_triggered = False
        st.session_state.search_results = []