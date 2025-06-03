class LanguageUtils:
    """语言工具类，用于处理多语言和检测文本语言"""
    
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
            "chart_analysis": "已生成图表分析",
            "chart_result": "图表分析结果：",
            "language": "语言",
            "language_switch": "切换语言",
            "chinese": "中文",
            "english": "English",
            "chart_alt_text": "数据分析图表: {0}",
            "init_success": "成功初始化 {0} AI模型",
            "init_failed": "初始化AI模型时出错: {0}",
            "no_dataframe": "请先上传数据文件，然后再初始化AI模型",
            "network_error": "网络连接错误：无法连接到AI服务。请检查您的网络连接、代理设置或防火墙设置。如果您在中国大陆地区，可能需要使用VPN或代理服务来访问OpenAI API。",
            "processing_error": "处理问题时出错: {0}",
            "session_history": "历史会话",
            "select_session": "选择会话记录",
            "session_loaded": "已加载会话",
            "chat_history": "对话记录",
            "refresh_history": "刷新记录",
            "history_time": "时间",
            "history_session": "会话ID",
            "history_question": "问题",
            "history_answer": "回答",
            "delete_session_button": "删除当前会话",
            "delete_all_button": "清空所有记录",
            "delete_record_button": "删除选中记录",
            "no_session_selected": "未选择会话",
            "session_history_deleted": "已删除当前会话记录",
            "record_deleted": "已删除选中记录",
            "record_delete_failed": "删除记录失败",
            "session_history_delete_failed": "删除会话记录失败",
            "all_history_deleted": "已清空所有对话记录",
            "all_history_delete_failed": "清空所有记录失败",
            "confirm_delete_session": "确定要删除当前会话的所有记录吗？",
            "confirm_delete_all": "确定要清空所有对话记录吗？",
            "session_tip": "选择历史会话可以继续之前的对话，点击下拉菜单选择要加载的会话。",
            "chat_history_tip": "这里显示所有对话记录，可以查看历史问题和回答。点击一行记录后，再点击\"加载记录\"按钮可以加载对应的会话。",
            "no_history": "暂无对话记录",
            "last_updated": "最后更新时间:",
            "load_session_button": "加载会话",
            "load_history_button": "加载记录",
            "no_row_selected": "请先选择一条记录",
            "session_loaded_from_history": "已从历史记录加载会话",
            "generated_chart": "生成的图表",
            "chart_info": "图表信息",
            "no_chart": "暂无图表",
            "chart_file": "图表文件",
            "generation_time": "生成时间",
            "loading_time": "加载时间",
            "chart_path": "路径",
            "chart_generated_view_right": "图表已生成，请查看右侧图表显示区域",
            "chart_loaded_view_right": "图表已加载，请查看右侧图表显示区域",
            "network_connection_error": "网络连接失败"
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
            "chart_analysis": "Chart analysis generated",
            "chart_result": "Chart analysis result:",
            "language": "Language",
            "language_switch": "Switch Language",
            "chinese": "中文",
            "english": "English",
            "chart_alt_text": "Data analysis chart: {0}",
            "init_success": "Successfully initialized {0} AI model",
            "init_failed": "Error initializing AI model: {0}",
            "no_dataframe": "Please upload a data file before initializing AI model",
            "network_error": "Network connection error: Unable to connect to AI service. Please check your network connection, proxy settings or firewall settings. If you are in mainland China, you may need to use a VPN or proxy service to access the OpenAI API.",
            "processing_error": "Error processing question: {0}",
            "session_history": "Session History",
            "select_session": "Select Session",
            "session_loaded": "Session Loaded",
            "chat_history": "Chat History",
            "refresh_history": "Refresh History",
            "history_time": "Time",
            "history_session": "Session ID",
            "history_question": "Question",
            "history_answer": "Answer",
            "delete_session_button": "Delete Current Session",
            "delete_all_button": "Clear All History",
            "delete_record_button": "Delete Selected Record",
            "no_session_selected": "No session selected",
            "session_history_deleted": "Session history deleted",
            "record_deleted": "Selected record deleted",
            "record_delete_failed": "Failed to delete record",
            "session_history_delete_failed": "Failed to delete session history",
            "all_history_deleted": "All history cleared",
            "all_history_delete_failed": "Failed to clear all history",
            "confirm_delete_session": "Are you sure you want to delete all records for this session?",
            "confirm_delete_all": "Are you sure you want to clear all conversation history?",
            "session_tip": "Select session history to continue previous conversation, click dropdown menu to select session to load.",
            "chat_history_tip": "Here shows all conversation history. You can view historical questions and answers. Click a row and then the 'Load History' button to load that session.",
            "no_history": "No conversation history",
            "last_updated": "Last updated time:",
            "load_session_button": "Load Session",
            "load_history_button": "Load History",
            "no_row_selected": "Please select a row first",
            "session_loaded_from_history": "Session loaded from history",
            "generated_chart": "Generated Chart",
            "chart_info": "Chart Information",
            "no_chart": "No Chart",
            "chart_file": "Chart File",
            "generation_time": "Generation Time",
            "loading_time": "Loading Time",
            "chart_path": "Path",
            "chart_generated_view_right": "Chart generated, please view the chart display area on the right",
            "chart_loaded_view_right": "Chart loaded, please view the chart display area on the right",
            "network_connection_error": "Network connection error"
        }
    }
    
    @staticmethod
    def get_text(language, key, *args):
        """
        获取指定语言的文本
        
        Args:
            language: 语言代码，'zh'或'en'
            key: 文本键
            *args: 格式化参数
        
        Returns:
            str: 翻译后的文本
        """
        if language not in LanguageUtils.LANGUAGE:
            language = "zh"  # 默认中文
            
        text = LanguageUtils.LANGUAGE[language].get(key, key)
        if args:
            try:
                return text.format(*args)
            except:
                return text
        return text
    
    @staticmethod
    def is_chinese(text):
        """
        检测文本是否主要是中文
        
        Args:
            text: 要检测的文本
            
        Returns:
            bool: 如果主要是中文则返回True
        """
        if not text:
            return False
            
        # 计算中文字符占比
        chinese_chars = 0
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                chinese_chars += 1
                
        # 如果中文字符占比超过10%，则认为是中文
        return chinese_chars / len(text) > 0.1 