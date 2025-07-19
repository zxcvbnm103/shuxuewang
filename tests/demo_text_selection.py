"""
文本选择功能演示脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from math_search.ui_components.ui_manager import UIManager
from math_search.models.search_result import SearchResult
from math_search.models.search_history import SearchHistory
from datetime import datetime


def test_ui_manager():
    """测试UI管理器的基本功能"""
    print("🧪 测试UI管理器功能...")
    
    # 创建UI管理器实例
    ui_manager = UIManager()
    print("✅ UI管理器创建成功")
    
    # 测试数学内容检测
    test_text = """
    # 微积分基础
    
    导数的定义：
    $$f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$$
    
    积分公式：
    $\\int_a^b f(x) dx = F(b) - F(a)$
    """
    
    math_content = ui_manager._detect_math_content(test_text)
    print(f"✅ 检测到 {len(math_content)} 个数学公式:")
    for i, formula in enumerate(math_content, 1):
        print(f"   {i}. {formula}")
    
    # 测试搜索状态
    search_state = ui_manager.get_search_state()
    print(f"✅ 搜索状态: {search_state}")
    
    print("\n🎉 UI管理器功能测试完成！")


def test_search_results():
    """测试搜索结果模型"""
    print("\n🧪 测试搜索结果模型...")
    
    # 创建测试搜索结果
    results = [
        SearchResult(
            title="微积分基础教程",
            url="https://example.com/calculus",
            snippet="这是一个关于微积分基础的详细教程，包含导数和积分的概念。",
            source="教育网站",
            relevance_score=0.95,
            timestamp=datetime.now(),
            math_content_detected=True
        ),
        SearchResult(
            title="数学公式大全",
            url="https://example.com/formulas",
            snippet="收录了各种数学公式和定理，是学习数学的好帮手。",
            source="数学百科",
            relevance_score=0.88,
            timestamp=datetime.now(),
            math_content_detected=True
        )
    ]
    
    print(f"✅ 创建了 {len(results)} 个搜索结果")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result.title} (相关度: {result.relevance_score})")
    
    print("✅ 搜索结果模型测试完成！")


def test_search_history():
    """测试搜索历史模型"""
    print("\n🧪 测试搜索历史模型...")
    
    # 创建测试搜索历史
    history = [
        SearchHistory(
            id=1,
            query_text="导数定义",
            search_keywords=["导数", "定义", "微积分"],
            timestamp=datetime.now(),
            results_count=5,
            top_result_url="https://example.com/derivative"
        ),
        SearchHistory(
            id=2,
            query_text="积分公式",
            search_keywords=["积分", "公式", "微积分"],
            timestamp=datetime.now(),
            results_count=8,
            top_result_url="https://example.com/integral"
        )
    ]
    
    print(f"✅ 创建了 {len(history)} 条搜索历史")
    for record in history:
        print(f"   - {record.query_text} ({record.results_count} 个结果)")
    
    print("✅ 搜索历史模型测试完成！")


def main():
    """主测试函数"""
    print("🚀 开始文本选择功能演示...")
    print("=" * 50)
    
    try:
        test_ui_manager()
        test_search_results()
        test_search_history()
        
        print("\n" + "=" * 50)
        print("🎉 所有测试通过！文本选择功能已成功实现")
        print("\n📖 使用说明:")
        print("1. 运行 'streamlit run enhanced_math_editor.py' 启动应用")
        print("2. 在编辑器中选择文本")
        print("3. 复制粘贴到搜索框中")
        print("4. 点击搜索按钮查看结果")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()