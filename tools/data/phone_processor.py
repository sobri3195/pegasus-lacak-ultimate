import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from .phone_providers import PHONE_PROVIDERS

class PhoneProcessor:
    def __init__(self):
        self.providers = PHONE_PROVIDERS

    def analyze_number(self, phone_number):
        """Analisis detail nomor telepon"""
        try:
            # Parse nomor telepon
            parsed = phonenumbers.parse(phone_number, "ID")
            
            # Dapatkan provider berdasarkan 4 digit awal
            prefix = str(parsed.national_number)[:4]
            provider = self.providers.get(prefix, "Unknown")
            
            return {
                "nomor": phone_number,
                "format": {
                    "nasional": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                    "internasional": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                    "E164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                },
                "provider": provider,
                "tipe": "Mobile" if phonenumbers.number_type(parsed) == phonenumbers.PhoneNumberType.MOBILE else "Fixed Line",
                "negara": geocoder.description_for_number(parsed, "id"),
                "valid": phonenumbers.is_valid_number(parsed),
                "possible": phonenumbers.is_possible_number(parsed),
                "timezone": timezone.time_zones_for_number(parsed)
            }
        except Exception as e:
            return {"error": f"Format nomor tidak valid: {str(e)}"}

    def validate_number(self, phone_number):
        """Validasi format nomor telepon"""
        try:
            parsed = phonenumbers.parse(phone_number, "ID")
            return phonenumbers.is_valid_number(parsed)
        except:
            return False 