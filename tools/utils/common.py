import re
import json
import hashlib
from datetime import datetime
from rich.table import Table
from rich.console import Console

console = Console()

def validate_phone(phone):
    """Validasi format nomor telepon"""
    pattern = r'^\+?62[0-9]{9,13}$'
    return bool(re.match(pattern, phone))

def validate_email(email):
    """Validasi format email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_ip(ip):
    """Validasi format IP address"""
    pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, ip))

def save_result(data, category, identifier):
    """Simpan hasil ke file JSON"""
    filename = f"output/{category}_{identifier}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return filename

def display_result_table(data, title):
    """Tampilkan hasil dalam format tabel"""
    table = Table(title=title)
    table.add_column("Informasi", style="cyan")
    table.add_column("Detail", style="yellow")
    
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value, indent=2)
        table.add_row(str(key), str(value))
    
    console.print(table) 