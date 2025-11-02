#!/usr/bin/python3
"""
Generator that streams rows one by one from the user_data table.
"""

from seed import connect_to_prodev

def stream_users():
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT user_id, name, email, age FROM user_data ORDER BY user_id"
    )

    # single loop requirement
    for row in iter(lambda: cursor.fetchone(), None):
        yield row

    cursor.close()
    conn.close()