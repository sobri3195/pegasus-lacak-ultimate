import requests
import json
from datetime import datetime
from .logger import PegasusLogger

class APIHandler:
    def __init__(self, config_file="config/settings.json"):
        self.load_config(config_file)
        self.logger = PegasusLogger()
        
    def load_config(self, config_file):
        """Load API keys dari config"""
        with open(config_file, 'r') as f:
            config = json.load(f)
            self.api_keys = config.get('api_keys', {})
            
    def make_request(self, url, method="GET", headers=None, params=None, data=None):
        """Buat HTTP request dengan error handling"""
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.log_activity(
                "system",
                f"API Request Failed: {url}",
                "error",
                str(e)
            )
            return {"error": str(e)} 