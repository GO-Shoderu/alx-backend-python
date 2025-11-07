import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        
        sql = kwargs.get("query")
        if sql is None and len(args) >= 2:
            sql = args[1]

        if sql is None:
            return func(*args, **kwargs)

        if sql in query_cache:
            return query_cache[sql]

        result = func(*args, **kwargs)
        query_cache[sql] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

users = fetch_users_with_cache(query="SELECT * FROM users")

users_again = fetch_users_with_cache(query="SELECT * FROM users")


print(users)
print(users_again)
