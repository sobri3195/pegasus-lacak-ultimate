import nmap
import socket
from datetime import datetime

class NetworkScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        
    def scan_target(self, target, scan_type="basic"):
        """Scan target network/host"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "scan_type": scan_type,
            "results": {}
        }
        
        try:
            if scan_type == "basic":
                results["results"] = self.basic_scan(target)
            elif scan_type == "full":
                results["results"] = self.full_scan(target)
            elif scan_type == "vuln":
                results["results"] = self.vulnerability_scan(target)
                
            return results
        except Exception as e:
            return {"error": str(e)}
            
    def basic_scan(self, target):
        """Basic port scan"""
        self.nm.scan(target, arguments="-F")
        return self.nm.analyse_nmap_xml_scan()
        
    def full_scan(self, target):
        """Full port scan dengan service detection"""
        self.nm.scan(target, arguments="-sS -sV -O")
        return self.nm.analyse_nmap_xml_scan()
        
    def vulnerability_scan(self, target):
        """Vulnerability scan"""
        self.nm.scan(target, arguments="-sV --script vuln")
        return self.nm.analyse_nmap_xml_scan() 