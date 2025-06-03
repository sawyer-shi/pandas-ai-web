import re

class ChartAnalyzer:
    """图表分析工具类，用于处理和检测用户的数据可视化需求"""
    
    @staticmethod
    def is_visualization_required(question):
        """
        判断用户问题是否需要生成可视化图表
        
        Args:
            question: 用户问题
            
        Returns:
            bool: 是否需要生成图表
        """
        # 转换为小写以便匹配
        question_lower = question.lower()
        
        # 图表相关关键词 - 中文
        chart_keywords_zh = [
            '图', '图表', '图像', '可视化', '画', '绘制', '画图', '制图',
            '柱状图', '条形图', '饼图', '折线图', '散点图', '直方图', '箱线图',
            '分布', '趋势', '变化', '对比', '比较',
            '显示', '展示', '呈现'
        ]
        
        # 图表相关关键词 - 英文
        chart_keywords_en = [
            'chart', 'graph', 'plot', 'visualize', 'visualization', 'draw', 'show',
            'bar chart', 'pie chart', 'line chart', 'scatter plot', 'histogram', 'boxplot',
            'distribution', 'trend', 'comparison', 'compare',
            'display', 'present', 'illustrate'
        ]
        
        # 数据分析可视化关键词
        analysis_keywords = [
            '分析', '统计', '总结', '概述', '模式', '规律',
            'analysis', 'statistics', 'summary', 'pattern', 'insight'
        ]
        
        # 检查是否包含图表关键词
        for keyword in chart_keywords_zh + chart_keywords_en:
            if keyword in question_lower:
                return True
        
        # 检查是否是分析类问题（可能需要图表辅助说明）
        analysis_count = 0
        for keyword in analysis_keywords:
            if keyword in question_lower:
                analysis_count += 1
        
        # 如果包含多个分析关键词，建议生成图表
        if analysis_count >= 2:
            return True
        
        # 检查特定的问句模式
        pattern_keywords = [
            '什么样', '如何', '怎样', '哪些', '什么关系', '什么特点',
            'what', 'how', 'which', 'relationship', 'feature', 'characteristic'
        ]
        
        for pattern in pattern_keywords:
            if pattern in question_lower and analysis_count >= 1:
                return True
        
        return False 