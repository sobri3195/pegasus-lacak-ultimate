from scapy.all import *
from datetime import datetime
import subprocess
import re

class WifiScanner:
    def __init__(self):
        self.interface = "wlan0"
        
    def scan_networks(self, timeout=30):
        """Scan jaringan WiFi di sekitar"""
        networks = {}
        
        def packet_handler(pkt):
            if pkt.haslayer(Dot11Beacon):
                bssid = pkt[Dot11].addr2
                ssid = pkt[Dot11Elt].info.decode() if pkt[Dot11Elt].info else "Hidden"
                try:
                    dbm_signal = pkt.dBm_AntSignal
                except:
                    dbm_signal = "N/A"
                    
                stats = pkt[Dot11Beacon].network_stats()
                
                networks[bssid] = {
                    "ssid": ssid,
                    "channel": stats.get("channel"),
                    "encryption": stats.get("crypto"),
                    "signal": dbm_signal
                }
                
        sniff(iface=self.interface, prn=packet_handler, timeout=timeout)
        return networks
        
    def check_vulnerability(self, bssid):
        """Cek kerentanan jaringan WiFi"""
        try:
            cmd = f"aircrack-ng --bssid {bssid} -w /path/to/wordlist.txt capture.cap"
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            return self.parse_aircrack_output(result.stdout)
        except Exception as e:
            return {"error": str(e)}
            
    def parse_aircrack_output(self, output):
        """Parse output dari aircrack-ng"""
        results = {
            "wps": False,
            "wpa": False,
            "weak_cipher": False
        }
        
        if "WPS enabled" in output:
            results["wps"] = True
        if "WPA (1 handshake)" in output:
            results["wpa"] = True
        if "TKIP" in output:
            results["weak_cipher"] = True
            
        return results 