import os
import pandas as pd
from .language_utils import LanguageUtils

class DataLoader:
    """数据加载工具类，负责加载CSV和Excel文件"""
    
    @staticmethod
    def load_file(file_path, language="zh"):
        """
        从文件路径加载数据
        
        Args:
            file_path: 文件路径
            language: 语言代码 ("zh" 或 "en")
            
        Returns:
            tuple: (数据帧, 状态消息, 成功标志)
        """
        if file_path is None:
            return None, LanguageUtils.get_text(language, "waiting_upload"), False
        
        try:
            # 获取文件扩展名
            file_ext = os.path.splitext(file_path)[1].lower()
            file_name = os.path.basename(file_path)
            dataframe = None
            encoding = None
        
            if file_ext == '.csv':
                # 尝试用不同的编码打开CSV文件
                encodings = ['utf-8', 'latin1', 'gbk', 'gb2312', 'shift-jis']
                for enc in encodings:
                    try:
                        dataframe = pd.read_csv(file_path, encoding=enc)
                        encoding = enc
                        break
                    except UnicodeDecodeError:
                        continue
                
                if dataframe is None:
                    return None, LanguageUtils.get_text(language, "encoding_error"), False
                    
            elif file_ext in ['.xls', '.xlsx', '.xlsm']:
                dataframe = pd.read_excel(file_path)
            else:
                return None, LanguageUtils.get_text(language, "unsupported_format", file_ext), False
            
            # 检查数据帧是否成功加载
            if dataframe is None or len(dataframe) == 0:
                return None, LanguageUtils.get_text(language, "no_valid_data"), False
            
            # 成功加载
            row_count = len(dataframe)
            
            # 返回成功状态
            if encoding:
                return dataframe, LanguageUtils.get_text(language, "file_loaded_encoding", row_count, encoding), True
            else:
                return dataframe, LanguageUtils.get_text(language, "file_loaded", row_count), True
            
        except Exception as e:
            return None, LanguageUtils.get_text(language, "load_error", str(e)), False
    
    @staticmethod
    def generate_preview_html(dataframe, max_rows=500, language="zh"):
        """
        生成数据预览HTML
        
        Args:
            dataframe: 数据帧
            max_rows: 最大显示行数
            language: 语言代码 ("zh" 或 "en")
            
        Returns:
            str: HTML预览
        """
        if dataframe is None:
            return ""
        
        row_count = len(dataframe)
        max_display_rows = min(max_rows, row_count)
        
        # 创建完整的HTML表格预览，带有行数统计信息
        if row_count <= max_display_rows:
            preview_html = f"<div style='margin-bottom:10px;'>{LanguageUtils.get_text(language, 'total_rows', row_count)}</div>"
            preview_html += dataframe.to_html(index=True, max_rows=None)
        else:
            preview_html = f"<div style='margin-bottom:10px;'>{LanguageUtils.get_text(language, 'total_rows_limit', row_count, max_display_rows)}</div>"
            preview_html += dataframe.head(max_display_rows).to_html(index=True)
            
        return preview_html 