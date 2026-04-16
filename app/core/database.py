import sqlite3
from typing import Optional, List, Dict


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("electro.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    # =========================
    # Tables
    # =========================
    def create_tables(self):
        cursor = self.conn.cursor()

        # Clients (CRM)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            industry TEXT,
            contact TEXT
        )
        """)

        # Equipment
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            client_id INTEGER,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
        """)

        # Work Orders (MMS)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            client_id INTEGER,
            equipment_id INTEGER,
            priority TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (equipment_id) REFERENCES equipment(id)
        )
        """)

        # Maintenance History
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            equipment_id INTEGER,
            issue TEXT,
            solution TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    # =========================
    # Clients
    # =========================
    def create_client(self, name: str, industry: str = "", contact: str = ""):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO clients (name, industry, contact) VALUES (?, ?, ?)",
            (name, industry, contact)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_client(self, client_id: Optional[int]) -> Optional[Dict]:
        if not client_id:
            return None

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    # =========================
    # Equipment
    # =========================
    def create_equipment(self, name: str, eq_type: str, client_id: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO equipment (name, type, client_id) VALUES (?, ?, ?)",
            (name, eq_type, client_id)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_equipment(self, equipment_id: Optional[int]) -> Optional[Dict]:
        if not equipment_id:
            return None

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM equipment WHERE id = ?", (equipment_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    # =========================
    # Work Orders
    # =========================
    def create_work_order(
        self,
        title: str,
        description: str,
        client_id: Optional[int],
        equipment_id: Optional[int],
        priority: str = "MEDIUM",
        status: str = "OPEN"
    ):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO work_orders
            (title, description, client_id, equipment_id, priority, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, client_id, equipment_id, priority, status))

        self.conn.commit()
        return cursor.lastrowid

    def get_work_orders(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM work_orders ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    # =========================
    # Maintenance History
    # =========================
    def add_history(
        self,
        client_id: Optional[int],
        equipment_id: Optional[int],
        issue: str,
        solution: str
    ):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO maintenance_history
            (client_id, equipment_id, issue, solution)
            VALUES (?, ?, ?, ?)
        """, (client_id, equipment_id, issue, solution))

        self.conn.commit()

    def get_history(self, client_id: Optional[int]) -> List[Dict]:
        if not client_id:
            return []

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM maintenance_history
            WHERE client_id = ?
            ORDER BY created_at DESC
        """, (client_id,))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]
