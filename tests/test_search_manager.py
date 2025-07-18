"""
搜索管理器测试
Search Manager Tests
"""

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from typing import List

from math_search.search_management.search_manager import SearchManager
from math_search.models.search_result import SearchResult
from math_search.config.settings import Settings, SearchAPIConfig


class TestSearchManager:
    """搜索管理器测试类"""
    
    @pytest.fixture
    def mock_settings(self):
        """创建模拟设置"""
        settings = Settings()
        settings.search_api = SearchAPIConfig(
            google_api_key="test_google_key",
            google_search_engine_id="test_engine_id",
            bing_api_key="test_bing_key",
            max_results_per_source=5,
            request_timeout=10
        )
        return settings
    
    @pytest.fixture
    def search_manager(self, mock_settings):
        """创建搜索管理器实例"""
        return SearchManager(mock_settings)
    
    def test_init_with_valid_settings(self, mock_settings):
        """测试使用有效设置初始化"""
        manager = SearchManager(mock_settings)
        assert manager.settings == mock_settings
        assert manager.logger is not None
    
    def test_init_with_invalid_settings(self):
        """测试使用无效设置初始化"""
        settings = Settings()
        settings.search_api = SearchAPIConfig()  # 没有API密钥
        
        # 应该能够初始化，但会有警告日志
        manager = SearchManager(settings)
        assert manager.settings == settings
    
    @patch('math_search.search_management.search_manager.requests.get')
    def test_search_web_google_success(self, mock_get, search_manager):
        """测试Google搜索成功"""
        # 模拟Google API响应
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [
                {
                    'title': 'Test Math Article',
                    'link': 'https://example.com/math',
                    'snippet': 'This is about calculus and derivatives'
                },
                {
                    'title': 'Another Math Resource',
                    'link': 'https://example.com/algebra',
                    'snippet': 'Linear algebra and matrices'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        results = search_manager.search_web(['calculus', 'derivative'])
        
        assert len(results) == 2
        assert results[0].title == 'Test Math Article'
        assert results[0].url == 'https://example.com/math'
        assert results[0].source == 'Google'
        assert results[0].math_content_detected == True
        
        # 验证API调用
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert 'googleapis.com' in call_args[0][0]
        assert call_args[1]['params']['q'] == 'calculus derivative'
    
    @patch('math_search.search_management.search_manager.requests.get')
    def test_search_web_bing_fallback(self, mock_get, search_manager):
        """测试Bing搜索作为备选"""
        # 设置Google搜索失败，Bing成功
        def side_effect(url, **kwargs):
            if 'googleapis.com' in url:
                raise Exception("Google API error")
            else:
                mock_response = Mock()
                mock_response.json.return_value = {
                    'webPages': {
                        'value': [
                            {
                                'name': 'Bing Math Result',
                                'url': 'https://bing.com/math',
                                'snippet': 'Mathematics and equations'
                            }
                        ]
                    }
                }
                mock_response.raise_for_status.return_value = None
                return mock_response
        
        mock_get.side_effect = side_effect
        
        results = search_manager.search_web(['mathematics'])
        
        assert len(results) == 1
        assert results[0].title == 'Bing Math Result'
        assert results[0].source == 'Bing'
        assert mock_get.call_count == 2  # Google失败后尝试Bing
    
    @patch('math_search.search_management.search_manager.requests.get')
    def test_search_academic_arxiv_success(self, mock_get, search_manager):
        """测试arXiv学术搜索成功"""
        # 模拟arXiv API响应
        mock_response = Mock()
        mock_response.text = '''<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <id>http://arxiv.org/abs/2301.00001v1</id>
            <title>Advanced Calculus Methods</title>
            <summary>This paper discusses advanced methods in calculus...</summary>
        </entry>
        <entry>
            <id>http://arxiv.org/abs/2301.00002v1</id>
            <title>Linear Algebra Applications</title>
            <summary>Applications of linear algebra in machine learning...</summary>
        </entry>
        </feed>'''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        results = search_manager.search_academic(['calculus', 'methods'])
        
        assert len(results) == 2
        assert results[0].title == 'Advanced Calculus Methods'
        assert results[0].url == 'http://arxiv.org/abs/2301.00001v1'
        assert results[0].source == 'arXiv'
        assert results[0].math_content_detected == True
        assert results[0].relevance_score == 0.9  # 学术来源高相关度
    
    def test_search_web_empty_keywords(self, search_manager):
        """测试空关键词搜索"""
        results = search_manager.search_web([])
        assert results == []
        
        results = search_manager.search_web([''])
        assert len(results) == 0
    
    def test_search_academic_empty_keywords(self, search_manager):
        """测试学术搜索空关键词"""
        results = search_manager.search_academic([])
        assert results == []
    
    def test_combine_results_basic(self, search_manager):
        """测试基本结果合并"""
        results1 = [
            SearchResult(
                title="Result 1",
                url="https://example.com/1",
                snippet="snippet 1",
                source="Google",
                relevance_score=0.9,
                timestamp=datetime.now(),
                math_content_detected=True
            )
        ]
        
        results2 = [
            SearchResult(
                title="Result 2",
                url="https://example.com/2",
                snippet="snippet 2",
                source="Bing",
                relevance_score=0.8,
                timestamp=datetime.now(),
                math_content_detected=False
            )
        ]
        
        combined = search_manager.combine_results([results1, results2])
        
        assert len(combined) == 2
        assert combined[0].relevance_score == 0.9  # 按相关度排序
        assert combined[1].relevance_score == 0.8
    
    def test_combine_results_deduplication(self, search_manager):
        """测试结果去重"""
        duplicate_result = SearchResult(
            title="Duplicate Result",
            url="https://example.com/same",
            snippet="same snippet",
            source="Google",
            relevance_score=0.9,
            timestamp=datetime.now(),
            math_content_detected=True
        )
        
        results1 = [duplicate_result]
        results2 = [duplicate_result]  # 相同URL
        
        combined = search_manager.combine_results([results1, results2])
        
        assert len(combined) == 1  # 去重后只有一个结果
    
    def test_detect_math_content_english(self, search_manager):
        """测试英文数学内容检测"""
        # 包含数学关键词
        assert search_manager._detect_math_content("This is about calculus and derivatives") == True
        assert search_manager._detect_math_content("Linear algebra with matrices") == True
        assert search_manager._detect_math_content("Probability and statistics") == True
        
        # 包含LaTeX符号
        assert search_manager._detect_math_content("The equation $x^2 + y^2 = 1$") == True
        assert search_manager._detect_math_content("\\frac{1}{2} is a fraction") == True
        
        # 不包含数学内容
        assert search_manager._detect_math_content("This is just regular text") == False
        assert search_manager._detect_math_content("") == False
    
    def test_detect_math_content_chinese(self, search_manager):
        """测试中文数学内容检测"""
        assert search_manager._detect_math_content("这是关于微积分的内容") == True
        assert search_manager._detect_math_content("线性代数和矩阵") == True
        assert search_manager._detect_math_content("概率统计方法") == True
        
        # 不包含数学内容
        assert search_manager._detect_math_content("这只是普通文本") == False
    
    @patch('math_search.search_management.search_manager.requests.get')
    def test_search_web_api_error_handling(self, mock_get, search_manager):
        """测试API错误处理"""
        # 模拟网络错误
        mock_get.side_effect = Exception("Network error")
        
        results = search_manager.search_web(['test'])
        
        # 应该返回空结果而不是抛出异常
        assert results == []
    
    @patch('math_search.search_management.search_manager.requests.get')
    def test_search_web_timeout_handling(self, mock_get, search_manager):
        """测试超时处理"""
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        results = search_manager.search_web(['test'])
        assert results == []
    
    def test_max_results_limit(self, search_manager):
        """测试结果数量限制"""
        # 设置较小的限制
        search_manager.settings.search_api.max_results_per_source = 2
        
        with patch('math_search.search_management.search_manager.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                'items': [
                    {'title': f'Result {i}', 'link': f'https://example.com/{i}', 'snippet': f'snippet {i}'}
                    for i in range(5)  # 返回5个结果
                ]
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            results = search_manager.search_web(['test'])
            
            # 应该只返回2个结果（受限制）
            assert len(results) == 2


class TestSearchManagerIntegration:
    """搜索管理器集成测试"""
    
    @pytest.fixture
    def integration_settings(self):
        """集成测试设置（使用模拟API）"""
        settings = Settings()
        settings.search_api = SearchAPIConfig(
            google_api_key="mock_key",
            google_search_engine_id="mock_engine",
            max_results_per_source=3,
            request_timeout=5
        )
        return settings
    
    def test_full_search_workflow(self, integration_settings):
        """测试完整搜索工作流"""
        manager = SearchManager(integration_settings)
        
        with patch('math_search.search_management.search_manager.requests.get') as mock_get:
            # 模拟Google搜索响应
            google_response = Mock()
            google_response.json.return_value = {
                'items': [
                    {
                        'title': 'Calculus Tutorial',
                        'link': 'https://math.com/calculus',
                        'snippet': 'Learn derivatives and integrals'
                    }
                ]
            }
            google_response.raise_for_status.return_value = None
            
            # 模拟arXiv搜索响应
            arxiv_response = Mock()
            arxiv_response.text = '''
            <entry>
                <id>http://arxiv.org/abs/2301.00001v1</id>
                <title>Advanced Calculus</title>
                <summary>Research on calculus methods</summary>
            </entry>
            '''
            arxiv_response.raise_for_status.return_value = None
            
            def mock_get_side_effect(url, **kwargs):
                if 'googleapis.com' in url:
                    return google_response
                elif 'arxiv.org' in url:
                    return arxiv_response
                else:
                    raise Exception("Unknown URL")
            
            mock_get.side_effect = mock_get_side_effect
            
            # 执行搜索
            web_results = manager.search_web(['calculus'])
            academic_results = manager.search_academic(['calculus'])
            
            # 合并结果
            combined = manager.combine_results([web_results, academic_results])
            
            assert len(web_results) == 1
            assert len(academic_results) == 1
            assert len(combined) == 2
            assert combined[0].relevance_score >= combined[1].relevance_score  # 按相关度排序


# 模拟测试辅助函数
def create_mock_search_result(title: str, url: str, source: str, relevance: float = 0.8) -> SearchResult:
    """创建模拟搜索结果"""
    return SearchResult(
        title=title,
        url=url,
        snippet=f"This is a snippet for {title}",
        source=source,
        relevance_score=relevance,
        timestamp=datetime.now(),
        math_content_detected=True
    )


# 性能测试
class TestSearchManagerPerformance:
    """搜索管理器性能测试"""
    
    def test_large_result_handling(self):
        """测试大量结果处理"""
        settings = Settings()
        manager = SearchManager(settings)
        
        # 创建大量模拟结果（确保相关度在0-1范围内）
        large_results = [
            [create_mock_search_result(f"Result {i}", f"https://example.com/{i}", "Google", 0.5 + (i % 50) * 0.01)
             for i in range(100)]
        ]
        
        # 测试合并性能
        import time
        start_time = time.time()
        combined = manager.combine_results(large_results)
        end_time = time.time()
        
        assert len(combined) == 100
        assert end_time - start_time < 1.0  # 应该在1秒内完成
        
        # 验证排序正确性
        for i in range(len(combined) - 1):
            assert combined[i].relevance_score >= combined[i + 1].relevance_score