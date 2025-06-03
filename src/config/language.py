"""
语言资源文件模块
负责管理应用程序的多语言支持
"""

# 语言资源文件 - 支持中英文
LANGUAGE = {
    "zh": {
        "title": "Pandas AI Web - 数据对话助手",
        "header": "Pandas AI Web - 与数据对话的AI助手",
        "model_selection": "AI模型选择",
        "select_model": "选择AI模型",
        "model_status": "模型状态",
        "model_will_initialize": "已选择 {0} 模型（在上传数据后将自动初始化）",
        "data_upload": "数据上传",
        "upload_file": "上传CSV、XLS或XLSX文件",
        "upload_status": "上传状态",
        "waiting_upload": "等待上传文件",
        "data_preview": "数据预览",
        "data_conversation": "数据对话",
        "chat_with_data": "与数据对话",
        "question_input": "输入你的问题",
        "question_placeholder": "例如: 这个数据的平均值是多少?",
        "ask_button": "提问",
        "clear_button": "清空对话",
        "thinking": "思考中...",
        "please_upload": "请先上传数据文件",
        "file_loaded": "成功加载数据文件({0}行)，并初始化{1}模型",
        "file_loaded_encoding": "成功加载数据文件({0}行)，使用{1}编码，并初始化{2}模型",
        "total_rows": "数据总行数: {0}",
        "total_rows_limit": "数据总行数: {0} (显示前{1}行)",
        "total_rows_encoding": "数据总行数: {0} (使用{1}编码加载)",
        "total_rows_limit_encoding": "数据总行数: {0} (显示前{1}行, 使用{2}编码加载)",
        "unsupported_format": "不支持的文件格式: {0}",
        "load_error": "加载文件时出错: {0}",
        "encoding_error": "CSV文件编码识别失败，请尝试保存为UTF-8编码",
        "no_valid_data": "文件没有有效数据",
        "chart_analysis": "已生成图表分析",
        "chart_result": "图表分析结果：",
        "chart_generated_view_right": "图表已生成，请查看右侧图表显示区域",
        "chart_loaded_view_right": "历史图表已加载，请查看右侧图表显示区域",
        "chart_file": "图表文件",
        "generation_time": "生成时间",
        "loading_time": "加载时间",
        "chart_path": "图表路径",
        "last_updated": "最后更新",
        "no_history": "暂无对话记录",
        "session_loaded_from_history": "从历史记录加载会话",
        "record_deleted": "记录已删除",
        "record_delete_failed": "删除记录失败",
        "no_row_selected": "请先选择一行记录",
        "openai_key_missing": "未在.env文件中配置OPENAI_API_KEY",
        "openai_init_failed": "创建OpenAI LLM实例失败: {0}",
        "azure_key_missing": "未在.env文件中配置AZURE_OPENAI_API_KEY",
        "azure_endpoint_missing": "未在.env文件中配置AZURE_OPENAI_ENDPOINT",
        "azure_deployment_missing": "未在.env文件中配置AZURE_OPENAI_DEPLOYMENT_NAME",
        "azure_connection_error": "网络连接错误：无法连接到Azure OpenAI服务",
        "azure_init_failed": "创建Azure OpenAI LLM实例失败: {0}",
        "ollama_connection_failed": "无法连接到Ollama服务 ({0})，请确保Ollama服务正在运行",
        "ollama_init_failed": "初始化Ollama模型失败: {0}",
        "unsupported_llm_type": "不支持的LLM类型: {0}",
        "language": "语言",
        "language_switch": "切换语言",
        "chinese": "中文",
        "english": "English",
        "chart_alt_text": "数据分析图表: {0}",
        "init_success": "成功初始化 {0} AI模型",
        "init_failed": "初始化AI模型时出错: {0}",
        "no_dataframe": "请先上传数据文件，然后再初始化AI模型",
        "network_error": "网络连接错误：无法连接到AI服务。请检查您的网络连接、代理设置或防火墙设置。如果您在中国大陆地区，可能需要使用VPN或代理服务来访问OpenAI API。",
        "network_connection_error": "网络连接错误",
        "processing_error": "处理问题时出错: {0}",
        "session_history": "历史会话",
        "select_session": "选择会话记录",
        "session_loaded": "已加载会话",
        "chat_history": "对话记录",
        "refresh_history": "刷新对话记录",
        "history_time": "时间",
        "history_question": "问题",
        "history_answer": "回答"
    },
    "en": {
        "title": "Pandas AI Web - Data Conversation Assistant",
        "header": "Pandas AI Web - Conversational AI for Your Data",
        "model_selection": "AI Model Selection",
        "select_model": "Select AI Model",
        "model_status": "Model Status",
        "model_will_initialize": "Selected {0} model (will initialize after data upload)",
        "data_upload": "Data Upload",
        "upload_file": "Upload CSV, XLS or XLSX file",
        "upload_status": "Upload Status",
        "waiting_upload": "Waiting for file upload",
        "data_preview": "Data Preview",
        "data_conversation": "Data Conversation",
        "chat_with_data": "Chat with Your Data",
        "question_input": "Enter your question",
        "question_placeholder": "Example: What is the average value in this data?",
        "ask_button": "Ask",
        "clear_button": "Clear Chat",
        "thinking": "Thinking...",
        "please_upload": "Please upload a data file first",
        "file_loaded": "Successfully loaded data file ({0} rows) and initialized {1} model",
        "file_loaded_encoding": "Successfully loaded data file ({0} rows) using {1} encoding and initialized {2} model",
        "total_rows": "Total rows: {0}",
        "total_rows_limit": "Total rows: {0} (showing first {1} rows)",
        "total_rows_encoding": "Total rows: {0} (loaded with {1} encoding)",
        "total_rows_limit_encoding": "Total rows: {0} (showing first {1} rows, loaded with {2} encoding)",
        "unsupported_format": "Unsupported file format: {0}",
        "load_error": "Error loading file: {0}",
        "encoding_error": "Failed to recognize CSV file encoding, please try saving as UTF-8",
        "no_valid_data": "The file contains no valid data",
        "chart_analysis": "Chart analysis generated",
        "chart_result": "Chart analysis result:",
        "chart_generated_view_right": "Chart generated, please view the chart display area on the right",
        "chart_loaded_view_right": "Chart history loaded, please view the chart display area on the right",
        "chart_file": "Chart file",
        "generation_time": "Generation time",
        "loading_time": "Loading time",
        "chart_path": "Chart path",
        "last_updated": "Last updated",
        "no_history": "No chat history",
        "session_loaded_from_history": "Load session from history",
        "record_deleted": "Record deleted",
        "record_delete_failed": "Failed to delete record",
        "no_row_selected": "Please select a row first",
        "openai_key_missing": "OPENAI_API_KEY not configured in .env file",
        "openai_init_failed": "Failed to create OpenAI LLM instance: {0}",
        "azure_key_missing": "AZURE_OPENAI_API_KEY not configured in .env file",
        "azure_endpoint_missing": "AZURE_OPENAI_ENDPOINT not configured in .env file",
        "azure_deployment_missing": "AZURE_OPENAI_DEPLOYMENT_NAME not configured in .env file",
        "azure_connection_error": "Network connection error: Unable to connect to Azure OpenAI service",
        "azure_init_failed": "Failed to create Azure OpenAI LLM instance: {0}",
        "ollama_connection_failed": "Unable to connect to Ollama service ({0}), please ensure Ollama service is running",
        "ollama_init_failed": "Failed to initialize Ollama model: {0}",
        "unsupported_llm_type": "Unsupported LLM type: {0}",
        "language": "Language",
        "language_switch": "Switch Language",
        "chinese": "中文",
        "english": "English",
        "chart_alt_text": "Data analysis chart: {0}",
        "init_success": "Successfully initialized {0} AI model",
        "init_failed": "Error initializing AI model: {0}",
        "no_dataframe": "Please upload a data file before initializing AI model",
        "network_error": "Network connection error: Unable to connect to AI service. Please check your network connection, proxy settings or firewall settings. If you are in mainland China, you may need to use a VPN or proxy service to access the OpenAI API.",
        "network_connection_error": "Network connection error",
        "processing_error": "Error processing question: {0}",
        "session_history": "Session History",
        "select_session": "Select Session",
        "session_loaded": "Session Loaded",
        "chat_history": "Chat History",
        "refresh_history": "Refresh History",
        "history_time": "Time",
        "history_question": "Question",
        "history_answer": "Answer"
    }
}

