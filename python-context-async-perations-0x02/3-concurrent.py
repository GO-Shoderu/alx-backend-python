import asyncio
import sqlite3
import aiosqlite

DB_PATH = "example.db"


async def async_fetch_users(db_path: str = DB_PATH):
    
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        async with db.execute("SELECT * FROM users") as cur:
            rows = await cur.fetchall()
            return rows


async def async_fetch_older_users(db_path: str = DB_PATH, min_age: int = 40):
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        async with db.execute("SELECT * FROM users WHERE age > ?", (min_age,)) as cur:
            rows = await cur.fetchall()
            return rows


async def fetch_concurrently(db_path: str = DB_PATH):
    
    all_users_task = async_fetch_users(db_path)
    older_users_task = async_fetch_older_users(db_path, 40)

    all_users, older_users = await asyncio.gather(all_users_task, older_users_task)

    print("All users:")
    for r in all_users:
        # Works because of row_factory = sqlite3.Row
        print(f"- id={r['id']}, name={r['name']}, age={r.get('age')}, email={r['email']}")

    print("\nUsers older than 40:")
    for r in older_users:
        print(f"- id={r['id']}, name={r['name']}, age={r['age']}, email={r['email']}")


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
