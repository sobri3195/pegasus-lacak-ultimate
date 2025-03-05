import logging
from datetime import datetime
import os

class PegasusLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.setup_logger()
        
    def setup_logger(self):
        """Setup logging configuration"""
        log_file = f"{self.log_dir}/pegasus_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('PegasusLacak')
        
    def log_activity(self, user, activity, status="success", details=None):
        """Log aktivitas pengguna"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "activity": activity,
            "status": status,
            "details": details
        }
        
        if status == "success":
            self.logger.info(f"User {user}: {activity}")
        else:
            self.logger.error(f"User {user}: {activity} - {details}") 