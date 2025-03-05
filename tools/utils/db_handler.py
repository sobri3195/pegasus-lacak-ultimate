import sqlite3
import json
from datetime import datetime
import os

class DatabaseHandler:
    def __init__(self, db_file="config/pegasus.db"):
        self.db_file = db_file
        self.setup_database()
        
    def setup_database(self):
        """Setup database dan tabel"""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        # Buat tabel untuk menyimpan hasil scan
        c.execute('''
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                scan_type TEXT,
                target TEXT,
                result_data TEXT,
                status TEXT
            )
        ''')
        
        # Buat tabel untuk log aktivitas
        c.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user TEXT,
                activity TEXT,
                details TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def save_scan_result(self, scan_type, target, result_data, status="success"):
        """Simpan hasil scan ke database"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO scan_results (timestamp, scan_type, target, result_data, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            scan_type,
            target,
            json.dumps(result_data),
            status
        ))
        
        conn.commit()
        conn.close()
        
    def get_scan_history(self, scan_type=None, limit=50):
        """Ambil riwayat scan"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        if scan_type:
            c.execute('''
                SELECT * FROM scan_results 
                WHERE scan_type = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (scan_type, limit))
        else:
            c.execute('''
                SELECT * FROM scan_results 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
        results = c.fetchall()
        conn.close()
        
        return [{
            "id": r[0],
            "timestamp": r[1],
            "scan_type": r[2],
            "target": r[3],
            "result_data": json.loads(r[4]),
            "status": r[5]
        } for r in results] 