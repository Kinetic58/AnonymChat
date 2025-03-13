import asyncio
import random
import sqlite3

from config.config import QUEUE_DATA, bot, TABLE
from different_function.admin import get_user_status, update_user_status


def create_chat_room(user_id, partner_id):
    conn = sqlite3.connect(TABLE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO table_db (user_id, partner_id) VALUES (?, ?)''', (user_id, partner_id))
    conn.commit()
    conn.close()


def delete_chat_room(user_id):
    conn = sqlite3.connect(TABLE)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM table_db WHERE user_id = ? OR partner_id = ?''', (user_id, user_id))
    conn.commit()
    conn.close()


async def find_partner(user_id):
    while True:
        conn = sqlite3.connect(QUEUE_DATA)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users_queue WHERE user_id != ? AND status_queue = 'WAIT' ''', (user_id,))
        partners = cursor.fetchall()
        conn.close()

        if partners:
            partner_id = random.choice(partners)[1]

            user_status = get_user_status(user_id)
            partner_status = get_user_status(partner_id)

            if user_status not in ['TALK', 'NOT WAIT'] and partner_status not in ['TALK', 'NOT WAIT']:
                update_user_status(user_id, 'TALK')
                update_user_status(partner_id, 'TALK')
                create_chat_room(user_id, partner_id)
                await bot.send_message(user_id,
                                       "✨ <b>Собеседник найден!</b> ✨\n\n"
                                       "<i>Приятного общения!</i>\n\n"
                                       "🛑 Если желаете завершить чат - нажмите на /stop", parse_mode='HTML')
                await bot.send_message(partner_id,
                                       "✨ <b>Собеседник найден!</b> ✨\n\n"
                                       "<i>Приятного общения!</i>\n\n"
                                       "🛑 Если желаете завершить чат - нажмите на /stop", parse_mode='HTML')
                break
            else:
                await asyncio.sleep(10)
        else:
            await asyncio.sleep(10)


async def find_premium_partner(user_id):
    while True:
        conn = sqlite3.connect(QUEUE_DATA)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users_queue WHERE user_id != ? AND status_queue = 'PREMIUM_WAIT' ''',
                       (user_id,))
        partners = cursor.fetchall()
        conn.close()

        if partners:
            partner_id = random.choice(partners)[1]

            user_status = get_user_status(user_id)
            partner_status = get_user_status(partner_id)

            if user_status not in ['TALK', 'NOT WAIT', 'WAIT'] and partner_status not in ['TALK', 'NOT WAIT', 'WAIT']:
                update_user_status(user_id, 'TALK')
                update_user_status(partner_id, 'TALK')
                create_chat_room(user_id, partner_id)
                await bot.send_message(user_id,
                                       "✨ <b>Собеседник найден!</b> ✨\n\n"
                                       "<i>Приятного общения!</i>\n\n"
                                       "🛑 Если желаете завершить чат - нажмите на /stop", parse_mode='HTML')
                await bot.send_message(partner_id,
                                       "✨ <b>Собеседник найден!</b> ✨\n\n"
                                       "<i>Приятного общения!</i>\n\n"
                                       "🛑 Если желаете завершить чат - нажмите на /stop", parse_mode='HTML')
                break
            else:
                await asyncio.sleep(10)
        else:
            await asyncio.sleep(10)



