import sqlite3

from config.config import DATABASE, MESSAGE_DATA, QUEUE_DATA, TABLE, CURRENCY_DATABASE, REGISTER_DB, INTEREST


def create_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                      id INTEGER PRIMARY KEY,
                      user_id INTEGER,
                      username TEXT,
                      rights TEXT,
                      label TEXT,
                      subscription INTEGER,
                      notification TEXT
                      )''')
    conn.commit()
    conn.close()


def create_history_db():
    conn = sqlite3.connect(MESSAGE_DATA)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history_chat(
                      id INTEGER PRIMARY KEY,
                      user_id INTEGER,
                      recipient TEXT,
                      message TEXT,
                      date TEXT
                      )''')
    conn.commit()
    conn.close()


def create_queue_db():
    conn = sqlite3.connect(QUEUE_DATA)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users_queue(
                      id INTEGER PRIMARY KEY,
                      user_id INTEGER,
                      username TEXT,
                      status_queue TEXT
                      )''')
    conn.commit()
    conn.close()


def currency_db():
    conn = sqlite3.connect(CURRENCY_DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_premium_currency(
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            username TEXT,
            count_curr INTEGER)
        ''')
    conn.commit()
    conn.close()


def create_table_for_people():
    conn = sqlite3.connect(TABLE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS table_db(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    partner_id INTEGER)''')
    conn.commit()
    conn.close()


def create_table_for_interests():
    conn = sqlite3.connect(INTEREST)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS interest(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    username TEXT,
    interest_gender TEXT,
    interest_age INTEGER,
    interest_town TEXT,
    interest_chat TEXT
    )''')
    conn.commit()
    conn.close()

