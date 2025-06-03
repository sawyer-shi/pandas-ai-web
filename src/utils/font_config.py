"""
matplotlib中文字体配置模块
确保图表能够正确显示中文字符
"""
import os
import platform
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rcParams

class FontManager:
    """字体管理器，负责配置matplotlib的中文字体支持"""
    
    def __init__(self):
        """初始化字体管理器"""
        self.system = platform.system()
        self.available_fonts = []
        self.chinese_fonts = []
        self._detect_chinese_fonts()
    
    def _detect_chinese_fonts(self):
        """检测系统中可用的中文字体"""
        try:
            # 常见的中文字体名称
            chinese_font_names = [
                'SimHei', 'Microsoft YaHei', 'SimSun', 'KaiTi', 'FangSong',
                'Microsoft JhengHei', 'PMingLiU', 'MingLiU',
                'STXihei', 'STKaiti', 'STSong', 'STFangsong',
                'PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'Heiti TC',
                'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'AR PL UMing CN',
                'Noto Sans CJK SC', 'Source Han Sans SC'
            ]
            
            # 简化的字体检测方法 - 直接使用系统默认字体
            print(f"当前系统: {self.system}")
            
            # 根据系统类型设置可能的字体
            if self.system == "Windows":
                # Windows系统常见字体
                possible_fonts = ['Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi', 'FangSong']
            elif self.system == "Darwin":  # macOS
                possible_fonts = ['PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'STXihei']
            else:  # Linux
                possible_fonts = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'AR PL UMing CN']
            
            # 尝试验证字体是否可用（简单测试）
            for font_name in possible_fonts:
                try:
                    # 创建字体属性测试
                    prop = fm.FontProperties(family=font_name)
                    if prop:
                        self.chinese_fonts.append(font_name)
                        print(f"✓ 找到字体: {font_name}")
                except Exception as e:
                    print(f"× 字体不可用: {font_name} - {e}")
                    continue
            
            # 如果没有找到任何字体，使用默认列表
            if not self.chinese_fonts:
                print("未通过测试找到字体，使用系统默认字体列表")
                self.chinese_fonts = possible_fonts
            
            print(f"最终可用的中文字体: {self.chinese_fonts}")
            
        except Exception as e:
            print(f"检测中文字体时出错: {e}")
            # 使用默认字体列表
            self._set_default_fonts()
    
    def _set_default_fonts(self):
        """设置默认中文字体列表"""
        print("使用默认字体配置")
        if self.system == "Windows":
            self.chinese_fonts = ['Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi']
        elif self.system == "Darwin":  # macOS
            self.chinese_fonts = ['PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'STXihei']
        else:  # Linux
            self.chinese_fonts = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC']
    
    def configure_matplotlib(self):
        """配置matplotlib以支持中文显示"""
        try:
            # 选择第一个可用的中文字体
            chinese_font = self._get_best_chinese_font()
            
            print(f"准备配置matplotlib字体: {chinese_font}")
            
            # 使用更安全的配置方法
            config_success = self._safe_configure_matplotlib(chinese_font)
            
            if config_success:
                print(f"✓ matplotlib中文字体配置成功，使用字体: {chinese_font}")
                return True
            else:
                print("⚠ 中文字体配置失败，使用默认配置")
                self._configure_fallback()
                return False
                
        except Exception as e:
            print(f"配置matplotlib中文字体时出错: {e}")
            self._configure_fallback()
            return False
    
    def _safe_configure_matplotlib(self, chinese_font):
        """安全的matplotlib配置方法"""
        try:
            if not chinese_font:
                return False
            
            # 基础配置
            basic_config = {
                'axes.unicode_minus': False,  # 解决负号显示问题
                'figure.dpi': 150,  # 提高图像清晰度
                'savefig.dpi': 150,
                'figure.figsize': (10, 6),
                'axes.titlesize': 14,
                'axes.labelsize': 12,
                'xtick.labelsize': 10,
                'ytick.labelsize': 10,
                'legend.fontsize': 10
            }
            
            # 字体配置
            font_config = {
                'font.family': 'sans-serif',
                'font.sans-serif': [chinese_font, 'DejaVu Sans', 'Liberation Sans', 'sans-serif']
            }
            
            # 分步骤应用配置，避免一次性配置失败
            # 1. 先应用基础配置
            for key, value in basic_config.items():
                try:
                    plt.rcParams[key] = value
                except Exception as e:
                    print(f"配置 {key} 失败: {e}")
            
            # 2. 再应用字体配置
            for key, value in font_config.items():
                try:
                    plt.rcParams[key] = value
                except Exception as e:
                    print(f"配置字体 {key} 失败: {e}")
            
            # 3. 尝试更新rcParams（可选）
            try:
                rcParams.update(basic_config)
                rcParams.update(font_config)
            except Exception as e:
                print(f"更新rcParams失败（可忽略）: {e}")
            
            print("matplotlib配置应用完成")
            return True
            
        except Exception as e:
            print(f"安全配置matplotlib时出错: {e}")
            return False
    
    def _get_best_chinese_font(self):
        """获取最佳的中文字体"""
        if not self.chinese_fonts:
            return None
        
        # 按优先级排序的字体列表
        priority_fonts = []
        if self.system == "Windows":
            priority_fonts = ['Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi']
        elif self.system == "Darwin":
            priority_fonts = ['PingFang SC', 'Hiragino Sans GB', 'Heiti SC']
        else:
            priority_fonts = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'WenQuanYi Zen Hei']
        
        # 选择第一个可用的优先字体
        for font in priority_fonts:
            if font in self.chinese_fonts:
                return font
        
        # 如果没有找到优先字体，返回第一个可用字体
        return self.chinese_fonts[0] if self.chinese_fonts else None
    
    def _configure_fallback(self):
        """配置备用字体设置"""
        try:
            # 基本配置，确保负号正常显示
            plt.rcParams['axes.unicode_minus'] = False
            plt.rcParams['figure.dpi'] = 150
            plt.rcParams['savefig.dpi'] = 150
            
            print("已应用备用字体配置")
        except Exception as e:
            print(f"配置备用字体时出错: {e}")
    
    def get_plot_kwargs(self):
        """获取绘图参数字典"""
        chinese_font = self._get_best_chinese_font()
        
        if chinese_font:
            return {
                "font.family": "sans-serif",
                "font.sans-serif": [chinese_font, 'DejaVu Sans', 'Liberation Sans', 'sans-serif'],
                "axes.unicode_minus": False,
                "figure.dpi": 150,
                "savefig.dpi": 150,
                "figure.figsize": (10, 6),
                "axes.titlesize": 14,
                "axes.labelsize": 12,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
                "legend.fontsize": 10
            }
        else:
            return {
                "axes.unicode_minus": False,
                "figure.dpi": 150,
                "savefig.dpi": 150
            }
    
    def test_chinese_display(self):
        """测试中文显示效果"""
        try:
            import numpy as np
            
            # 创建测试图表
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # 测试数据
            x = ['产品A', '产品B', '产品C', '产品D']
            y = [20, 35, 30, 25]
            
            # 绘制柱状图
            bars = ax.bar(x, y, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
            
            # 设置标题和标签
            ax.set_title('中文字体测试图表', fontsize=16, fontweight='bold')
            ax.set_xlabel('产品类别', fontsize=12)
            ax.set_ylabel('销售数量', fontsize=12)
            
            # 在柱子上添加数值标签
            for bar, value in zip(bars, y):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{value}', ha='center', va='bottom')
            
            # 保存测试图表
            test_file = 'test_chinese_font.png'
            plt.savefig(test_file, dpi=150, bbox_inches='tight')
            plt.close()
            
            if os.path.exists(test_file):
                print(f"✓ 中文字体测试成功，测试图片保存为: {test_file}")
                return True
            else:
                print("✗ 中文字体测试失败")
                return False
                
        except Exception as e:
            print(f"测试中文字体时出错: {e}")
            return False

# 创建全局字体管理器实例
font_manager = FontManager()

def configure_chinese_fonts():
    """配置中文字体的便捷函数"""
    return font_manager.configure_matplotlib()

def get_chinese_plot_kwargs():
    """获取中文绘图参数的便捷函数"""
    return font_manager.get_plot_kwargs() 