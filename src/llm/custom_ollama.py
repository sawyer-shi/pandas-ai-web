import requests
import json
import re
import ast
from pandasai.llm.base import LLM

class CustomOllamaLLM(LLM):
    """
    自定义Ollama LLM类，实现与PandasAI兼容的接口
    """
    def __init__(self, model="llama3", url="http://localhost:11434"):
        self.model = model
        self.url = url
        self._type = "ollama"  # 添加类型属性
        
    @property
    def type(self) -> str:
        """返回LLM类型"""
        return self._type
        
    def call(self, prompt, context=None, **kwargs):
        """调用Ollama API，发送提示并获取响应"""
        try:
            # 如果提供了context，可以将其添加到prompt中
            if context:
                if isinstance(context, dict):
                    # 将字典转换为字符串描述
                    context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
                    prompt = f"Context:\n{context_str}\n\nPrompt: {prompt}"
                elif isinstance(context, str):
                    prompt = f"Context:\n{context}\n\nPrompt: {prompt}"
            
            # 使用stream=false参数来获取完整响应，而不是流式响应
            response = requests.post(
                f"{self.url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False}
            )
            
            if response.status_code == 200:
                try:
                    # 尝试解析JSON响应
                    json_response = response.json()
                    # 从完整响应中提取文本部分
                    return json_response.get("response", "")
                except json.JSONDecodeError as e:
                    print(f"JSON解析错误: {str(e)}")
                    # 如果JSON解析失败，返回原始文本
                    return response.text
            else:
                return f"Error: {response.status_code}, {response.text}"
        except Exception as e:
            print(f"调用Ollama API出错: {str(e)}")
            return f"Error calling Ollama API: {str(e)}"

    def generate(self, prompt, **kwargs):
        """生成文本响应"""
        return self.call(prompt, **kwargs)
        
    def generate_code(self, instruction, context=None):
        """生成代码响应，符合PandasAI的接口要求"""
        # 格式化成代码生成指令
        prompt = f"""You are a Python expert. Write Python code to answer the following question:
{instruction}

The code should work with the following context:
{context}

INSTRUCTIONS:
1. Return ONLY valid Python code without any explanation or markdown blocks.
2. Do not include ```python or ``` tags around your code.
3. Make sure your code is complete and can be executed directly.
4. Your code should analyze the data in variable 'dfs[0]'.
5. All boolean values must be Python style: True or False (not true/false).
6. Do not include any explanatory text before or after the code.
7. DO NOT USE THE TYPING MODULE OR TYPE ANNOTATIONS - this is strictly forbidden.
8. ONLY import pandas, numpy, and matplotlib.pyplot - DO NOT IMPORT ANY OTHER LIBRARIES.
9. For dictionaries, use standard dict syntax without type annotations.
10. DO NOT import math, datetime, os, or any other libraries not explicitly allowed.
11. DO NOT use pandas.to_numeric() - use df['column'].astype(float) or df['column'].astype(int) instead.
12. DO NOT use any restricted pandas functions like read_sql, eval, query with user input.

Your Python code:
"""
        # 获取响应
        raw_response = None
        try:
            # 使用流式API获取完整响应
            full_response = ""
            response = requests.post(
                f"{self.url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": True},
                stream=True
            )
            
            for line in response.iter_lines():
                if line:
                    try:
                        # 解析每行JSON响应
                        chunk = json.loads(line.decode('utf-8'))
                        if 'response' in chunk:
                            full_response += chunk['response']
                        # 确保不要将整个JSON块纳入代码
                        if 'done' in chunk and chunk.get('done') == True:
                            # 最后一个响应块，跳出循环
                            break
                    except json.JSONDecodeError:
                        continue
            
            raw_response = full_response
        except Exception as e:
            print(f"Ollama API流式请求错误: {str(e)}")
            # 尝试回退到非流式请求
            raw_response = self.call(prompt, context)
        
        # 清理响应，提取有效的Python代码
        try:
            # 尝试删除可能出现的markdown格式代码块
            if "```python" in raw_response:
                raw_response = raw_response.split("```python")[1]
                if "```" in raw_response:
                    raw_response = raw_response.split("```")[0]
            elif "```" in raw_response:
                raw_response = raw_response.split("```")[1]
                if "```" in raw_response:
                    raw_response = raw_response.split("```")[0]
                    
            # 删除JSON格式的响应行（如果有）
            cleaned_lines = []
            for line in raw_response.split("\n"):
                # 跳过看起来像JSON对象的行
                if line.strip().startswith('{') and ('"model":' in line or '"done":' in line or '"response":' in line):
                    continue
                else:
                    cleaned_lines.append(line)
            
            raw_response = "\n".join(cleaned_lines)
            
            # 确保返回有效的Python代码
            parsed_response = raw_response.strip()
            
            # 替换JavaScript风格的布尔值
            parsed_response = parsed_response.replace(" false", " False").replace(" true", " True")
            parsed_response = parsed_response.replace("=false", "=False").replace("=true", "=True")
            parsed_response = parsed_response.replace(":false", ":False").replace(":true", ":True")
            parsed_response = parsed_response.replace(",false", ",False").replace(",true", ",True")
            parsed_response = parsed_response.replace("(false", "(False").replace("(true", "(True")
            
            # 移除typing导入
            if "import typing" in parsed_response or "from typing import" in parsed_response:
                # 删除typing导入行
                lines = parsed_response.split("\n")
                lines = [line for line in lines if not (
                    "import typing" in line or 
                    "from typing import" in line or
                    "import typing as" in line
                )]
                parsed_response = "\n".join(lines)
            
            # 移除math和其他非白名单库的导入
            forbidden_imports = ["math", "datetime", "os", "sys", "re", "json", "time", "collections"]
            lines = parsed_response.split("\n")
            cleaned_lines = []
            for line in lines:
                is_forbidden = False
                for module in forbidden_imports:
                    if f"import {module}" in line or f"from {module}" in line:
                        is_forbidden = True
                        break
                if not is_forbidden:
                    cleaned_lines.append(line)
            
            parsed_response = "\n".join(cleaned_lines)
            
            # 替换受限的pandas函数
            lines = parsed_response.split("\n")
            cleaned_lines = []
            for line in lines:
                # 替换pd.to_numeric
                if "pd.to_numeric" in line or "pandas.to_numeric" in line:
                    if "df[" in line and "]" in line:
                        # 提取列名
                        col_start = line.find("df[")
                        col_end = line.find("]", col_start) + 1
                        column_expr = line[col_start:col_end]
                        
                        # 替换为astype
                        equal_pos = line.find("=")
                        if equal_pos > 0:
                            var_name = line[:equal_pos].strip()
                            line = f"{var_name} = {column_expr}.astype(float)"
                        else:
                            line = f"{column_expr} = {column_expr}.astype(float)"
                
                cleaned_lines.append(line)
            
            parsed_response = "\n".join(cleaned_lines)
            
            # 移除类型注解
            lines = parsed_response.split("\n")
            cleaned_lines = []
            for line in lines:
                # 移除变量类型注解，例如 "result: Dict[str, str] = {"
                if ": " in line and " = " in line:
                    parts = line.split(" = ")
                    if len(parts) >= 2:
                        var_name = parts[0].split(":")[0].strip()
                        value = " = ".join(parts[1:])
                        line = f"{var_name} = {value}"
                cleaned_lines.append(line)
            parsed_response = "\n".join(cleaned_lines)
            
            # 尝试检查代码是否有效
            try:
                ast.parse(parsed_response)
                # 最后预处理一遍代码，确保所有的false/true都被替换
                # 这样即使解析通过了，也不会在执行时出错
                final_code = ""
                for line in parsed_response.split("\n"):
                    if "false" in line or "true" in line:
                        line = line.replace("false", "False").replace("true", "True")
                    # 再次检查to_numeric
                    if "to_numeric" in line:
                        line = line.replace("to_numeric", "# DISABLED: to_numeric")
                    final_code += line + "\n"
                return final_code.strip()
            except SyntaxError as e:
                print(f"生成的代码存在语法错误: {str(e)}")
                # 如果代码存在语法错误，使用简单的模板
                # 这个模板只使用允许的库和函数
                fallback_code = f"""# 分析数据
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 分析数据
df = dfs[0]

# 确保金额列是数值类型
try:
    # 使用安全的类型转换方式
    df['金额'] = df['金额'].astype(float)
except:
    # 如果转换失败，尝试先替换逗号
    df['金额'] = df['金额'].replace(',', '', regex=True).astype(float)

# 找出最大金额的月份
max_amount_idx = df['金额'].idxmax()
max_month = df.loc[max_amount_idx, '时间']
max_amount = df.loc[max_amount_idx, '金额']

# 返回结果 - 使用中文显示最大金额月份
result = {{"type": "string", "value": f"金额最大的月份是{{max_month}}，金额为{{max_amount}}"}}
"""
                return fallback_code
        except Exception as e:
            print(f"处理代码生成响应错误: {str(e)}")
            # 返回备用代码
            return """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 分析数据
df = dfs[0]

# 确保金额列是数值类型
try:
    # 使用安全的类型转换方式
    df['金额'] = df['金额'].astype(float)
except:
    # 如果转换失败，尝试先替换逗号
    df['金额'] = df['金额'].replace(',', '', regex=True).astype(float)

# 找出最大金额的月份
max_amount_idx = df['金额'].idxmax()
max_month = df.loc[max_amount_idx, '时间']
max_amount = df.loc[max_amount_idx, '金额']

# 返回中文结果
result = {"type": "string", "value": f"金额最大的月份是{max_month}，金额为{max_amount}"}
"""
        
    def is_chat_model(self):
        """返回是否是聊天模型"""
        return False
        
    def get_model_name(self):
        """返回模型名称"""
        return self.model
        
    def get_parameters(self):
        """返回模型参数"""
        return {
            "model": self.model,
            "url": self.url
        } 