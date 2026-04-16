import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("electro.db", check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT
        )
        """)

        self.conn.commit()

    def insert_work_order(self, description):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO work_orders (description) VALUES (?)",
            (description,)
        )
        self.conn.commit()

    def get_work_orders(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM work_orders")
        return cursor.fetchall()
