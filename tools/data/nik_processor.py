from datetime import datetime

class NIKProcessor:
    def __init__(self):
        self.month_names = {
            "01": "Januari", "02": "Februari", "03": "Maret",
            "04": "April", "05": "Mei", "06": "Juni",
            "07": "Juli", "08": "Agustus", "09": "September",
            "10": "Oktober", "11": "November", "12": "Desember"
        }

    def parse_nik(self, nik):
        """Parse informasi dari NIK"""
        try:
            province_code = nik[:2]
            regency_code = nik[2:4]
            district_code = nik[4:6]
            birth_date = nik[6:8]
            birth_month = nik[8:10]
            birth_year = nik[10:12]
            sequence = nik[12:]

            # Proses tanggal lahir
            day = int(birth_date)
            gender = "Perempuan" if day > 40 else "Laki-laki"
            if day > 40:
                day -= 40

            # Proses tahun
            year = int(birth_year)
            if year < 30:  # Asumsi tahun 2000+
                year += 2000
            else:  # Asumsi tahun 1900+
                year += 1900

            return {
                "nik": nik,
                "wilayah": {
                    "provinsi_code": province_code,
                    "kabupaten_code": regency_code,
                    "kecamatan_code": district_code
                },
                "tanggal_lahir": {
                    "tanggal": str(day),
                    "bulan": self.month_names.get(birth_month, birth_month),
                    "tahun": str(year),
                    "lengkap": f"{day} {self.month_names.get(birth_month, birth_month)} {year}"
                },
                "jenis_kelamin": gender,
                "kode_unik": sequence,
                "umur": self.calculate_age(day, int(birth_month), year)
            }
        except Exception as e:
            return {"error": f"Format NIK tidak valid: {str(e)}"}

    def calculate_age(self, day, month, year):
        """Hitung umur berdasarkan tanggal lahir"""
        today = datetime.now()
        age = today.year - year
        
        # Kurangi 1 tahun jika belum ulang tahun
        if month > today.month or (month == today.month and day > today.day):
            age -= 1
            
        return age 