import asyncio
import sqlite3
import aiosqlite

DB_PATH = "example.db"

async def async_fetch_users():
    
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        async with db.execute("SELECT * FROM users") as cur:
            rows = await cur.fetchall()
            return rows

async def async_fetch_older_users():
    
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cur:
            rows = await cur.fetchall()
            return rows

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All users:")
    for r in all_users:
        print(f"- id={r['id']}, name={r['name']}, age={r['age']}, email={r['email']}")

    print("\nUsers older than 40:")
    for r in older_users:
        print(f"- id={r['id']}, name={r['name']}, age={r['age']}, email={r['email']}")

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
