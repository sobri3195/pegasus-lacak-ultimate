import re

try:
    from dns import resolver
except ImportError:  # optional dependency fallback
    resolver = None

from .email_providers import EMAIL_PROVIDERS


class EmailProcessor:
    def __init__(self):
        self.providers = EMAIL_PROVIDERS

    def analyze_email(self, email):
        try:
            if not self.validate_format(email):
                return {"error": "Format email tidak valid"}

            username, domain = email.split('@', 1)
            domain = domain.lower()

            return {
                "email": email,
                "username": username,
                "domain": domain,
                "provider_info": self.get_provider_info(domain),
                "format_valid": True,
                "mx_records": self.check_mx_records(domain),
                "disposable": self.check_if_disposable(domain)
            }
        except Exception as e:
            return {"error": f"Gagal menganalisis email: {str(e)}"}

    def validate_format(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def get_provider_info(self, domain):
        if domain in self.providers:
            return self.providers[domain]

        parts = domain.split('.')
        if len(parts) >= 2:
            tld = f"{parts[-2]}.{parts[-1]}"
            if tld in self.providers:
                return self.providers[tld]

        return {"name": "Unknown", "type": "Unknown", "country": "Unknown"}

    def check_mx_records(self, domain):
        if resolver is None:
            return []
        try:
            mx_records = resolver.resolve(domain, 'MX')
            return [str(mx.exchange) for mx in mx_records]
        except Exception:
            return []

    def check_if_disposable(self, domain):
        disposable_domains = {
            "tempmail.com", "10minutemail.com", "throwawaymail.com"
        }
        return domain in disposable_domains
