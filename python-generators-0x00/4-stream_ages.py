#!/usr/bin/python3
"""
    Memory-efficient average age computation using generators.
"""

from seed import connect_to_prodev
from decimal import Decimal


def stream_user_ages():
    """
        Generator that yields each user's age one by one.
    """
    conn = connect_to_prodev()
    cur = conn.cursor()

    # Single query to stream ages lazily
    cur.execute("SELECT age FROM user_data")

    for (age,) in cur:
        yield int(age) if isinstance(age, Decimal) else age

    cur.close()
    conn.close()


def compute_average_age():
    
    total = 0
    count = 0

    # One loop to consume the generator
    for age in stream_user_ages():
        total += age
        count += 1

    avg = total / count if count else 0
    print(f"Average age of users: {avg:.2f}")


# Allow running directly
if __name__ == "__main__":
    compute_average_age()
