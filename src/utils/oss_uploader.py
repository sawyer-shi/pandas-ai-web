import os
import uuid
from datetime import datetime

class OSSUploader:
    """OSS上传工具类，负责上传图表到阿里云OSS"""
    
    def __init__(self, oss_config):
        """
        初始化OSS上传工具
        
        Args:
            oss_config: OSS配置字典
        """
        self.oss_config = oss_config
        self.has_oss_sdk = self._check_oss_sdk()
    
    def _check_oss_sdk(self):
        """检查是否安装了阿里云OSS SDK"""
        try:
            import oss2
            return True
        except ImportError:
            print("警告：未安装阿里云OSS SDK (oss2)，将使用本地图片存储。请使用 pip install oss2 安装。")
            return False
    
    def is_enabled(self):
        """
        检查OSS上传是否启用
        
        Returns:
            bool: 是否启用OSS上传
        """
        return (self.oss_config.get("enabled", False) and 
                self.has_oss_sdk and 
                self.oss_config.get("access_key_id") and 
                self.oss_config.get("access_key_secret") and 
                self.oss_config.get("bucket") and 
                self.oss_config.get("endpoint"))
    
    def upload_file(self, local_file_path):
        """
        上传文件到OSS
        
        Args:
            local_file_path: 本地文件路径
        
        Returns:
            str: 成功返回OSS URL，失败返回None
        """
        if not self.is_enabled():
            return None
        
        try:
            # 动态导入oss2模块
            import oss2
            
            # 创建Bucket实例
            auth = oss2.Auth(
                self.oss_config["access_key_id"], 
                self.oss_config["access_key_secret"]
            )
            bucket = oss2.Bucket(
                auth, 
                self.oss_config["endpoint"], 
                self.oss_config["bucket"]
            )
            
            # 生成唯一的文件名
            file_name = os.path.basename(local_file_path)
            file_ext = os.path.splitext(file_name)[1]
            unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())[:8]}{file_ext}"
            
            # 生成OSS路径
            oss_path = f"{self.oss_config['directory']}/{unique_name}" if self.oss_config['directory'] else unique_name
            
            # 上传文件
            with open(local_file_path, 'rb') as f:
                bucket.put_object(oss_path, f)
            
            # 构建并返回URL
            oss_url = f"https://{self.oss_config['bucket']}.{self.oss_config['endpoint']}/{oss_path}"
            print(f"图表已上传到OSS: {oss_url}")
            return oss_url
            
        except Exception as e:
            print(f"上传图片到OSS失败: {str(e)}")
            return None 