class LanguageManager:
    """Manages language resources for internationalization.
    
    This class provides access to text resources in different languages
    and handles language switching.
    """
    
    def __init__(self, default_language="zh"):
        """Initialize the language manager.
        
        Args:
            default_language: Default language code ('zh' or 'en')
        """
        self.current_language = default_language
        self.resources = self._initialize_language_resources()
    
    def _initialize_language_resources(self):
        """Initialize language resource dictionaries."""
        return {
            "zh": {
                "title": "Pandas AI Web - 数据对话助手",
                "header": "Pandas AI Web - 与数据对话的AI助手",
                "model_selection": "AI模型选择",
                "select_model": "选择AI模型",
                "model_status": "模型状态",
                "model_will_initialize": "已选择 {0} 模型（在上传数据后将自动初始化）",
                "data_upload": "数据上传",
                "upload_file": "上传CSV、XLS或XLSX文件",
                "upload_status": "上传状态",
                "waiting_upload": "等待上传文件",
                "data_preview": "数据预览",
                "data_conversation": "数据对话",
                "chat_with_data": "与数据对话",
                "question_input": "输入你的问题",
                "question_placeholder": "例如: 这个数据的平均值是多少?",
                "ask_button": "提问",
                "clear_button": "清空对话",
                "thinking": "思考中...",
                "please_upload": "请先上传数据文件",
                "file_loaded": "成功加载数据文件({0}行)，并初始化{1}模型",
                "file_loaded_encoding": "成功加载数据文件({0}行)，使用{1}编码，并初始化{2}模型",
                "total_rows": "数据总行数: {0}",
                "total_rows_limit": "数据总行数: {0} (显示前{1}行)",
                "total_rows_encoding": "数据总行数: {0} (使用{1}编码加载)",
                "total_rows_limit_encoding": "数据总行数: {0} (显示前{1}行, 使用{2}编码加载)",
                "unsupported_format": "不支持的文件格式: {0}",
                "load_error": "加载文件时出错: {0}",
                "encoding_error": "CSV文件编码识别失败，请尝试保存为UTF-8编码",
                "no_valid_data": "文件没有有效数据",
                "chart_analysis": "已生成图表分析",
                "chart_result": "图表分析结果：",
                "chart_generated_view_right": "图表已生成，请查看右侧图表显示区域",
                "chart_loaded_view_right": "历史图表已加载，请查看右侧图表显示区域",
                "chart_file": "图表文件",
                "generation_time": "生成时间",
                "loading_time": "加载时间",
                "chart_path": "图表路径",
                "last_updated": "最后更新",
                "no_history": "暂无对话记录",
                "session_loaded_from_history": "从历史记录加载会话",
                "record_deleted": "记录已删除",
                "record_delete_failed": "删除记录失败",
                "no_row_selected": "请先选择一行记录",
                "openai_key_missing": "未在.env文件中配置OPENAI_API_KEY",
                "openai_init_failed": "创建OpenAI LLM实例失败: {0}",
                "azure_key_missing": "未在.env文件中配置AZURE_OPENAI_API_KEY",
                "azure_endpoint_missing": "未在.env文件中配置AZURE_OPENAI_ENDPOINT",
                "azure_deployment_missing": "未在.env文件中配置AZURE_OPENAI_DEPLOYMENT_NAME",
                "azure_connection_error": "网络连接错误：无法连接到Azure OpenAI服务",
                "azure_init_failed": "创建Azure OpenAI LLM实例失败: {0}",
                "ollama_connection_failed": "无法连接到Ollama服务 ({0})，请确保Ollama服务正在运行",
                "ollama_init_failed": "初始化Ollama模型失败: {0}",
                "unsupported_llm_type": "不支持的LLM类型: {0}",
                "language": "语言",
                "language_switch": "切换语言",
                "chinese": "中文",
                "english": "English",
                "chart_alt_text": "数据分析图表: {0}",
                "init_success": "成功初始化 {0} AI模型",
                "init_failed": "初始化AI模型时出错: {0}",
                "no_dataframe": "请先上传数据文件，然后再初始化AI模型",
                "network_error": "网络连接错误：无法连接到AI服务。请检查您的网络连接、代理设置或防火墙设置。如果您在中国大陆地区，可能需要使用VPN或代理服务来访问OpenAI API。",
                "network_connection_error": "网络连接错误",
                "processing_error": "处理问题时出错: {0}",
                "session_history": "历史会话",
                "select_session": "选择会话记录",
                "session_loaded": "已加载会话",
                "chat_history": "对话记录",
                "refresh_history": "刷新对话记录",
                "history_time": "时间",
                "history_question": "问题",
                "history_answer": "回答"
            },
            "en": {
                "title": "Pandas AI Web - Data Conversation Assistant",
                "header": "Pandas AI Web - Conversational AI for Your Data",
                "model_selection": "AI Model Selection",
                "select_model": "Select AI Model",
                "model_status": "Model Status",
                "model_will_initialize": "Selected {0} model (will initialize after data upload)",
                "data_upload": "Data Upload",
                "upload_file": "Upload CSV, XLS or XLSX file",
                "upload_status": "Upload Status",
                "waiting_upload": "Waiting for file upload",
                "data_preview": "Data Preview",
                "data_conversation": "Data Conversation",
                "chat_with_data": "Chat with Your Data",
                "question_input": "Enter your question",
                "question_placeholder": "Example: What is the average value in this data?",
                "ask_button": "Ask",
                "clear_button": "Clear Chat",
                "thinking": "Thinking...",
                "please_upload": "Please upload a data file first",
                "file_loaded": "Successfully loaded data file ({0} rows) and initialized {1} model",
                "file_loaded_encoding": "Successfully loaded data file ({0} rows) using {1} encoding and initialized {2} model",
                "total_rows": "Total rows: {0}",
                "total_rows_limit": "Total rows: {0} (showing first {1} rows)",
                "total_rows_encoding": "Total rows: {0} (loaded with {1} encoding)",
                "total_rows_limit_encoding": "Total rows: {0} (showing first {1} rows, loaded with {2} encoding)",
                "unsupported_format": "Unsupported file format: {0}",
                "load_error": "Error loading file: {0}",
                "encoding_error": "Failed to recognize CSV file encoding, please try saving as UTF-8",
                "no_valid_data": "The file contains no valid data",
                "chart_analysis": "Chart analysis generated",
                "chart_result": "Chart analysis result:",
                "chart_generated_view_right": "Chart generated, please view the chart display area on the right",
                "chart_loaded_view_right": "Chart history loaded, please view the chart display area on the right",
                "chart_file": "Chart file",
                "generation_time": "Generation time",
                "loading_time": "Loading time",
                "chart_path": "Chart path",
                "last_updated": "Last updated",
                "no_history": "No chat history",
                "session_loaded_from_history": "Load session from history",
                "record_deleted": "Record deleted",
                "record_delete_failed": "Failed to delete record",
                "no_row_selected": "Please select a row first",
                "openai_key_missing": "OPENAI_API_KEY not configured in .env file",
                "openai_init_failed": "Failed to create OpenAI LLM instance: {0}",
                "azure_key_missing": "AZURE_OPENAI_API_KEY not configured in .env file",
                "azure_endpoint_missing": "AZURE_OPENAI_ENDPOINT not configured in .env file",
                "azure_deployment_missing": "AZURE_OPENAI_DEPLOYMENT_NAME not configured in .env file",
                "azure_connection_error": "Network connection error: Unable to connect to Azure OpenAI service",
                "azure_init_failed": "Failed to create Azure OpenAI LLM instance: {0}",
                "ollama_connection_failed": "Unable to connect to Ollama service ({0}), please ensure Ollama service is running",
                "ollama_init_failed": "Failed to initialize Ollama model: {0}",
                "unsupported_llm_type": "Unsupported LLM type: {0}",
                "language": "Language",
                "language_switch": "Switch Language",
                "chinese": "中文",
                "english": "English",
                "chart_alt_text": "Data analysis chart: {0}",
                "init_success": "Successfully initialized {0} AI model",
                "init_failed": "Error initializing AI model: {0}",
                "no_dataframe": "Please upload a data file before initializing AI model",
                "network_error": "Network connection error: Unable to connect to AI service. Please check your network connection, proxy settings or firewall settings. If you are in mainland China, you may need to use a VPN or proxy service to access the OpenAI API.",
                "network_connection_error": "Network connection error",
                "processing_error": "Error processing question: {0}",
                "session_history": "Session History",
                "select_session": "Select Session",
                "session_loaded": "Session Loaded",
                "chat_history": "Chat History",
                "refresh_history": "Refresh History",
                "history_time": "Time",
                "history_question": "Question",
                "history_answer": "Answer"
            }
        }
    
    def get_text(self, key, *args):
        """Get text in the current language.
        
        Args:
            key: Resource key
            *args: Format arguments, if any
            
        Returns:
            Formatted text string in the current language
        """
        # Get text from current language resources or fallback to key
        text = self.resources.get(self.current_language, {}).get(key, key)
        
        # Apply format arguments if provided
        if args:
            try:
                return text.format(*args)
            except:
                return text
        return text
    
    def change_language(self, language_code):
        """Change the current language.
        
        Args:
            language_code: Language code ('zh' or 'en')
            
        Returns:
            Dictionary with all UI text in the new language
        """
        if language_code in self.resources:
            self.current_language = language_code
            
            # Return all text resources for the new language to update UI
            return {
                "title": self.get_text("title"),
                "header": self.get_text("header"),
                "model_selection": self.get_text("model_selection"),
                "select_model": self.get_text("select_model"),
                "model_status_label": self.get_text("model_status"),
                "data_upload": self.get_text("data_upload"),
                "upload_file": self.get_text("upload_file"),
                "upload_status_label": self.get_text("upload_status"),
                "upload_status_value": self.get_text("waiting_upload"),
                "data_preview": self.get_text("data_preview"),
                "data_conversation": self.get_text("data_conversation"),
                "chat_with_data": self.get_text("chat_with_data"),
                "question_input": self.get_text("question_input"),
                "question_placeholder": self.get_text("question_placeholder"),
                "ask_button": self.get_text("ask_button"),
                "clear_button": self.get_text("clear_button"),
                "language_label": self.get_text("language"),
                "session_history": self.get_text("session_history"),
                "select_session": self.get_text("select_session"),
                "chat_history": self.get_text("chat_history"),
                "refresh_history": self.get_text("refresh_history"),
                "history_time": self.get_text("history_time"),
                "history_question": self.get_text("history_question"),
                "history_answer": self.get_text("history_answer")
            }
        return None
    
    def detect_language(self, text):
        """Detect language from text input.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Detected language code ('zh' or 'en')
        """
        if not text:
            return self.current_language
        
        # Count Chinese characters
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        
        # If more than 10% Chinese characters, return Chinese
        return "zh" if chinese_chars / len(text) > 0.1 else "en"

# Create a singleton instance
language_manager = LanguageManager() 