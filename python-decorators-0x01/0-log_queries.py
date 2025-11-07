from datetime import datetime
import sqlite3
import functools

def log_queries(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        sql = kwargs.get("query")

        if sql is None and len(args) > 0:
            sql = args[0]

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] SQL: {sql}")

        return fn(*args, **kwargs)
    
    return wrapper

@log_queries
def fetch_all_users(query):

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

users = fetch_all_users(query="SELECT * FROM users")
