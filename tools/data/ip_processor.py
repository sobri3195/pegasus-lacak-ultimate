import socket
import requests
from ipaddress import ip_address, IPv4Address, IPv6Address

class IPProcessor:
    def __init__(self):
        self.api_url = "http://ip-api.com/json/{}"
        
    def analyze_ip(self, ip):
        """Analisis detail IP address"""
        try:
            # Validasi IP
            ip_obj = ip_address(ip)
            
            # Dapatkan info geolokasi
            geo_info = self.get_geo_info(ip)
            
            return {
                "ip": ip,
                "version": "IPv4" if isinstance(ip_obj, IPv4Address) else "IPv6",
                "valid": True,
                "type": self.get_ip_type(ip_obj),
                "reverse_dns": self.get_reverse_dns(ip),
                "geolocation": geo_info,
                "is_private": ip_obj.is_private,
                "is_global": ip_obj.is_global,
                "network": str(ip_obj.network)
            }
        except Exception as e:
            return {"error": f"IP tidak valid: {str(e)}"}
            
    def get_ip_type(self, ip_obj):
        """Tentukan tipe IP"""
        if ip_obj.is_private:
            return "Private"
        elif ip_obj.is_multicast:
            return "Multicast"
        elif ip_obj.is_loopback:
            return "Loopback"
        elif ip_obj.is_link_local:
            return "Link-local"
        else:
            return "Public"
            
    def get_reverse_dns(self, ip):
        """Dapatkan reverse DNS"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None
            
    def get_geo_info(self, ip):
        """Dapatkan informasi geolokasi"""
        try:
            response = requests.get(self.api_url.format(ip))
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None 