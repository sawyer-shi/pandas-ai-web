import os
import sys
import logging
from .app_controller import AppController
from .ui.app_ui import AppUI

def main():
    """应用程序主入口"""
    # 确保必要的目录存在
    os.makedirs("charts", exist_ok=True)
    os.makedirs("exports/charts", exist_ok=True)
    os.makedirs("avatar", exist_ok=True)
    os.makedirs("config", exist_ok=True)
    
    # 配置matplotlib中文字体支持
    try:
        from .utils.font_config import configure_chinese_fonts
        font_success = configure_chinese_fonts()
        if font_success:
            print("✓ matplotlib中文字体配置成功")
        else:
            print("⚠ matplotlib中文字体配置失败，将使用默认字体")
    except Exception as e:
        print(f"⚠ 配置中文字体时出错: {e}")
    
    # 应用PandasAI补丁，修复prompt_id问题
    try:
        from .utils.pandasai_patch import apply_patches
        apply_patches()
        print("✓ PandasAI补丁应用成功")
    except Exception as e:
        print(f"⚠ 应用PandasAI补丁失败: {e}")
        print("应用程序可能无法正常工作")
    
    # 创建应用控制器
    controller = AppController()
    
    # 创建UI应用
    app_ui = AppUI(controller)
    
    # 创建Gradio界面
    interface = app_ui.create_interface()
    
    # 从环境变量读取配置参数
    server_name = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    share = os.getenv("GRADIO_SHARE", "true").lower() == "true"
    
    print(f"正在启动服务器...")
    print(f"服务器地址: http://{server_name}:{server_port}")
    if share:
        print("将创建公共分享链接...")
    else:
        print("仅在本地访问")
    
    # 启动应用
    interface.launch(
        server_name=server_name,
        server_port=server_port,
        share=share
    )

if __name__ == "__main__":
    main() 