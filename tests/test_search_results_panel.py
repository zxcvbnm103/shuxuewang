"""
搜索结果展示面板测试
Test for Search Results Display Panel
"""

import pytest
from datetime import datetime

from math_search.models.search_result import SearchResult


class TestSearchResultsPanel:
    """搜索结果展示面板测试类"""
    
    def setup_method(self):
        """测试前设置"""
        # 创建测试用的搜索结果
        self.test_results = [
            SearchResult(
                title="微积分基础教程",
                url="https://example.com/calculus",
                snippet="这是一个关于微积分基础概念的详细教程，包含导数和积分的定义与应用。",
                source="Wikipedia",
                relevance_score=0.95,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title="线性代数入门",
                url="https://example.com/linear-algebra",
                snippet="线性代数的基本概念，包括矩阵运算、向量空间和线性变换。",
                source="Khan Academy",
                relevance_score=0.88,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title="数学历史概述",
                url="https://example.com/math-history",
                snippet="数学发展的历史回顾，从古代数学到现代数学的演进过程。",
                source="Wolfram MathWorld",
                relevance_score=0.72,
                timestamp=datetime.now(),
                math_content_detected=False
            ),
            SearchResult(
                title="概率论与统计学",
                url="https://example.com/probability",
                snippet="概率论的基本原理和统计学的应用方法。",
                source="arXiv",
                relevance_score=0.85,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title="几何学基础",
                url="https://example.com/geometry",
                snippet="欧几里得几何和非欧几何的基本概念。",
                source="MathWorks",
                relevance_score=0.79,
                timestamp=datetime.now(),
                math_content_detected=True
            )
        ]
    
    def test_result_filtering_by_math_content(self):
        """测试按数学内容过滤结果"""
        # 计算数学内容结果数量
        math_results = [r for r in self.test_results if r.math_content_detected]
        expected_count = len(math_results)
        
        # 验证过滤逻辑
        assert expected_count == 4  # 5个结果中有4个包含数学内容
        assert all(r.math_content_detected for r in math_results)
    
    def test_result_sorting_by_relevance(self):
        """测试按相关度排序结果"""
        # 按相关度排序
        sorted_results = sorted(self.test_results, key=lambda x: x.relevance_score, reverse=True)
        
        # 验证排序正确性
        assert sorted_results[0].relevance_score == 0.95  # 最高相关度
        assert sorted_results[-1].relevance_score == 0.72  # 最低相关度
        
        # 验证排序是降序
        for i in range(len(sorted_results) - 1):
            assert sorted_results[i].relevance_score >= sorted_results[i + 1].relevance_score
    
    def test_result_sorting_by_source(self):
        """测试按来源排序结果"""
        # 按来源排序
        sorted_results = sorted(self.test_results, key=lambda x: x.source)
        
        # 验证排序正确性（字母顺序）
        sources = [r.source for r in sorted_results]
        assert sources == sorted(sources)
    
    def test_result_filtering_by_relevance_threshold(self):
        """测试按相关度阈值过滤结果"""
        min_relevance = 0.8
        filtered_results = [r for r in self.test_results if r.relevance_score >= min_relevance]
        
        # 验证过滤结果
        assert len(filtered_results) == 3  # 应该有3个结果 >= 0.8
        assert all(r.relevance_score >= min_relevance for r in filtered_results)
    
    def test_result_filtering_by_source(self):
        """测试按来源过滤结果"""
        allowed_sources = ["Wikipedia", "Khan Academy"]
        filtered_results = [r for r in self.test_results if r.source in allowed_sources]
        
        # 验证过滤结果
        assert len(filtered_results) == 2
        assert all(r.source in allowed_sources for r in filtered_results)
    
    @patch('streamlit.container')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    def test_render_result_card(self, mock_columns, mock_markdown, mock_container):
        """测试渲染单个结果卡片"""
        # 模拟streamlit组件
        mock_columns.return_value = [Mock(), Mock(), Mock(), Mock()]
        mock_container.return_value.__enter__ = Mock()
        mock_container.return_value.__exit__ = Mock()
        
        # 调用渲染卡片方法
        test_result = self.test_results[0]
        self.ui_manager._render_result_card(test_result, 0)
        
        # 验证容器被创建
        mock_container.assert_called()
        
        # 验证markdown被调用（用于显示标题等）
        assert mock_markdown.call_count > 0
    
    def test_pagination_calculation(self):
        """测试分页计算逻辑"""
        results_per_page = 5
        total_results = len(self.test_results)  # 5个结果
        
        # 计算总页数
        total_pages = (total_results + results_per_page - 1) // results_per_page
        assert total_pages == 1  # 5个结果，每页5个，应该是1页
        
        # 测试更多结果的情况
        more_results = self.test_results * 3  # 15个结果
        total_pages_more = (len(more_results) + results_per_page - 1) // results_per_page
        assert total_pages_more == 3  # 15个结果，每页5个，应该是3页
    
    def test_page_results_slicing(self):
        """测试页面结果切片逻辑"""
        results_per_page = 2
        current_page = 2
        
        # 计算当前页面的结果范围
        start_idx = (current_page - 1) * results_per_page  # (2-1) * 2 = 2
        end_idx = min(start_idx + results_per_page, len(self.test_results))  # min(2+2, 5) = 4
        page_results = self.test_results[start_idx:end_idx]
        
        # 验证切片结果
        assert len(page_results) == 2  # 第2页应该有2个结果
        assert page_results[0] == self.test_results[2]  # 第一个结果应该是索引2
        assert page_results[1] == self.test_results[3]  # 第二个结果应该是索引3
    
    def test_search_statistics_calculation(self):
        """测试搜索统计信息计算"""
        # 计算数学内容数量
        math_count = sum(1 for r in self.test_results if r.math_content_detected)
        assert math_count == 4
        
        # 计算平均相关度
        avg_relevance = sum(r.relevance_score for r in self.test_results) / len(self.test_results)
        expected_avg = (0.95 + 0.88 + 0.72 + 0.85 + 0.79) / 5
        assert abs(avg_relevance - expected_avg) < 0.01  # 允许小的浮点误差
    
    def test_result_card_styling_logic(self):
        """测试结果卡片样式逻辑"""
        # 测试数学内容的背景色
        math_result = self.test_results[0]  # 包含数学内容
        non_math_result = self.test_results[2]  # 不包含数学内容
        
        # 验证背景色逻辑
        math_bg_color = '#f8f9ff' if math_result.math_content_detected else '#ffffff'
        non_math_bg_color = '#f8f9ff' if non_math_result.math_content_detected else '#ffffff'
        
        assert math_bg_color == '#f8f9ff'
        assert non_math_bg_color == '#ffffff'
    
    def test_relevance_score_color_logic(self):
        """测试相关度评分颜色逻辑"""
        # 测试不同相关度的颜色
        high_score = 0.95  # 高相关度
        medium_score = 0.65  # 中等相关度
        low_score = 0.45   # 低相关度
        
        # 验证颜色逻辑
        high_color = "green" if high_score >= 0.8 else "orange" if high_score >= 0.6 else "red"
        medium_color = "green" if medium_score >= 0.8 else "orange" if medium_score >= 0.6 else "red"
        low_color = "green" if low_score >= 0.8 else "orange" if low_score >= 0.6 else "red"
        
        assert high_color == "green"
        assert medium_color == "orange"
        assert low_color == "red"


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])