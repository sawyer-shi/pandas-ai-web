# Pandas AI Web - 数据对话助手 | Data Conversation Assistant

[中文](#中文文档) | [English](#english-documentation)

## 中文文档

### 项目介绍

Pandas AI Web 是一个基于PandasAI和Gradio开发的数据对话应用，让您能够通过自然语言与您的数据进行交互。只需上传CSV或Excel文件，选择AI模型，然后用自然语言提问，即可获得数据洞察和可视化结果。

### Screenshots
![QQ20250603-162827](https://github.com/user-attachments/assets/2763455f-fba7-417a-a03c-1a16b9b27502)
![QQ20250603-170735](https://github.com/user-attachments/assets/a776e2dc-5ec7-4679-8ca4-930c078849d1)

### 特点

- 支持中英文双语界面
- 多种AI模型支持：OpenAI、Azure OpenAI、Ollama本地模型
- 自动识别并处理多种文件编码，包括UTF-8、GBK等
- 支持CSV、XLS和XLSX文件格式
- 智能识别用户意图，只在明确要求时才生成数据可视化图表
- 生成的图表支持中文显示和完整Unicode字符集
- 显示完整数据预览，方便数据分析
- 图表支持上传到阿里云OSS进行共享
- 聊天界面支持复制和分享功能
- **新增**: 对话历史记录存储在SQLite数据库中，支持会话管理
- **新增**: 会话选择功能，可以加载和查看历史会话
- **新增**: 自动检测用户问题语言，并以相同语言回复

### 安装与配置

#### 方式一：直接源码安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/sawyer-shi/pandas-ai-web.git
   cd pandas-ai-web
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 创建并配置 `.env` 文件：
   ```bash
   # OpenAI配置
   OPENAI_API_KEY=your_openai_key

   # 或者 Azure OpenAI配置
   AZURE_OPENAI_API_KEY=your_azure_key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
   AZURE_OPENAI_API_VERSION=2023-05-15

   # 或者 Ollama配置
   OLLAMA_MODEL=llama3
   OLLAMA_BASE_URL=http://localhost:11434
   
   # 默认AI模型类型 (OpenAI, Azure, Ollama)
   DEFAULT_LLM_TYPE=Azure
   ```

4. 启动应用：
   ```bash
   python main.py
   ```

#### 方式二：Python venv虚拟环境安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/sawyer-shi/pandas-ai-web.git
   cd pandas-ai-web
   ```

2. 创建虚拟环境：
   ```bash
   # 创建虚拟环境
   python -m venv .venv
   
   # 激活虚拟环境
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. 安装依赖：
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. 创建并配置 `.env` 文件（同方式一）

5. 启动应用：
   ```bash
   python main.py
   ```

6. 退出虚拟环境：
   ```bash
   deactivate
   ```

#### 方式三：Conda环境安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/sawyer-shi/pandas-ai-web.git
   cd pandas-ai-web
   ```

2. 创建Conda环境：
   ```bash
   # 创建新的Conda环境
   conda create -n pandas-ai-web python=3.9
   
   # 激活环境
   conda activate pandas-ai-web
   ```

3. 安装依赖：
   ```bash
   # 升级pip
   pip install --upgrade pip
   
   # 安装项目依赖
   pip install -r requirements.txt
   
   # 或者使用conda安装常用包，然后安装剩余依赖
   conda install pandas numpy matplotlib sqlite
   pip install -r requirements.txt
   ```

4. 创建并配置 `.env` 文件（同方式一）

5. 启动应用：
   ```bash
   python main.py
   ```

6. 退出Conda环境：
   ```bash
   conda deactivate
   ```

#### OSS配置（可选）

配置阿里云OSS用于图表存储和分享：
编辑 `config/config.ini` 文件：
```ini
[common]
access_key_id = your-access-key-id
access_key_secret = your-access-key-secret
bucket = your-bucket-name
directory = chartlist
endpoint = oss-cn-hangzhou.aliyuncs.com
```

#### 环境要求

- **Python版本**: 3.8+ (推荐 3.9 或 3.10)
- **操作系统**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **内存**: 至少 4GB RAM (推荐 8GB+)
- **存储**: 至少 1GB 可用空间
- **网络**: 稳定的网络连接 (用于AI模型API调用)

#### 可选组件

- **Ollama**: 本地AI模型支持，需要单独安装Ollama服务
- **中文字体**: Windows用户通常已预装，Linux用户可能需要安装中文字体包

### 快速开始

1. **克隆项目**：
   ```bash
   git clone https://github.com/yourusername/pandas-ai-web.git
   cd pandas-ai-web
   ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**：
   ```bash
   # 复制示例环境变量文件
   cp env.example .env
   
   # 编辑.env文件，添加你的API密钥
   # 例如：OPENAI_API_KEY=your_actual_api_key
   ```

4. **启动应用**：
   ```bash
   python main.py
   ```

5. **打开浏览器**，访问显示的URL（通常是 http://127.0.0.1:7860）

### 使用方法

1. 启动应用：

   **推荐启动方式（标准入口）：**
   ```bash
   python main.py
   ```

   **其他启动方式：**
   ```bash
   # 带调试功能启动（包含详细日志）
   python run_app.py

   # 本地启动（不创建共享链接，避免下载frpc）
   python start_app.py
   ```

2. 在浏览器中打开显示的URL（通常是http://127.0.0.1:7860）

3. 选择界面语言（中文或英文）

4. 选择AI模型（OpenAI、Azure或Ollama）

5. 上传数据文件（CSV或Excel）

6. 在聊天框中提问，例如：
   - "这个数据的平均值是多少?"
   - "绘制销售额随时间变化的折线图"
   - "数据中的异常值有哪些?"
   - "计算每个城市的销售总额并展示为饼图"

7. 查看历史会话：
   - 在界面底部的"历史会话"标签页中选择之前的会话
   - 在"对话记录"标签页中查看所有问答记录

### 故障排除

- **网络连接错误**：如果您在中国大陆，可能需要使用代理才能连接到OpenAI API
- **中文字体问题**：确保您的系统安装了中文字体（如微软雅黑、宋体等）
- **图表上传失败**：检查阿里云OSS配置是否正确，确保网络连接正常
- **SQLite错误**：如果出现数据库错误，尝试删除`chat_history.db`文件，应用将自动创建新的数据库

### 项目结构

```
pandas-ai-web/
├── main.py                  # 标准应用入口
├── run_app.py               # 带调试功能的启动脚本
├── start_app.py             # 本地启动脚本（不创建共享链接）
├── requirements.txt         # 项目依赖
├── README.md                # 项目说明（本文件）
├── env.example              # 环境变量配置示例
├── .gitignore               # Git忽略文件配置
├── src/                     # 源代码目录
│   ├── app.py               # 应用程序主模块
│   ├── app_controller.py    # 应用控制器
│   ├── config/              # 配置管理模块
│   │   ├── config_manager.py
│   │   └── settings.py
│   ├── database/            # 数据库管理模块
│   │   └── db_manager.py
│   ├── llm/                 # AI模型管理模块
│   │   ├── custom_ollama.py
│   │   └── llm_factory.py
│   ├── storage/             # 存储管理模块
│   │   └── chart_storage.py
│   ├── ui/                  # 用户界面模块
│   │   └── app_ui.py
│   └── utils/               # 工具模块
│       ├── chart_analyzer.py
│       ├── data_loader.py
│       ├── font_config.py
│       ├── image_utils.py
│       ├── language_utils.py
│       ├── oss_uploader.py
│       └── pandasai_patch.py
├── config/                  # 配置文件目录
│   ├── config.ini           # OSS配置（需要自行创建）
│   └── config.ini.example   # OSS配置示例
├── charts/                  # 生成的图表存储目录
├── avatar/                  # 头像图片目录
└── chat_history.db          # SQLite数据库（自动创建）
```

## English Documentation

### Project Introduction

Pandas AI Web is a data conversation application developed based on PandasAI and Gradio, allowing you to interact with your data using natural language. Simply upload a CSV or Excel file, select an AI model, and ask questions in natural language to get data insights and visualizations.

### Screenshots
![QQ20250603-162827](https://github.com/user-attachments/assets/2763455f-fba7-417a-a03c-1a16b9b27502)
![QQ20250603-170735](https://github.com/user-attachments/assets/a776e2dc-5ec7-4679-8ca4-930c078849d1)

### Features

- Bilingual interface (Chinese and English)
- Multiple AI model support: OpenAI, Azure OpenAI, local Ollama models
- Automatic recognition and processing of various file encodings, including UTF-8, GBK, etc.
- Support for CSV, XLS, and XLSX file formats
- Intelligent detection of user intent, only generating data visualization charts when explicitly requested
- Generated charts support Chinese and full Unicode character sets
- Complete data preview display for convenient analysis
- Chart upload to Alibaba Cloud OSS for sharing
- Chat interface with copy and share functionality
- **New**: Chat history stored in SQLite database with session management
- **New**: Session selection for loading and viewing previous conversations
- **New**: Automatic language detection for responding in the same language as the user's query

### Installation and Configuration

#### Method 1: Direct Source Code Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pandas-ai-web.git
   cd pandas-ai-web
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create and configure the `.env` file:
   ```bash
   # OpenAI configuration
   OPENAI_API_KEY=your_openai_key

   # Or Azure OpenAI configuration
   AZURE_OPENAI_API_KEY=your_azure_key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
   AZURE_OPENAI_API_VERSION=2023-05-15

   # Or Ollama configuration
   OLLAMA_MODEL=llama3
   OLLAMA_BASE_URL=http://localhost:11434
   
   # Default AI model type (OpenAI, Azure, Ollama)
   DEFAULT_LLM_TYPE=Azure
   ```

4. Start the application:
   ```bash
   python main.py
   ```

#### Method 2: Python venv Virtual Environment Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pandas-ai-web.git
   cd pandas-ai-web
   ```

2. Create a virtual environment:
   ```bash
   # Create a virtual environment
   python -m venv .venv
   
   # Activate the virtual environment
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Create and configure the `.env` file (same as method one)

5. Start the application:
   ```bash
   python main.py
   ```

6. Exit the virtual environment:
   ```bash
   deactivate
   ```

#### Method 3: Conda Environment Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pandas-ai-web.git
   cd pandas-ai-web
   ```

2. Create a Conda environment:
   ```bash
   # Create a new Conda environment
   conda create -n pandas-ai-web python=3.9
   
   # Activate the environment
   conda activate pandas-ai-web
   ```

3. Install dependencies:
   ```bash
   # Upgrade pip
   pip install --upgrade pip
   
   # Install project dependencies
   pip install -r requirements.txt
   
   # Or use conda to install common packages and then install remaining dependencies
   conda install pandas numpy matplotlib sqlite
   pip install -r requirements.txt
   ```

4. Create and configure the `.env` file (same as method one)

5. Start the application:
   ```bash
   python main.py
   ```

6. Exit the Conda environment:
   ```bash
   conda deactivate
   ```

#### OSS Configuration (Optional)

Configure Alibaba Cloud OSS for chart storage and sharing:
Edit the `config/config.ini` file:
```ini
[common]
access_key_id = your-access-key-id
access_key_secret = your-access-key-secret
bucket = your-bucket-name
directory = chartlist
endpoint = oss-cn-hangzhou.aliyuncs.com
```

#### Environment Requirements

- **Python version**: 3.8+ (recommended 3.9 or 3.10)
- **Operating system**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Memory**: At least 4GB RAM (recommended 8GB+)
- **Storage**: At least 1GB available space
- **Network**: Stable internet connection (for AI model API calls)

#### Optional Components

- **Ollama**: Local AI model support, requires separate Ollama service installation
- **Chinese fonts**: Windows users usually have them pre-installed, Linux users may need to install Chinese font packages

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/pandas-ai-web.git
   cd pandas-ai-web
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit the .env file and add your API keys
   # Example: OPENAI_API_KEY=your_actual_api_key
   ```

4. **Start the application**:
   ```bash
   python main.py
   ```

5. **Open your browser** and visit the displayed URL (usually http://127.0.0.1:7860)

### Usage

1. Start the application:

   **Recommended startup method (standard entry):**
   ```bash
   python main.py
   ```

   **Alternative startup methods:**
   ```bash
   # Start with debugging features (includes detailed logs)
   python run_app.py

   # Local startup (no shared links, avoids downloading frpc)
   python start_app.py
   ```

2. Open the displayed URL in your browser (usually http://127.0.0.1:7860)

3. Select interface language (Chinese or English)

4. Choose an AI model (OpenAI, Azure, or Ollama)

5. Upload a data file (CSV or Excel)

6. Ask questions in the chat box, for example:
   - "What is the average value in this data?"
   - "Plot a line chart of sales over time"
   - "What are the outliers in the data?"
   - "Calculate the total sales for each city and display as a pie chart"

7. View historical sessions:
   - Select previous sessions in the "Session History" tab at the bottom of the interface
   - View all Q&A records in the "Chat History" tab

### Troubleshooting

- **Network connection errors**: If you are in mainland China, you may need to use a proxy to connect to the OpenAI API
- **Chinese font issues**: Make sure your system has Chinese fonts installed (such as Microsoft YaHei, SimSun, etc.)
- **Chart upload failure**: Check if your Alibaba Cloud OSS configuration is correct and ensure network connectivity 
- **SQLite errors**: If you encounter database errors, try deleting the `chat_history.db` file, and the application will automatically create a new database

### Project Structure

```
pandas-ai-web/
├── main.py                  # Standard application entry
├── run_app.py               # Startup script with debugging features
├── start_app.py             # Local startup script (no shared links)
├── requirements.txt         # Dependencies
├── README.md                # Project documentation (this file)
├── env.example              # Environment variable configuration example
├── .gitignore               # Git ignore file configuration
├── src/                     # Source code directory
│   ├── app.py               # Main application module
│   ├── app_controller.py    # Application controller
│   ├── config/              # Configuration management modules
│   │   ├── config_manager.py
│   │   └── settings.py
│   ├── database/            # Database management modules
│   │   └── db_manager.py
│   ├── llm/                 # AI model management modules
│   │   ├── custom_ollama.py
│   │   └── llm_factory.py
│   ├── storage/             # Storage management modules
│   │   └── chart_storage.py
│   ├── ui/                  # User interface modules
│   │   └── app_ui.py
│   └── utils/               # Utility modules
│       ├── chart_analyzer.py
│       ├── data_loader.py
│       ├── font_config.py
│       ├── image_utils.py
│       ├── language_utils.py
│       ├── oss_uploader.py
│       └── pandasai_patch.py
├── config/                  # Configuration directory
│   ├── config.ini           # OSS configuration (needs to be created)
│   └── config.ini.example   # OSS configuration example
├── charts/                  # Directory for generated charts
└── avatar/                  # Avatar images directory
└── chat_history.db          # SQLite database (automatically created)
```


## License

MIT License 
