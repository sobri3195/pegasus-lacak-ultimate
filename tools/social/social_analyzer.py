import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class SocialAnalyzer:
    def __init__(self):
        self.platforms = {
            "facebook": {
                "url": "https://facebook.com/{}",
                "selectors": {
                    "name": "h1.profile-name",
                    "photo": "img.profile-photo"
                }
            },
            "instagram": {
                "url": "https://instagram.com/{}",
                "selectors": {
                    "name": "h2.profile-name",
                    "bio": "div.biography"
                }
            },
            "twitter": {
                "url": "https://twitter.com/{}",
                "selectors": {
                    "name": "h2.profile-name",
                    "bio": "div.bio"
                }
            }
        }
        
    def analyze_username(self, username):
        """Analisis username di berbagai platform"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "platforms": {}
        }
        
        for platform, config in self.platforms.items():
            results["platforms"][platform] = self.check_platform(platform, username, config)
            
        return results
        
    def check_platform(self, platform, username, config):
        """Cek keberadaan username di platform"""
        try:
            url = config["url"].format(username)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return {
                    "exists": True,
                    "url": url,
                    "name": self.extract_element(soup, config["selectors"].get("name")),
                    "bio": self.extract_element(soup, config["selectors"].get("bio")),
                    "photo": self.extract_element(soup, config["selectors"].get("photo"))
                }
            return {"exists": False, "url": url}
            
        except Exception as e:
            return {"error": str(e)}
            
    def extract_element(self, soup, selector):
        """Extract elemen dari HTML menggunakan selector"""
        if not selector:
            return None
        element = soup.select_one(selector)
        return element.text.strip() if element else None 