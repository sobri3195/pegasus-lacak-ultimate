import logging
from datetime import datetime
import os
import json


class PegasusLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.setup_logger()

    def setup_logger(self):
        """Setup logging configuration"""
        log_file = f"{self.log_dir}/pegasus_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger('PegasusLacak')

    def log_activity(self, user, activity, status="success", details=None):
        """Log aktivitas pengguna"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "activity": activity,
            "status": status,
            "details": details
        }

        if status == "success":
            self.logger.info(f"User {user}: {activity}")
        else:
            self.logger.error(f"User {user}: {activity} - {details}")

        history_file = os.path.join(self.log_dir, "scan_history.jsonl")
        with open(history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

    def view_scan_history(self, console, limit=20):
        """Tampilkan riwayat scan terakhir"""
        history_file = os.path.join(self.log_dir, "scan_history.jsonl")
        if not os.path.exists(history_file):
            console.print("[yellow]Belum ada riwayat scan.[/yellow]")
            return

        with open(history_file, "r", encoding="utf-8") as f:
            lines = f.readlines()[-limit:]

        if not lines:
            console.print("[yellow]Belum ada riwayat scan.[/yellow]")
            return

        for line in lines:
            entry = json.loads(line)
            console.print(
                f"[cyan]{entry.get('timestamp')}[/cyan] | "
                f"[green]{entry.get('status', 'unknown')}[/green] | "
                f"{entry.get('activity', '')}"
            )
