# Pandas AI Web - 智能数据对话助手

[English](#english) | [中文](#中文)

---

## 中文

### 项目简介

Pandas AI Web 是一个基于 PandasAI 和 Gradio 开发的智能数据对话应用。只需上传 CSV 或 Excel 文件，选择 AI 模型，即可用自然语言与您的数据进行对话，获取数据洞察和可视化图表。

### 主要特性

- 🌐 双语界面（中文/English）
- 🤖 多种 AI 模型支持：OpenAI、Azure OpenAI、本地 Ollama 模型
- 📊 支持 CSV、XLS、XLSX 文件格式
- 🔍 自动编码识别（UTF-8、GBK 等）
- 📈 智能图表生成（饼图、柱状图、折线图、雷达图等）
- 🎨 中文字符完美支持
- 💬 对话历史记录存储
- 🔄 会话管理与加载
- 🐳 Docker 容器化部署
- 📱 响应式界面设计

### 快速开始

#### 🐳 Docker 部署（推荐）

1. 克隆仓库：
   ```bash
   git clone https://github.com/sawyer-shi/pandas-ai-web.git
   cd pandas-ai-web
   ```

2. 配置环境变量：
   ```bash
   cp env.docker-example .env
   # 编辑 .env 文件，配置您的 API 密钥
   ```

3. 启动服务：
   ```bash
   docker-compose up -d
   ```

4. 访问应用：
   打开浏览器访问 `http://localhost:7860`

#### 🐍 Python 本地部署

1. 创建虚拟环境：
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量：
   ```bash
   cp env.example .env
   # 编辑 .env 文件
   ```

4. 启动应用：
   ```bash
   python main.py
   ```

### 使用方法

1. 选择 AI 模型（OpenAI、Azure OpenAI 或 Ollama）
2. 上传 CSV 或 Excel 数据文件
3. 在对话框中输入您的问题
4. 查看 AI 生成的答案和图表
5. 使用历史记录功能回顾之前的对话

### 支持的问题类型

- 数据统计分析："这个数据集有多少行？"
- 数据可视化："用柱状图展示销售数据"
- 趋势分析："销售额的变化趋势如何？"
- 数据筛选："显示销售额大于1000的记录"
- 对比分析："比较不同地区的销售情况"

### 配置说明

环境变量配置（`.env` 文件）：
```env
# 服务器配置
GRADIO_SERVER_PORT=7860
GRADIO_SHARE=false

# OpenAI 配置
OPENAI_API_KEY=your_openai_key
OPENAI_BASE_URL=https://api.openai.com/v1

# Azure OpenAI 配置
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_API_VERSION=2024-02-01

# Ollama 配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# 默认设置
DEFAULT_LLM_TYPE=Ollama
```

### 开发贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 许可证

本项目使用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

---

## English

### Project Introduction

Pandas AI Web is an intelligent data conversation application built on PandasAI and Gradio. Simply upload a CSV or Excel file, select an AI model, and interact with your data using natural language to gain insights and visualizations.

### Key Features

- 🌐 Bilingual interface (Chinese/English)
- 🤖 Multiple AI model support: OpenAI, Azure OpenAI, local Ollama models
- 📊 Support for CSV, XLS, XLSX file formats
- 🔍 Automatic encoding detection (UTF-8, GBK, etc.)
- 📈 Smart chart generation (pie, bar, line, radar charts, etc.)
- 🎨 Perfect Chinese character support
- 💬 Chat history storage
- 🔄 Session management and loading
- 🐳 Docker containerized deployment
- 📱 Responsive interface design

### Quick Start

#### 🐳 Docker Deployment (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/sawyer-shi/pandas-ai-web.git
   cd pandas-ai-web
   ```

2. Configure environment variables:
   ```bash
   cp env.docker-example .env
   # Edit the .env file to configure your API keys
   ```

3. Start the service:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   Open your browser and visit `http://localhost:7860`

#### 🐍 Python Local Deployment

1. Create virtual environment:
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp env.example .env
   # Edit the .env file
   ```

4. Start the application:
   ```bash
   python main.py
   ```

### Usage

1. Select AI model (OpenAI, Azure OpenAI, or Ollama)
2. Upload CSV or Excel data file
3. Enter your questions in the chat box
4. View AI-generated answers and charts
5. Use history feature to review previous conversations

### Supported Query Types

- Data statistics: "How many rows are in this dataset?"
- Data visualization: "Show sales data with a bar chart"
- Trend analysis: "What's the trend in sales?"
- Data filtering: "Show records with sales > 1000"
- Comparative analysis: "Compare sales across different regions"

### Configuration

Environment variables (`.env` file):
```env
# Server configuration
GRADIO_SERVER_PORT=7860
GRADIO_SHARE=false

# OpenAI configuration
OPENAI_API_KEY=your_openai_key
OPENAI_BASE_URL=https://api.openai.com/v1

# Azure OpenAI configuration
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_API_VERSION=2024-02-01

# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Default settings
DEFAULT_LLM_TYPE=Ollama
```

### Contributing

Issues and Pull Requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=sawyer-shi/pandas-ai-web&type=Date)](https://star-history.com/#sawyer-shi/pandas-ai-web&Date) 
