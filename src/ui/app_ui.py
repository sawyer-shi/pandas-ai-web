import os
import gradio as gr
from ..utils.language_utils import LanguageUtils
from ..utils.data_loader import DataLoader

# 尝试导入pandas，如果失败则设置为None
try:
    import pandas as pd
except ImportError:
    pd = None

# 检查机器人头像文件是否存在，如果不存在，使用默认表情符号
ROBOT_AVATAR = "avatar/robot.jpg"
if not os.path.exists(ROBOT_AVATAR):
    ROBOT_AVATAR = "🤖"

class AppUI:
    """UI应用类，负责Gradio界面的创建和交互"""
    
    def __init__(self, app_controller):
        """
        初始化UI应用
        
        Args:
            app_controller: 应用控制器实例
        """
        self.controller = app_controller
        # 默认中文
        self.language = "zh"
    
    def get_text(self, key, *args):
        """获取当前语言的UI文本"""
        return LanguageUtils.get_text(self.language, key, *args)
    
    def create_interface(self):
        """创建Gradio界面"""
        with gr.Blocks(
            title=self.get_text("title"),
            css="""
            /* 全局页面滚动样式 */
            html, body {
                height: 100%;
                overflow: auto;
                margin: 0;
                padding: 0;
            }
            
            /* 确保Gradio容器可以正常滚动 */
            .gradio-container {
                height: auto !important;
                min-height: 100vh !important;
                overflow: visible !important;
                padding-bottom: 20px !important;
            }
            
            /* 主界面容器 */
            .main-container {
                height: auto !important;
                min-height: 100vh !important;
                overflow: visible !important;
                padding-bottom: 20px !important;
            }
            
            /* 确保所有组件容器都可以正常滚动 */
            .gr-tab-item {
                height: auto !important;
                overflow: visible !important;
            }
            
            .gr-column {
                height: auto !important;
                overflow: visible !important;
            }
            
            .gr-row {
                height: auto !important;
                overflow: visible !important;
            }
            
            /* 美化全局滚动条 */
            html::-webkit-scrollbar {
                width: 12px;
            }
            
            html::-webkit-scrollbar-track {
                background: #f1f1f1;
            }
            
            html::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 6px;
            }
            
            html::-webkit-scrollbar-thumb:hover {
                background: #a8a8a8;
            }
            
            /* 表格样式 */
            .main-title {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-size: 1.5em;
                font-weight: bold;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            /* 数据预览区域样式 */
            .data-preview-container {
                max-height: 500px !important;
                overflow-y: auto !important;
                overflow-x: auto !important;
                border: 1px solid #e0e0e0 !important;
                border-radius: 6px !important;
                padding: 10px !important;
                background: #fafafa !important;
                margin-top: 10px !important;
            }
            
            .data-preview-container table {
                width: 100% !important;
                border-collapse: collapse !important;
                font-size: 0.85em !important;
                margin: 0 !important;
            }
            
            .data-preview-container th {
                background: #f8f9fa !important;
                position: sticky !important;
                top: 0 !important;
                z-index: 10 !important;
                padding: 8px 6px !important;
                border: 1px solid #dee2e6 !important;
                font-size: 0.8em !important;
                font-weight: 600 !important;
                text-align: left !important;
                white-space: nowrap !important;
            }
            
            .data-preview-container td {
                padding: 6px !important;
                border: 1px solid #dee2e6 !important;
                font-size: 0.75em !important;
                white-space: nowrap !important;
                text-align: left !important;
            }
            
            .data-preview-container tr:nth-child(even) {
                background-color: #f9f9f9 !important;
            }
            
            .data-preview-container tr:hover {
                background-color: #e8f4fd !important;
            }
            
            /* 滚动条样式美化 */
            .data-preview-container::-webkit-scrollbar {
                width: 8px !important;
                height: 8px !important;
            }
            
            .data-preview-container::-webkit-scrollbar-track {
                background: #f1f1f1 !important;
                border-radius: 4px !important;
            }
            
            .data-preview-container::-webkit-scrollbar-thumb {
                background: #c1c1c1 !important;
                border-radius: 4px !important;
            }
            
            .data-preview-container::-webkit-scrollbar-thumb:hover {
                background: #a8a8a8 !important;
            }
            
            .tip-text {
                color: #666;
                font-size: 0.9em;
                font-style: italic;
                margin-top: -5px;
                margin-bottom: 10px;
            }
            .history-container {
                margin-top: 10px;
                display: flex;
                flex-direction: column;
                overflow: visible;
            }
            
            /* 历史记录表格样式 */
            .history-table {
                max-height: 400px;
                overflow: visible;
                border: 1px solid #e0e0e0;
                border-top: none;
                border-radius: 0 0 6px 6px;
                margin-bottom: 10px;
                position: relative;
            }
            
            /* 只在这里显示滚动条 */
            .history-table .dataframe {
                max-height: 400px;
                overflow-y: auto;
                overflow-x: auto;
                font-size: 0.9em;
                position: relative;
            }
            
            /* 确保表格容器可以滚动 */
            .history-table .table-wrap {
                font-size: 0.9em;
                overflow: auto;
                max-height: 400px;
            }
            
            /* 美化滚动条样式 */
            .history-table .dataframe::-webkit-scrollbar,
            .history-table .table-wrap::-webkit-scrollbar {
                width: 12px;
                height: 12px;
                background-color: #f5f5f5;
            }
            
            .history-table .dataframe::-webkit-scrollbar-track,
            .history-table .table-wrap::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 6px;
            }
            
            .history-table .dataframe::-webkit-scrollbar-thumb,
            .history-table .table-wrap::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 6px;
                border: 1px solid #f1f1f1;
            }
            
            .history-table .dataframe::-webkit-scrollbar-thumb:hover,
            .history-table .table-wrap::-webkit-scrollbar-thumb:hover {
                background: #a8a8a8;
            }
            
            .history-table .dataframe::-webkit-scrollbar-corner,
            .history-table .table-wrap::-webkit-scrollbar-corner {
                background: #f1f1f1;
            }
            
            /* 确保历史容器不会限制滚动 */
            .history-container {
                margin-top: 10px;
                display: flex;
                flex-direction: column;
                overflow: visible;
                height: auto;
                max-height: none;
            }
            
            /* 移除对滚动条的隐藏 */
            .history-table::-webkit-scrollbar {
                display: block;
            }
            
            /* 强制表格布局 */
            .history-table table,
            .history-table .dataframe table {
                width: 100% !important;
                border-collapse: collapse !important;
                table-layout: fixed !important;
                margin: 0 !important;
            }
            
            /* 表头样式 */
            .history-table th,
            .history-table .dataframe th {
                background: #f8f9fa !important;
                position: sticky !important;
                top: 0 !important;
                z-index: 10 !important;
                padding: 8px 6px !important;
                border-bottom: 1px solid #dee2e6 !important;
                border-right: 1px solid #dee2e6 !important;
                font-size: 0.85em !important;
                font-weight: 600 !important;
                text-align: left !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
                box-sizing: border-box !important;
            }
            
            /* 固定列宽 */
            .history-table th:first-child,
            .history-table .dataframe th:first-child,
            .history-table td:first-child,
            .history-table .dataframe td:first-child {
                width: 16% !important;
                min-width: 16% !important;
                max-width: 16% !important;
            }
            
            .history-table th:nth-child(2),
            .history-table .dataframe th:nth-child(2),
            .history-table td:nth-child(2),
            .history-table .dataframe td:nth-child(2) {
                width: 16% !important;
                min-width: 16% !important;
                max-width: 16% !important;
            }
            
            .history-table th:nth-child(3),
            .history-table .dataframe th:nth-child(3),
            .history-table td:nth-child(3),
            .history-table .dataframe td:nth-child(3) {
                width: 22% !important;
                min-width: 22% !important;
                max-width: 22% !important;
            }
            
            .history-table th:nth-child(4),
            .history-table .dataframe th:nth-child(4),
            .history-table td:nth-child(4),
            .history-table .dataframe td:nth-child(4) {
                width: 25% !important;
                min-width: 25% !important;
                max-width: 25% !important;
            }
            
            .history-table th:nth-child(5),
            .history-table .dataframe th:nth-child(5),
            .history-table td:nth-child(5),
            .history-table .dataframe td:nth-child(5) {
                width: 11% !important;
                min-width: 11% !important;
                max-width: 11% !important;
            }
            
            .history-table th:nth-child(6),
            .history-table .dataframe th:nth-child(6),
            .history-table td:nth-child(6),
            .history-table .dataframe td:nth-child(6) {
                width: 10% !important;
                min-width: 10% !important;
                max-width: 10% !important;
            }
            
            .history-table th:last-child,
            .history-table .dataframe th:last-child {
                border-right: none !important;
            }
            
            /* 表体样式 */
            .history-table td,
            .history-table .dataframe td {
                padding: 8px 6px !important;
                border-bottom: 1px solid #f0f0f0 !important;
                border-right: 1px solid #f0f0f0 !important;
                font-size: 0.85em !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
                cursor: pointer !important;
                vertical-align: middle !important;
                box-sizing: border-box !important;
            }
            
            .history-table td:last-child,
            .history-table .dataframe td:last-child {
                border-right: none !important;
            }
            
            .history-table tr:hover {
                background-color: #f5f5f5;
            }
            
            .history-table tr.selected {
                background-color: #e3f2fd;
            }
            
            /* 按钮组样式 */
            .history-buttons {
                display: flex;
                gap: 8px;
                justify-content: flex-start;
                padding: 5px 0;
                margin-top: 5px;
                border-top: 1px solid #e0e0e0;
                background: #fafafa;
                border-radius: 0 0 6px 6px;
                padding: 10px;
            }
            
            .history-buttons button {
                font-size: 0.85em;
                padding: 6px 12px;
                height: 32px;
                border-radius: 4px;
                border: 1px solid #d0d7de;
                transition: all 0.2s ease;
            }
            
            .history-buttons button:hover {
                transform: translateY(-1px);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .history-buttons button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            /* 表格上方的按钮组样式 */
            .history-buttons-top {
                display: flex !important;
                flex-direction: row !important;
                gap: 8px !important;
                align-items: center !important;
                justify-content: flex-start !important;
                padding: 8px !important;
                background: #f8f9fa !important;
                border-radius: 6px 6px 0 0 !important;
                border-bottom: 1px solid #e0e0e0 !important;
                height: auto !important;
                min-height: 50px !important;
                overflow: visible !important;
            }
            
            /* 统一所有控件的高度和样式 */
            .history-buttons-top > * {
                height: 36px;
                margin: 0;
                flex-shrink: 0;
                box-sizing: border-box;
            }
            
            /* 搜索输入框样式 - 均衡占满一行 */
            .search-input {
                flex: 1;
                min-width: 0;
                background: white !important;
                border: 1px solid #d0d7de !important;
                border-radius: 4px !important;
                height: 36px !important;
                display: block !important;
                pointer-events: auto !important;
                cursor: text !important;
                position: relative !important;
                z-index: 10 !important;
            }
            
            /* 针对无容器的搜索输入框 */
            .search-input.no-container {
                padding: 0 !important;
                margin: 0 !important;
                border: 1px solid #d0d7de !important;
                border-radius: 4px !important;
                overflow: hidden !important;
            }
            
            /* 强制显示并确保可交互 */
            .search-input,
            .search-input > *,
            .search-input .gr-textbox,
            .search-input .gr-form,
            .search-input input,
            .search-input textarea {
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
                position: relative !important;
                pointer-events: auto !important;
                cursor: text !important;
                z-index: 10 !important;
            }
            
            /* 输入框本身的样式 - 确保可交互 */
            .search-input input,
            .search-input textarea {
                width: 100% !important;
                height: 32px !important;
                margin: 0 !important;
                padding: 6px 10px !important;
                border: 1px solid #d0d7de !important;
                border-radius: 2px !important;
                background: white !important;
                font-size: 14px !important;
                line-height: 1.2 !important;
                box-sizing: border-box !important;
                pointer-events: auto !important;
                cursor: text !important;
                outline: none !important;
                user-select: text !important;
                -webkit-user-select: text !important;
                -moz-user-select: text !important;
                -ms-user-select: text !important;
            }
            
            /* 无容器模式的输入框 */
            .search-input.no-container input,
            .search-input.no-container textarea {
                border: none !important;
                border-radius: 0 !important;
                height: 34px !important;
                margin: 0 !important;
                padding: 8px 12px !important;
            }
            
            /* 输入框获得焦点时的样式 */
            .search-input input:focus,
            .search-input textarea:focus {
                outline: 2px solid #007bff !important;
                outline-offset: -2px !important;
                background: #fff !important;
                border-color: #007bff !important;
            }
            
            /* 确保Gradio包装器不阻止交互 */
            .search-input .gr-textbox,
            .search-input .gr-form,
            .search-input .wrap {
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
                width: 100% !important;
                height: 36px !important;
                margin: 0 !important;
                padding: 2px !important;
                border: none !important;
                background: white !important;
                pointer-events: auto !important;
                cursor: text !important;
                position: relative !important;
                z-index: 10 !important;
            }
            
            /* 移除可能阻止交互的规则 */
            .search-input * {
                pointer-events: auto !important;
                user-select: auto !important;
                -webkit-user-select: auto !important;
                -moz-user-select: auto !important;
                -ms-user-select: auto !important;
            }
            
            /* 确保没有其他元素遮挡 */
            .history-buttons-top {
                position: relative !important;
                z-index: 5 !important;
            }
            
            /* 搜索按钮样式 - 均衡占满一行 */
            .search-button {
                flex: 1;
                min-width: 0;
                white-space: nowrap;
            }
            
            /* 控制按钮样式 - 均衡占满一行 */
            .control-button {
                flex: 1;
                min-width: 0;
                white-space: nowrap;
            }
            
            /* 按钮标签样式 */
            .button-label-container {
                margin-top: 2px !important;
                margin-bottom: 0 !important;
            }
            
            .button-label {
                font-size: 0.75em !important;
                color: #666 !important;
                text-align: center !important;
                margin: 0 !important;
                padding: 0 !important;
                line-height: 1 !important;
            }
            
            /* 搜索按钮额外样式 */
            .search-button {
                background: #007bff !important;
                border-color: #007bff !important;
                color: white !important;
            }
            
            .search-button:hover {
                background: #0056b3 !important;
                border-color: #0056b3 !important;
            }
            
            /* 状态指示器 */
            .selection-indicator {
                font-size: 0.8em;
                color: #666;
                margin-bottom: 5px;
                padding: 4px 8px;
                background: #f0f8ff;
                border-radius: 4px;
                border-left: 3px solid #007bff;
                display: none;
            }
            
            .selection-indicator.visible {
                display: block;
            }
            
            /* 标签页优化 */
            .history-container .tab-nav {
                margin-bottom: 10px;
            }
            
            .history-container .tab-nav button {
                padding: 8px 16px;
                font-size: 0.9em;
                border-radius: 4px 4px 0 0;
            }
            
            /* 紧凑布局 */
            .compact-layout {
                display: flex;
                flex-direction: column;
                gap: 0;
                margin: 0;
                padding: 0;
            }
            
            .compact-layout > * {
                margin: 0;
                padding: 0;
            }
            """
        ) as interface:
            # 标题 - 美化显示
            header = gr.HTML(f"""
                <div class="main-title">
                    {self.get_text("header")}
                </div>
            """)
            
            # 语言选择
            with gr.Row():
                with gr.Column(scale=1):
                    language_choice = gr.Radio(
                        label=self.get_text("language"),
                        choices=[self.get_text("chinese"), self.get_text("english")],
                        value=self.get_text("chinese"),
                        interactive=True
                    )
            
            with gr.Row():
                with gr.Column(scale=1):
                    # 左侧栏：模型选择和数据上传
                    with gr.Group():
                        model_selection_header = gr.Markdown(self.get_text("model_selection"))
                        llm_choice = gr.Radio(
                            label=self.get_text("select_model"), 
                            choices=["OpenAI", "Azure", "Ollama"],
                            value=self.controller.llm_type,
                            interactive=True
                        )
                        model_status = gr.Textbox(
                            label=self.get_text("model_status"), 
                            value=self.get_text("model_will_initialize", self.controller.llm_type)
                        )
                    
                    with gr.Group():
                        data_upload_header = gr.Markdown(self.get_text("data_upload"))
                        file_input = gr.File(
                            label=self.get_text("upload_file"),
                            file_count="single",
                            type="filepath"
                        )
                        upload_status = gr.Textbox(
                            label=self.get_text("upload_status"), 
                            value=self.get_text("waiting_upload")
                        )
                        data_preview = gr.HTML(
                            label=self.get_text("data_preview"),
                            elem_classes="data-preview-container"
                        )
                
                with gr.Column(scale=2):
                    # 右侧：聊天界面
                    chat_header = gr.Markdown(self.get_text("data_conversation"))
                    with gr.Row():
                        with gr.Column(scale=3):
                            chatbot = gr.Chatbot(
                                label=self.get_text("chat_with_data"),
                                height=500,
                                bubble_full_width=False,
                                show_copy_button=True,
                                avatar_images=(None, None),  # 用户和助手头像
                                type="messages"  # 使用新的消息格式，支持更好的图片显示
                            )
                        with gr.Column(scale=1):
                            # 图片展示区域
                            chart_display_header = gr.Markdown(f"**{self.get_text('generated_chart')}**")
                            chart_display = gr.Image(
                                label=self.get_text("generated_chart"),
                                height=400,
                                show_label=False,
                                show_share_button=False,
                                interactive=False
                            )
                            chart_info = gr.Textbox(
                                label=self.get_text("chart_info"),
                                value=self.get_text("no_chart"),
                                interactive=False,
                                lines=4
                            )
                    
                    with gr.Row():
                        question_input = gr.Textbox(
                            label=self.get_text("question_input"),
                            placeholder=self.get_text("question_placeholder"),
                            scale=8,
                            interactive=True
                        )
                        ask_button = gr.Button(value=self.get_text("ask_button"), scale=1)
                        clear_button = gr.Button(value=self.get_text("clear_button"), scale=1)
            
            # 移到提问框下方：会话历史和对话记录
            with gr.Row():
                with gr.Column(elem_classes="history-container", scale=1):
                    # 历史会话和对话记录区域
                    with gr.Tabs() as tabs:
                        with gr.TabItem(label=self.get_text("chat_history")) as chat_tab:
                            with gr.Column(elem_classes="compact-layout"):
                                # 对话记录查看窗口
                                chat_history_header = gr.Markdown("**" + self.get_text("chat_history") + "**")
                                
                                # 选择状态指示器
                                selection_status = gr.Markdown(
                                    value="",
                                    elem_classes="selection-indicator",
                                    visible=False
                                )
                                
                                # 按钮组 - 移动到表格上方
                                with gr.Row(elem_classes="history-buttons-top"):
                                    search_input = gr.Textbox(
                                        placeholder=self.get_text("search_placeholder"),
                                        lines=1,
                                        show_label=False,
                                        elem_classes="search-input",
                                        value="",
                                        interactive=True,
                                        container=False
                                    )
                                    search_btn = gr.Button(
                                        self.get_text("search_button"),
                                        variant="primary",
                                        size="sm",
                                        elem_classes="search-button"
                                    )
                                    refresh_history_btn = gr.Button(
                                        self.get_text("refresh_history"),
                                        variant="secondary",
                                        size="sm",
                                        elem_classes="control-button"
                                    )
                                    delete_all_btn = gr.Button(
                                        self.get_text("delete_all_button"),
                                        variant="secondary", 
                                        size="sm",
                                        elem_classes="control-button"
                                    )
                                
                                chat_history_display = gr.Dataframe(
                                    headers=[
                                        self.get_text("history_time"), 
                                        self.get_text("history_session"),
                                        self.get_text("history_question"), 
                                        self.get_text("history_answer"),
                                        self.get_text("load_record_action"),
                                        self.get_text("delete_action")
                                    ],
                                    col_count=(6, "fixed"),
                                    interactive=True,
                                    wrap=False,
                                    column_widths=["16%", "16%", "22%", "25%", "11%", "10%"],
                                    elem_classes="history-table",
                                    row_count=5
                                )
                                
                                # 存储当前选中的行信息（隐藏元素）
                                selected_row_info = gr.Textbox(visible=False, value="")
                                
                                # 存储当前搜索关键词（隐藏元素）
                                current_search_keywords = gr.Textbox(visible=False, value="")
            
            # 初始化对话记录显示 - 确保使用正确的语言
            chat_history_display.value = self.controller.refresh_current_history()
            
            # 事件处理
            
            # 处理语言切换
            def change_lang(choice):
                # 切换语言 - 直接判断选择的是中文还是英文
                new_lang = "zh" if choice == "中文" else "en"
                self.language = new_lang
                self.controller.set_language(new_lang)
                
                # 获取当前上传状态的文本，如果有文件已上传，需要重新生成状态消息
                current_upload_status = self.get_text("waiting_upload")
                current_data_preview = ""
                
                # 如果控制器有数据文件，重新生成状态消息和预览
                if hasattr(self.controller, 'df') and self.controller.df is not None:
                    try:
                        # 重新生成预览HTML
                        preview_html = DataLoader.generate_preview_html(self.controller.df, 500, new_lang)
                        current_data_preview = preview_html
                        
                        # 重新生成状态消息
                        row_count = len(self.controller.df)
                        model_name = self.controller.get_model_name()
                        current_upload_status = self.get_text("file_loaded_encoding", row_count, "utf-8", f"{self.controller.llm_type} ({model_name})")
                    except Exception as e:
                        print(f"更新上传状态时出错: {e}")
                        current_upload_status = self.get_text("waiting_upload")
                
                # 创建新的文件上传组件，包含正确的语言文本和CSS类
                new_file_input = gr.File(
                    label=self.get_text("upload_file"),
                    file_count="single",
                    type="filepath"
                )
                
                # 更新界面文本
                return (
                    gr.update(value=f"""
                        <div class="main-title">
                            {self.get_text("header")}
                        </div>
                    """),             # header
                    gr.update(value=self.get_text("model_selection")),    # model_selection_header
                    gr.update(label=self.get_text("select_model")),       # llm_choice
                    gr.update(label=self.get_text("model_status")),       # model_status
                    gr.update(value=self.get_text("model_will_initialize", self.controller.llm_type)), # model_status 值
                    gr.update(value=self.get_text("data_upload")),        # data_upload_header
                    new_file_input,                                       # file_input
                    gr.update(label=self.get_text("upload_status")),      # upload_status
                    gr.update(value=current_upload_status),               # upload_status 值 - 使用新语言
                    gr.update(label=self.get_text("data_preview"), value=current_data_preview),       # data_preview - 同时更新label和value
                    gr.update(value=self.get_text("data_conversation")),  # chat_header
                    gr.update(label=self.get_text("chat_with_data")),     # chatbot
                    gr.update(label=self.get_text("question_input"), placeholder=self.get_text("question_placeholder"), interactive=True, visible=True), # question_input
                    gr.update(value=self.get_text("ask_button")),         # ask_button
                    gr.update(value=self.get_text("clear_button")),       # clear_button
                    gr.update(label=self.get_text("language")),           # language_choice
                    gr.update(value=f"**{self.get_text('generated_chart')}**"), # chart_display_header
                    gr.update(label=self.get_text("generated_chart")),    # chart_display
                    gr.update(label=self.get_text("chart_info"), value=self.get_text("no_chart")),         # chart_info - 同时更新label和value
                    gr.update(value=f"**{self.get_text('chat_history')}**"), # chat_history_header 
                    gr.update(
                        headers=[
                            self.get_text("history_time"), 
                            self.get_text("history_session"),
                            self.get_text("history_question"), 
                            self.get_text("history_answer"),
                            self.get_text("load_record_action"),
                            self.get_text("delete_action")
                        ],
                        value=self.controller.refresh_current_history()
                    ),                                                  # chat_history_display
                    gr.update(placeholder=self.get_text("search_placeholder"), interactive=True, container=False),   # search_input
                    gr.update(value=self.get_text("search_button")),   # search_btn
                    gr.update(value=self.get_text("refresh_history")),   # refresh_history_btn
                    gr.update(value=self.get_text("delete_all_button")),   # delete_all_btn
                    gr.update(label=self.get_text("chat_history")),        # TabItem - 对话记录
                    gr.update()   # current_search_keywords - 保持不变
                )
            
            # 智能刷新功能：根据当前搜索状态决定显示内容
            def smart_refresh(search_keywords):
                """根据当前搜索状态智能刷新表格"""
                if search_keywords and search_keywords.strip():
                    # 如果当前有搜索关键词，重新执行搜索
                    return self.controller.search_history(search_keywords)
                else:
                    # 否则显示所有记录
                    return self.controller.refresh_current_history()
            
            # 在事件处理程序中注册新文件组件的上传事件
            def register_new_upload_event(file_input):
                # 注册新文件上传组件的事件处理程序
                if file_input and hasattr(file_input, 'upload'):
                    file_input.upload(
                        fn=self.controller.load_dataframe,
                        inputs=[file_input],
                        outputs=[upload_status, data_preview]
                    ).then(
                        # 上传新文件后清除聊天记录和图表显示
                        fn=lambda: ([], None, self.get_text("no_chart")),
                        inputs=[],
                        outputs=[chatbot, chart_display, chart_info]
                    ).then(
                        # 刷新历史记录显示
                        fn=self.controller.refresh_current_history,
                        inputs=[],
                        outputs=[chat_history_display]
                    )
                return None
            
            # 语言切换事件
            language_choice.change(
                fn=change_lang,
                inputs=[language_choice],
                outputs=[
                    header,
                    model_selection_header,
                    llm_choice,
                    model_status,
                    model_status,
                    data_upload_header,
                    file_input,
                    upload_status,
                    upload_status,
                    data_preview,
                    chat_header,
                    chatbot,
                    question_input,
                    ask_button,
                    clear_button,
                    language_choice,
                    chart_display_header,
                    chart_display,
                    chart_info,
                    chat_history_header,
                    chat_history_display,
                    search_input,
                    search_btn,
                    refresh_history_btn,
                    delete_all_btn,
                    chat_tab,
                    current_search_keywords
                ]
            ).then(
                fn=register_new_upload_event,
                inputs=[file_input],
                outputs=None
            ).then(
                # 语言切换后根据当前搜索状态智能刷新历史数据
                fn=smart_refresh,
                inputs=[current_search_keywords],
                outputs=[chat_history_display]
            )
            
            # 自动处理模型切换
            llm_choice.change(
                fn=self.controller.change_model,
                inputs=[llm_choice],
                outputs=[model_status]
            )
            
            # 刷新后重置选择状态并更新表头的函数
            def reset_selection_and_update_headers():
                """刷新后重置选择状态并更新表头语言"""
                return (
                    "", 
                    gr.update(visible=False), 
                    gr.update(headers=[
                        self.get_text("history_time"), 
                        self.get_text("history_session"),
                        self.get_text("history_question"), 
                        self.get_text("history_answer"),
                        self.get_text("load_record_action"),
                        self.get_text("delete_action")
                    ])
                )

            # 加载所有记录功能
            def load_all_records():
                """加载所有记录并清空搜索状态"""
                all_records = self.controller.refresh_current_history()
                return all_records, ""  # 清空搜索关键词
            
            # 刷新对话记录
            refresh_history_btn.click(
                fn=load_all_records,
                inputs=[],
                outputs=[chat_history_display, current_search_keywords]
            ).then(
                # 刷新后重置选择状态并更新表头
                fn=reset_selection_and_update_headers,
                inputs=[],
                outputs=[selected_row_info, selection_status, chat_history_display]
            )
            
            # 优化行选择处理
            def handle_table_selection(current_keywords, evt: gr.SelectData):
                """处理表格行选择事件"""
                try:
                    if evt is None:
                        return "", gr.update(visible=False), None, self.get_text("no_chart"), []
                    
                    print(f"表格选择事件: {evt}")
                    
                    # 获取点击的行和列
                    row_index = evt.index[0] if isinstance(evt.index, (list, tuple)) else evt.index
                    col_index = evt.index[1] if isinstance(evt.index, (list, tuple)) and len(evt.index) > 1 else None
                    
                    # 根据当前搜索状态获取对应的历史记录
                    if current_keywords and current_keywords.strip():
                        # 如果有搜索关键词，获取搜索结果
                        current_history = self.controller.search_history(current_keywords)
                        print(f"使用搜索结果，关键词: {current_keywords}")
                    else:
                        # 否则获取所有记录
                        current_history = self.controller.refresh_current_history()
                        print(f"使用所有记录")
                    
                    if current_history and 0 <= row_index < len(current_history):
                        # 获取选中行的数据
                        selected_row = current_history[row_index]
                        
                        # 检查是否点击的是第5列（点击加载数据列）
                        if col_index == 4 and len(selected_row) > 4 and selected_row[4]:
                            # 通过行数据获取时间和问题信息来查找对应的数据库记录
                            time_info = selected_row[0]  # 第1列：时间
                            question_info = selected_row[2]  # 第3列：问题
                            
                            # 调用控制器方法通过时间和问题查找记录
                            try:
                                # 构建查询信息
                                time_question_info = f"{time_info}|{question_info}"
                                
                                print(f"🔍 点击加载数据: 行索引 {row_index}, 时间: {time_info}, 问题: {question_info[:50]}...")
                                
                                # 通过时间和问题信息获取记录信息
                                record_info = self.controller.get_record_by_time_question(time_question_info)
                                
                                if record_info:
                                    session_id = record_info.get('session_id')
                                    record_id = record_info.get('record_id')
                                    has_chart = record_info.get('has_chart', 0)
                                    
                                    # 调用控制器的加载记录方法
                                    new_chatbot, status, chart_file, chart_info = self.controller.load_history_record(session_id, [], record_id)
                                    
                                    print(f"✅ 点击加载数据: 会话ID {session_id}, 记录ID {record_id}, 包含图表: {bool(has_chart)}, 状态: {status}")
                                    
                                    # 添加滚动定位功能：在聊天记录中找到对应的问答位置
                                    if new_chatbot and len(new_chatbot) > 0:
                                        # 查找与当前问题匹配的聊天记录位置
                                        target_index = -1
                                        for i, (user_msg, bot_msg) in enumerate(new_chatbot):
                                            if user_msg and question_info in user_msg:
                                                target_index = i
                                                break
                                        
                                        # 如果找到了目标位置，在聊天记录中添加滚动定位标记
                                        if target_index >= 0:
                                            # 在目标位置添加一个临时的定位标记
                                            updated_chatbot = []
                                            for i, (user_msg, bot_msg) in enumerate(new_chatbot):
                                                if i == target_index:
                                                    # 在目标问答前添加定位标记
                                                    updated_chatbot.append((
                                                        f"📍 **[定位到此问答]** {user_msg}",
                                                        bot_msg
                                                    ))
                                                else:
                                                    updated_chatbot.append((user_msg, bot_msg))
                                            new_chatbot = updated_chatbot
                                            
                                            # 添加JavaScript代码来实现滚动定位
                                            scroll_script = """
                                            <script>
                                            setTimeout(function() {
                                                // 查找包含定位标记的聊天消息
                                                var messages = document.querySelectorAll('.message');
                                                for (var i = 0; i < messages.length; i++) {
                                                    var msg = messages[i];
                                                    if (msg.textContent.includes('📍 **[定位到此问答]**')) {
                                                        // 滚动到该消息位置
                                                        msg.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                                        // 高亮显示该消息
                                                        msg.style.backgroundColor = '#fff3cd';
                                                        msg.style.border = '2px solid #ffc107';
                                                        msg.style.borderRadius = '8px';
                                                        msg.style.padding = '10px';
                                                        // 5秒后移除高亮
                                                        setTimeout(function() {
                                                            msg.style.backgroundColor = '';
                                                            msg.style.border = '';
                                                            msg.style.borderRadius = '';
                                                            msg.style.padding = '';
                                                        }, 5000);
                                                        break;
                                                    }
                                                }
                                            }, 1000);
                                            </script>
                                            """
                                            
                                            # 将滚动脚本添加到第一个消息中
                                            if new_chatbot and len(new_chatbot) > 0:
                                                first_user_msg, first_bot_msg = new_chatbot[0]
                                                new_chatbot[0] = (first_user_msg, first_bot_msg + scroll_script)
                                    
                                    # 返回加载结果，包括更新的聊天记录和图表
                                    return "", gr.update(visible=False), chart_file, chart_info, new_chatbot
                                else:
                                    print("❌ 未找到对应的数据库记录")
                                    return "", gr.update(visible=False), None, "未找到对应的数据库记录", []
                                    
                            except Exception as e:
                                print(f"❌ 点击加载数据失败: {str(e)}")
                                return "", gr.update(visible=False), None, f"点击加载数据失败: {str(e)}", []
                        
                        # 检查是否点击的是第6列（删除操作列）
                        elif col_index == 5 and len(selected_row) > 5 and selected_row[5]:
                            # 通过行数据获取时间和问题信息来查找对应的数据库记录
                            time_info = selected_row[0]  # 第1列：时间
                            question_info = selected_row[2]  # 第3列：问题
                            
                            # 调用控制器方法通过时间和问题查找记录
                            try:
                                # 构建查询信息
                                time_question_info = f"{time_info}|{question_info}"
                                
                                # 删除记录
                                status = self.delete_selected_record(time_question_info)
                                
                                print(f"✅ 删除记录: {time_question_info}, 状态: {status}")
                                
                                # 返回删除结果，不修改聊天记录和图表
                                return "", gr.update(visible=False), None, None, []
                                
                            except Exception as e:
                                print(f"❌ 删除记录失败: {str(e)}")
                                return "", gr.update(visible=False), None, f"删除记录失败: {str(e)}", []
                        else:
                            # 普通行选择逻辑
                            # 构建行标识信息：时间|问题
                            time_info = selected_row[0]  # 第1列：时间
                            question_info = selected_row[2]  # 第3列：问题
                            row_info = f"{time_info}|{question_info}"
                            
                            # 构建状态显示文本
                            status_text = f"已选择: {time_info[:10]} - {question_info[:20]}..."
                            
                            print(f"选中行 {row_index}: {row_info}")
                            
                            return (
                                row_info,
                                gr.update(value=status_text, visible=True),
                                None,  # 不修改图表显示
                                None,  # 不修改图表信息
                                []     # 不修改聊天记录
                            )
                    else:
                        print(f"无效的行索引: {row_index}")
                        return "", gr.update(visible=False), None, None, []
                        
                except Exception as e:
                    print(f"处理表格选择时出错: {str(e)}")
                    return "", gr.update(visible=False), None, f"处理失败: {str(e)}", []
            
            # 选择对话记录行
            chat_history_display.select(
                fn=handle_table_selection,
                inputs=[current_search_keywords],
                outputs=[selected_row_info, selection_status, chart_display, chart_info, chatbot]
            ).then(
                # 根据当前搜索状态智能刷新表格
                fn=smart_refresh,
                inputs=[current_search_keywords],
                outputs=[chat_history_display]
            )
            
            # 搜索功能
            def search_history(search_keywords):
                """搜索历史记录"""
                results = self.controller.search_history(search_keywords)
                return results, search_keywords  # 同时返回搜索结果和关键词
            
            # 搜索按钮点击事件
            search_btn.click(
                fn=search_history,
                inputs=[search_input],
                outputs=[chat_history_display, current_search_keywords]
            )
            
            # 搜索输入框回车事件
            search_input.submit(
                fn=search_history,
                inputs=[search_input],
                outputs=[chat_history_display, current_search_keywords]
            )
            
            # 聊天交互
            ask_button.click(
                fn=self.controller.ask_question,  # 先只显示用户问题
                inputs=[question_input, chatbot],
                outputs=[chatbot, chart_display, chart_info]
            ).then(
                # 禁用按钮
                fn=lambda: (gr.update(interactive=False), gr.update(interactive=False)),
                inputs=None,
                outputs=[ask_button, clear_button]
            ).then(
                fn=self.controller.process_question,  # 然后处理AI回复
                inputs=[question_input, chatbot],
                outputs=[chatbot, chart_display, chart_info],
                show_progress=True  # 显示加载进度
            ).then(
                # 重新启用按钮并清空输入框
                fn=lambda: (gr.update(interactive=True), gr.update(interactive=True), ""),
                inputs=None,
                outputs=[ask_button, clear_button, question_input]
            ).then(
                # 更新对话记录显示，根据当前搜索状态智能刷新
                fn=smart_refresh,
                inputs=[current_search_keywords],
                outputs=[chat_history_display]
            )
            
            # 按Enter键发送
            question_input.submit(
                fn=self.controller.ask_question,  # 先只显示用户问题
                inputs=[question_input, chatbot],
                outputs=[chatbot, chart_display, chart_info]
            ).then(
                # 禁用按钮
                fn=lambda: (gr.update(interactive=False), gr.update(interactive=False)),
                inputs=None,
                outputs=[ask_button, clear_button]
            ).then(
                fn=self.controller.process_question,  # 然后处理AI回复
                inputs=[question_input, chatbot],
                outputs=[chatbot, chart_display, chart_info],
                show_progress=True  # 显示加载进度
            ).then(
                # 重新启用按钮并清空输入框
                fn=lambda: (gr.update(interactive=True), gr.update(interactive=True), ""),
                inputs=None,
                outputs=[ask_button, clear_button, question_input]
            )
            
            # 清空聊天
            clear_button.click(
                fn=self.controller.clear_chat,
                inputs=[chatbot],
                outputs=[chatbot, chart_display, chart_info]
            )
            
            # 删除所有历史记录事件
            delete_all_btn.click(
                fn=self.controller.delete_all_history,
                inputs=[],
                outputs=[]
            ).then(
                # 刷新会话列表和历史记录
                fn=lambda: ([], self.get_text("all_history_deleted"), "", gr.update(visible=False)),
                inputs=[],
                outputs=[chatbot, upload_status, selected_row_info, selection_status]
            ).then(
                # 更新对话记录显示并重置按钮状态，清空搜索状态
                fn=load_all_records,
                inputs=[],
                outputs=[chat_history_display, current_search_keywords]
            )
            
            file_input.upload(
                fn=self.controller.load_dataframe,
                inputs=[file_input],
                outputs=[upload_status, data_preview]
            ).then(
                # 上传新文件后清除聊天记录和图表显示
                fn=lambda: ([], None, self.get_text("no_chart")),
                inputs=[],
                outputs=[chatbot, chart_display, chart_info]
            ).then(
                # 刷新历史记录显示，清空搜索状态
                fn=load_all_records,
                inputs=[],
                outputs=[chat_history_display, current_search_keywords]
            )
            

            
        return interface 

    def load_selected_history(self, time_question_info, chatbot):
        """
        加载选中的会话历史记录
        
        Args:
            time_question_info: 选中行的时间和问题信息
            chatbot: 当前对话框内容
            
        Returns:
            tuple: 更新后的对话框内容、状态消息、图表文件、图表信息
        """
        try:
            print(f"尝试通过时间和问题信息加载会话: {time_question_info}")
            
            if not time_question_info:
                return chatbot, self.get_text("no_row_selected"), None, self.get_text("no_chart")
            
            # 先通过时间和问题信息获取记录ID
            record_id = self.controller.db_manager.get_record_by_time_and_question(time_question_info)
            
            if not record_id:
                return chatbot, self.get_text("no_row_selected"), None, self.get_text("no_chart")
            
            # 然后获取记录ID对应的会话ID
            session_id = self.controller.get_session_id_by_record_id(record_id)
            
            if not session_id:
                return chatbot, self.get_text("no_session_selected"), None, self.get_text("no_chart")
                
            # 最后加载会话（现在返回4个值）
            return self.controller.load_history_record(session_id, chatbot)
        except Exception as e:
            print(f"加载会话历史记录时出错: {str(e)}")
            return chatbot, f"加载失败: {str(e)}", None, f"{self.get_text('load_error', str(e))}"

    def delete_selected_record(self, time_question_info):
        """
        删除选中的单条记录
        
        Args:
            time_question_info: 选中行的时间和问题信息
            
        Returns:
            str: 状态消息
        """
        try:
            print(f"尝试通过时间和问题信息删除记录: {time_question_info}")
            
            if not time_question_info:
                return self.get_text("no_row_selected")
            
            # 先通过时间和问题信息获取记录ID
            record_id = self.controller.db_manager.get_record_by_time_and_question(time_question_info)
            
            if not record_id:
                return self.get_text("no_row_selected")
            
            # 调用控制器方法删除记录
            success, message = self.controller.delete_record(record_id)
            return message
        except Exception as e:
            print(f"删除记录时出错: {str(e)}")
            return f"删除失败: {str(e)}" 