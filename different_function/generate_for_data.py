import random
import sqlite3
import string

from config.config import INTEREST


def generate_random_string():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def update_interest(user_id, column, value):
    conn = sqlite3.connect(INTEREST)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE interest SET {column} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()


def add_or_update_user(user_id, username):
    conn = sqlite3.connect(INTEREST)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO interest (user_id, username) VALUES (?, ?)
                      ON CONFLICT(user_id) DO UPDATE SET username=excluded.username''', (user_id, username))
    conn.commit()
    conn.close()
