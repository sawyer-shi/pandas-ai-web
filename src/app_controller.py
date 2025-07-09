import os
import socket
import time
import uuid
import json
import requests
from datetime import datetime
import matplotlib

from pandasai import Agent

from .utils.language_utils import LanguageUtils
from .utils.data_loader import DataLoader
from .utils.chart_analyzer import ChartAnalyzer
from .utils.oss_uploader import OSSUploader
from .utils.image_utils import create_image_html
from .utils.font_config import get_chinese_plot_kwargs, ensure_chinese_font_for_pandasai
from .database.db_manager import DBManager
from .config.config_manager import ConfigManager
from .llm.llm_factory import LLMFactory
from .storage.chart_storage import chart_storage

class AppController:
    """应用控制器类，作为应用的核心，协调各个模块的工作"""
    
    def __init__(self):
        """初始化应用控制器"""
        # 确保必要的目录存在
        os.makedirs("charts", exist_ok=True)
        os.makedirs("exports/charts", exist_ok=True)  # 添加PandasAI默认导出目录
        os.makedirs("avatar", exist_ok=True)
        
        # 初始化组件
        self.db_manager = DBManager()
        self.config_manager = ConfigManager()
        self.oss_config = self.config_manager.load_oss_config()
        self.oss_uploader = OSSUploader(self.oss_config)
        
        # 尝试获取当前主机信息
        try:
            self.client_id = socket.gethostname()
        except:
            self.client_id = str(uuid.uuid4())
        
        # 初始化成员变量
        self.df = None
        self.agent = None
        self.session_id = str(uuid.uuid4())  # 创建会话ID
        self.session_file = ""  # 会话文件名
        
        # 尝试从环境变量获取默认模型类型
        self.default_llm_type = os.getenv("DEFAULT_LLM_TYPE")
        if not self.default_llm_type:
            if os.getenv("OPENAI_API_KEY"):
                self.default_llm_type = "OpenAI"
            elif os.getenv("AZURE_OPENAI_API_KEY"):
                self.default_llm_type = "Azure"
            else:
                self.default_llm_type = "Ollama"
        
        self.llm_type = self.default_llm_type
        
        # 语言设置 - 默认中文
        self.language = "zh"
        
        # 加载聊天历史记录
        self.chat_history = []
    
    def get_sessions(self):
        """获取会话列表"""
        try:
            # 从数据库获取会话列表
            sessions = self.db_manager.get_sessions_for_client(self.client_id)
            
            # 如果没有找到任何会话，尝试获取所有会话
            if not sessions:
                print("未找到与当前客户端关联的会话，尝试获取所有会话")
                sessions = self.db_manager.get_all_sessions()
            
            # 为每个会话添加更友好的显示格式
            for session in sessions:
                # 提取文件名和时间戳
                file_name = session.get("session_file", "")
                timestamp = session.get("timestamp", "")
                
                # 如果时间戳存在且长度合适，截取日期部分
                if timestamp and len(timestamp) > 10:
                    date_part = timestamp[:10]
                    session["display_name"] = f"{file_name} ({date_part})"
                else:
                    session["display_name"] = file_name
            
            print(f"获取到 {len(sessions)} 个会话")
            return sessions
        except Exception as e:
            print(f"获取会话列表时出错: {str(e)}")
            return []
    
    def display_chat_history(self):
        """显示所有的聊天记录历史"""
        return self.db_manager.display_all_history(self.language)
    
    def refresh_current_history(self):
        """刷新当前的历史记录显示"""
        history_data = self.db_manager.display_all_history(self.language)
        
        # 如果没有历史记录，显示提示信息
        if not history_data:
            # 创建一个包含"暂无对话记录"提示的记录
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            return [[
                f"{self.get_text('last_updated')} {current_time}", 
                "-",  # 会话ID列
                self.get_text('no_history'), 
                "-",  # 回答列
                "-",  # 加载操作列
                "-"   # 删除操作列
            ]]
            
        return history_data
    
    def search_history(self, search_keywords):
        """
        搜索历史记录
        
        Args:
            search_keywords: 搜索关键词
            
        Returns:
            list: 搜索结果列表
        """
        if not search_keywords or not search_keywords.strip():
            # 如果搜索关键词为空，返回所有历史记录
            return self.db_manager.display_all_history(self.language)
        
        # 执行搜索
        results = self.db_manager.search_history_by_question(search_keywords, self.language)
        
        # 如果没有结果，返回提示信息
        if not results:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            return [[
                f"{self.get_text('last_updated')} {current_time}", 
                "-",  # 会话ID列
                self.get_text('no_search_results'), 
                "-",  # 回答列
                "-",  # 加载操作列
                "-"   # 删除操作列
            ]]
        
        return results
    
    def set_language(self, language):
        """设置界面语言"""
        if language in ["zh", "en"]:
            self.language = language
    
    def get_text(self, key, *args):
        """获取当前语言的文本"""
        return LanguageUtils.get_text(self.language, key, *args)
    
    def _clean_chart_files(self, preserve_referenced=True):
        """
        清理图表文件的统一方法
        
        Args:
            preserve_referenced: 是否保留被数据库记录引用的图表文件
        """
        try:
            import glob
            
            # 获取所有图表文件
            chart_files = glob.glob("charts/*.png") + glob.glob("charts/*.jpg") + glob.glob("charts/*.jpeg") + glob.glob("charts/*.svg")
            export_chart_files = glob.glob("exports/charts/*.png") + glob.glob("exports/charts/*.jpg") + glob.glob("exports/charts/*.jpeg") + glob.glob("exports/charts/*.svg")
            all_chart_files = chart_files + export_chart_files
            
            if not all_chart_files:
                print("没有找到需要清理的图表文件")
                return 0
            
            # 如果需要保留被引用的图表，先获取数据库中引用的图表路径
            referenced_charts = set()
            if preserve_referenced:
                try:
                    # 从数据库获取所有被引用的图表路径
                    referenced_charts = self.db_manager.get_all_referenced_chart_paths()
                    print(f"数据库中有 {len(referenced_charts)} 个被引用的图表")
                except Exception as e:
                    print(f"获取引用图表列表时出错: {e}")
                    referenced_charts = set()
            
            # 清理图表文件
            cleaned_count = 0
            preserved_count = 0
            
            for chart_file in all_chart_files:
                # 标准化路径用于比较
                normalized_path = os.path.relpath(chart_file).replace('\\', '/')
                
                # 检查是否被数据库引用
                is_referenced = False
                if preserve_referenced:
                    for ref_path in referenced_charts:
                        if ref_path and (normalized_path == ref_path or 
                                       os.path.basename(normalized_path) == os.path.basename(ref_path)):
                            is_referenced = True
                            break
                
                if is_referenced:
                    preserved_count += 1
                    print(f"保留被引用的图表文件: {chart_file}")
                else:
                    try:
                        os.remove(chart_file)
                        cleaned_count += 1
                        print(f"清理图表文件: {chart_file}")
                    except Exception as e:
                        print(f"删除图表文件失败 {chart_file}: {e}")
            
            if cleaned_count > 0 or preserved_count > 0:
                print(f"图表清理完成: 清理了 {cleaned_count} 个文件，保留了 {preserved_count} 个文件")
            
            return cleaned_count
        except Exception as e:
            print(f"清理图表文件时出错: {e}")
            return 0
    
    def load_dataframe(self, file):
        """从上传的文件加载pandas数据框"""
        if file is None:
            return self.get_text("waiting_upload"), None
        
        try:
            # 加载数据文件 - 传递当前语言
            dataframe, message, success = DataLoader.load_file(file, self.language)
            
            if not success:
                return message, None
            
            # 创建新的会话
            self.session_id, self.session_file = self.db_manager.create_session(
                self.client_id, 
                os.path.basename(file)
            )
            
            # 完全重置所有相关状态
            self.df = None  # 先清空旧数据
            self.agent = None  # 清空旧的Agent
            self.chat_history = []  # 重置聊天记录
            
            # 强制垃圾回收以确保旧状态被清理
            import gc
            gc.collect()
            
            # 清理所有旧的图表缓存文件
            self._clean_chart_files()
            
            # 设置新数据
            self.df = dataframe
            print(f"✅ 新数据已加载: {len(self.df)} 行 x {len(self.df.columns)} 列")
            print(f"📊 数据列名: {list(self.df.columns)}")
            
            # 初始化AI处理器 - 这会创建新的Agent
            init_result, success = self.initialize_ai(self.llm_type)
            if not success:
                return f"{self.get_text('load_error')}: {init_result}", None
            
            # 生成预览HTML - 传递当前语言
            preview_html = DataLoader.generate_preview_html(self.df, 500, self.language)
            
            # 更新模型状态显示，包含模型具体名称
            model_name = self.get_model_name()
            result_message = f"{message}，并初始化{self.llm_type} ({model_name})模型"
            
            print(f"✅ 数据加载完成: {result_message}")
            return result_message, preview_html
            
        except Exception as e:
            print(f"❌ 数据加载失败: {str(e)}")
            return self.get_text("load_error", str(e)), None
    
    def initialize_ai(self, llm_type):
        """初始化选择的AI模型"""
        self.llm_type = llm_type
        
        try:
            # 首先检查是否已上传数据
            if self.df is None:
                return self.get_text("no_dataframe"), False
            
            # 强制清除旧的Agent实例
            self.agent = None
            print(f"🔄 正在初始化 {llm_type} 模型...")
                
            # 创建LLM实例
            llm, success, error_msg = LLMFactory.create_llm(llm_type, self.language)
            
            if not success:
                return error_msg, False
                
            # 生成数据描述，包含列名信息
            data_description = self._generate_data_description()
            print(f"📋 数据描述已生成，包含 {len(self.df.columns)} 个列")
            
            # 确保中文字体配置
            plot_kwargs = ensure_chinese_font_for_pandasai()
            
            # 配置PandasAI
            config = {
                "llm": llm,
                "save_charts": True,  # 保存生成的图表
                "verbose": True,  # 启用详细输出
                "enforce_privacy": False,  # 不强制隐私保护
                "auto_vis": False,  # 禁用自动生成可视化图表，只有在用户明确要求时才生成
                "enable_cache": False,  # 禁用缓存以避免列名混淆
                "custom_head": 5,  # 显示更多行来帮助理解数据
                # 设置matplotlib字体和样式配置，确保中文正常显示
                "custom_plot_kwargs": plot_kwargs
            }
            
            # 创建全新的Agent实例
            print(f"🤖 正在创建新的 Agent 实例...")
            self.agent = Agent(self.df, config=config, description=data_description)
            
            # 验证Agent是否正确初始化
            if self.agent is None:
                return self.get_text("init_failed", "Agent creation failed"), False
            
            print(f"✅ {llm_type} 模型初始化成功，Agent 已就绪")
            return self.get_text("init_success", llm_type), True
            
        except Exception as e:
            error_msg = f"初始化失败: {str(e)}"
            print(f"❌ {error_msg}")
            return self.get_text("init_failed", str(e)), False
    
    def _generate_data_description(self):
        """生成数据描述，帮助LLM更好地理解数据结构"""
        if self.df is None:
            return ""
        
        # 获取列名和基本信息
        columns_info = []
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            sample_values = self.df[col].dropna().head(3).tolist()
            columns_info.append(f"'{col}' ({dtype}): {sample_values}")
        
        description = f"""
数据集包含 {len(self.df)} 行 {len(self.df.columns)} 列。
列信息：
{chr(10).join(columns_info)}

重要提示：
- 请使用准确的列名，不要猜测或替换列名
- 销售相关数据在'销售额'列中，不是'金额'列
- 时间相关数据在'日期'列中，不是'时间'列
- 所有分析都应基于实际存在的列名
"""
        return description
    
    def change_model(self, llm_type):
        """切换模型时的处理函数"""
        self.llm_type = llm_type
        
        if self.df is None:
            return self.get_text("model_will_initialize", llm_type)
        
        result, success = self.initialize_ai(llm_type)
        if success:
            # 获取模型名称并显示
            model_name = self.get_model_name()
            return f"{result} ({model_name})"
        return result
    
    def ask_question(self, question, chatbot):
        """
        处理用户问题 - 仅将问题添加到chatbot
        """
        if not question:
            return chatbot, None, None
        
        # 更新chatbot消息列表 - 使用新的messages格式
        updated_chatbot = list(chatbot) if chatbot is not None else []
        updated_chatbot.append({"role": "user", "content": question})
        
        return updated_chatbot, None, None
    
    def process_question(self, question, chatbot):
        """
        处理用户问题并生成AI回答
        """
        if not question:
            return chatbot, None, None
            
        # 更新chatbot消息列表 - 使用新的messages格式
        updated_chatbot = list(chatbot) if chatbot is not None else []
        
        # 如果没有数据，返回错误信息
        if self.df is None:
            if updated_chatbot and len(updated_chatbot) > 0:
                # 如果最后一条是用户消息，添加助手回复
                if updated_chatbot[-1].get("role") == "user":
                    updated_chatbot.append({"role": "assistant", "content": self.get_text("please_upload")})
                else:
                    # 更新最后一条助手消息
                    updated_chatbot[-1]["content"] = self.get_text("please_upload")
            else:
                # 添加新的问答对
                updated_chatbot.extend([
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": self.get_text("please_upload")}
                ])
            return updated_chatbot, None, None
            
        # 初始化AI模型（如果尚未初始化）
        if self.agent is None:
            init_result, success = self.initialize_ai(self.llm_type)
            if not success:
                if updated_chatbot and len(updated_chatbot) > 0 and updated_chatbot[-1].get("role") == "user":
                    updated_chatbot.append({"role": "assistant", "content": f"{self.get_text('init_failed')}: {init_result}"})
                else:
                    updated_chatbot.extend([
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": f"{self.get_text('init_failed')}: {init_result}"}
                    ])
                return updated_chatbot, None, None
        
        # 更新最后一条消息的回答为"思考中..."或添加新的助手消息
        if updated_chatbot and len(updated_chatbot) > 0 and updated_chatbot[-1].get("role") == "user":
            updated_chatbot.append({"role": "assistant", "content": self.get_text("thinking")})
        else:
            updated_chatbot.extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": self.get_text("thinking")}
            ])
        
        # 分析用户意图，检查是否明确要求绘图
        should_generate_chart = ChartAnalyzer.is_visualization_required(question)
        print(f"用户问题: '{question}' - 是否需要生成图表: {should_generate_chart}")
        
        # 重试机制
        max_retries = 3
        retry_count = 0
        
        chart_file_for_display = None  # 用于独立图片显示区域
        chart_info_text = self.get_text("no_chart")  # 图表信息文本
        
        while retry_count < max_retries:
            try:
                # 清理旧图表记录
                latest_chart_time = 0
                chart_file = None
                
                # 如果用户明确要求绘图，临时启用自动可视化
                # 在PandasAI 2.0+中，配置保存在_config字典中而不是config对象中
                if hasattr(self.agent, "_config"):
                    current_config = self.agent._config
                    
                    # 检测提问的语言
                    is_chinese = LanguageUtils.is_chinese(question)
                    response_language = "zh" if is_chinese else "en"
                    
                    # 根据检测到的语言修改问题，添加语言提示
                    modified_question = question
                    if is_chinese:
                        # 如果是中文提问，确保回答是中文
                        if not any(keyword in question.lower() for keyword in ['中文', '请用中文', '用中文回答']):
                            modified_question = f"{question}。请用中文回答。"
                    else:
                        # 如果是英文提问，确保回答是英文
                        if not any(keyword in question.lower() for keyword in ['english', 'in english', 'respond in english']):
                            modified_question = f"{question}. Please respond in English."
                    
                    print(f"🔤 语言检测: {'中文' if is_chinese else '英文'}")
                    print(f"🔤 原问题: {question}")
                    print(f"🔤 修改后问题: {modified_question}")
                    
                    # 创建新的配置字典，保留原始配置的所有内容
                    config_dict = {
                        "llm": current_config.get("llm", None),
                        "save_charts": current_config.get("save_charts", True),
                        "verbose": current_config.get("verbose", True),
                        "enforce_privacy": current_config.get("enforce_privacy", False),
                        "auto_vis": should_generate_chart,  # 根据用户意图设置auto_vis
                        "enable_cache": current_config.get("enable_cache", False),
                        "custom_head": current_config.get("custom_head", 5)
                    }
                    
                    # 确保中文字体配置并获取plot_kwargs
                    plot_kwargs = ensure_chinese_font_for_pandasai()
                    
                    # 安全地添加custom_plot_kwargs
                    if "custom_plot_kwargs" in current_config:
                        # 合并现有配置和中文字体配置
                        existing_kwargs = current_config["custom_plot_kwargs"]
                        if isinstance(existing_kwargs, dict):
                            existing_kwargs.update(plot_kwargs)
                            config_dict["custom_plot_kwargs"] = existing_kwargs
                        else:
                            config_dict["custom_plot_kwargs"] = plot_kwargs
                    else:
                        config_dict["custom_plot_kwargs"] = plot_kwargs
                    
                    # 重新应用配置
                    self.agent._config = config_dict
                    
                    # 在调用chat前再次确保字体配置
                    ensure_chinese_font_for_pandasai()
                    
                    # 使用修改后的问题调用Agent的chat方法
                    result = self.agent.chat(modified_question)
                    
                    # 恢复默认设置（关闭自动可视化）
                    config_dict["auto_vis"] = False
                    self.agent._config = config_dict
                else:
                    # 不支持配置的情况下，仍然添加语言提示
                    is_chinese = LanguageUtils.is_chinese(question)
                    modified_question = question
                    if is_chinese:
                        if not any(keyword in question.lower() for keyword in ['中文', '请用中文', '用中文回答']):
                            modified_question = f"{question}。请用中文回答。"
                    else:
                        if not any(keyword in question.lower() for keyword in ['english', 'in english', 'respond in english']):
                            modified_question = f"{question}. Please respond in English."
                    
                    print(f"🔤 语言检测: {'中文' if is_chinese else '英文'}")
                    print(f"🔤 修改后问题: {modified_question}")
                    
                    # 确保中文字体配置
                    ensure_chinese_font_for_pandasai()
                    
                    # 直接使用chat方法
                    result = self.agent.chat(modified_question)
                
                # 检查结果中是否包含图表路径
                print(f"🔍 检查AI返回结果: {result}")
                print(f"🔍 结果类型: {type(result)}")
                
                if isinstance(result, dict):
                    # 检查常见的图表路径字段
                    for path_field in ['path', 'figure_path', 'chart_path', 'image_path', 'plot_path']:
                        if path_field in result and isinstance(result[path_field], str) and os.path.exists(result[path_field]):
                            file_mod_time = os.path.getmtime(result[path_field])
                            if file_mod_time > latest_chart_time:
                                chart_file = result[path_field]
                                latest_chart_time = file_mod_time
                                print(f"✅ 从结果字段 '{path_field}' 检测到图表: {chart_file}")
                    
                    # 处理特殊格式的字典：{'type': 'xxx', 'value': yyy}
                    if 'type' in result and 'value' in result:
                        print(f"🔍 检测到类型化结果: type={result['type']}, value={result['value']}")
                        
                        if result['type'] == 'string':
                            processed_result = str(result['value'])
                        elif result['type'] == 'number':
                            processed_result = str(result['value'])
                        # 检查是否返回了图像路径
                        elif result['type'] == 'plot' and 'path' in result and os.path.exists(result['path']):
                            chart_file = result['path']
                            processed_result = self.get_text("chart_analysis")
                            print(f"✅ 从结果['path']检测到图表: {chart_file}")
                        elif result['type'] == 'plot' and 'value' in result and isinstance(result['value'], str) and os.path.exists(result['value']):
                            chart_file = result['value']
                            processed_result = self.get_text("chart_analysis")
                            print(f"✅ 从结果['value']检测到图表: {chart_file}")
                        else:
                            # 其他类型按原样格式化为JSON
                            processed_result = json.dumps(result, ensure_ascii=False, indent=2)
                    else:
                        # 普通字典格式化为JSON字符串
                        processed_result = json.dumps(result, ensure_ascii=False, indent=2)
                elif isinstance(result, (int, float)):
                    # 数字类型转换为字符串
                    processed_result = str(result)
                elif isinstance(result, list):
                    # 处理列表，可能包含多个返回值
                    if all(isinstance(item, dict) and 'type' in item and 'value' in item for item in result):
                        # 列表中都是{'type': xxx, 'value': yyy}格式
                        values = []
                        for item in result:
                            if item['type'] in ['string', 'number']:
                                values.append(str(item['value']))
                            # 检查列表中是否有图表项
                            elif item['type'] == 'plot' and 'path' in item and os.path.exists(item['path']):
                                chart_file = item['path']
                                values.append(self.get_text("chart_analysis"))
                            elif item['type'] == 'plot' and 'value' in item and isinstance(item['value'], str) and os.path.exists(item['value']):
                                chart_file = item['value']
                                values.append(self.get_text("chart_analysis"))
                            else:
                                values.append(json.dumps(item, ensure_ascii=False))
                        processed_result = "\n".join(values)
                    else:
                        # 普通列表
                        processed_result = json.dumps(result, ensure_ascii=False, indent=2)
                elif isinstance(result, str):
                    # 对于字符串类型，检查是否包含图片路径
                    # 检查常见的图片路径模式
                    if result.endswith(('.png', '.jpg', '.jpeg', '.svg')) and os.path.exists(result):
                        chart_file = result
                        processed_result = self.get_text("chart_analysis")
                    else:
                        processed_result = result
                else:
                    # 处理其他非字符串类型
                    processed_result = str(result)
                
                # 如果直接返回了一个图片路径字符串
                if isinstance(result, str) and os.path.exists(result) and result.endswith(('.png', '.jpg', '.jpeg', '.svg')):
                    chart_file = result
                    processed_result = self.get_text("chart_result")
                    print(f"✅ 从字符串结果检测到图表: {chart_file}")
                
                # 如果还没有检测到图表文件，作为备用方案扫描目录
                if not chart_file:
                    print("🔍 未从结果中检测到图表，开始目录扫描...")
                    chart_dirs = ["charts", "exports/charts"]
                    
                    for chart_dir in chart_dirs:
                        if os.path.exists(chart_dir):
                            chart_files = [f for f in os.listdir(chart_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.svg'))]
                            print(f"🔍 扫描目录 {chart_dir}: 找到 {len(chart_files)} 个图表文件")
                            
                            # 按修改时间排序，获取最新的图表文件
                            for f in chart_files:
                                file_path = os.path.join(chart_dir, f)
                                mod_time = os.path.getmtime(file_path)
                                if mod_time > latest_chart_time:
                                    latest_chart_time = mod_time
                                    chart_file = file_path
                                    print(f"✅ 从目录扫描检测到更新图表: {chart_file} (修改时间: {mod_time})")
                
                print(f"📊 最终图表检测结果: chart_file={chart_file}")
                
                # 如果有图表文件，处理图片显示
                if chart_file and os.path.exists(chart_file):
                    print(f"✅ 确认图表文件存在: {chart_file}")
                    
                    # 如果图表在exports/charts目录，复制到charts目录以保持一致性
                    final_chart_path = chart_file
                    if chart_file.startswith('exports/charts/'):
                        # 提取文件名
                        chart_filename = os.path.basename(chart_file)
                        # 目标路径在charts目录
                        target_path = os.path.join('charts', chart_filename)
                        
                        try:
                            # 复制文件到charts目录
                            import shutil
                            shutil.copy2(chart_file, target_path)
                            final_chart_path = target_path
                            print(f"📋 图表已复制到主目录: {final_chart_path}")
                        except Exception as e:
                            print(f"⚠️ 复制图表文件失败: {str(e)}, 使用原路径")
                            # 如果复制失败，使用原路径
                            final_chart_path = chart_file
                    
                    # 设置独立图片显示区域的数据
                    chart_file_for_display = final_chart_path
                    
                    # 获取绝对路径
                    absolute_path = os.path.abspath(final_chart_path)
                    
                    chart_info_text = f"""{self.get_text('chart_file')}: {os.path.basename(final_chart_path)}
{self.get_text('generation_time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{self.get_text('chart_path')}: {absolute_path}"""
                    
                    # 保存到本地存储，同时尝试上传到OSS
                    local_path, oss_url = chart_storage.save_chart(final_chart_path)
                    
                    if oss_url:
                        # 使用OSS URL - 创建包含文本和图片的内容
                        updated_chatbot[-1]["content"] = f"{processed_result}\n\n![Chart]({oss_url})"
                    else:
                        # 使用简单的文本描述，因为有独立的图片显示区域
                        updated_chatbot[-1]["content"] = f"{processed_result}\n\n✅ {self.get_text('chart_generated_view_right')}"
                    
                    # 使用复制后的路径保存到数据库
                    chart_file = final_chart_path
                else:
                    # 仅更新文本内容
                    updated_chatbot[-1]["content"] = processed_result
                
                # 保存到历史记录
                history_content = processed_result
                if chart_file:
                    history_content += f"\n[{self.get_text('chart_alt_text', os.path.basename(chart_file))}]"
                
                # 保存聊天记录到SQLite数据库
                model_name = self.get_model_name()
                self.db_manager.save_chat_history(
                    self.session_id, 
                    self.session_file, 
                    self.client_id, 
                    question, 
                    history_content, 
                    self.llm_type, 
                    model_name,
                    chart_path=chart_file  # 直接传入图表文件路径
                )
                
                return updated_chatbot, chart_file_for_display, chart_info_text
            except requests.exceptions.ConnectionError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    error_msg = self.get_text("network_error")
                    updated_chatbot[-1]["content"] = error_msg
                    return updated_chatbot, None, self.get_text("network_connection_error")
                time.sleep(2)  # 重试前等待2秒
            except KeyError as e:
                # 专门处理列名错误
                column_name = str(e).strip("'\"")
                if column_name and self.df is not None:
                    available_columns = list(self.df.columns)
                    error_msg = f"列名错误：找不到列 '{column_name}'。可用的列名有：{', '.join(available_columns)}"
                else:
                    error_msg = f"数据列访问错误：{str(e)}"
                
                updated_chatbot[-1]["content"] = error_msg
                return updated_chatbot, None, f"错误: {error_msg}"
            except Exception as e:
                error_msg = str(e)
                if "Connection error" in error_msg or "SSL" in error_msg or "EOF occurred" in error_msg:
                    error_msg = self.get_text("network_error")
                else:
                    error_msg = self.get_text("processing_error", error_msg)
                
                updated_chatbot[-1]["content"] = error_msg
                return updated_chatbot, None, f"处理错误: {error_msg}"
    
    def clear_chat(self, chatbot):
        """清空当前聊天界面和图表显示"""
        # 清理当前会话的图表文件（不保留引用，因为用户要求清空）
        self._clean_chart_files(preserve_referenced=False)
        return [], None, self.get_text("no_chart")
    
    def delete_session_history(self, session_id):
        """
        删除指定会话的所有聊天历史记录
        
        Args:
            session_id: 要删除的会话ID
        """
        if not session_id:
            return
            
        success = self.db_manager.delete_session_history(session_id)
        
        # 函数现在不需要返回值，因为UI不再显示结果
        return
    
    def delete_all_history(self):
        """
        删除所有聊天历史记录
        """
        success = self.db_manager.delete_all_history()
        
        # 函数现在不需要返回值，因为UI不再显示结果
        return
    
    def load_session(self, session_id):
        """加载指定的会话"""
        if not session_id:
            return [], self.get_text("no_session_selected")
            
        # 如果session_id是字典，尝试提取值
        if isinstance(session_id, dict) and "value" in session_id:
            session_id = session_id["value"]
            
        # 更新当前会话ID
        self.session_id = session_id
        
        # 获取会话文件名
        self.session_file = self.db_manager.get_session_file_by_id(session_id)
        
        # 加载聊天记录
        history = self.db_manager.get_chat_history_for_session(session_id)
        
        # 如果没有找到记录，返回提示
        if not history:
            return [], f"{self.get_text('session_loaded')}: {self.session_file} (无对话记录)"
        
        # 转换为Gradio Chatbot新的messages格式
        chatbot_messages = []
        for msg in history:
            # 添加用户消息
            chatbot_messages.append({"role": "user", "content": msg["question"]})
            
            # 处理助手回复，检查是否包含图片
            answer_content = msg["answer"]
            
            # 检查是否有图片路径
            if msg.get('has_chart') and msg.get('chart_path') and os.path.exists(msg['chart_path']):
                # 分离文本和图片路径
                text_content = answer_content
                
                # 移除图片路径相关文本
                import re
                chart_patterns = [
                    r'本地图片路径:\s*[^\n]+',
                    r'file://[^\n]+',
                    r'<img[^>]*>',  # 移除现有的img标签
                    r'<br><small>图片路径:[^<]*</small>',  # 移除图片路径信息
                    r'!\[.*?\]\([^)]+\)',  # 移除Markdown图片语法
                    r'[A-Za-z]:\\[^<>:|?*\n]+\.(png|jpg|jpeg|svg)',  # Windows绝对路径
                    r'/[^<>:|?*\n]+\.(png|jpg|jpeg|svg)'  # Unix绝对路径
                ]
                
                for pattern in chart_patterns:
                    text_content = re.sub(pattern, '', text_content)
                
                # 清理多余的空行和<br>标签
                text_content = re.sub(r'(<br>\s*){3,}', '<br><br>', text_content)
                text_content = re.sub(r'\n{3,}', '\n\n', text_content).strip()
                
                # 构建包含图片的HTML内容
                absolute_path = os.path.abspath(msg['chart_path'])
                relative_path = os.path.relpath(absolute_path, os.getcwd()).replace('\\', '/')
                
                # 使用图片工具创建HTML
                img_html = create_image_html(msg['chart_path'], "数据分析图表")
                
                # 合并文本和图片
                content = f"{text_content}<br><br>{img_html}<br><small>图片路径: {relative_path}</small>"
                chatbot_messages.append({"role": "assistant", "content": content})
            else:
                # 纯文本回复
                chatbot_messages.append({"role": "assistant", "content": answer_content})
        
        return chatbot_messages, f"{self.get_text('session_loaded')}: {self.session_file}"
    
    def get_model_name(self):
        """获取当前加载的模型具体名称"""
        if self.agent:
            # First try with _config (for PandasAI 2.0+)
            if hasattr(self.agent, "_config") and self.agent._config and "llm" in self.agent._config:
                llm = self.agent._config["llm"]
                if self.llm_type == "OpenAI":
                    # 对于OpenAI模型，显示模型名称
                    return getattr(llm, "model", "gpt-3.5-turbo")
                elif self.llm_type == "Azure":
                    # 对于Azure模型，显示部署名称
                    return getattr(llm, "deployment_name", "unknown")
                elif self.llm_type == "Ollama":
                    # 对于Ollama模型，显示具体的模型名称
                    if hasattr(llm, "model"):
                        return llm.model
                    elif hasattr(llm, "get_model_name"):
                        return llm.get_model_name()
                    else:
                        return os.getenv("OLLAMA_MODEL", "llama3")
            # Fallback to config for older versions
            elif hasattr(self.agent, "config") and self.agent.config and hasattr(self.agent.config, "llm"):
                llm = self.agent.config.llm
                if self.llm_type == "OpenAI":
                    # 对于OpenAI模型，显示模型名称
                    return getattr(llm, "model", "gpt-3.5-turbo")
                elif self.llm_type == "Azure":
                    # 对于Azure模型，显示部署名称
                    return getattr(llm, "deployment_name", "unknown")
                elif self.llm_type == "Ollama":
                    # 对于Ollama模型，显示具体的模型名称
                    if hasattr(llm, "model"):
                        return llm.model
                    elif hasattr(llm, "get_model_name"):
                        return llm.get_model_name()
                    else:
                        return os.getenv("OLLAMA_MODEL", "llama3")
        return self.llm_type  # 如果无法获取具体名称，返回类型
        
    def get_session_id_by_details(self, timestamp, question):
        """
        根据时间戳和问题获取会话ID
        
        Args:
            timestamp: 时间戳，格式为"2025-06-02 17:29 (模型名称)"
            question: 问题文本
            
        Returns:
            str: 会话ID或空字符串
        """
        try:
            # 从时间戳中提取日期时间部分
            if '(' in timestamp:
                time_part = timestamp[:timestamp.find('(')].strip()
            else:
                time_part = timestamp.strip()
                
            # 删除问题中的省略号
            if question.endswith('...'):
                question = question[:-3]
                
            # 调用数据库管理器查询会话ID
            return self.db_manager.get_session_id_by_details(time_part, question)
        except Exception as e:
            print(f"根据详情获取会话ID时出错: {str(e)}")
            return ""
        
    def load_history_record(self, session_id, chatbot, specific_record_id=None):
        """
        从历史记录中加载选中的会话记录到当前对话框
        
        Args:
            session_id: 选中的会话ID
            chatbot: 当前的对话框内容
            specific_record_id: 可选，指定要显示图表的记录ID
            
        Returns:
            tuple: 更新后的对话框内容、状态消息、图表文件路径、图表信息
        """
        try:
            # 检查是否有选中的会话ID
            if not session_id:
                print("未选择会话ID")
                return chatbot, self.get_text("no_row_selected"), None, self.get_text("no_chart")
                
            # 如果session_id是字典，尝试提取值
            if isinstance(session_id, dict) and "value" in session_id:
                session_id = session_id["value"]
                
            print(f"正在加载会话: {session_id}")
            
            # 更新当前会话ID
            self.session_id = session_id
            
            # 获取会话文件名
            self.session_file = self.db_manager.get_session_file_by_id(session_id)
            if not self.session_file:
                print(f"未找到会话文件名: {session_id}")
                return chatbot, f"未找到会话: {session_id[:8]}...", None, self.get_text("no_chart")
            
            print(f"找到会话文件: {self.session_file}")
            
            # 加载聊天记录
            history = self.db_manager.get_chat_history_for_session(session_id)
            
            # 如果没有找到记录，返回提示
            if not history:
                print(f"会话 {session_id} 没有聊天记录")
                return chatbot, self.get_text("no_history"), None, self.get_text("no_chart")
            
            print(f"加载了 {len(history)} 条聊天记录")
            
            # 查找要显示的图表文件
            target_chart_file = None
            target_chart_info = self.get_text("no_chart")
            
            # 如果指定了特定记录ID，先尝试加载该记录的图表
            if specific_record_id:
                try:
                    chart_file, chart_info, status = self.load_chart_by_record_id(specific_record_id)
                    if chart_file:
                        target_chart_file = chart_file
                        target_chart_info = chart_info
                        print(f"✅ 成功加载指定记录 {specific_record_id} 的图表: {chart_file}")
                    else:
                        print(f"❌ 指定记录 {specific_record_id} 没有图表或图表不存在")
                except Exception as e:
                    print(f"❌ 加载指定记录图表失败: {str(e)}")
            
            # 转换为Gradio Chatbot新的messages格式
            chatbot_messages = []
            fallback_chart_file = None
            fallback_chart_info = self.get_text("no_chart")
            
            for i, msg in enumerate(history):
                # 添加用户消息
                chatbot_messages.append({"role": "user", "content": msg["question"]})
                
                # 处理助手回复，检查是否包含图片
                answer_content = msg["answer"]
                
                print(f"处理消息 {i+1}: has_chart={msg.get('has_chart')}, chart_path={msg.get('chart_path')}")
                
                # 检查是否有图片路径
                if msg.get('has_chart') and msg.get('chart_path'):
                    chart_path = msg['chart_path']
                    print(f"检查图表路径: {chart_path}")
                    
                    # 使用新的路径解析方法
                    resolved_chart_path = self._resolve_chart_path(chart_path)
                    
                    if resolved_chart_path:
                        # 如果还没有目标图表，或者没有指定特定记录ID，则更新备用图表信息
                        if not target_chart_file:
                            fallback_chart_file = resolved_chart_path
                            absolute_path = fallback_chart_file
                            
                            fallback_chart_info = f"""{self.get_text('chart_file')}: {os.path.basename(fallback_chart_file)}
{self.get_text('loading_time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{self.get_text('chart_path')}: {absolute_path}"""
                            
                            print(f"更新备用图表信息: 文件={fallback_chart_file}, 绝对路径={absolute_path}")
                        
                        # 分离文本和图片路径
                        text_content = answer_content
                        
                        # 移除图片路径相关文本
                        import re
                        chart_patterns = [
                            r'本地图片路径:\s*[^\n]+',
                            r'file://[^\n]+',
                            r'<img[^>]*>',  # 移除现有的img标签
                            r'<br><small>图片路径:[^<]*</small>',  # 移除图片路径信息
                            r'!\[.*?\]\([^)]+\)',  # 移除Markdown图片语法
                            r'[A-Za-z]:\\[^<>:|?*\n]+\.(png|jpg|jpeg|svg)',  # Windows绝对路径
                            r'/[^<>:|?*\n]+\.(png|jpg|jpeg|svg)',  # Unix绝对路径
                            r'exports/charts/[^<>:|?*\n]+\.(png|jpg|jpeg|svg)',  # exports目录路径
                            r'charts/[^<>:|?*\n]+\.(png|jpg|jpeg|svg)'  # charts目录路径
                        ]
                        
                        for pattern in chart_patterns:
                            text_content = re.sub(pattern, '', text_content)
                        
                        # 清理多余的空行和<br>标签
                        text_content = re.sub(r'(<br>\s*){3,}', '<br><br>', text_content)
                        text_content = re.sub(r'\n{3,}', '\n\n', text_content).strip()
                        
                        # 添加提示信息而不是实际的图片HTML
                        content = f"{text_content}\n\n✅ {self.get_text('chart_loaded_view_right')}"
                        chatbot_messages.append({"role": "assistant", "content": content})
                    else:
                        print(f"❌ 未找到图表文件: {chart_path}")
                        # 纯文本回复
                        chatbot_messages.append({"role": "assistant", "content": answer_content})
                else:
                    print(f"无图表信息: has_chart={msg.get('has_chart')}, chart_path={msg.get('chart_path')}")
                    # 纯文本回复
                    chatbot_messages.append({"role": "assistant", "content": answer_content})
            
            # 决定最终显示的图表：优先使用目标图表，否则使用备用图表
            final_chart_file = target_chart_file if target_chart_file else fallback_chart_file
            final_chart_info = target_chart_info if target_chart_file else fallback_chart_info
            
            print(f"最终图表信息: final_chart_file={final_chart_file}, final_chart_info={final_chart_info}")
            
            return chatbot_messages, f"{self.get_text('session_loaded_from_history')}: {self.session_file}", final_chart_file, final_chart_info
        except Exception as e:
            print(f"加载会话记录时出错: {str(e)}")
            return chatbot, f"加载会话记录失败: {str(e)}", None, f"加载错误: {str(e)}"
    
    def delete_record(self, record_id):
        """
        删除单条聊天记录
        
        Args:
            record_id: 记录ID
            
        Returns:
            tuple: (是否成功, 消息)
        """
        try:
            if not record_id:
                print("未选择记录ID")
                return False, self.get_text("no_row_selected")
            
            print(f"正在删除记录: {record_id}")
            success = self.db_manager.delete_record(record_id)
            
            if success:
                return True, self.get_text("record_deleted")
            else:
                return False, self.get_text("record_delete_failed")
        except Exception as e:
            print(f"删除记录时出错: {str(e)}")
            return False, f"{self.get_text('record_delete_failed')}: {str(e)}"
    
    def get_session_id_by_record_id(self, record_id):
        """
        通过记录ID获取会话ID
        
        Args:
            record_id: 记录ID
            
        Returns:
            str: 会话ID或空字符串
        """
        try:
            if not record_id:
                return ""
                
            return self.db_manager.get_session_id_by_record_id(record_id)
        except Exception as e:
            print(f"通过记录ID获取会话ID时出错: {str(e)}")
            return ""
    
    def get_record_by_time_question(self, time_question_info):
        """
        通过时间和问题信息获取记录详细信息
        
        Args:
            time_question_info: 格式为"时间信息|问题信息"的字符串
            
        Returns:
            dict: 包含session_id, record_id, has_chart等信息的字典
        """
        try:
            # 首先获取record_id
            record_id = self.db_manager.get_record_by_time_and_question(time_question_info)
            
            if not record_id:
                return None
            
            # 获取记录的详细信息
            conn = self.db_manager._connect()
            cursor = conn.cursor()
            
            cursor.execute(
                '''
                SELECT 
                    session_id,
                    has_chart,
                    chart_path
                FROM 
                    chat_history 
                WHERE 
                    id = ?
                ''',
                (record_id,)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'session_id': result[0],
                    'record_id': record_id,
                    'has_chart': result[1],
                    'chart_path': result[2]
                }
            return None
            
        except Exception as e:
            print(f"通过时间和问题获取记录信息时出错: {str(e)}")
            return None
    
    def _resolve_chart_path(self, chart_path):
        """
        解析图表文件路径，尝试在多个可能的位置查找文件
        
        Args:
            chart_path: 原始图表路径
            
        Returns:
            str: 找到的图表文件的绝对路径，如果未找到则返回None
        """
        if not chart_path:
            return None
            
        # 如果路径直接存在，返回绝对路径
        if os.path.exists(chart_path):
            return os.path.abspath(chart_path)
        
        # 提取文件名
        chart_filename = os.path.basename(chart_path)
        
        # 尝试在多个可能的位置查找
        possible_paths = [
            chart_path,  # 原始路径
            os.path.join('charts', chart_filename),  # charts目录
            os.path.join('exports/charts', chart_filename),  # exports/charts目录
            chart_filename,  # 当前目录
        ]
        
        # 如果原路径包含目录，也尝试相对路径
        if '/' in chart_path or '\\' in chart_path:
            # 如果是exports/charts路径，尝试charts目录
            if 'exports/charts' in chart_path:
                possible_paths.append(chart_path.replace('exports/charts', 'charts'))
            # 如果是charts路径，尝试exports/charts目录
            elif 'charts' in chart_path:
                possible_paths.append(chart_path.replace('charts', 'exports/charts'))
        
        # 逐一尝试路径
        for possible_path in possible_paths:
            if os.path.exists(possible_path):
                print(f"✅ 在位置找到图表文件: {possible_path}")
                return os.path.abspath(possible_path)
        
        print(f"❌ 未找到图表文件: {chart_path}, 尝试了 {len(possible_paths)} 个位置")
        return None
    
    def load_chart_by_record_id(self, record_id):
        """
        根据记录ID加载对应的图表
        
        Args:
            record_id: 聊天记录ID
            
        Returns:
            tuple: (图表文件路径, 图表信息文本, 状态消息)
        """
        try:
            if not record_id:
                return None, self.get_text("no_chart"), "未指定记录ID"
            
            # 从数据库获取记录信息
            conn = self.db_manager._connect()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT has_chart, chart_path, question, answer, created_at
                FROM chat_history 
                WHERE id = ?
            ''', (record_id,))
            
            record = cursor.fetchone()
            conn.close()
            
            if not record:
                return None, self.get_text("no_chart"), "未找到指定记录"
            
            has_chart, chart_path, question, answer, created_at = record
            
            if not has_chart or not chart_path:
                return None, self.get_text("no_chart"), "该记录不包含图表"
            
            # 使用路径解析方法查找图表文件
            resolved_chart_path = self._resolve_chart_path(chart_path)
            
            if not resolved_chart_path:
                return None, self.get_text("no_chart"), f"图表文件不存在: {chart_path}"
            
            # 生成图表信息
            chart_filename = os.path.basename(resolved_chart_path)
            chart_info = f"图表文件: {chart_filename}\n加载时间: {created_at}\n路径: {resolved_chart_path}"
            
            print(f"✅ 成功加载图表: {resolved_chart_path}")
            return resolved_chart_path, chart_info, "图表加载成功"
            
        except Exception as e:
            print(f"加载图表时出错: {e}")
            return None, self.get_text("no_chart"), f"加载图表失败: {str(e)}" 