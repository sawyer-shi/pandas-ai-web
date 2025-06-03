import base64
import os
import shutil
from typing import Optional

def image_to_base64(image_path: str) -> Optional[str]:
    """
    将图片文件转换为Base64编码
    
    Args:
        image_path: 图片文件路径
        
    Returns:
        Base64编码的字符串，如果失败则返回None
    """
    try:
        if not os.path.exists(image_path):
            return None
            
        with open(image_path, 'rb') as img_file:
            # 读取图片文件
            img_data = img_file.read()
            
            # 转换为Base64编码
            base64_data = base64.b64encode(img_data).decode('utf-8')
            
            # 获取文件扩展名以确定MIME类型
            ext = os.path.splitext(image_path)[1].lower()
            mime_type = get_mime_type(ext)
            
            # 返回完整的data URL
            return f"data:{mime_type};base64,{base64_data}"
            
    except Exception as e:
        print(f"图片转Base64失败: {str(e)}")
        return None

def get_mime_type(extension: str) -> str:
    """
    根据文件扩展名获取MIME类型
    
    Args:
        extension: 文件扩展名（包含点号）
        
    Returns:
        MIME类型字符串
    """
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp'
    }
    
    return mime_types.get(extension.lower(), 'image/png')

def copy_to_public_dir(image_path: str) -> Optional[str]:
    """
    将图片复制到public目录以便通过HTTP访问
    
    Args:
        image_path: 原始图片路径
        
    Returns:
        public目录中的相对路径，如果失败则返回None
    """
    try:
        if not os.path.exists(image_path):
            return None
            
        # 创建public目录
        public_dir = os.path.join(os.getcwd(), "public", "images")
        os.makedirs(public_dir, exist_ok=True)
        
        # 生成唯一的文件名
        filename = os.path.basename(image_path)
        public_path = os.path.join(public_dir, filename)
        
        # 复制文件
        shutil.copy2(image_path, public_path)
        
        # 返回相对路径
        return f"/public/images/{filename}"
        
    except Exception as e:
        print(f"复制图片到public目录失败: {str(e)}")
        return None

def create_image_html(image_path: str, alt_text: str = "Chart", max_width: str = "100%") -> str:
    """
    创建包含图片的HTML代码，使用多种fallback方案
    
    Args:
        image_path: 图片文件路径
        alt_text: 图片替代文本
        max_width: 图片最大宽度
        
    Returns:
        HTML代码字符串
    """
    if not os.path.exists(image_path):
        return f'<p style="color: red;">图片文件不存在: {image_path}</p>'
    
    # 方案1: 尝试Gradio file service
    absolute_path = os.path.abspath(image_path)
    gradio_file_url = f"/file={absolute_path}"
    
    # 方案2: 复制到public目录
    public_url = copy_to_public_dir(image_path)
    
    # 方案3: Base64编码
    base64_data = image_to_base64(image_path)
    
    # 构建HTML，按优先级使用不同方案
    html_parts = []
    
    if public_url:
        html_parts.append(f'<img src="{public_url}" alt="{alt_text}" style="max-width:{max_width}; height:auto; margin-top:10px;" />')
    
    if base64_data:
        html_parts.append(f'<img src="{base64_data}" alt="{alt_text}" style="max-width:{max_width}; height:auto; margin-top:10px;" />')
    
    # Gradio file service作为fallback
    html_parts.append(f'<img src="{gradio_file_url}" alt="{alt_text}" style="max-width:{max_width}; height:auto; margin-top:10px;" />')
    
    # 创建带有多个fallback的HTML
    if len(html_parts) > 1:
        return f'''
        <div class="chart-container">
            {html_parts[0]}
            <script>
                // 如果图片加载失败，尝试其他方案
                document.querySelectorAll('.chart-container img').forEach((img, index) => {{
                    img.onerror = function() {{
                        if (index < {len(html_parts) - 1}) {{
                            this.style.display = 'none';
                            // 尝试下一个图片
                        }}
                    }};
                }});
            </script>
        </div>
        '''
    else:
        return html_parts[0]

def create_markdown_image(image_path: str, alt_text: str = "Chart") -> str:
    """
    创建Markdown格式的图片链接（适用于Gradio）
    
    Args:
        image_path: 图片文件路径
        alt_text: 图片替代文本
        
    Returns:
        Markdown格式的图片字符串
    """
    if not os.path.exists(image_path):
        return f"**图片文件不存在**: {image_path}"
    
    # 尝试复制到public目录
    public_url = copy_to_public_dir(image_path)
    if public_url:
        return f"![{alt_text}]({public_url})"
    
    # Fallback: 使用绝对路径
    absolute_path = os.path.abspath(image_path).replace('\\', '/')
    return f"![{alt_text}](file://{absolute_path})" 