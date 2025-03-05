import requests
import json
import subprocess
from datetime import datetime
import os

class OSINTTools:
    def __init__(self, tools_dir="tools/osint/bin"):
        self.tools_dir = tools_dir
        self.setup_tools()
        
    def setup_tools(self):
        """Setup OSINT tools"""
        os.makedirs(self.tools_dir, exist_ok=True)
        # Install atau update tools jika diperlukan
        
    def run_sherlock(self, username):
        """Run Sherlock untuk username search"""
        try:
            cmd = ["python", f"{self.tools_dir}/sherlock/sherlock.py", username, "--json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            return {"error": str(e)}
            
    def run_holehe(self, email):
        """Run Holehe untuk email check"""
        try:
            cmd = ["holehe", email, "--json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            return {"error": str(e)}
            
    def run_maigret(self, username):
        """Run Maigret untuk social media search"""
        try:
            cmd = ["maigret", username, "--json"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            return {"error": str(e)} 