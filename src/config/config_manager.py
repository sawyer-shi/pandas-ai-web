import os
import configparser

# 配置文件路径
CONFIG_DIR = "config"
OSS_CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

# 默认OSS配置
DEFAULT_OSS_CONFIG = {
    "enabled": False,
    "access_key_id": "",
    "access_key_secret": "",
    "bucket": "",
    "directory": "chartlist",
    "endpoint": "oss-cn-hangzhou.aliyuncs.com"
}

class ConfigManager:
    """配置管理类，负责加载和保存配置"""
    
    @staticmethod
    def ensure_config_dir():
        """确保配置目录存在"""
        os.makedirs(CONFIG_DIR, exist_ok=True)
    
    @staticmethod
    def load_oss_config():
        """
        加载OSS配置
        
        Returns:
            dict: OSS配置字典
        """
        oss_config = DEFAULT_OSS_CONFIG.copy()
        
        if os.path.exists(OSS_CONFIG_FILE):
            try:
                config = configparser.ConfigParser()
                config.read(OSS_CONFIG_FILE, encoding='utf-8')
                
                if 'common' in config:
                    # 显式读取enabled标志
                    oss_config["enabled"] = config['common'].getboolean('enabled', False)
                    oss_config["access_key_id"] = config['common'].get('access_key_id', '')
                    oss_config["access_key_secret"] = config['common'].get('access_key_secret', '')
                    oss_config["bucket"] = config['common'].get('bucket', '')
                    oss_config["directory"] = config['common'].get('directory', 'chartlist')
                    oss_config["endpoint"] = config['common'].get('endpoint', 'oss-cn-hangzhou.aliyuncs.com')
                    
                    # 如果用户没有设置enabled标志，但提供了完整的其他配置，则自动启用
                    if (not oss_config["enabled"] and 
                        oss_config["access_key_id"] and 
                        oss_config["access_key_secret"] and 
                        oss_config["bucket"] and 
                        oss_config["endpoint"]):
                        print("注意: OSS配置完整但enabled未设置为true，建议在config.ini中设置enabled=true")
                
                print(f"OSS配置已加载，enabled={oss_config['enabled']}")
            except Exception as e:
                print(f"加载OSS配置出错: {str(e)}")
        else:
            ConfigManager.create_default_oss_config()
            
        return oss_config
    
    @staticmethod
    def create_default_oss_config():
        """创建默认OSS配置文件"""
        ConfigManager.ensure_config_dir()
        
        try:
            with open(OSS_CONFIG_FILE, 'w', encoding='utf-8') as f:
                f.write("""[common]
# 是否启用阿里云OSS进行图片存储，true=启用，false=禁用
enabled = false                    
access_key_id = your-access-key-id      # 阿里云OSS的Access Key ID
access_key_secret = your-access-key-secret # 阿里云OSS的Access Key Secret
bucket = your-bucket-name                 # 阿里云OSS的Bucket名称
directory = chartlist                       # Bucket下的以及目录
endpoint = oss-cn-hangzhou.aliyuncs.com   # 阿里云OSS的Endpoint
""")
            print(f"已创建OSS配置模板文件: {OSS_CONFIG_FILE}，请修改配置后重启应用")
        except Exception as e:
            print(f"创建OSS配置模板文件失败: {str(e)}")
    
    @staticmethod
    def save_oss_config(oss_config):
        """
        保存OSS配置
        
        Args:
            oss_config: OSS配置字典
        """
        ConfigManager.ensure_config_dir()
        
        try:
            config = configparser.ConfigParser()
            config['common'] = {
                'enabled': str(oss_config.get('enabled', False)).lower(),
                'access_key_id': oss_config.get('access_key_id', ''),
                'access_key_secret': oss_config.get('access_key_secret', ''),
                'bucket': oss_config.get('bucket', ''),
                'directory': oss_config.get('directory', 'chartlist'),
                'endpoint': oss_config.get('endpoint', 'oss-cn-hangzhou.aliyuncs.com')
            }
            
            with open(OSS_CONFIG_FILE, 'w', encoding='utf-8') as f:
                config.write(f)
                
            print(f"OSS配置已保存到: {OSS_CONFIG_FILE}")
        except Exception as e:
            print(f"保存OSS配置出错: {str(e)}") 