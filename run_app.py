"""
更强大的应用程序启动脚本，增加了错误处理和日志输出
"""
import os
import sys
import logging
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app_debug.log", encoding="utf-8"),  # 使用UTF-8编码避免中文问题
        logging.StreamHandler(sys.stdout)
    ]
)

def check_environment():
    """检查环境并清理临时文件"""
    logging.info("检查运行环境...")
    
    # 确保必要的目录存在
    required_dirs = ["charts", "exports/charts", "avatar", "config", "exports", "src/utils"]
    for directory in required_dirs:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"已确保目录存在: {directory}")
    
    # 检查数据库文件
    db_file = "chat_history.db"
    if not os.path.exists(db_file):
        logging.info(f"创建新的数据库文件: {db_file}")
    else:
        logging.info(f"已有数据库文件: {db_file}")
    
    # 检查示例数据
    example_data = "example_data.csv"
    if os.path.exists(example_data):
        logging.info(f"示例数据文件已存在: {example_data}")
    else:
        logging.warning(f"示例数据文件不存在: {example_data}")
    
    # 检查配置文件
    config_file = "config/config.ini"
    if os.path.exists(config_file):
        logging.info(f"配置文件已存在: {config_file}")
    else:
        logging.warning(f"配置文件不存在: {config_file}")
    
    logging.info("环境检查完成")

def apply_patches():
    """应用必要的补丁"""
    logging.info("应用补丁...")
    
    try:
        # 导入并应用PandasAI补丁
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from src.utils.pandasai_patch import apply_patches as apply_pandasai_patches
        apply_pandasai_patches()
        logging.info("补丁应用完成")
        return True
    except Exception as e:
        logging.error(f"应用补丁失败: {str(e)}")
        return False

def run_application():
    """运行应用程序主体"""
    try:
        # **优先配置matplotlib中文字体支持 - 必须在导入其他模块之前**
        try:
            from src.utils.font_config import configure_chinese_fonts
            font_success = configure_chinese_fonts()
            if font_success:
                logging.info("✓ matplotlib中文字体配置成功")
                print("✓ matplotlib中文字体配置成功")
            else:
                logging.warning("⚠ matplotlib中文字体配置失败，将使用默认字体")
                print("⚠ matplotlib中文字体配置失败，将使用默认字体")
        except Exception as e:
            logging.error(f"⚠ 配置中文字体时出错: {e}")
            print(f"⚠ 配置中文字体时出错: {e}")
        
        # 然后再导入其他模块（避免matplotlib配置被覆盖）
        from src.app_controller import AppController
        from src.ui.app_ui import AppUI
        
        logging.info("正在初始化应用控制器...")
        controller = AppController()
        
        logging.info("正在创建UI应用...")
        app_ui = AppUI(controller)
        
        logging.info("正在创建Gradio界面...")
        interface = app_ui.create_interface()
        
        logging.info("启动应用界面 (使用本地URL)...")
        print("\n" + "="*50)
        print("应用程序已启动！")
        print("请在浏览器中访问以下地址:")
        print("http://127.0.0.1:7860")
        print("="*50 + "\n")
        
        # 启动应用 - 使用share=False避免下载frpc
        interface.launch(share=False)
        
    except ImportError as e:
        logging.error(f"导入错误: {str(e)}")
        print(f"错误: 无法导入必要的模块。请确保已安装所有依赖: {str(e)}")
        print("提示: 运行 'pip install -r requirements.txt' 安装所有依赖")
        return False
    except Exception as e:
        logging.error(f"应用程序启动错误: {str(e)}")
        print(f"错误: 启动应用程序时出错: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("正在启动 Pandas AI Web 应用...")
    
    try:
        # 检查环境
        check_environment()
        
        # 应用补丁
        if not apply_patches():
            print("警告: 部分补丁应用失败，应用程序可能无法正常工作")
        
        # 运行应用
        success = run_application()
        
        if not success:
            print("\n应用程序启动失败。请查看 app_debug.log 文件了解详细信息。")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n用户中断，应用程序已停止")
    except Exception as e:
        logging.error(f"未处理的异常: {str(e)}")
        print(f"\n发生未知错误: {str(e)}")
        print("详细信息已写入 app_debug.log 文件")
        sys.exit(1) 