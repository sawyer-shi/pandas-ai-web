import os
import uuid
from datetime import datetime

from src.config.settings import settings

class ChartStorage:
    """Handles chart image storage in both local filesystem and OSS."""
    
    def __init__(self):
        """Initialize the chart storage."""
        self.local_dir = "charts"
        # Ensure the local directory exists
        os.makedirs(self.local_dir, exist_ok=True)
        
        # Check if OSS is available and enabled
        self.oss_enabled = settings.is_oss_enabled()
        if self.oss_enabled:
            try:
                import oss2
                self.oss_available = True
            except ImportError:
                self.oss_available = False
                print("Warning: Alibaba Cloud OSS SDK not installed. Using local storage only.")
        else:
            self.oss_available = False
    
    def save_chart(self, chart_data, file_extension=".png"):
        """Save chart data to storage.
        
        Args:
            chart_data: The chart data to save (file path or binary data)
            file_extension: The file extension (default: .png)
            
        Returns:
            tuple: (local_path, oss_url) - oss_url will be None if OSS is not used
        """
        # Generate a unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}{file_extension}"
        local_path = os.path.join(self.local_dir, filename)
        
        # If chart_data is a file path, copy it to our storage location
        if isinstance(chart_data, str) and os.path.exists(chart_data):
            import shutil
            shutil.copy2(chart_data, local_path)
        # If chart_data is binary data, write it directly
        elif isinstance(chart_data, bytes):
            with open(local_path, 'wb') as f:
                f.write(chart_data)
        else:
            raise ValueError("Invalid chart data. Must be a file path or binary data.")
        
        # Convert to absolute path for display
        local_display_path = os.path.abspath(local_path).replace('\\', '/')
        
        # Upload to OSS if enabled and available
        oss_url = None
        if self.oss_enabled and self.oss_available:
            oss_url = self._upload_to_oss(local_path, filename)
        
        return local_display_path, oss_url
    
    def _upload_to_oss(self, local_file_path, filename=None):
        """Upload a file to Alibaba Cloud OSS.
        
        Args:
            local_file_path: Path to the local file
            filename: Optional custom filename in OSS
            
        Returns:
            str: The URL of the file in OSS, or None if upload failed
        """
        if not self.oss_enabled or not self.oss_available:
            return None
        
        try:
            import oss2
            
            # Get OSS configuration
            oss_config = settings.oss_config
            
            # Create OSS Auth and Bucket instances
            auth = oss2.Auth(oss_config["access_key_id"], oss_config["access_key_secret"])
            bucket = oss2.Bucket(auth, oss_config["endpoint"], oss_config["bucket"])
            
            # Use provided filename or generate one from the local path
            if not filename:
                filename = os.path.basename(local_file_path)
            
            # Generate the OSS path
            oss_path = f"{oss_config['directory']}/{filename}" if oss_config['directory'] else filename
            
            # Upload the file
            with open(local_file_path, 'rb') as f:
                bucket.put_object(oss_path, f)
            
            # Construct and return the OSS URL
            oss_url = f"https://{oss_config['bucket']}.{oss_config['endpoint']}/{oss_path}"
            print(f"Chart uploaded to OSS: {oss_url}")
            return oss_url
            
        except Exception as e:
            print(f"Error uploading to OSS: {str(e)}")
            return None

# Create a singleton instance
chart_storage = ChartStorage() 