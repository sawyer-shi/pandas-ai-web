import os
import matplotlib
import matplotlib.font_manager as fm

def setup_chinese_fonts():
    """Configure matplotlib fonts to properly display Chinese characters.
    
    This function detects the operating system and available fonts, then
    configures matplotlib to use appropriate fonts for Chinese characters.
    """
    # Check operating system
    system_platform = os.name
    
    # Default font settings (will be adjusted based on system)
    font_names = ['SimHei', 'Microsoft YaHei', 'SimSun', 'WenQuanYi Micro Hei', 'Arial Unicode MS']
    font_found = False
    
    # Find available fonts in the system
    system_fonts = fm.findSystemFonts()
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    print(f"Detected {len(system_fonts)} system fonts")
    
    # Try common Chinese fonts
    for font_name in font_names:
        if font_name.lower() in [f.lower() for f in available_fonts]:
            print(f"Using Chinese font: {font_name}")
            matplotlib.rcParams['font.family'] = font_name
            font_found = True
            break
    
    # If no Chinese fonts were found, use OS-specific defaults
    if not font_found:
        if system_platform == 'nt':  # Windows
            # On Windows, default to Microsoft YaHei
            matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
            print("On Windows, defaulting to Microsoft YaHei font")
        elif system_platform == 'posix':  # Linux/Mac
            # On Linux/Mac, try to use system fonts
            if 'WenQuanYi' in ' '.join(available_fonts):
                matplotlib.rcParams['font.family'] = 'WenQuanYi Micro Hei'
                print("On Linux, using WenQuanYi font")
            else:
                matplotlib.rcParams['sans-serif'] = ['Heiti TC', 'Adobe Heiti Std', 'Adobe Fan Heiti Std']
                print("On Mac/Linux, using default Chinese fonts")
    
    # Fix negative sign display issue
    matplotlib.rcParams['axes.unicode_minus'] = False
    
    # Improve image quality with higher DPI
    matplotlib.rcParams['figure.dpi'] = 150
    
    print("Chinese font configuration completed")
    
    return {
        "font.family": matplotlib.rcParams.get('font.family', 'SimHei'),
        "font.sans-serif": matplotlib.rcParams.get('font.sans-serif', ['SimHei', 'Microsoft YaHei']),
        "axes.unicode_minus": False,
        "figure.dpi": 150
    } 