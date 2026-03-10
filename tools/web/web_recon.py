import requests
from bs4 import BeautifulSoup
import whois
import ssl
import socket
from datetime import datetime

try:
    import dns.resolver
except ImportError:  # optional dependency fallback
    dns = None


class WebRecon:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def analyze_website(self, domain):
        return {
            "timestamp": datetime.now().isoformat(),
            "domain": domain,
            "whois": self.get_whois_info(domain),
            "dns": self.get_dns_info(domain),
            "ssl": self.check_ssl(domain),
            "headers": self.check_headers(domain),
            "technologies": self.detect_technologies(domain),
            "security_headers": self.check_security_headers(domain)
        }

    def get_whois_info(self, domain):
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
        if dns is None:
            return {"error": "dnspython dependency is not installed"}

        records = {}
        for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
            except Exception:
                records[record_type] = []
        return records

    def check_ssl(self, domain):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
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

    def check_headers(self, domain):
        url = domain if domain.startswith(("http://", "https://")) else f"https://{domain}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            return dict(response.headers)
        except Exception as e:
            return {"error": str(e)}

    def detect_technologies(self, domain):
        url = domain if domain.startswith(("http://", "https://")) else f"https://{domain}"
        tech = []
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            server = response.headers.get("Server")
            powered_by = response.headers.get("X-Powered-By")
            if server:
                tech.append(server)
            if powered_by:
                tech.append(powered_by)

            soup = BeautifulSoup(response.text, "html.parser")
            generators = soup.find_all("meta", attrs={"name": "generator"})
            for meta in generators:
                content = meta.get("content")
                if content:
                    tech.append(content)
            return sorted(set(tech))
        except Exception:
            return tech

    def check_security_headers(self, domain):
        required = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy"
        ]
        headers = self.check_headers(domain)
        if "error" in headers:
            return headers

        return {h: headers.get(h) for h in required}
