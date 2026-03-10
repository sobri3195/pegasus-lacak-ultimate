#!/usr/bin/env python3
import os
import sys
import hashlib
import getpass
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import pyfiglet
from cryptography.fernet import Fernet
import json
from datetime import datetime
import platform
import signal
from rich.prompt import Prompt

# Import komponen
from tools.data.nik_processor import NIKProcessor
from tools.data.phone_processor import PhoneProcessor
from tools.data.email_processor import EmailProcessor
from tools.data.ip_processor import IPProcessor
from tools.social.social_analyzer import SocialAnalyzer
from tools.darkweb.darkweb_scanner import DarkWebScanner
from tools.web.web_recon import WebRecon
from tools.utils.logger import PegasusLogger
from tools.utils.encryption import PegasusEncryption
from tools.utils.report_generator import ReportGenerator

# Inisialisasi Rich Console
console = Console()
logger = PegasusLogger()

class PegasusLacak:
    def __init__(self):
        self.console = console
        self.logger = logger
        self.report_gen = ReportGenerator()
        
        # Initialize processors
        self.nik_processor = NIKProcessor()
        self.phone_processor = PhoneProcessor()
        self.email_processor = EmailProcessor()
        self.ip_processor = IPProcessor()
        self.social_analyzer = SocialAnalyzer()
        self.darkweb_scanner = DarkWebScanner()
        self.web_recon = WebRecon()
        
        self.setup_security()
        self.setup_directories()
        self.load_config()
        self.tools = self.load_tools()

    def setup_security(self):
        """Setup keamanan dan enkripsi"""
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.password_hash = hashlib.sha256('sobri'.encode()).hexdigest()

    def setup_directories(self):
        """Setup struktur direktori"""
        directories = ['config', 'tools', 'logs', 'output']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def load_config(self):
        """Load konfigurasi dari config/settings.json"""
        config_file = 'config/settings.json'
        if not os.path.exists(config_file):
            self.create_default_config(config_file)
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def create_default_config(self, config_file):
        """Buat konfigurasi default"""
        default_config = {
            'version': '1.0.0',
            'author': 'Letda Kes dr. Sobri',
            'max_login_attempts': 3,
            'log_level': 'INFO'
        }
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=4)

    def load_tools(self):
        """Load daftar tools"""
        return {
            "📱 Phone Tracking": {
                "PhoneInfoga": "Analisis nomor telepon",
                "TrueCaller": "Identifikasi pemilik nomor",
                "LocalPhoneDB": "Database nomor lokal",
                "CellLocator": "Pelacakan cell tower",
                "SMSAnalyzer": "Analisis SMS"
            },
            "💬 WhatsApp Analysis": {
                "WhatsAppTracker": "Monitor status online",
                "WA-Inspector": "Analisis profil WhatsApp",
                "ChatExporter": "Export riwayat chat",
                "StatusSaver": "Simpan status WhatsApp",
                "GroupAnalyzer": "Analisis grup WhatsApp"
            },
            "📧 Email Investigation": {
                "Holehe": "Verifikasi email",
                "EmailHarvester": "Pengumpulan email",
                "H8mail": "Cek kebocoran email",
                "DomainRecon": "Analisis domain",
                "HeaderAnalyzer": "Analisis header email"
            },
            "🆔 NIK/KTP Scanner": {
                "NIKValidator": "Validasi nomor KTP",
                "DemographicInfo": "Info demografis",
                "AddressTracker": "Pelacakan alamat",
                "FamilyTree": "Pohon keluarga",
                "DocumentScanner": "Scan dokumen KTP"
            },
            "🌍 IP Tracking": {
                "IPGeoLocation": "Lokasi geografis IP",
                "PortScanner": "Scanning port",
                "NetworkMapper": "Pemetaan jaringan",
                "PacketAnalyzer": "Analisis paket data",
                "DNSRecon": "Reconnaissance DNS"
            }
        }

    def show_banner(self):
        """Tampilkan banner aplikasi"""
        banner = pyfiglet.figlet_format("PEGASUS LACAK", font="slant")
        self.console.print(f"[bold red]{banner}[/bold red]")
        self.console.print(Panel.fit(
            "[bold yellow]Developed by: Letda Kes dr. Sobri[/bold yellow]\n"
            "[bold green]Version: 1.0.0[/bold green]"
        ))

    def authenticate(self):
        """Proses autentikasi pengguna"""
        attempts = 0
        max_attempts = self.config.get('max_login_attempts', self.config.get('settings', {}).get('max_login_attempts', 3))
        
        while attempts < max_attempts:
            try:
                password = getpass.getpass("[bold yellow]Enter Password: [/bold yellow]")
                if hashlib.sha256(password.encode()).hexdigest() == self.password_hash:
                    self.console.print("[bold green]Login Berhasil![/bold green]")
                    self.logger.log_activity("Login berhasil")
                    return True
                else:
                    attempts += 1
                    remaining = max_attempts - attempts
                    self.console.print(f"[bold red]Password Salah! Sisa percobaan: {remaining}[/bold red]")
                    self.logger.log_activity(f"Login gagal - Percobaan ke-{attempts}")
            except KeyboardInterrupt:
                self.console.print("\n[bold red]Program dihentikan oleh pengguna.[/bold red]")
                sys.exit(1)
        
        self.console.print("[bold red]Terlalu banyak percobaan gagal. Program dihentikan.[/bold red]")
        sys.exit(1)

    def log_activity(self, activity):
        """Catat aktivitas ke file log"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "activity": activity,
            "user": os.getenv('USER', 'unknown')
        }
        
        log_file = f"logs/activity_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')

    def main_menu(self):
        """Tampilkan menu utama"""
        while True:
            self.console.clear()
            self.show_banner()
            
            menu_items = [
                "[1] NIK Scanner",
                "[2] Phone Number Analysis",
                "[3] Email Investigation",
                "[4] IP Address Analysis",
                "[5] Social Media Analysis",
                "[6] Dark Web Scan",
                "[7] Website Reconnaissance",
                "[8] View Scan History",
                "[9] Settings",
                "[0] Exit"
            ]
            
            for item in menu_items:
                self.console.print(item)
                
            choice = Prompt.ask("\n[bold cyan]Select an option[/bold cyan]", choices=["1","2","3","4","5","6","7","8","9","0"])
            
            if choice == "0":
                self.console.print("[yellow]Thank you for using Pegasus Lacak Ultimate![/yellow]")
                sys.exit(0)
                
            self.handle_menu_choice(choice)
            
    def handle_menu_choice(self, choice):
        """Handle pilihan menu"""
        options = {
            "1": self.nik_scan_menu,
            "2": self.phone_scan_menu,
            "3": self.email_scan_menu,
            "4": self.ip_scan_menu,
            "5": self.social_scan_menu,
            "6": self.darkweb_scan_menu,
            "7": self.web_scan_menu,
            "8": self.view_history,
            "9": self.settings_menu
        }
        
        func = options.get(choice)
        if func:
            func()
            
    def nik_scan_menu(self):
        """Menu untuk NIK scanner"""
        self.console.clear()
        self.console.print("[bold]NIK Scanner[/bold]")
        
        nik = Prompt.ask("[cyan]Enter NIK[/cyan]")
        results = self.nik_processor.parse_nik(nik)
        
        if "error" not in results:
            self.display_results("NIK Analysis Results", results)
            self.save_results("nik", nik, results)
        else:
            self.console.print(f"[red]Error: {results['error']}[/red]")
            
        input("\nPress Enter to continue...")

    def phone_scan_menu(self):
        """Menu untuk analisis nomor telepon"""
        self.console.clear()
        self.console.print("[bold]Phone Number Analysis[/bold]")
        
        phone = Prompt.ask("[cyan]Enter phone number (format: +628xxx):[/cyan]")
        results = self.phone_processor.analyze_number(phone)
        self._display_and_save("Phone Analysis Results", "phone", phone, results)
        input("\nPress Enter to continue...")
        
    def email_scan_menu(self):
        """Menu untuk analisis email"""
        self.console.clear()
        self.console.print("[bold]Email Investigation[/bold]")
        
        email = Prompt.ask("[cyan]Enter email address:[/cyan]")
        results = self.email_processor.analyze_email(email)
        self._display_and_save("Email Analysis Results", "email", email, results)
        input("\nPress Enter to continue...")
        
    def ip_scan_menu(self):
        """Menu untuk analisis IP"""
        self.console.clear()
        self.console.print("[bold]IP Address Analysis[/bold]")
        
        ip = Prompt.ask("[cyan]Enter IP address:[/cyan]")
        results = self.ip_processor.analyze_ip(ip)
        self._display_and_save("IP Analysis Results", "ip", ip, results)
        input("\nPress Enter to continue...")
        
    def social_scan_menu(self):
        """Menu untuk analisis media sosial"""
        self.console.clear()
        self.console.print("[bold]Social Media Analysis[/bold]")
        
        username = Prompt.ask("[cyan]Enter username:[/cyan]")
        results = self.social_analyzer.analyze_username(username)
        self._display_and_save("Social Media Analysis Results", "social", username, results)
        input("\nPress Enter to continue...")
        
    def darkweb_scan_menu(self):
        """Menu untuk scan dark web"""
        self.console.clear()
        self.console.print("[bold]Dark Web Scan[/bold]")
        
        target_type = Prompt.ask("[cyan]Target type[/cyan]", choices=["email", "phone", "username", "ip"], default="email")
        target_value = Prompt.ask("[cyan]Target value:[/cyan]")
        results = self.darkweb_scanner.scan_target(target_type, target_value)
        self._display_and_save("Dark Web Scan Results", "darkweb", target_value, results)
        input("\nPress Enter to continue...")
        
    def web_scan_menu(self):
        """Menu untuk rekonstruksi website"""
        self.console.clear()
        self.console.print("[bold]Website Reconnaissance[/bold]")
        
        url = Prompt.ask("[cyan]Enter website URL:[/cyan]")
        domain = url.replace("https://", "").replace("http://", "").split('/')[0]
        results = self.web_recon.analyze_website(domain)
        self._display_and_save("Website Reconnaissance Results", "web", domain, results)
        input("\nPress Enter to continue...")
        
    def view_history(self):
        """Menu untuk melihat riwayat scan"""
        self.console.clear()
        self.console.print("[bold]Scan History[/bold]")
        
        self.logger.view_scan_history(self.console)
        input("\nPress Enter to continue...")
        
    def settings_menu(self):
        """Menu untuk mengatur pengaturan"""
        self.console.clear()
        self.console.print("[bold]Settings[/bold]")
        
        current_attempts = self.config.get('max_login_attempts', self.config.get('settings', {}).get('max_login_attempts', 3))
        self.console.print(f"Current max login attempts: [cyan]{current_attempts}[/cyan]")

        new_attempts = Prompt.ask(
            "[cyan]Set max login attempts (1-10), kosongkan untuk batal[/cyan]",
            default=str(current_attempts)
        )

        try:
            new_attempts_int = int(new_attempts)
            if 1 <= new_attempts_int <= 10:
                self.config['max_login_attempts'] = new_attempts_int
                with open('config/settings.json', 'w') as f:
                    json.dump(self.config, f, indent=4)
                self.console.print("[green]Settings updated successfully.[/green]")
            else:
                self.console.print("[red]Value must be between 1 and 10.[/red]")
        except ValueError:
            self.console.print("[red]Invalid input. Settings unchanged.[/red]")

        input("\nPress Enter to continue...")

    def _display_and_save(self, title, scan_type, target, results):
        if "error" in results:
            self.console.print(f"[red]Error: {results['error']}[/red]")
            return

        self.display_results(title, results)
        self.save_results(scan_type, target, results)

    def display_results(self, title, data):
        """Tampilkan hasil dalam format tabel"""
        self.report_gen.display_result_table(data, title)
        
    def save_results(self, scan_type, target, results):
        """Simpan hasil scan"""
        # Generate report
        report_files = self.report_gen.generate_report(results, scan_type)
        
        # Log activity
        self.logger.log_activity(
            "system",
            f"Scan completed: {scan_type} - {target}",
            "success",
            report_files
        )
        
        self.console.print(f"\n[green]Results saved:[/green]")
        for fmt, path in report_files.items():
            self.console.print(f"- {fmt.upper()}: {path}")

def check_system_requirements():
    """Cek persyaratan sistem"""
    if platform.system() not in ['Linux', 'Darwin']:
        console.print("[bold red]Error: Program ini hanya mendukung sistem Linux/Unix![/bold red]")
        sys.exit(1)

def main():
    try:
        check_system_requirements()
        app = PegasusLacak()
        app.main_menu()
    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Fatal error: {str(e)}[/red]")
        logger.log_activity("system", "Program crash", "error", str(e))

if __name__ == "__main__":
    # Handle Ctrl+C dengan lebih elegan
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
    main() 
