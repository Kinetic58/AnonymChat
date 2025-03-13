import asyncio
import random
import sqlite3
import string
from datetime import datetime, timedelta

from config.config import bot, dp, DATABASE, MESSAGE_DATA, QUEUE_DATA, TABLE, CURRENCY_DATABASE
from user_keyboard.keyboard import admin_menu, user_menu, premium_user_menu


def get_chat_room(user_id):
    conn = sqlite3.connect(TABLE)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM table_db WHERE user_id = ? OR partner_id = ?''', (user_id, user_id))
    chat_room = cursor.fetchone()
    conn.close()
    return chat_room


def get_recipient_id(message):
    user_id = message.from_user.id
    chat_room = get_chat_room(user_id)
    if chat_room:
        partner_id = chat_room[2] if chat_room[1] == user_id else chat_room[1]
        return partner_id
    else:
        return None


def save_message(user_id, recipient_id, text, date):
    conn = sqlite3.connect(MESSAGE_DATA)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO history_chat (user_id, recipient, message, date) VALUES (?, ?, ?, ?)''',
                   (user_id, recipient_id, text, date))
    conn.commit()
    conn.close()


def get_user_status(user_id):
    conn = sqlite3.connect(QUEUE_DATA)
    cursor = conn.cursor()
    cursor.execute('''SELECT status_queue FROM users_queue WHERE user_id = ?''', (user_id,))
    user_status = cursor.fetchone()[0]
    conn.close()
    return user_status


def update_user_status(user_id, status):
    conn = sqlite3.connect(QUEUE_DATA)
    cursor = conn.cursor()
    cursor.execute('''UPDATE users_queue SET status_queue = ? WHERE user_id = ?''', (status, user_id))
    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users''')
    users = cursor.fetchall()
    conn.close()
    return users


def get_all_messages():
    conn = sqlite3.connect(MESSAGE_DATA)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM history_chat''')
    messages = cursor.fetchall()
    conn.close()
    return messages


def get_active_tables():
    conn = sqlite3.connect(TABLE)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM table_db''')
    tables = cursor.fetchall()
    conn.close()
    return tables


def get_user_rights(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT rights FROM users WHERE user_id = ?", (user_id,))
    rights = cursor.fetchone()
    conn.close()
    return rights[0] if rights else None


async def get_menu_markup(user_rights):
    if user_rights == 'admin':
        return await admin_menu()
    elif user_rights == 'premium':
        return await premium_user_menu()
    else:
        return await user_menu()


def find_user_by_username(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data


def find_user_by_username_2(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username=?", (username,))
    user_id = cursor.fetchone()
    conn.close()

    if user_id:
        return user_id[0]
    else:
        return None


def update_subscription(user_id, new_subscription_status):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET rights=? WHERE user_id=?", (new_subscription_status, user_id))
    conn.commit()
    conn.close()


def find_messages_by_user_id(user_id):
    conn = sqlite3.connect(MESSAGE_DATA)
    cursor = conn.cursor()
    cursor.execute("SELECT message, user_id, recipient FROM history_chat WHERE user_id = ? OR recipient = ?",
                   (user_id, user_id))
    messages = cursor.fetchall()
    conn.close()
    return messages


def get_users_with_notification_enabled():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE notification = 'Включены'")
    users = cursor.fetchall()
    conn.close()
    return users


def find_user_by_user_id(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data


def get_all_admin_ids():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE rights='admin'")
    admin_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return admin_ids


def find_table_info_by_user_id(user_id):
    conn = sqlite3.connect(TABLE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table_db WHERE user_id = ?", (user_id,))
    table_info = cursor.fetchone()
    conn.close()
    return table_info



