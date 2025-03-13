import random
import sqlite3

from config.config import CURRENCY_DATABASE, DATABASE


def choose_chest_update(user_id):
    conn = sqlite3.connect(CURRENCY_DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET count_curr=count_curr+20 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()


def get_user_currency(user_id):
    conn = sqlite3.connect(CURRENCY_DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT count_curr FROM users_premium_currency WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def update_currency(user_id, cost, subscription_type):
    current_currency = get_user_currency(user_id)
    if current_currency >= cost:
        conn = sqlite3.connect(CURRENCY_DATABASE)
        cursor = conn.cursor()
        conn_users = sqlite3.connect(DATABASE)
        cursor_user = conn_users.cursor()
        cursor.execute("UPDATE users_premium_currency SET count_curr = count_curr - ? WHERE user_id = ?",
                       (cost, user_id))
        conn.commit()
        cursor_user.execute("UPDATE users SET rights = 'premium' WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    else:
        return False


async def chest_game(user_id, chosen_chest):
    points = random.randint(5, 100)
    correct_chest = random.randint(1, 3)

    if chosen_chest == correct_chest:
        conn = sqlite3.connect(CURRENCY_DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users_premium_currency SET count_curr = count_curr + ?
            WHERE user_id = ?
        ''', (points, user_id))
        conn.commit()
        conn.close()

        return points, correct_chest
    else:
        return 0, correct_chest


async def add_points(user_id, points):
    conn = sqlite3.connect(CURRENCY_DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users_premium_currency WHERE user_id = ?", (user_id,))
    user_record = cursor.fetchone()

    if user_record:
        cursor.execute("UPDATE users_premium_currency SET count_curr = count_curr + ? WHERE user_id = ?",
                       (points, user_id))
    else:
        cursor.execute("INSERT INTO users_premium_currency (user_id, count_curr) VALUES (?, ?)", (user_id, points))

    conn.commit()
    conn.close()