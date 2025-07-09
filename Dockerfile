# 使用Python 3.11官方镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    fonts-wqy-zenhei \
    fonts-wqy-microhei \
    fonts-liberation \
    libfontconfig1 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY . .

# 创建必要的目录
RUN mkdir -p charts exports/charts avatar config

# 设置环境变量
ENV PYTHONPATH=/app
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860
ENV GRADIO_SHARE=false

# 暴露端口
EXPOSE 7860

# 启动命令
CMD ["python", "main.py"] 