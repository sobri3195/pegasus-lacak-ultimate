import requests
from bs4 import BeautifulSoup
import whois
import dns.resolver
import ssl
import socket
from datetime import datetime

class WebRecon:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def analyze_website(self, domain):
        """Analisis website secara menyeluruh"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "domain": domain,
            "whois": self.get_whois_info(domain),
            "dns": self.get_dns_info(domain),
            "ssl": self.check_ssl(domain),
            "headers": self.check_headers(domain),
            "technologies": self.detect_technologies(domain),
            "security_headers": self.check_security_headers(domain)
        }
        return results
        
    def get_whois_info(self, domain):
        """Dapatkan informasi WHOIS"""
        try:
            w = whois.whois(domain)
            return {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "name_servers": w.name_servers
            }
        except Exception as e:
            return {"error": str(e)}
            
    def get_dns_info(self, domain):
        """Dapatkan informasi DNS"""
        records = {}
        try:
            for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    records[record_type] = [str(rdata) for rdata in answers]
                except:
                    records[record_type] = []
            return records
        except Exception as e:
            return {"error": str(e)}
            
    def check_ssl(self, domain):
        """Cek sertifikat SSL"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        "issuer": dict(x[0] for x in cert['issuer']),
                        "subject": dict(x[0] for x in cert['subject']),
                        "version": cert['version'],
                        "valid_from": cert['notBefore'],
                        "valid_until": cert['notAfter']
                    }
        except Exception as e:
            return {"error": str(e)} 