"""
配置管理模块
负责加载和管理应用程序的配置
"""

import os
import configparser
from dotenv import load_dotenv

class Settings:
    """Configuration manager for PandasAI web application.
    
    This class handles loading settings from both .env and config.ini files,
    providing a unified interface for accessing configuration options.
    """
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize configuration values
        self.config_dir = "config"
        self.config_file = os.path.join(self.config_dir, "config.ini")
        
        # OpenAI settings
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Azure OpenAI settings
        self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
        self.azure_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        # Ollama settings
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        
        # Default LLM type
        self.default_llm_type = self._determine_default_llm_type()
        
        # Aliyun OSS settings (will be loaded from config.ini)
        self.oss_config = {
            "enabled": False,
            "access_key_id": "",
            "access_key_secret": "",
            "bucket": "",
            "directory": "chartlist",
            "endpoint": "oss-cn-hangzhou.aliyuncs.com"
        }
        
        # Load config.ini settings
        self.load_config_ini()
        
        # Create necessary directories
        self._ensure_directories()
    
    def _determine_default_llm_type(self):
        """Determine the default LLM type based on available API keys."""
        default_type = os.getenv("DEFAULT_LLM_TYPE")
        if not default_type:
            if self.openai_api_key:
                default_type = "OpenAI"
            elif self.azure_api_key and self.azure_endpoint:
                default_type = "Azure"
            else:
                default_type = "Ollama"
        return default_type
    
    def load_config_ini(self):
        """Load settings from config.ini file."""
        if os.path.exists(self.config_file):
            try:
                config = configparser.ConfigParser()
                config.read(self.config_file, encoding='utf-8')
                
                # Load OSS settings if 'common' section exists
                if 'common' in config:
                    # Check if there's an explicit enabled setting
                    if 'enabled' in config['common']:
                        self.oss_config["enabled"] = config['common'].getboolean('enabled', False)
                    
                    # Load other OSS settings
                    self.oss_config["access_key_id"] = config['common'].get('access_key_id', '')
                    self.oss_config["access_key_secret"] = config['common'].get('access_key_secret', '')
                    self.oss_config["bucket"] = config['common'].get('bucket', '')
                    self.oss_config["directory"] = config['common'].get('directory', 'chartlist')
                    self.oss_config["endpoint"] = config['common'].get('endpoint', 'oss-cn-hangzhou.aliyuncs.com')
                    
                    # If no explicit enabled setting but we have complete credentials, enable OSS
                    if 'enabled' not in config['common']:
                        # Only enable if all required credentials are provided
                        self.oss_config["enabled"] = bool(
                            self.oss_config["access_key_id"] and 
                            self.oss_config["access_key_secret"] and 
                            self.oss_config["bucket"] and 
                            self.oss_config["endpoint"]
                        )
                
                print(f"Successfully loaded configuration from {self.config_file}")
                if self.oss_config["enabled"]:
                    print(f"OSS storage enabled for charts: bucket={self.oss_config['bucket']}")
                else:
                    print("OSS storage disabled, using local storage for charts")
                    
            except Exception as e:
                print(f"Error loading configuration from {self.config_file}: {str(e)}")
    
    def _ensure_directories(self):
        """Ensure necessary directories exist."""
        os.makedirs("charts", exist_ok=True)
        os.makedirs("exports/charts", exist_ok=True)
        os.makedirs("avatar", exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)
    
    def create_default_config(self):
        """Create a default config.ini file if it doesn't exist."""
        if not os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    f.write("""[common]
# Whether to enable Alibaba Cloud OSS for chart storage
enabled = false
access_key_id = your-access-key-id      # Alibaba Cloud OSS Access Key ID
access_key_secret = your-access-key-secret # Alibaba Cloud OSS Access Key Secret
bucket = your-bucket-name                 # Alibaba Cloud OSS Bucket name
directory = chartlist                       # Directory in the bucket
endpoint = oss-cn-hangzhou.aliyuncs.com   # Alibaba Cloud OSS Endpoint
""")
                print(f"Created default configuration template: {self.config_file}")
            except Exception as e:
                print(f"Error creating default configuration file: {str(e)}")
    
    def is_oss_enabled(self):
        """Check if OSS storage is enabled and properly configured."""
        # First check if it's explicitly enabled in the config
        if not self.oss_config["enabled"]:
            return False
        
        # Then check if we have the OSS SDK installed
        try:
            import oss2
            has_oss = True
        except ImportError:
            has_oss = False
            print("Warning: Alibaba Cloud OSS SDK (oss2) is not installed. "
                  "Using local storage for charts. Install with: pip install oss2")
            return False
        
        # Finally check if all required credentials are provided
        if (self.oss_config["access_key_id"] and 
            self.oss_config["access_key_secret"] and 
            self.oss_config["bucket"] and 
            self.oss_config["endpoint"]):
            return True
        else:
            print("Warning: OSS is enabled but credentials are incomplete. Using local storage.")
            return False

# Create a singleton instance
settings = Settings() 