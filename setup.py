import os
import json
import sys
from rich.console import Console
from rich.prompt import Prompt
from cryptography.fernet import Fernet

console = Console()

def setup_environment():
    """Setup lingkungan aplikasi"""
    try:
        # Buat direktori
        directories = ['config', 'tools', 'logs', 'output']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            console.print(f"[green]✓[/green] Membuat direktori {directory}")

        # Generate kunci enkripsi
        key = Fernet.generate_key()
        with open('config/security.key', 'wb') as f:
            f.write(key)
        console.print("[green]✓[/green] Generate kunci enkripsi")

        # Setup konfigurasi
        setup_config()
        
        console.print("\n[bold green]Setup berhasil![/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]Error during setup: {str(e)}[/bold red]")
        sys.exit(1)

def setup_config():
    """Setup file konfigurasi"""
    config = {
        "version": "1.0.0",
        "author": "Letda Kes dr. Sobri",
        "max_login_attempts": 3,
        "log_level": "INFO",
        "api_keys": {}
    }
    
    # Tanya API keys
    console.print("\n[bold]Setup API Keys[/bold]")
    apis = ["truecaller", "ipapi", "shodan"]
    for api in apis:
        key = Prompt.ask(f"Masukkan API key untuk {api} (kosongkan jika tidak ada)")
        if key:
            config["api_keys"][api] = key

    # Simpan konfigurasi
    with open('config/settings.json', 'w') as f:
        json.dump(config, f, indent=4)
    console.print("[green]✓[/green] Menyimpan konfigurasi")

if __name__ == "__main__":
    console.print("[bold]🦄 Pegasus-Lacak-Ultimate Setup[/bold]")
    setup_environment() 