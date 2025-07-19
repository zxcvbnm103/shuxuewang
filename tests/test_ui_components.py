"""
UI组件单元测试
"""
import unittest
import sys
import os
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from math_search.ui_components.ui_manager import UIManager
from math_search.models.search_result import SearchResult
from math_search.models.search_history import SearchHistory


class TestUIManager(unittest.TestCase):
    """UI管理器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.ui_manager = UIManager()
    
    def test_ui_manager_initialization(self):
        """测试UI管理器初始化"""
        self.assertIsInstance(self.ui_manager, UIManager)
    
    def test_detect_math_content(self):
        """测试数学内容检测功能"""
        # 测试包含LaTeX公式的文本
        text_with_math = """
        这是一个包含数学公式的文本：
        $$f(x) = x^2 + 2x + 1$$
        还有行内公式 $y = mx + b$
        以及环境公式：
        \\begin{equation}
        E = mc^2
        \\end{equation}
        """
        
        math_content = self.ui_manager._detect_math_content(text_with_math)
        
        # 应该检测到至少2个数学公式
        self.assertGreaterEqual(len(math_content), 2)
        
        # 检查是否包含预期的公式
        formula_found = any('f(x) = x^2 + 2x + 1' in formula for formula in math_content)
        self.assertTrue(formula_found, "应该检测到块级公式")
        
        inline_found = any('y = mx + b' in formula for formula in math_content)
        self.assertTrue(inline_found, "应该检测到行内公式")
    
    def test_detect_math_content_empty(self):
        """测试空文本的数学内容检测"""
        empty_text = ""
        math_content = self.ui_manager._detect_math_content(empty_text)
        self.assertEqual(len(math_content), 0)
        
        # 测试无数学内容的文本
        plain_text = "这是一段普通的文本，没有任何数学公式。"
        math_content = self.ui_manager._detect_math_content(plain_text)
        self.assertEqual(len(math_content), 0)
    
    def test_get_search_state(self):
        """测试获取搜索状态"""
        # 由于在测试环境中没有Streamlit session state，
        # 这个测试主要验证方法不会抛出异常
        try:
            search_state = self.ui_manager.get_search_state()
            self.assertIsInstance(search_state, dict)
            
            # 验证返回的字典包含必要的键
            expected_keys = ['selected_text', 'search_triggered', 'has_results']
            for key in expected_keys:
                self.assertIn(key, search_state)
                
        except Exception as e:
            # 在测试环境中，Streamlit session state可能不可用
            # 这是预期的行为
            self.assertIn('session_state', str(e).lower())


class TestSearchResultIntegration(unittest.TestCase):
    """搜索结果集成测试"""
    
    def test_search_result_creation(self):
        """测试搜索结果创建"""
        result = SearchResult(
            title="测试标题",
            url="https://example.com",
            snippet="测试摘要",
            source="测试来源",
            relevance_score=0.85,
            timestamp=datetime.now(),
            math_content_detected=True
        )
        
        self.assertEqual(result.title, "测试标题")
        self.assertEqual(result.url, "https://example.com")
        self.assertEqual(result.relevance_score, 0.85)
        self.assertTrue(result.math_content_detected)
    
    def test_search_result_sorting(self):
        """测试搜索结果排序"""
        results = [
            SearchResult(
                title="结果1",
                url="https://example1.com",
                snippet="摘要1",
                source="来源1",
                relevance_score=0.7,
                timestamp=datetime.now(),
                math_content_detected=False
            ),
            SearchResult(
                title="结果2",
                url="https://example2.com",
                snippet="摘要2",
                source="来源2",
                relevance_score=0.9,
                timestamp=datetime.now(),
                math_content_detected=True
            ),
            SearchResult(
                title="结果3",
                url="https://example3.com",
                snippet="摘要3",
                source="来源3",
                relevance_score=0.8,
                timestamp=datetime.now(),
                math_content_detected=True
            )
        ]
        
        # 按相关度排序
        sorted_results = sorted(results, key=lambda x: x.relevance_score, reverse=True)
        
        self.assertEqual(sorted_results[0].relevance_score, 0.9)
        self.assertEqual(sorted_results[1].relevance_score, 0.8)
        self.assertEqual(sorted_results[2].relevance_score, 0.7)


class TestSearchHistoryIntegration(unittest.TestCase):
    """搜索历史集成测试"""
    
    def test_search_history_creation(self):
        """测试搜索历史创建"""
        history = SearchHistory(
            id=1,
            query_text="测试查询",
            search_keywords=["测试", "查询"],
            timestamp=datetime.now(),
            results_count=5,
            top_result_url="https://example.com"
        )
        
        self.assertEqual(history.id, 1)
        self.assertEqual(history.query_text, "测试查询")
        self.assertEqual(len(history.search_keywords), 2)
        self.assertEqual(history.results_count, 5)
    
    def test_search_history_sorting(self):
        """测试搜索历史排序"""
        now = datetime.now()
        
        history_list = [
            SearchHistory(
                id=1,
                query_text="查询1",
                search_keywords=["关键词1"],
                timestamp=datetime(2023, 1, 1),
                results_count=3,
                top_result_url="https://example1.com"
            ),
            SearchHistory(
                id=2,
                query_text="查询2",
                search_keywords=["关键词2"],
                timestamp=now,
                results_count=5,
                top_result_url="https://example2.com"
            )
        ]
        
        # 按时间排序（最新的在前）
        sorted_history = sorted(history_list, key=lambda x: x.timestamp, reverse=True)
        
        self.assertEqual(sorted_history[0].id, 2)  # 最新的记录
        self.assertEqual(sorted_history[1].id, 1)  # 较旧的记录


class TestMathContentDetection(unittest.TestCase):
    """数学内容检测专项测试"""
    
    def setUp(self):
        """测试前准备"""
        self.ui_manager = UIManager()
    
    def test_latex_block_formulas(self):
        """测试LaTeX块级公式检测"""
        text = "这里有一个块级公式：$$\\int_0^1 x^2 dx = \\frac{1}{3}$$"
        math_content = self.ui_manager._detect_math_content(text)
        
        self.assertGreater(len(math_content), 0)
        block_formula_found = any('\\int_0^1 x^2 dx' in formula for formula in math_content)
        self.assertTrue(block_formula_found)
    
    def test_latex_inline_formulas(self):
        """测试LaTeX行内公式检测"""
        text = "这里有一个行内公式：$f(x) = x^2$，很简单。"
        math_content = self.ui_manager._detect_math_content(text)
        
        self.assertGreater(len(math_content), 0)
        inline_formula_found = any('f(x) = x^2' in formula for formula in math_content)
        self.assertTrue(inline_formula_found)
    
    def test_latex_environments(self):
        """测试LaTeX环境检测"""
        text = """
        \\begin{align}
        x + y &= 1 \\\\
        x - y &= 0
        \\end{align}
        """
        math_content = self.ui_manager._detect_math_content(text)
        
        self.assertGreater(len(math_content), 0)
        env_found = any('begin{align}' in formula for formula in math_content)
        self.assertTrue(env_found)
    
    def test_mixed_math_content(self):
        """测试混合数学内容检测"""
        text = """
        # 数学公式示例
        
        行内公式：$a^2 + b^2 = c^2$
        
        块级公式：
        $$\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$$
        
        环境公式：
        \\begin{equation}
        E = mc^2
        \\end{equation}
        
        LaTeX命令：\\sqrt{x+1}
        """
        
        math_content = self.ui_manager._detect_math_content(text)
        
        # 应该检测到多个数学公式
        self.assertGreaterEqual(len(math_content), 3)
        
        # 验证不同类型的公式都被检测到
        has_inline = any('a^2 + b^2 = c^2' in formula for formula in math_content)
        has_block = any('\\sum_{i=1}^n i' in formula for formula in math_content)
        has_env = any('E = mc^2' in formula for formula in math_content)
        
        self.assertTrue(has_inline, "应该检测到行内公式")
        self.assertTrue(has_block, "应该检测到块级公式")
        self.assertTrue(has_env, "应该检测到环境公式")


def run_tests():
    """运行所有测试"""
    print("🧪 开始运行UI组件测试...")
    print("=" * 60)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestUIManager,
        TestSearchResultIntegration,
        TestSearchHistoryIntegration,
        TestMathContentDetection
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 所有测试通过！")
        print(f"✅ 运行了 {result.testsRun} 个测试")
    else:
        print("❌ 部分测试失败")
        print(f"失败: {len(result.failures)}, 错误: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)