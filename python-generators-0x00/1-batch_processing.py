#!/usr/bin/python3
"""
    Batch processing with generators.

        - stream_users_in_batches(batch_size): generator yielding lists of rows
        - batch_processing(batch_size): prints users with age > 25
"""

from seed import connect_to_prodev
from decimal import Decimal
from contextlib import suppress

def stream_users_in_batches(batch_size):
    """
        Generator that yields rows from user_data in batches of `batch_size`.
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be a positive integer")

    conn = connect_to_prodev()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT user_id, name, email, age FROM user_data ORDER BY user_id")

    for batch in iter(lambda: cur.fetchmany(batch_size), []):
        yield batch

    cur.close()
    conn.close()

def _normalize(row):
    """ Normalize row data types as needed. """
    if isinstance(row.get("age"), Decimal):
        row = dict(row)              # copy so we don't mutate connector internals
        row["age"] = int(row["age"])
    return row

def batch_processing(batch_size):
    """
        Processes each batch and prints users with age > 25.
    """
    with suppress(BrokenPipeError):
        for batch in stream_users_in_batches(batch_size):          # loop 1
            for row in batch:                                      # loop 2
                r = _normalize(row)
                if r.get("age") is not None and r["age"] > 25:
                    print(r, end="\n\n")
