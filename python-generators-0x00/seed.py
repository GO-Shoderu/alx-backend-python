#!/usr/bin/env python3
"""
seed.py
Prototypes required by the task:

- connect_db() -> connects to the MySQL server (no specific DB yet)
- create_database(connection) -> creates ALX_prodev if it does not exist
- connect_to_prodev() -> connects to the ALX_prodev database
- create_table(connection) -> creates user_data with required fields
- insert_data(connection, csv_path) -> inserts CSV rows if not present
"""

import csv
import os
import uuid
from typing import Optional

import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv


# Load app-side DB settings from .app.env (not the Docker env)
load_dotenv(".app.env")

DB_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("MYSQL_PORT", "3306"))
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = os.getenv("MYSQL_DB", "ALX_prodev")


def _connect(db: Optional[str] = None):
    """Internal helper to connect with or without a specific database."""
    kwargs = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "autocommit": False,  # we control commits
    }
    if db:
        kwargs["database"] = db
    return mysql.connector.connect(**kwargs)


def connect_db():
    """Connecting to the MySQL server."""
    try:
        conn = _connect(db=None)
        return conn
    except mysql.connector.Error as err:
        print(f"[connect_db] Error: {err}")
        return None


def create_database(connection):
    """Creating the database ALX_prodev if it does not exist."""
    try:
        cur = connection.cursor()
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
        connection.commit()
        cur.close()
        print(f"Database {DB_NAME} created/ensured")
    except mysql.connector.Error as err:
        print(f"[create_database] Error: {err}")
        try:
            connection.rollback()
        except Exception:
            pass


def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        conn = _connect(db=DB_NAME)
        return conn
    except mysql.connector.Error as err:
        print(f"[connect_to_prodev] Error: {err}")
        return None


def create_table(connection):
    """
        Creating table user_data if it does not exist.
    """

    create_sql = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) NOT NULL,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL,
        PRIMARY KEY (user_id),
        UNIQUE KEY uniq_email (email)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    try:
        cur = connection.cursor()
        cur.execute(create_sql)
        connection.commit()
        cur.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"[create_table] Error: {err}")
        try:
            connection.rollback()
        except Exception:
            pass


def _row_exists_by_email(connection, email: str) -> bool:
    """
        Checking if a row exists given an email
    """

    sql = "SELECT 1 FROM user_data WHERE email=%s LIMIT 1;"
    cur = connection.cursor()
    cur.execute(sql, (email,))
    found = cur.fetchone() is not None
    cur.close()
    return found

def insert_data(connection, csv_path: str):
    """
        Inserting data from CSV into user_data if not already present.
    """
    
    if not os.path.exists(csv_path):
        print(f"[insert_data] CSV not found: {csv_path}")
        return

    def _clean_str(val):
        return val.strip() if isinstance(val, str) else None

    insert_sql = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
          name=VALUES(name),
          age=VALUES(age)
    """

    inserted = 0
    skipped = 0
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Normalize header keys to lower-case lookups
            field_map = { (k or "").strip().lower(): k for k in reader.fieldnames or [] }
            name_key  = field_map.get("name")
            email_key = field_map.get("email")
            age_key   = field_map.get("age")

            if not (name_key and email_key and age_key):
                print("[insert_data] CSV is missing one of the headers: name,email,age")
                return

            cur = connection.cursor()
            for row in reader:
                if not row:
                    skipped += 1
                    continue

                name  = _clean_str(row.get(name_key))
                email = _clean_str(row.get(email_key))
                age_raw = row.get(age_key)

                # Skip blank/malformed lines early
                if not name or not email or age_raw in (None, ""):
                    skipped += 1
                    continue

                try:
                    age = int(str(age_raw).strip())
                except (ValueError, TypeError):
                    skipped += 1
                    continue

                cur.execute(
                    insert_sql,
                    (str(uuid.uuid4()), name, email, age)
                )
                inserted += 1

            connection.commit()
            cur.close()

        print(f"Inserted/updated {inserted} rows from {csv_path} (skipped {skipped})")
    except mysql.connector.Error as err:
        print(f"[insert_data] DB Error: {err}")
        try:
            connection.rollback()
        except Exception:
            pass
    except Exception as ex:
        print(f"[insert_data] General Error: {ex}")
