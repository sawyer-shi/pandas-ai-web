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
            /* 主标题样式 */
            .main-title {
                font-size: 2.5em !important;
                font-weight: bold !important;
                text-align: center !important;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                background-clip: text !important;
                margin: 20px 0 30px 0 !important;
                padding: 20px !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1) !important;
                line-height: 1.2 !important;
                border-bottom: 3px solid #f0f0f0 !important;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
                border-radius: 10px !important;
                background-color: rgba(255,255,255,0.9) !important;
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
                max-height: 400px;
                overflow: hidden;
                margin-top: 10px;
                display: flex;
                flex-direction: column;
            }
            
            /* 历史记录表格样式 */
            .history-table {
                max-height: 280px;
                overflow: hidden;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                margin-bottom: 10px;
            }
            
            .history-table .table-wrap {
                max-height: 280px;
                overflow-y: auto;
                font-size: 0.9em;
            }
            
            .history-table table {
                width: 100%;
                border-collapse: collapse;
            }
            
            .history-table th {
                background: #f8f9fa;
                position: sticky;
                top: 0;
                z-index: 10;
                padding: 8px 6px;
                border-bottom: 1px solid #dee2e6;
                font-size: 0.85em;
                font-weight: 600;
                text-align: left;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            .history-table td {
                padding: 6px;
                border-bottom: 1px solid #f0f0f0;
                font-size: 0.85em;
                max-width: 200px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                cursor: pointer;
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
                            scale=8
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
                                
                                chat_history_display = gr.Dataframe(
                                    headers=[
                                        self.get_text("history_time"), 
                                        self.get_text("history_session"),
                                        self.get_text("history_question"), 
                                        self.get_text("history_answer")
                                    ],
                                    col_count=(4, "fixed"),
                                    interactive=True,
                                    wrap=False,
                                    column_widths=["20%", "25%", "25%", "30%"],
                                    elem_classes="history-table",
                                    row_count=6
                                )
                                
                                # 按钮组
                                with gr.Row(elem_classes="history-buttons"):
                                    refresh_history_btn = gr.Button(
                                        self.get_text("refresh_history"),
                                        variant="secondary",
                                        size="sm"
                                    )
                                    load_history_btn = gr.Button(
                                        self.get_text("load_history_button"),
                                        variant="primary",
                                        size="sm",
                                        interactive=False  # 初始禁用
                                    )
                                    delete_record_btn = gr.Button(
                                        self.get_text("delete_record_button"),
                                        variant="secondary",
                                        size="sm",
                                        interactive=False  # 初始禁用
                                    )
                                    delete_all_btn = gr.Button(
                                        self.get_text("delete_all_button"),
                                        variant="secondary", 
                                        size="sm"
                                    )
                                
                                # 存储当前选中的行信息（隐藏元素）
                                selected_row_info = gr.Textbox(visible=False, value="")
            
            # 初始化对话记录显示
            chat_history_display.value = self.controller.display_chat_history()
            
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
                    gr.update(label=self.get_text("question_input")),     # question_input
                    gr.update(placeholder=self.get_text("question_placeholder")), # question_input placeholder
                    gr.update(value=self.get_text("ask_button")),         # ask_button
                    gr.update(value=self.get_text("clear_button")),       # clear_button
                    gr.update(label=self.get_text("language")),           # language_choice
                    gr.update(value=f"**{self.get_text('generated_chart')}**"), # chart_display_header
                    gr.update(label=self.get_text("generated_chart")),    # chart_display
                    gr.update(label=self.get_text("chart_info"), value=self.get_text("no_chart")),         # chart_info - 同时更新label和value
                    gr.update(value=f"**{self.get_text('chat_history')}**"), # chat_history_header 
                    gr.update(headers=[
                        self.get_text("history_time"), 
                        self.get_text("history_session"),
                        self.get_text("history_question"), 
                        self.get_text("history_answer")
                    ]),                                                  # chat_history_display
                    gr.update(value=self.get_text("refresh_history")),   # refresh_history_btn
                    gr.update(value=self.get_text("load_history_button")),   # load_history_btn
                    gr.update(value=self.get_text("delete_record_button")),   # delete_record_btn
                    gr.update(value=self.get_text("delete_all_button")),   # delete_all_btn
                    gr.update(label=self.get_text("chat_history"))         # TabItem - 对话记录
                )
            
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
                    question_input,
                    ask_button,
                    clear_button,
                    language_choice,
                    chart_display_header,
                    chart_display,
                    chart_info,
                    chat_history_header,
                    chat_history_display,
                    refresh_history_btn,
                    load_history_btn,
                    delete_record_btn,
                    delete_all_btn,
                    chat_tab
                ]
            ).then(
                fn=register_new_upload_event,
                inputs=[file_input],
                outputs=None
            ).then(
                # 语言切换后刷新历史数据以使用新的语言提示
                fn=self.controller.refresh_current_history,
                inputs=[],
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
                    gr.update(interactive=False), 
                    gr.update(interactive=False),
                    gr.update(headers=[
                        self.get_text("history_time"), 
                        self.get_text("history_session"),
                        self.get_text("history_question"), 
                        self.get_text("history_answer")
                    ])
                )

            # 刷新对话记录
            refresh_history_btn.click(
                fn=self.controller.refresh_current_history,
                inputs=[],
                outputs=[chat_history_display]
            ).then(
                # 刷新后重置选择状态并更新表头
                fn=reset_selection_and_update_headers,
                inputs=[],
                outputs=[selected_row_info, selection_status, load_history_btn, delete_record_btn, chat_history_display]
            )
            
            # 优化行选择处理
            def handle_table_selection(evt: gr.SelectData):
                """处理表格行选择事件"""
                try:
                    if evt is None:
                        return "", gr.update(visible=False), gr.update(interactive=False), gr.update(interactive=False)
                    
                    print(f"表格选择事件: {evt}")
                    
                    # 获取选中的行索引
                    row_index = evt.index[0] if isinstance(evt.index, (list, tuple)) else evt.index
                    
                    # 获取当前显示的历史记录
                    current_history = self.controller.refresh_current_history()
                    
                    if current_history and 0 <= row_index < len(current_history):
                        # 获取选中行的数据
                        selected_row = current_history[row_index]
                        
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
                            gr.update(interactive=True),
                            gr.update(interactive=True)
                        )
                    else:
                        print(f"无效的行索引: {row_index}")
                        return "", gr.update(visible=False), gr.update(interactive=False), gr.update(interactive=False)
                        
                except Exception as e:
                    print(f"处理表格选择时出错: {str(e)}")
                    return "", gr.update(visible=False), gr.update(interactive=False), gr.update(interactive=False)
            
            # 选择对话记录行
            chat_history_display.select(
                fn=handle_table_selection,
                outputs=[selected_row_info, selection_status, load_history_btn, delete_record_btn]
            )
            
            # 加载选中的对话记录
            def load_selected_with_feedback(row_info, chatbot):
                """加载选中记录并提供反馈"""
                if not row_info:
                    return chatbot, self.get_text("no_row_selected"), "", gr.update(visible=False), None, self.get_text("no_chart")
                
                # 调用原有的加载方法（现在返回4个值）
                new_chatbot, status, chart_file, chart_info = self.load_selected_history(row_info, chatbot)
                
                # 成功加载后清除选择状态
                if "成功" in status or "successfully" in status.lower():
                    return new_chatbot, status, "", gr.update(visible=False), chart_file, chart_info
                else:
                    return new_chatbot, status, row_info, gr.update(visible=True), chart_file, chart_info
            
            load_history_btn.click(
                fn=load_selected_with_feedback,
                inputs=[selected_row_info, chatbot],
                outputs=[chatbot, upload_status, selected_row_info, selection_status, chart_display, chart_info]
            ).then(
                # 加载后禁用按钮
                fn=lambda: (gr.update(interactive=False), gr.update(interactive=False)),
                inputs=[],
                outputs=[load_history_btn, delete_record_btn]
            )
            
            # 删除选中的单条记录
            def delete_selected_with_feedback(row_info):
                """删除选中记录并提供反馈"""
                if not row_info:
                    return self.get_text("no_row_selected"), row_info, gr.update(visible=True)
                
                # 调用原有的删除方法
                status = self.delete_selected_record(row_info)
                
                # 成功删除后清除选择状态
                if "成功" in status or "successfully" in status.lower() or "删除" in status:
                    return status, "", gr.update(visible=False)
                else:
                    return status, row_info, gr.update(visible=True)
            
            delete_record_btn.click(
                fn=delete_selected_with_feedback,
                inputs=[selected_row_info],
                outputs=[upload_status, selected_row_info, selection_status]
            ).then(
                # 删除后刷新记录显示并重置按钮状态
                fn=self.controller.refresh_current_history,
                inputs=[],
                outputs=[chat_history_display]
            ).then(
                # 重置按钮状态
                fn=lambda: (gr.update(interactive=False), gr.update(interactive=False)),
                inputs=[],
                outputs=[load_history_btn, delete_record_btn]
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
                # 更新对话记录显示
                fn=self.controller.refresh_current_history,
                inputs=[],
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
                # 更新对话记录显示并重置按钮状态
                fn=self.controller.refresh_current_history,
                inputs=[],
                outputs=[chat_history_display]
            ).then(
                # 重置按钮状态
                fn=lambda: (gr.update(interactive=False), gr.update(interactive=False)),
                inputs=[],
                outputs=[load_history_btn, delete_record_btn]
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
                # 刷新历史记录显示
                fn=self.controller.refresh_current_history,
                inputs=[],
                outputs=[chat_history_display]
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