import re
from datetime import datetime

class NIKScanner:
    def __init__(self):
        self.nik_pattern = r'^\d{16}$'
        self.province_codes = {
            "11": "Aceh",
            "12": "Sumatera Utara",
            # ... tambahkan kode provinsi lainnya
        }

    def validate_nik(self, nik):
        """Validasi format NIK"""
        if not re.match(self.nik_pattern, nik):
            return {"valid": False, "error": "Format NIK tidak valid"}

        result = {
            "timestamp": datetime.now().isoformat(),
            "nik": nik,
            "valid": True,
            "province": self.get_province(nik[:2]),
            "district": self.get_district(nik[2:4]),
            "subdistrict": nik[4:6],
            "birth_info": self.get_birth_info(nik[6:12]),
            "unique_code": nik[12:]
        }
        return result

    def get_province(self, code):
        """Dapatkan nama provinsi dari kode"""
        return self.province_codes.get(code, "Unknown")

    def get_district(self, code):
        """Dapatkan nama kabupaten/kota dari kode"""
        # Implementasi lookup kabupaten
        return f"District code: {code}"

    def get_birth_info(self, code):
        """Parse informasi tanggal lahir"""
        day = int(code[:2])
        if day > 40:  # Untuk perempuan
            day -= 40
        month = int(code[2:4])
        year = int(code[4:6])
        year += 1900 if year > 50 else 2000

        return {
            "date": f"{day:02d}",
            "month": f"{month:02d}",
            "year": str(year),
            "gender": "Perempuan" if int(code[:2]) > 40 else "Laki-laki"
        } 