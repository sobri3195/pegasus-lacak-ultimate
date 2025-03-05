import re
from dns import resolver
from .email_providers import EMAIL_PROVIDERS

class EmailProcessor:
    def __init__(self):
        self.providers = EMAIL_PROVIDERS
        
    def analyze_email(self, email):
        """Analisis detail email"""
        try:
            username, domain = email.split('@')
            
            # Cek provider
            provider_info = self.get_provider_info(domain)
            
            # Cek MX records
            mx_records = self.check_mx_records(domain)
            
            return {
                "email": email,
                "username": username,
                "domain": domain,
                "provider_info": provider_info,
                "format_valid": self.validate_format(email),
                "mx_records": mx_records,
                "disposable": self.check_if_disposable(domain)
            }
        except Exception as e:
            return {"error": f"Gagal menganalisis email: {str(e)}"}
            
    def validate_format(self, email):
        """Validasi format email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
        
    def get_provider_info(self, domain):
        """Dapatkan informasi provider email"""
        # Cek domain langsung
        if domain in self.providers:
            return self.providers[domain]
            
        # Cek domain level atas
        tld = domain.split('.')[-2] + '.' + domain.split('.')[-1]
        if tld in self.providers:
            return self.providers[tld]
            
        return {"name": "Unknown", "type": "Unknown", "country": "Unknown"}
        
    def check_mx_records(self, domain):
        """Cek MX records domain"""
        try:
            mx_records = resolver.resolve(domain, 'MX')
            return [str(mx.exchange) for mx in mx_records]
        except:
            return []
            
    def check_if_disposable(self, domain):
        """Cek apakah email disposable"""
        disposable_domains = [
            "tempmail.com", "10minutemail.com", "throwawaymail.com"
            # Tambahkan domain disposable lainnya
        ]
        return domain in disposable_domains 