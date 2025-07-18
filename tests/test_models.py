"""
数据模型单元测试
Data Models Unit Tests
"""

import unittest
from datetime import datetime
from math_search.models import SearchResult, SearchHistory, MathTerm


class TestSearchResult(unittest.TestCase):
    """SearchResult 数据模型测试"""
    
    def setUp(self):
        """测试前准备"""
        self.valid_data = {
            'title': '线性代数基础',
            'url': 'https://example.com/linear-algebra',
            'snippet': '线性代数是数学的一个分支...',
            'source': 'Wikipedia',
            'relevance_score': 0.85,
            'timestamp': datetime.now(),
            'math_content_detected': True
        }
    
    def test_valid_search_result_creation(self):
        """测试有效的搜索结果创建"""
        result = SearchResult(**self.valid_data)
        self.assertEqual(result.title, self.valid_data['title'])
        self.assertEqual(result.url, self.valid_data['url'])
        self.assertEqual(result.relevance_score, self.valid_data['relevance_score'])
        self.assertTrue(result.math_content_detected)
    
    def test_empty_title_validation(self):
        """测试空标题验证"""
        invalid_data = self.valid_data.copy()
        invalid_data['title'] = ''
        with self.assertRaises(ValueError) as context:
            SearchResult(**invalid_data)
        self.assertIn('标题和URL不能为空', str(context.exception))
    
    def test_empty_url_validation(self):
        """测试空URL验证"""
        invalid_data = self.valid_data.copy()
        invalid_data['url'] = ''
        with self.assertRaises(ValueError) as context:
            SearchResult(**invalid_data)
        self.assertIn('标题和URL不能为空', str(context.exception))
    
    def test_invalid_relevance_score_validation(self):
        """测试无效相关度评分验证"""
        # 测试负数
        invalid_data = self.valid_data.copy()
        invalid_data['relevance_score'] = -0.1
        with self.assertRaises(ValueError) as context:
            SearchResult(**invalid_data)
        self.assertIn('相关度评分必须在0-1之间', str(context.exception))
        
        # 测试大于1的数
        invalid_data['relevance_score'] = 1.1
        with self.assertRaises(ValueError) as context:
            SearchResult(**invalid_data)
        self.assertIn('相关度评分必须在0-1之间', str(context.exception))
    
    def test_to_dict_serialization(self):
        """测试字典序列化"""
        result = SearchResult(**self.valid_data)
        result_dict = result.to_dict()
        
        self.assertEqual(result_dict['title'], self.valid_data['title'])
        self.assertEqual(result_dict['url'], self.valid_data['url'])
        self.assertEqual(result_dict['relevance_score'], self.valid_data['relevance_score'])
        self.assertIsInstance(result_dict['timestamp'], str)  # 应该被转换为ISO格式字符串
    
    def test_from_dict_deserialization(self):
        """测试字典反序列化"""
        result = SearchResult(**self.valid_data)
        result_dict = result.to_dict()
        reconstructed_result = SearchResult.from_dict(result_dict)
        
        self.assertEqual(reconstructed_result.title, result.title)
        self.assertEqual(reconstructed_result.url, result.url)
        self.assertEqual(reconstructed_result.relevance_score, result.relevance_score)
        self.assertEqual(reconstructed_result.timestamp, result.timestamp)


class TestSearchHistory(unittest.TestCase):
    """SearchHistory 数据模型测试"""
    
    def setUp(self):
        """测试前准备"""
        self.valid_data = {
            'id': 1,
            'query_text': '线性代数矩阵运算',
            'search_keywords': ['线性代数', '矩阵', '运算'],
            'timestamp': datetime.now(),
            'results_count': 15,
            'top_result_url': 'https://example.com/top-result'
        }
    
    def test_valid_search_history_creation(self):
        """测试有效的搜索历史创建"""
        history = SearchHistory(**self.valid_data)
        self.assertEqual(history.id, self.valid_data['id'])
        self.assertEqual(history.query_text, self.valid_data['query_text'])
        self.assertEqual(history.search_keywords, self.valid_data['search_keywords'])
        self.assertEqual(history.results_count, self.valid_data['results_count'])
    
    def test_empty_query_text_validation(self):
        """测试空查询文本验证"""
        invalid_data = self.valid_data.copy()
        invalid_data['query_text'] = ''
        with self.assertRaises(ValueError) as context:
            SearchHistory(**invalid_data)
        self.assertIn('查询文本不能为空', str(context.exception))
    
    def test_negative_results_count_validation(self):
        """测试负数结果数量验证"""
        invalid_data = self.valid_data.copy()
        invalid_data['results_count'] = -1
        with self.assertRaises(ValueError) as context:
            SearchHistory(**invalid_data)
        self.assertIn('结果数量不能为负数', str(context.exception))
    
    def test_empty_keywords_validation(self):
        """测试空关键词验证"""
        invalid_data = self.valid_data.copy()
        invalid_data['search_keywords'] = []
        with self.assertRaises(ValueError) as context:
            SearchHistory(**invalid_data)
        self.assertIn('搜索关键词不能为空', str(context.exception))
    
    def test_negative_id_validation(self):
        """测试负数ID验证"""
        invalid_data = self.valid_data.copy()
        invalid_data['id'] = -1
        with self.assertRaises(ValueError) as context:
            SearchHistory(**invalid_data)
        self.assertIn('ID不能为负数', str(context.exception))
    
    def test_to_dict_serialization(self):
        """测试字典序列化"""
        history = SearchHistory(**self.valid_data)
        history_dict = history.to_dict()
        
        self.assertEqual(history_dict['id'], self.valid_data['id'])
        self.assertEqual(history_dict['query_text'], self.valid_data['query_text'])
        self.assertEqual(history_dict['search_keywords'], self.valid_data['search_keywords'])
        self.assertIsInstance(history_dict['timestamp'], str)
    
    def test_from_dict_deserialization(self):
        """测试字典反序列化"""
        history = SearchHistory(**self.valid_data)
        history_dict = history.to_dict()
        reconstructed_history = SearchHistory.from_dict(history_dict)
        
        self.assertEqual(reconstructed_history.id, history.id)
        self.assertEqual(reconstructed_history.query_text, history.query_text)
        self.assertEqual(reconstructed_history.search_keywords, history.search_keywords)
        self.assertEqual(reconstructed_history.timestamp, history.timestamp)
    
    def test_get_summary(self):
        """测试获取摘要功能"""
        history = SearchHistory(**self.valid_data)
        summary = history.get_summary()
        
        self.assertIn(self.valid_data['query_text'], summary)
        self.assertIn('线性代数', summary)
        self.assertIn(str(self.valid_data['results_count']), summary)
    
    def test_get_summary_with_long_text(self):
        """测试长文本摘要截断"""
        long_data = self.valid_data.copy()
        long_data['query_text'] = 'a' * 100  # 超过50字符的长文本
        long_data['search_keywords'] = ['keyword1', 'keyword2', 'keyword3', 'keyword4', 'keyword5']  # 超过3个关键词
        
        history = SearchHistory(**long_data)
        summary = history.get_summary()
        
        self.assertIn('...', summary)  # 应该包含截断标记


