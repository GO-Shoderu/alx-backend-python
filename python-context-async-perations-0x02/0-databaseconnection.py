import sqlite3
from typing import Optional

class DatabaseConnection:
    
    def __init__(self, path: str):
        self.path = path
        self.conn: Optional[sqlite3.Connection] = None

    def __enter__(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        
        return self.conn

    def __exit__(self, exc_type, exc, tb) -> bool:
        try:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
        finally:
            self.conn.close()
        return False


def _seed(conn: sqlite3.Connection) -> None:
    
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    count = cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO users(name, email) VALUES (?, ?)",
            [
                ("Ada Lovelace", "ada@example.com"),
                ("Grace Hopper", "grace@example.com"),
                ("Guido van Rossum", "guido@example.com"),
            ],
        )

if __name__ == "__main__":
    with DatabaseConnection("example.db") as conn:
        _seed(conn)

        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        print("Users:")
        for r in rows:
            print(f"- id={r['id']}, name={r['name']}, email={r['email']}")
