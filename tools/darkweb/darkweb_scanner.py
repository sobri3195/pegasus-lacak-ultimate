import requests
import json
from datetime import datetime
import hashlib

class DarkWebScanner:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.endpoints = {
            "breach": "https://api.darkweb.local/breach",
            "paste": "https://api.darkweb.local/paste",
            "market": "https://api.darkweb.local/market"
        }
        
    def scan_target(self, target_type, target_value):
        """Scan target di dark web"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "target_type": target_type,
            "target_value": target_value,
            "hash": hashlib.sha256(target_value.encode()).hexdigest(),
            "findings": {
                "breaches": self.check_breaches(target_value),
                "pastes": self.check_pastes(target_value),
                "markets": self.check_markets(target_value)
            }
        }
        return results
        
    def check_breaches(self, target):
        """Cek kebocoran data"""
        try:
            response = self.make_request(
                self.endpoints["breach"],
                params={"target": target}
            )
            return response.get("breaches", [])
        except:
            return []
            
    def check_pastes(self, target):
        """Cek di paste sites"""
        try:
            response = self.make_request(
                self.endpoints["paste"],
                params={"target": target}
            )
            return response.get("pastes", [])
        except:
            return []
            
    def check_markets(self, target):
        """Cek di dark markets"""
        try:
            response = self.make_request(
                self.endpoints["market"],
                params={"target": target}
            )
            return response.get("listings", [])
        except:
            return []
            
    def make_request(self, url, params=None):
        """Buat HTTP request dengan API key"""
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        response = requests.get(url, headers=headers, params=params, timeout=30)
        return response.json() 