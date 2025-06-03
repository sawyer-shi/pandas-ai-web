import os
import requests
from dotenv import load_dotenv
from pandasai.llm.openai import OpenAI
from pandasai.llm.azure_openai import AzureOpenAI
from .custom_ollama import CustomOllamaLLM
from ..utils.language_utils import LanguageUtils

# 加载环境变量
load_dotenv()

class LLMFactory:
    """LLM工厂类，负责创建不同类型的LLM实例"""
    
    @staticmethod
    def test_internet_connection():
        """测试网络连接情况"""
        try:
            # 尝试连接到OpenAI的API域名
            response = requests.get("https://api.openai.com", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def create_llm(llm_type, language="zh"):
        """
        创建指定类型的LLM实例
        
        Args:
            llm_type: LLM类型，支持 'OpenAI', 'Azure', 'Ollama'
            language: 语言代码 ("zh" 或 "en")
            
        Returns:
            tuple: (LLM实例, 成功标志, 错误消息)
        """
        # 加载环境变量中的API密钥
        openai_api_key = os.getenv("OPENAI_API_KEY")
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
        azure_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        # Ollama配置
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        
        llm = None
        error_msg = ""
        success = False
        
        if llm_type == "OpenAI":
            if not openai_api_key:
                return None, False, LanguageUtils.get_text(language, "openai_key_missing")
            
            # 检查OpenAI API的网络连接
            if not LLMFactory.test_internet_connection():
                return None, False, LanguageUtils.get_text(language, "network_connection_error")
            
            try:
                llm = OpenAI(api_token=openai_api_key)
                success = True
            except Exception as e:
                error_msg = LanguageUtils.get_text(language, "openai_init_failed", str(e))
                
        elif llm_type == "Azure":
            if not azure_api_key:
                return None, False, LanguageUtils.get_text(language, "azure_key_missing")
            if not azure_endpoint:
                return None, False, LanguageUtils.get_text(language, "azure_endpoint_missing")
            if not azure_deployment_name:
                return None, False, LanguageUtils.get_text(language, "azure_deployment_missing")
            
            # 检查Azure API的网络连接
            try:
                response = requests.get(azure_endpoint, timeout=5)
            except:
                return None, False, LanguageUtils.get_text(language, "azure_connection_error")
            
            try:
                # 方法1: 使用新的参数结构
                llm = AzureOpenAI(
                    api_key=azure_api_key,  # 使用api_key而不是api_token
                    azure_endpoint=azure_endpoint,  # 直接使用azure_endpoint参数
                    api_version=azure_api_version,
                    deployment_name=azure_deployment_name
                )
                success = True
            except Exception as e:
                try:
                    if "base_url and azure_endpoint are mutually exclusive" in str(e):
                        # 方法2: 如果上面的方法失败，尝试仅使用base_url
                        llm = AzureOpenAI(
                            api_key=azure_api_key,
                            base_url=f"{azure_endpoint}/openai/deployments/{azure_deployment_name}",
                            api_version=azure_api_version,
                            deployment_name=azure_deployment_name
                        )
                        success = True
                    else:
                        # 方法3: 如果仍然失败，尝试旧版兼容模式
                        llm = AzureOpenAI(
                            api_token=azure_api_key,
                            api_base=azure_endpoint,
                            api_version=azure_api_version,
                            deployment_name=azure_deployment_name
                        )
                        success = True
                except Exception as e2:
                    error_msg = LanguageUtils.get_text(language, "azure_init_failed", str(e2))
        
        elif llm_type == "Ollama":
            # 检查Ollama服务是否可用
            try:
                response = requests.get(f"{ollama_base_url}/api/tags", timeout=5)
            except:
                return None, False, LanguageUtils.get_text(language, "ollama_connection_failed", ollama_base_url)
            
            try:
                # 使用自定义Ollama LLM类
                llm = CustomOllamaLLM(
                    model=ollama_model,
                    url=ollama_base_url
                )
                success = True
                print(f"使用自定义OllamaLLM初始化: {ollama_model}@{ollama_base_url}")
            except Exception as e:
                error_msg = LanguageUtils.get_text(language, "ollama_init_failed", str(e))
                
        else:
            error_msg = LanguageUtils.get_text(language, "unsupported_llm_type", llm_type)
        
        return llm, success, error_msg 