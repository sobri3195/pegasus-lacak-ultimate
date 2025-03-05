import json
import os
from datetime import datetime

class ConfigManager:
    def __init__(self, config_file="config/settings.json"):
        self.config_file = config_file
        self.load_config()
        
    def load_config(self):
        """Load konfigurasi dari file"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = self.create_default_config()
            self.save_config()
            
    def save_config(self):
        """Simpan konfigurasi ke file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
            
    def create_default_config(self):
        """Buat konfigurasi default"""
        return {
            "version": "1.0.0",
            "author": "Letda Kes dr. Sobri",
            "last_updated": datetime.now().isoformat(),
            "api_keys": {},
            "settings": {
                "max_login_attempts": 3,
                "log_level": "INFO",
                "save_results": True,
                "auto_update": True
            },
            "paths": {
                "tools": "tools/",
                "output": "output/",
                "logs": "logs/"
            }
        }
        
    def get_setting(self, key, default=None):
        """Ambil nilai setting"""
        return self.config.get("settings", {}).get(key, default)
        
    def set_setting(self, key, value):
        """Set nilai setting"""
        if "settings" not in self.config:
            self.config["settings"] = {}
        self.config["settings"][key] = value
        self.save_config()
        
    def get_api_key(self, service):
        """Ambil API key"""
        return self.config.get("api_keys", {}).get(service)
        
    def set_api_key(self, service, key):
        """Set API key"""
        if "api_keys" not in self.config:
            self.config["api_keys"] = {}
        self.config["api_keys"][service] = key
        self.save_config() 