"""
搜索管理器实现
Search Manager Implementation
"""

import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from urllib.parse import urlencode

from ..interfaces.search_manager import ISearchManager
from ..models.search_result import SearchResult
from ..config.settings import Settings


class SearchManager(ISearchManager):
    """搜索管理器实现类"""
    
    def __init__(self, settings: Settings):
        """
        初始化搜索管理器
        
        Args:
            settings: 应用配置
        """
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        
        # 验证配置
        config_errors = settings.validate()
        if config_errors:
            self.logger.warning(f"配置验证警告: {', '.join(config_errors)}")
    
    def search_web(self, keywords: List[str]) -> List[SearchResult]:
        """
        网页搜索
        
        Args:
            keywords: 搜索关键词列表
            
        Returns:
            搜索结果列表
        """
        if not keywords:
            return []
        
        query = " ".join(keywords)
        results = []
        
        # 尝试Google搜索
        if self.settings.search_api.google_api_key and self.settings.search_api.google_search_engine_id:
            try:
                google_results = self._search_google(query)
                results.extend(google_results)
                self.logger.info(f"Google搜索返回 {len(google_results)} 个结果")
            except Exception as e:
                self.logger.error(f"Google搜索失败: {e}")
        
        # 如果Google搜索失败或没有配置，尝试Bing搜索
        if not results and self.settings.search_api.bing_api_key:
            try:
                bing_results = self._search_bing(query)
                results.extend(bing_results)
                self.logger.info(f"Bing搜索返回 {len(bing_results)} 个结果")
            except Exception as e:
                self.logger.error(f"Bing搜索失败: {e}")
        
        return results[:self.settings.search_api.max_results_per_source]
    
    def search_academic(self, keywords: List[str]) -> List[SearchResult]:
        """
        学术搜索
        
        Args:
            keywords: 搜索关键词列表
            
        Returns:
            学术搜索结果列表
        """
        if not keywords:
            return []
        
        query = " ".join(keywords)
        results = []
        
        # arXiv搜索
        try:
            arxiv_results = self._search_arxiv(query)
            results.extend(arxiv_results)
            self.logger.info(f"arXiv搜索返回 {len(arxiv_results)} 个结果")
        except Exception as e:
            self.logger.error(f"arXiv搜索失败: {e}")
        
        return results[:self.settings.search_api.max_results_per_source]
    
    def combine_results(self, results: List[List[SearchResult]]) -> List[SearchResult]:
        """
        合并搜索结果
        
        Args:
            results: 多个搜索结果列表
            
        Returns:
            合并后的搜索结果列表
        """
        combined = []
        seen_urls = set()
        
        # 合并所有结果，去重
        for result_list in results:
            for result in result_list:
                if result.url not in seen_urls:
                    combined.append(result)
                    seen_urls.add(result.url)
        
        # 按相关度排序
        combined.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return combined
    
    def _search_google(self, query: str) -> List[SearchResult]:
        """
        Google Custom Search API搜索
        
        Args:
            query: 搜索查询
            
        Returns:
            搜索结果列表
        """
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.settings.search_api.google_api_key,
            'cx': self.settings.search_api.google_search_engine_id,
            'q': query,
            'num': min(10, self.settings.search_api.max_results_per_source)
        }
        
        response = requests.get(
            url, 
            params=params, 
            timeout=self.settings.search_api.request_timeout
        )
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        for item in data.get('items', []):
            # 检测数学内容
            math_detected = self._detect_math_content(
                item.get('title', '') + ' ' + item.get('snippet', '')
            )
            
            result = SearchResult(
                title=item.get('title', ''),
                url=item.get('link', ''),
                snippet=item.get('snippet', ''),
                source='Google',
                relevance_score=0.8,  # 默认相关度，后续会被相关度计算器重新计算
                timestamp=datetime.now(),
                math_content_detected=math_detected
            )
            results.append(result)
        
        return results
    
    def _search_bing(self, query: str) -> List[SearchResult]:
        """
        Bing Search API搜索
        
        Args:
            query: 搜索查询
            
        Returns:
            搜索结果列表
        """
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {
            'Ocp-Apim-Subscription-Key': self.settings.search_api.bing_api_key
        }
        params = {
            'q': query,
            'count': min(10, self.settings.search_api.max_results_per_source)
        }
        
        response = requests.get(
            url, 
            headers=headers, 
            params=params,
            timeout=self.settings.search_api.request_timeout
        )
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        for item in data.get('webPages', {}).get('value', []):
            # 检测数学内容
            math_detected = self._detect_math_content(
                item.get('name', '') + ' ' + item.get('snippet', '')
            )
            
            result = SearchResult(
                title=item.get('name', ''),
                url=item.get('url', ''),
                snippet=item.get('snippet', ''),
                source='Bing',
                relevance_score=0.8,  # 默认相关度
                timestamp=datetime.now(),
                math_content_detected=math_detected
            )
            results.append(result)
        
        return results
    
    def _search_arxiv(self, query: str) -> List[SearchResult]:
        """
        arXiv API搜索
        
        Args:
            query: 搜索查询
            
        Returns:
            搜索结果列表
        """
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': min(10, self.settings.search_api.max_results_per_source)
        }
        
        url = f"{self.settings.search_api.arxiv_base_url}?{urlencode(params)}"
        
        response = requests.get(url, timeout=self.settings.search_api.request_timeout)
        response.raise_for_status()
        
        # 简单的XML解析（实际项目中应该使用专门的XML解析库）
        results = []
        content = response.text
        
        # 这里使用简单的字符串解析，实际应该使用xml.etree.ElementTree
        entries = content.split('<entry>')
        for entry in entries[1:]:  # 跳过第一个空条目
            try:
                title_start = entry.find('<title>') + 7
                title_end = entry.find('</title>')
                title = entry[title_start:title_end].strip() if title_start > 6 else ''
                
                summary_start = entry.find('<summary>') + 9
                summary_end = entry.find('</summary>')
                summary = entry[summary_start:summary_end].strip() if summary_start > 8 else ''
                
                id_start = entry.find('<id>') + 4
                id_end = entry.find('</id>')
                arxiv_id = entry[id_start:id_end].strip() if id_start > 3 else ''
                
                if title and arxiv_id:
                    result = SearchResult(
                        title=title,
                        url=arxiv_id,
                        snippet=summary[:200] + '...' if len(summary) > 200 else summary,
                        source='arXiv',
                        relevance_score=0.9,  # 学术来源给予更高的默认相关度
                        timestamp=datetime.now(),
                        math_content_detected=True  # arXiv主要是学术论文，假设包含数学内容
                    )
                    results.append(result)
            except Exception as e:
                self.logger.warning(f"解析arXiv条目失败: {e}")
                continue
        
        return results
    
    def _detect_math_content(self, text: str) -> bool:
        """
        检测文本中是否包含数学内容
        
        Args:
            text: 待检测文本
            
        Returns:
            是否包含数学内容
        """
        if not text:
            return False
        
        # 简单的数学内容检测
        math_keywords = [
            'equation', 'formula', 'theorem', 'proof', 'mathematics', 'calculus',
            'algebra', 'geometry', 'statistics', 'probability', 'function',
            'derivative', 'integral', 'matrix', 'vector', 'polynomial',
            '方程', '公式', '定理', '证明', '数学', '微积分', '代数', '几何',
            '统计', '概率', '函数', '导数', '积分', '矩阵', '向量', '多项式'
        ]
        
        text_lower = text.lower()
        for keyword in math_keywords:
            if keyword in text_lower:
                return True
        
        # 检测LaTeX符号
        latex_patterns = ['$', '\\', '_{', '^{', '\\frac', '\\sum', '\\int']
        for pattern in latex_patterns:
            if pattern in text:
                return True
        
        return False