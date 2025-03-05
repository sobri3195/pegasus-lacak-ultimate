import requests
import json
import os
from datetime import datetime

class PegasusUpdater:
    def __init__(self):
        self.current_version = "1.0.0"
        self.update_url = "https://api.github.com/repos/user/pegasus-lacak/releases/latest"
        
    def check_updates(self):
        """Cek pembaruan tersedia"""
        try:
            response = requests.get(self.update_url)
            if response.status_code == 200:
                latest = response.json()
                latest_version = latest["tag_name"].strip("v")
                return {
                    "current_version": self.current_version,
                    "latest_version": latest_version,
                    "update_available": self.compare_versions(latest_version),
                    "release_notes": latest["body"],
                    "download_url": latest["assets"][0]["browser_download_url"]
                }
        except Exception as e:
            return {"error": str(e)}
            
    def compare_versions(self, latest):
        """Bandingkan versi"""
        current = [int(x) for x in self.current_version.split(".")]
        new = [int(x) for x in latest.split(".")]
        
        for i in range(len(current)):
            if new[i] > current[i]:
                return True
            elif new[i] < current[i]:
                return False
        return False
        
    def download_update(self, url, target_path):
        """Download pembaruan"""
        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(target_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        
            return True
        except Exception as e:
            return False 