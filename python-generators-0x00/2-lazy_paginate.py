#!/usr/bin/python3
"""
    Lazy pagination with generators.
"""

from seed import connect_to_prodev


def paginate_users(page_size, offset):
    """
    Fetch a single page of users.

    Args:
        page_size (int): number of rows in a page (must be > 0)
        offset (int): starting offset in the table (must be >= 0)

    Returns:
        list[dict]: rows for this page
    """
    if page_size <= 0:
        raise ValueError("page_size must be a positive integer")
    if offset < 0:
        raise ValueError("offset must be >= 0")

    conn = connect_to_prodev()
    cur = conn.cursor(dictionary=True)

    # ORDER BY for deterministic paging
    cur.execute(
        """
        SELECT user_id, name, email, age
        FROM user_data
        ORDER BY user_id
        LIMIT %s OFFSET %s
        """,
        (int(page_size), int(offset)),
    )
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator that lazily yields pages (lists of dicts).

    Yields:
        list[dict]: next page of rows
    """
    offset = 0
    
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            return
        yield page
        offset += page_size


# Compatibility alias so that the 3-main.py (importing lazy_pagination) works.
lazy_pagination = lazy_paginate
