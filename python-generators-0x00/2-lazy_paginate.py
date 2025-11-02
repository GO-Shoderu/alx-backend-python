#!/usr/bin/python3
"""
    Lazy pagination with generators.
"""

from seed import connect_to_prodev

def paginateusers(page_size, offset):
    
    if page_size <= 0:
        raise ValueError("page_size must be a positive integer")
    if offset < 0:
        raise ValueError("offset must be >= 0")

    conn = connect_to_prodev()
    cur = conn.cursor(dictionary=True)

    query = f"SELECT * FROM user_data LIMIT {int(page_size)} OFFSET {int(offset)}"
    cur.execute(query)
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

def paginate_users(page_size, offset):
    return paginateusers(page_size, offset)

def lazypaginate(page_size):
    
    offset = 0
    
    while True:
        page = paginateusers(page_size, offset)
        if not page:
            return
        yield page
        offset += page_size

lazy_paginate = lazypaginate
lazy_pagination = lazypaginate