class TestMathTerm(unittest.TestCase):
    """MathTerm 数据模型测试"""
    
    def setUp(self):
        """测试前准备"""
        self.valid_data = {
            'term': '导数',
            'latex_representation': r'\frac{d}{dx}',
            'category': 'calculus',
            'confidence': 0.9
        }
    
    def test_valid_math_term_creation(self):
        """测试有效的数学术语创建"""
        term = MathTerm(**self.valid_data)
        self.assertEqual(term.term, self.valid_data['term'])
        self.assertEqual(term.latex_representation, self.valid_data['latex_representation'])
        self.assertEqual(term.category, self.valid_data['category'])
        self.assertEqual(term.confidence, self.valid_data['confidence'])
    
    def test_empty_term_validation(self):
        """测试空术语验证"""
        invalid_data = self.valid_data.copy()
        invalid_data['term'] = ''
        with self.assertRaises(ValueError) as context:
            MathTerm(**invalid_data)
        self.assertIn('术语不能为空', str(context.exception))
    
    def test_invalid_confidence_validation(self):
        """测试无效置信度验证"""
        # 测试负数
        invalid_data = self.valid_data.copy()
        invalid_data['confidence'] = -0.1
        with self.assertRaises(ValueError) as context:
            MathTerm(**invalid_data)
        self.assertIn('置信度必须在0-1之间', str(context.exception))
        
        # 测试大于1的数
        invalid_data['confidence'] = 1.1
        with self.assertRaises(ValueError) as context:
            MathTerm(**invalid_data)
        self.assertIn('置信度必须在0-1之间', str(context.exception))
    
    def test_invalid_category_validation(self):
        """测试无效类别验证"""
        invalid_data = self.valid_data.copy()
        invalid_data['category'] = 'invalid_category'
        with self.assertRaises(ValueError) as context:
            MathTerm(**invalid_data)
        self.assertIn('无效的数学类别', str(context.exception))
    
    def test_valid_categories(self):
        """测试所有有效类别"""
        valid_categories = [
            'algebra', 'calculus', 'geometry', 'statistics', 
            'linear_algebra', 'differential_equations', 'topology',
            'number_theory', 'discrete_math', 'analysis', 'other'
        ]
        
        for category in valid_categories:
            data = self.valid_data.copy()
            data['category'] = category
            term = MathTerm(**data)  # 不应该抛出异常
            self.assertEqual(term.category, category)
    
    def test_to_dict_serialization(self):
        """测试字典序列化"""
        term = MathTerm(**self.valid_data)
        term_dict = term.to_dict()
        
        self.assertEqual(term_dict['term'], self.valid_data['term'])
        self.assertEqual(term_dict['latex_representation'], self.valid_data['latex_representation'])
        self.assertEqual(term_dict['category'], self.valid_data['category'])
        self.assertEqual(term_dict['confidence'], self.valid_data['confidence'])
    
    def test_from_dict_deserialization(self):
        """测试字典反序列化"""
        term = MathTerm(**self.valid_data)
        term_dict = term.to_dict()
        reconstructed_term = MathTerm.from_dict(term_dict)
        
        self.assertEqual(reconstructed_term.term, term.term)
        self.assertEqual(reconstructed_term.latex_representation, term.latex_representation)
        self.assertEqual(reconstructed_term.category, term.category)
        self.assertEqual(reconstructed_term.confidence, term.confidence)
    
    def test_is_high_confidence(self):
        """测试高置信度判断"""
        # 测试高置信度
        high_confidence_data = self.valid_data.copy()
        high_confidence_data['confidence'] = 0.85
        high_term = MathTerm(**high_confidence_data)
        self.assertTrue(high_term.is_high_confidence())
        
        # 测试低置信度
        low_confidence_data = self.valid_data.copy()
        low_confidence_data['confidence'] = 0.7
        low_term = MathTerm(**low_confidence_data)
        self.assertFalse(low_term.is_high_confidence())
        
        # 测试边界值
        boundary_data = self.valid_data.copy()
        boundary_data['confidence'] = 0.8
        boundary_term = MathTerm(**boundary_data)
        self.assertTrue(boundary_term.is_high_confidence())


if __name__ == '__main__':
    unittest.main()