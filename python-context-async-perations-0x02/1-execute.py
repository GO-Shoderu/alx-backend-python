import sqlite3
from typing import Optional, Sequence, Any, List

class ExecuteQuery:
    
    def __init__(self, db_path: str, sql: str, params: Optional[Sequence[Any]] = None):
        self.db_path = db_path
        self.sql = sql
        self.params = params or []
        self.conn: Optional[sqlite3.Connection] = None
        self.rows: Optional[List[sqlite3.Row]] = None

    def __enter__(self) -> List[sqlite3.Row]:
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        cur.execute(self.sql, self.params)
        self.rows = cur.fetchall()
        cur.close()
        
        return self.rows

    def __exit__(self, exc_type, exc, tb) -> bool:
        try:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
        finally:
            self.conn.close()
            
        return False

def _seed(db_path: str):
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER NOT NULL
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO users(name, email, age) VALUES (?, ?, ?)",
                [
                    ("Ada Lovelace", "ada@example.com", 36),
                    ("Grace Hopper", "grace@example.com", 85),
                    ("Guido van Rossum", "guido@example.com", 31),
                    ("Linus Torvalds", "linus@example.com", 24),
                ],
            )
        conn.commit()


if __name__ == "__main__":
    db_file = "example.db"
    _seed(db_file)  
    
    sql = "SELECT * FROM users WHERE age > ?"
    params = [25]

    with ExecuteQuery(db_file, sql, params) as results:
        print("Users with age > 25:")
        for r in results:
            print(f"- id={r['id']}, name={r['name']}, age={r['age']}, email={r['email']}")
