"""
应用启动文件，使用share=False参数避免Gradio下载frpc文件
"""
from src.app import main

if __name__ == "__main__":
    # 重定义main函数
    import sys
    from src.app_controller import AppController
    from src.ui.app_ui import AppUI
    import os
    
    def patched_main():
        """修补后的主函数，禁用share选项"""
        # 确保必要的目录存在
        os.makedirs("charts", exist_ok=True)
        os.makedirs("exports/charts", exist_ok=True)
        os.makedirs("avatar", exist_ok=True)
        os.makedirs("config", exist_ok=True)
        
        # 创建应用控制器
        controller = AppController()
        
        # 创建UI应用
        app_ui = AppUI(controller)
        
        # 创建Gradio界面
        interface = app_ui.create_interface()
        
        # 启动应用 - 使用share=False避免下载frpc
        print("使用本地URL启动应用（不创建共享链接）...")
        interface.launch(share=False)
    
    # 替换main函数并运行
    patched_main() 