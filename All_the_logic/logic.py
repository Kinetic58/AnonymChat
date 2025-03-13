import os
import random
import sqlite3
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from different_function.generate_for_data import generate_random_string, update_interest
from different_function.game import get_user_currency, update_currency, chest_game, add_points
from different_function.search_and_dialog import find_partner, delete_chat_room, find_premium_partner
from user_keyboard.keyboard import user_menu, premium_user_menu, admin_menu, game_menu, back_menu, cancel_markup, \
    subs_buy, chest_menu, greater_or_lower_menu, get_cancel_button, rules_menu_key, start_prem_search, gender_keyboard, \
    get_interests_keyboard
from config.config import bot, dp, REGISTER_DB
from different_function.admin import get_recipient_id, save_message, update_user_status, \
 \
    get_chat_room, get_all_users, get_all_messages, get_active_tables, get_user_rights, \
    get_menu_markup, find_user_by_username, update_subscription, find_messages_by_user_id, get_all_admin_ids, \
    find_user_by_user_id, get_users_with_notification_enabled, find_table_info_by_user_id, \
    find_user_by_username_2
from config.config import DATABASE, QUEUE_DATA, CURRENCY_DATABASE
from all_state.finite_state_ma import SomeState, SpamState, TableState, AnonSMS, Registration, Form


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    conn_users = sqlite3.connect(DATABASE)
    conn_queue = sqlite3.connect(QUEUE_DATA)
    cursor_users = conn_users.cursor()
    cursor_queue = conn_queue.cursor()
    conn_balance = sqlite3.connect(CURRENCY_DATABASE)
    cursor_balance = conn_balance.cursor()

    cursor_users.execute("SELECT * FROM users WHERE user_id = ?", (message.from_user.id,))
    user_data = cursor_users.fetchone()
    if user_data:
        user_rights = user_data[3]
        if user_rights == 'admin':
            with open('image/KINETIC_WITH_LOVE.jpg', 'rb') as photo:
                await message.reply_photo(photo)
            await message.reply(f'Добрый день, <b>{message.from_user.username}</b>! 😊\n\n'
                                f'Добро пожаловать в меню администратора! 🛠️\n\n'
                                f'Что бы вы хотели узнать сегодня? 🤔\n\n'
                                f'<b>Выберите доступную опцию:</b>',
                                parse_mode='HTML', reply_markup=await admin_menu())
        if user_rights == 'user':
            with open('image/KINETIC_WITH_LOVE.jpg', 'rb') as photo:
                await message.reply_photo(photo)
            await message.reply(f'Добрый день, <b>{message.from_user.username}</b>! 😊\n\n'
                                f'Добро пожаловать в главное меню! 🚀\n\n'
                                f'Давайте посмотрим, что у нас здесь новенького! 📩\n\n'
                                f'<b>Выберите доступную опцию:</b>',
                                parse_mode='HTML', reply_markup=await user_menu())
        if user_rights == 'premium':
            with open('image/KINETIC_WITH_LOVE.jpg', 'rb') as photo:
                await message.reply_photo(photo)
            await message.reply(f'Добрый день, <b>{message.from_user.username}</b>! 😊\n\n'
                                f'Добро пожаловать в главное меню для Premium подписчиков! 🚀\n\n'
                                f'Давайте посмотрим, что у нас здесь новенького! 📩\n\n'
                                f'<b>Выберите доступную опцию:</b>',
                                parse_mode='HTML', reply_markup=await premium_user_menu())
    else:
        cursor_users.execute(
            "INSERT INTO users (user_id, username, rights, label, subscription, notification) VALUES (?, ?, ?, ?, ?, ?)",
            (message.from_user.id, message.from_user.username, 'user', generate_random_string(), 0, 'Включены')
        )
        conn_users.commit()

        cursor_queue.execute(
            "INSERT INTO users_queue (user_id, username, status_queue) VALUES (?, ?, ?)",
            (message.from_user.id, message.from_user.username, 'NOT WAIT')
        )
        conn_queue.commit()

        cursor_balance.execute(
            '''INSERT INTO users_premium_currency (user_id, username, count_curr) VALUES (?, ?, ?)''',
            (message.from_user.id, message.from_user.username, 0))
        conn_balance.commit()
        with open('image/KINETIC_WITH_LOVE.jpg', 'rb') as photo:
            await message.reply_photo(photo)
        await message.reply(f'Добрый день, <b>{message.from_user.username}</b>! 😊\n\n'
                            f'Рад видеть тебя здесь! 🎉\n\n'
                            f'Я - бот, который поможет тебе отправить анонимное сообщение! 📬\n\n'
                            f'Давай я покажу, что умею! 💪\n\n'
                            f'<b>Выбери интересующий тебя функционал:</b>',
                            parse_mode='HTML', reply_markup=await user_menu())

    conn_users.close()
    conn_queue.close()
    await message.delete()


@dp.callback_query_handler(lambda query: query.data == 'rules')
async def rules_menu(query: types.CallbackQuery):
    message_text = (
        '<b>Приветствуем вас в разделе правил пользования!</b> 📜\n\n'
        'Здесь вы найдете все необходимые сведения о правилах пользования, тарифах и нашей политике '
        'конфиденциальности. Просто нажмите на соответствующую кнопку ниже и ознакомьтесь с деталями:'
    )
    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text=message_text, reply_markup=await rules_menu_key(), parse_mode='HTML')


@dp.callback_query_handler(lambda query: query.data == 'profile')
async def profile_callback(query: types.CallbackQuery):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    user_id = query.from_user.id
    cursor.execute("SELECT user_id, username, rights, label, subscription, notification FROM users "
                   "WHERE "
                   "user_id=?", (user_id,))

    user_data = cursor.fetchone()

    if user_data:
        user_id, username, rights, label, subscription, notification = user_data
        message_text = (
            f"<b>Профиль пользователя:</b>\n\n"
            f"👤 <strong>ID пользователя:</strong> {user_id}\n"
            f"👨‍💼 <strong>Имя пользователя:</strong> {username}\n"
            f"🔑 <strong>Права:</strong> {rights}\n"
            f"🏷️ <strong>Метка:</strong> {label}\n"
            f"🔔 <strong>Уведомления: {notification}</strong>\n\n"
            "Нажмите кнопку 'Назад', чтобы вернуться в главное меню."
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton('💰 Оплатить подписку', callback_data='payment_choose'))
        keyboard.row(types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu_ru'))

        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text=message_text, reply_markup=keyboard, parse_mode='HTML')


@dp.callback_query_handler(lambda query: query.data == 'back_to_menu_ru')
async def back_to_ru_menu(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_rights = get_user_rights(user_id)
    keyboard_markup = None

    if user_rights == 'admin':
        keyboard_markup = await admin_menu()
    elif user_rights == 'premium':
        keyboard_markup = await premium_user_menu()
    else:
        keyboard_markup = await user_menu()

    if keyboard_markup:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        user_id = query.from_user.id
        cursor.execute("SELECT username FROM users "
                       "WHERE "
                       "user_id=?", (user_id,))

        user_data = cursor.fetchone()
        if user_data:
            username = user_data[0]
            message_text = (
                f'Добрый день, <b>{username}</b>! 😊\n\n'
                f'Добро пожаловать в главное меню! 🚀\n\n'
                f'Давайте посмотрим, что у нас здесь новенького! 📩\n\n'
                f'<b>Выберите доступную опцию:</b>'
            )
            await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                        text=message_text, reply_markup=keyboard_markup, parse_mode='HTML')
        conn.close()
    else:
        pass


@dp.callback_query_handler(lambda c: c.data == 'start_search')
async def start_search(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    update_user_status(user_id, 'WAIT')
    await bot.send_message(user_id, "🔍 <b>Поиск собеседника...</b> 🔍\n\n"
                                    "<i>Среднее время ожидания - 10 секунд</i>", parse_mode='HTML')
    await find_partner(user_id)


@dp.message_handler(commands=['stop'])
async def stop_chat(message: types.Message):
    user_id = message.from_user.id
    chat_room = get_chat_room(user_id)

    if chat_room:
        partner_id = chat_room[2] if chat_room[1] == user_id else chat_room[1]
        delete_chat_room(user_id)
        update_user_status(user_id, 'NOT WAIT')
        update_user_status(partner_id, 'NOT WAIT')

        user_rights = get_user_rights(user_id)
        partner_rights = get_user_rights(partner_id)

        user_menu_markup = await get_menu_markup(user_rights)
        partner_menu_markup = await get_menu_markup(partner_rights)

        await bot.send_message(user_id, "✨ <b>Общение завершено!</b> ✨\n\n"
                                        "<i>Вы успешно завершили чат.</i>\n\n"
                                        "<b>Теперь вы можете воспользоваться главным меню.</b>\n\n"
                                        "🔍 Если хотите начать новый поиск собеседника, нажмите на кнопку "
                                        "'Начать поиск'.", reply_markup=user_menu_markup, parse_mode='HTML')
        await bot.send_message(partner_id, "✨ <b>Общение завершено!</b> ✨\n\n"
                                           "<i>Вы успешно завершили чат.</i>\n\n"
                                           "<b>Теперь вы можете воспользоваться главным меню.</b>\n\n"
                                           "🔍 Если хотите начать новый поиск собеседника, нажмите на кнопку "
                                           "'Начать поиск'.", reply_markup=partner_menu_markup, parse_mode='HTML')
    else:
        await bot.send_message(user_id, "⚠️ <b>Ошибка!</b> ⚠️\n\n"
                                        "Вы не находитесь в активном чате. Нажмите на кнопку "
                                        "'Начать поиск', чтобы найти собеседника.", parse_mode='HTML')


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_messages(message: types.Message):
    user_id = message.from_user.id
    recipient_id = get_recipient_id(message)
    chat_room = get_chat_room(user_id)

    if chat_room:
        partner_id = chat_room[2] if chat_room[1] == user_id else chat_room[1]
        await bot.send_message(partner_id, message.text)
        save_message(user_id, recipient_id, message.text, message.date)

    else:
        await bot.send_message(user_id, "⚠️ <b>Ошибка!</b> ⚠️\n\n"
                                        "Вы не находитесь в активном чате. Нажмите на кнопку "
                                        "'Начать поиск', чтобы найти собеседника.", parse_mode='HTML')


@dp.callback_query_handler(lambda query: query.data == 'settings')
async def choose_settings(query: types.CallbackQuery):
    user_id = query.from_user.id
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''SELECT notification FROM users WHERE user_id = ?''', (user_id,))
    notification_status = cursor.fetchone()

    settings_menu_text = (
        "🛠 <b>Настройки</b> 🛠\n\n"
        "Выберите один из вариантов ниже:\n\n"
        "1️⃣ <b>Уведомления</b>\n"
        "Настроить уведомления рассылки.\n\n"
        "2️⃣ <b>Статистика</b>\n"
        "Просмотреть статистику в боте.\n\n"
        "❌ Для выхода из меню настроек нажмите на кнопку 'Назад'."
    )
    keyboard_settings = types.InlineKeyboardMarkup()

    if notification_status and notification_status[0] == 'Выключены':
        keyboard_settings.row(types.InlineKeyboardButton('🔔 Включить уведомления', callback_data='on_notification'))
    else:
        keyboard_settings.row(types.InlineKeyboardButton('🔕 Выключить уведомления', callback_data='off_notification'))

    keyboard_settings.row(types.InlineKeyboardButton('🔰 Статистика', callback_data='user_info'))
    keyboard_settings.row(types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu_ru'))

    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text=settings_menu_text, reply_markup=keyboard_settings, parse_mode='HTML')


@dp.callback_query_handler(lambda query: query.data == 'on_notification')
async def on_notification_in_bot(query: types.CallbackQuery):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    user_id = query.from_user.id
    cursor.execute('''UPDATE users SET notification = 'Включены' WHERE user_id = ?''', (user_id,))
    conn.commit()
    conn.close()
    settings_menu_text = (
        "🛠 <b>Настройки</b> 🛠\n\n"
        "Выберите один из вариантов ниже:\n\n"
        "1️⃣ <b>Уведомления</b>\n"
        "Настроить уведомления рассылки.\n\n"
        "2️⃣ <b>Статистика</b>\n"
        "Просмотреть статистику в боте.\n\n"
        "❌ Для выхода из меню настроек нажмите на кнопку 'Назад'."
    )
    keyboard_settings = types.InlineKeyboardMarkup()
    keyboard_settings.row(types.InlineKeyboardButton('🔕 Выключить уведомления', callback_data='off_notification'))
    keyboard_settings.row(types.InlineKeyboardButton('🔰 Статистика', callback_data='user_info'))
    keyboard_settings.row(types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu_ru'))

    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text=settings_menu_text, reply_markup=keyboard_settings, parse_mode='HTML')


@dp.callback_query_handler(lambda query: query.data == 'off_notification')
async def on_notification_in_bot(query: types.CallbackQuery):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    user_id = query.from_user.id
    cursor.execute('''UPDATE users SET notification = 'Выключены' WHERE user_id = ?''', (user_id,))
    conn.commit()
    conn.close()
    settings_menu_text = (
        "🛠 <b>Настройки</b> 🛠\n\n"
        "Выберите один из вариантов ниже:\n\n"
        "1️⃣ <b>Уведомления</b>\n"
        "Настроить уведомления рассылки.\n\n"
        "2️⃣ <b>Статистика</b>\n"
        "Просмотреть статистику в боте.\n\n"
        "❌ Для выхода из меню настроек нажмите на кнопку 'Назад'."
    )
    keyboard_settings = types.InlineKeyboardMarkup()
    keyboard_settings.row(types.InlineKeyboardButton('🔔 Включить уведомления', callback_data='on_notification'))
    keyboard_settings.row(types.InlineKeyboardButton('🔰 Статистика', callback_data='user_info'))
    keyboard_settings.row(types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu_ru'))

    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text=settings_menu_text, reply_markup=keyboard_settings, parse_mode='HTML')


@dp.callback_query_handler(lambda c: c.data == 'all_user')
async def all_users_handler(callback_query: types.CallbackQuery):
    users = get_all_users()
    if users:
        for user in users:
            await bot.send_message(callback_query.from_user.id, str(user))
    else:
        await bot.send_message(callback_query.from_user.id, "Информация о пользователях не найдена.")


@dp.callback_query_handler(lambda c: c.data == 'all_message')
async def all_messages_handler(callback_query: types.CallbackQuery):
    messages = get_all_messages()
    if messages:
        for message in messages:
            await bot.send_message(callback_query.from_user.id, str(message))
    else:
        await bot.send_message(callback_query.from_user.id, "Информация о сообщениях не найдена.")


@dp.callback_query_handler(lambda c: c.data == 'active_table')
async def active_tables_handler(callback_query: types.CallbackQuery):
    tables = get_active_tables()
    if tables:
        for table in tables:
            await bot.send_message(callback_query.from_user.id, str(table))
    else:
        await bot.send_message(callback_query.from_user.id, "Информация о активных таблицах не найдена.")


@dp.callback_query_handler(lambda query: query.data == 'search_user')
async def search_user(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, "Введите username пользователя в формате @example:")
    await SomeState.UsernameSearch.set()


@dp.message_handler(state=SomeState.UsernameSearch)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text.strip()
    user_info = find_user_by_username(username)
    if user_info:
        response_text = "<b>Информация о пользователе:</b>\n\n"
        response_text += f"<b>ID пользователя:</b> {user_info[1]}\n"
        response_text += f"<b>Имя пользователя:</b> {user_info[2]}\n"
        if len(user_info) >= 3:
            response_text += f"<b>Права:</b> {user_info[3]}\n"
        if len(user_info) >= 4:
            response_text += f"<b>Метка:</b> {user_info[4]}\n"
        if len(user_info) >= 5:
            response_text += f"<b>Подписка:</b> {'Премиум' if user_info[5] else 'Бесплатная'}\n"
        if len(user_info) >= 6:
            response_text += f"<b>Уведомления:</b> {user_info[6]}\n"
    else:
        response_text = "Пользователь не найден."
    await bot.send_message(message.chat.id, response_text, parse_mode='HTML')
    await state.finish()


@dp.callback_query_handler(lambda query: query.data == 'give_subscription')
async def give_subscription(query: types.CallbackQuery):
    admin_id = 933411060
    await bot.send_message(admin_id, "Введите username пользователя в формате @example:")
    await SomeState.SubscriptionUsername.set()


@dp.message_handler(state=SomeState.SubscriptionUsername)
async def process_subscription_username(message: types.Message, state: FSMContext):
    username = message.text.strip()
    user_data = find_user_by_username(username)
    if user_data:
        user_id = user_data[1]
        await bot.send_message(user_id, "Вам была оформлена подписка на бесконечный период.")
        update_subscription(user_id, 'premium')
        response_text = f"Пользователю с username {username} была выдана подписка."
        admin_ids = get_all_admin_ids()
        for admin_id in admin_ids:
            await bot.send_message(admin_id, response_text)
    else:
        response_text = "Пользователь не найден."
        await bot.send_message(message.chat.id, response_text)

    await state.finish()


@dp.callback_query_handler(lambda query: query.data == 'search_message')
async def search_message(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, "Введите username пользователя:")
    await SomeState.MessageUsername.set()


@dp.message_handler(state=SomeState.MessageUsername)
async def process_message_username(message: types.Message, state: FSMContext):
    username = message.text.strip()
    user_data = find_user_by_username(username)
    if user_data:
        user_id = user_data[1]
        messages = find_messages_by_user_id(user_id)
        if messages:
            response_text = ""
            for msg_data in messages:
                msg, sender_id, recipient_id = msg_data
                sender_data = find_user_by_user_id(sender_id)
                recipient_data = find_user_by_user_id(recipient_id)
                if sender_data and sender_data[2]:
                    sender_name = sender_data[2]
                    if sender_id == user_id:
                        response_text += f"{sender_name}: {msg}\n"
                    else:
                        response_text += f"Получено от {sender_name}: {msg}\n"
                if recipient_data and recipient_data[2]:
                    recipient_name = recipient_data[2]
                    if recipient_id == user_id:
                        response_text += f"Получено от {recipient_name}: {msg}\n"
            response_text = response_text.strip()
        else:
            response_text = "У пользователя нет сообщений в базе данных."
    else:
        response_text = "Пользователь не найден."
    await bot.send_message(message.chat.id, response_text)
    await state.finish()


@dp.callback_query_handler(lambda query: query.data == 'spam')
async def message_for_all_users_from_admin(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.from_user.id,
                           "Отправьте сообщение или файл для отправки всем пользователям:",
                           reply_markup=cancel_markup())
    await SpamState.waiting_for_input.set()


@dp.callback_query_handler(lambda c: c.data == 'cancel_spam', state=SpamState.waiting_for_input)
async def cancel_spam(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(callback_query.from_user.id, "Рассылка отменена.")
    await bot.answer_callback_query(callback_query.id)


@dp.message_handler(content_types=types.ContentTypes.ANY, state=SpamState.waiting_for_input)
async def process_message_or_file_from_admin(message: types.Message, state: FSMContext):
    input_message = message.text or message.caption or message.document or message.audio or message.photo
    users = get_users_with_notification_enabled()
    for user_tuple in users:
        user_id = user_tuple[1]
        if message.text:
            await bot.send_message(user_id, input_message)
        elif message.caption:
            await bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)
        elif message.document:
            await bot.send_document(user_id, message.document.file_id, caption=message.caption)
        elif message.audio:
            await bot.send_audio(user_id, message.audio.file_id, caption=message.caption)
        elif message.photo:
            await bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)
    await state.finish()
    await bot.send_message(message.from_user.id, "Сообщение успешно отправлено всем пользователям!")


@dp.callback_query_handler(lambda query: query.data == 'search_table')
async def search_table_handler(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, "Введите username пользователя для поиска стола:")
    await TableState.TableSearchUsername.set()


@dp.message_handler(state=TableState.TableSearchUsername)
async def process_table_search_username(message: types.Message, state: FSMContext):
    username = message.text.strip()
    user_data = find_user_by_username(username)
    if user_data:
        user_id = user_data[1]
        table_info = find_table_info_by_user_id(user_id)
        if table_info:
            response_text = f"Информация о столе:\n{table_info}"
        else:
            response_text = "Информация о столе не найдена."
    else:
        response_text = "Пользователь не найден."

    await bot.send_message(message.chat.id, response_text)
    await state.finish()


@dp.callback_query_handler(lambda query: query.data == 'premium_play')
async def game_for_premium(query: types.CallbackQuery):
    game_text = (
        "<b>🎉 Добро пожаловать в Игровое Меню! 🎉</b>\n\n"
        "Выберите одну из захватывающих игр и попытайте удачу:\n\n"
        "<b>🔓 1. Сундуки</b> - Открывайте сундуки и выигрывайте ценные призы, но учтите, в некоторых сундуках "
        "бомбы!\n\n"
        "<b>📈 2. Больше или Меньше</b> - Угадайте, будет ли следующее число больше или меньше предыдущего!\n\n"
        "<b>🎰 3. Рулетка</b> - каждые 24 часа получай до 100 баллов на свой баланс!"
    )
    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text=game_text, reply_markup=await game_menu(), parse_mode='HTML')


@dp.callback_query_handler(lambda query: query.data == 'count_currency')
async def profile_number_2(query: types.CallbackQuery):
    user_id = query.from_user.id
    count_curr = get_user_currency(user_id)
    menu_curr_text = (
        f"<b>Меню бонусных баллов 💳</b>\n\n"
        f"👛 Ваши баллы: <code>{count_curr}</code>\n\n"
        f"Что вы хотите сделать?\n"
        f"1️⃣ <b>Обменять баллы на подписку</b>\n"
        f"2️⃣ <b>Сыграть в игры</b>\n\n"
        f"ℹ️ Это вы можете сделать в разделах главного меню!"
    )
    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text=menu_curr_text, reply_markup=await back_menu(), parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data == 'cancel_message', state='*')
async def cancel_message(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Отправка сообщения была отменена.")
    await call.answer()
    await state.finish()


@dp.callback_query_handler(lambda query: query.data == 'send_anon_message')
async def give_subscription(query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(query.from_user.id, "Введите username пользователя в формате example:",
                           reply_markup=get_cancel_button())
    await AnonSMS.wait_username.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=AnonSMS.wait_username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text.strip()
    user_id = find_user_by_username_2(username)
    if user_id is not None:
        await state.update_data(recipient_user_id=user_id)
        await bot.send_message(message.chat.id, "Введите текст сообщения, который вы хотите отправить.")
        await AnonSMS.next()
    else:
        await message.answer("Пользователь с таким именем не найден.", reply_markup=get_cancel_button())


@dp.message_handler(content_types=types.ContentTypes.ANY, state=AnonSMS.wait_sms)
async def process_message_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    recipient_user_id = data.get('recipient_user_id')
    if recipient_user_id:
        if message.text:
            message_text = message.text
            await bot.send_message(recipient_user_id, f"Анонимное сообщение: {message_text}")
        elif message.photo:
            await message.photo[-1].download('photo.jpg')
            with open('photo.jpg', 'rb') as photo:
                await bot.send_photo(recipient_user_id, photo)
        elif message.sticker:
            await bot.send_sticker(recipient_user_id, message.sticker.file_id)
        elif message.document:
            await bot.send_document(recipient_user_id, message.document.file_id)
        else:
            await message.answer("Сожалеем, но мы не можем отправить это содержимое.")

        await message.answer("Ваше сообщение было отправлено анонимно.")
        await state.finish()
    else:
        await message.answer("Что-то пошло не так. Пожалуйста, попробуйте снова.")


@dp.callback_query_handler(lambda query: query.data == 'shop_currency')
async def shop_in_bot(query: types.CallbackQuery):
    shop_menu_text = (
        "<b>🌟 Добро пожаловать в Магазин Премиум-подписок! 🌟</b>\n"
        "<i>Здесь вы можете обменять ваши баллы на ценные премиум-подписки.</i>\n\n"
        "💎 <b>Доступные опции:</b>\n"
        "1️⃣ <b>Трехдневная подписка</b> - 200 баллов\n"
        "2️⃣ <b>Одномесячная подписка</b> - 300 баллов\n"
        "3️⃣ <b>Трехмесячная подписка</b> - 540 баллов (10% скидка!)\n"
        "4️⃣ <b>Годовая подписка</b> - 1820 баллов (20% скидка!)\n\n"
        "<u>Подписка позволяет вам получать эксклюзивные функции:</u>\n"
        "🔹 Premium поиск\n"
        "🔹 Доступ к эксклюзивному контенту\n"
        "🔹 Игры\n"
        "🔹 Анонимные сообщения\n"
        "🔹 Быстрая поддержка\n\n"
        "Для обмена баллов на подписку напишите <b>Номер опции</b>.\n"
        "<i>Убедитесь, что у вас достаточно баллов для выбранной подписки!</i>"
    )
    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text=shop_menu_text, reply_markup=await subs_buy(), parse_mode='HTML')


SUBSCRIPTION_COSTS = {
    'three_days': 200,
    'subs_month': 300,
    'subs_3_month': 540,
    'subs_year': 1820
}


@dp.callback_query_handler(lambda c: c.data in SUBSCRIPTION_COSTS.keys())
async def handle_subscription_purchase(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    subscription_type = callback_query.data
    cost = SUBSCRIPTION_COSTS[subscription_type]

    if update_currency(user_id, cost, subscription_type):
        await callback_query.message.answer("Подписка успешно приобретена!")
    else:
        await callback_query.message.answer("Недостаточно баллов для покупки этой подписки.")

    await callback_query.answer()


last_roulette_usage = {}


@dp.callback_query_handler(lambda query: query.data == 'roulette')
async def every_24_hours_roulette(query: types.CallbackQuery):
    user_id = query.from_user.id
    current_time = time.time()

    if user_id in last_roulette_usage:
        last_usage_time = last_roulette_usage[user_id]
        time_elapsed = current_time - last_usage_time

        if time_elapsed < 24 * 60 * 60:
            await bot.answer_callback_query(query.id,
                                            text="Вы уже использовали эту функцию в течение последних 24 часов.")
            return

    last_roulette_usage[user_id] = current_time

    count = random.randrange(0, 50)
    conn = sqlite3.connect(CURRENCY_DATABASE)
    cursor = conn.cursor()
    cursor.execute('''UPDATE users_premium_currency SET count_curr = count_curr + ? WHERE user_id = ?''',
                   (count, user_id))
    conn.commit()
    conn.close()
    curr_text = (
        f'Ваш баланс баллов обновлен на {count}!\n\n'
        f'Следующий раз Вы сможете воспользоваться функцией через 24 часа.'
    )
    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text=curr_text, reply_markup=await back_menu(), parse_mode='HTML')


last_button_press = {}


@dp.callback_query_handler(lambda query: query.data == 'chest')
async def start_chest_game(query: types.CallbackQuery):
    user_id = query.from_user.id

    current_time = time.time()
    if user_id in last_button_press and current_time - last_button_press[user_id] < 24 * 3600:
        await bot.answer_callback_query(query.id,
                                        text="Вы уже использовали эту функцию в течение последних 24 часов.")
    else:
        chest_text = (
            '''
            Выберите сундук:
            '''
        )
        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text=chest_text, reply_markup=await chest_menu(), parse_mode='HTML')


@dp.callback_query_handler(lambda query: query.data.startswith('chest_'))
async def handle_chest_choice(query: types.CallbackQuery):
    user_id = query.from_user.id
    chosen_chest = int(query.data.split('_')[1])

    points, correct_chest = await chest_game(user_id, chosen_chest)

    if points > 0:
        win_chest_text = f"Поздравляем! Вы выбрали правильный сундук (номер {correct_chest}). В нем {points} баллов!"
        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text=win_chest_text, reply_markup=await back_menu(), parse_mode='HTML')
    else:
        lose_chest_text = (f"Вы выбрали неправильный сундук. Правильный сундук был номер {correct_chest}. Попробуйте "
                           f"еще раз!")
        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text=lose_chest_text, reply_markup=await back_menu(), parse_mode='HTML')

    last_button_press[user_id] = time.time()


@dp.callback_query_handler(lambda c: c.data == 'prem_ser')
async def choose_search_premium(query: types.CallbackQuery):
    text_choose = (
        'Выберите тип поиска:'
    )
    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text=text_choose, reply_markup=await start_prem_search(), parse_mode='HTML'
                                )


@dp.callback_query_handler(lambda c: c.data == 'premium_search')
async def start_search(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    update_user_status(user_id, 'PREMIUM_WAIT')
    await bot.send_message(user_id, "🔍 <b>Поиск собеседника...</b> 🔍\n\n"
                                    "<i>Среднее время ожидания - 10 секунд</i>", parse_mode='HTML')
    await find_premium_partner(user_id)


@dp.message_handler(commands=['stop_premium'])
async def stop_chat(message: types.Message):
    user_id = message.from_user.id
    chat_room = get_chat_room(user_id)

    if chat_room:
        partner_id = chat_room[2] if chat_room[1] == user_id else chat_room[1]
        delete_chat_room(user_id)
        update_user_status(user_id, 'NOT WAIT')
        update_user_status(partner_id, 'NOT WAIT')

        user_rights = get_user_rights(user_id)
        partner_rights = get_user_rights(partner_id)

        user_menu_markup = await get_menu_markup(user_rights)
        partner_menu_markup = await get_menu_markup(partner_rights)

        await bot.send_message(user_id, "✨ <b>Общение завершено!</b> ✨\n\n"
                                        "<i>Вы успешно завершили чат.</i>\n\n"
                                        "<b>Теперь вы можете воспользоваться главным меню.</b>\n\n"
                                        "🔍 Если хотите начать новый поиск собеседника, нажмите на кнопку "
                                        "'Начать поиск'.", reply_markup=user_menu_markup, parse_mode='HTML')
        await bot.send_message(partner_id, "✨ <b>Общение завершено!</b> ✨\n\n"
                                           "<i>Вы успешно завершили чат.</i>\n\n"
                                           "<b>Теперь вы можете воспользоваться главным меню.</b>\n\n"
                                           "🔍 Если хотите начать новый поиск собеседника, нажмите на кнопку "
                                           "'Начать поиск'.", reply_markup=partner_menu_markup, parse_mode='HTML')
    else:
        await bot.send_message(user_id, "⚠️ <b>Ошибка!</b> ⚠️\n\n"
                                        "Вы не находитесь в активном чате. Нажмите на кнопку "
                                        "'Начать поиск', чтобы найти собеседника.", parse_mode='HTML')


last_button_press_big_small = {}


@dp.callback_query_handler(lambda query: query.data == 'random_game')
async def start_random_game(query: types.CallbackQuery):
    user_id = query.from_user.id

    current_time = time.time()
    if user_id in last_button_press_big_small and current_time - last_button_press_big_small[user_id][
        "time"] < 24 * 3600:
        await bot.answer_callback_query(query.id, text="Вы уже использовали эту функцию в течение последних 24 часов.")
    else:
        secret_number = random.randint(1, 100)
        shown_number = random.randint(1, 100)

        game_text = f"Выбрано число: {shown_number}. Угадайте, будет ли загаданное число больше или меньше?"
        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text=game_text, reply_markup=await greater_or_lower_menu(), parse_mode='HTML')

        last_button_press_big_small[user_id] = {"time": current_time, "secret_number": secret_number,
                                                "shown_number": shown_number}


@dp.callback_query_handler(lambda query: query.data.startswith('guess_'))
async def handle_guess(query: types.CallbackQuery):
    user_id = query.from_user.id
    guess = query.data.split('_')[1]

    game_info = last_button_press_big_small.get(user_id)

    if not game_info:
        await bot.answer_callback_query(query.id, text="Пожалуйста, начните игру снова.")
        return

    secret_number = game_info["secret_number"]
    shown_number = game_info["shown_number"]
    current_time = time.time()

    if current_time - game_info["time"] < 24 * 3600:
        if (guess == "greater" and secret_number > shown_number) or (guess == "lower" and secret_number < shown_number):
            await bot.answer_callback_query(query.id, text="Поздравляем! Вы угадали!")
            await add_points(user_id, 100)
        else:
            await bot.answer_callback_query(query.id, text="К сожалению, вы не угадали. Попробуйте еще раз.")
    else:
        await bot.answer_callback_query(query.id,
                                        text="Извините, вы можете использовать эту функцию только раз в 24 часа.")


@dp.callback_query_handler(lambda query: query.data == 'registration')
async def start_registration(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Какой у вас пол?", reply_markup=gender_keyboard())
    await Registration.gender.set()


@dp.callback_query_handler(state=Registration.gender)
async def set_gender(callback_query: types.CallbackQuery, state: FSMContext):
    gender = callback_query.data
    await state.update_data(gender=gender)
    await callback_query.message.answer("Сколько вам лет? (введите число от 16 до 90)")
    await Registration.next()


@dp.message_handler(lambda message: not message.text.isdigit() or not 16 <= int(message.text) <= 90,
                    state=Registration.age)
async def invalid_age(message: types.Message):
    await message.answer("Пожалуйста, введите корректный возраст (число от 16 до 90).")


@dp.message_handler(state=Registration.age)
async def set_age(message: types.Message, state: FSMContext):
    age = int(message.text)
    await state.update_data(age=age)
    await message.answer("В каком городе вы проживаете?")
    await Registration.next()


@dp.message_handler(state=Registration.city)
async def set_city(message: types.Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)

    user_data = await state.get_data()
    gender = user_data['gender']
    age = user_data['age']
    city = user_data['city']
    conn = sqlite3.connect(REGISTER_DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO database_premium (username, gender, age, town) VALUES (?, ?, ?, ?)",
                   (message.from_user.username, gender, age, city))
    conn.commit()
    conn.close()

    await message.answer("Регистрация завершена! Спасибо!")
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'userinfo')
async def process_callback_userinfo(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text="Установите Ваши интересы",
                                reply_markup=get_interests_keyboard())


@dp.callback_query_handler(lambda c: c.data.startswith('gender_'))
async def process_callback_gender(callback_query: types.CallbackQuery):
    gender = callback_query.data.split('_')[1]
    update_interest(callback_query.from_user.id, 'interest_gender', gender)
    await bot.answer_callback_query(callback_query.id, text="Пол выбран и записан")
    try:
        await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                            reply_markup=get_interests_keyboard())
    except MessageNotModified:
        pass


@dp.callback_query_handler(lambda c: c.data.startswith('age_'))
async def process_callback_age(callback_query: types.CallbackQuery):
    age = callback_query.data.split('_')[1]
    update_interest(callback_query.from_user.id, 'interest_age', age)
    await bot.answer_callback_query(callback_query.id, text="Возраст выбран и записан")
    try:
        await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                            reply_markup=get_interests_keyboard())
    except MessageNotModified:
        pass


@dp.callback_query_handler(lambda c: c.data.startswith('chat_'))
async def process_callback_chat(callback_query: types.CallbackQuery):
    chat_type = callback_query.data.split('_')[1]
    update_interest(callback_query.from_user.id, 'interest_chat', chat_type)
    await bot.answer_callback_query(callback_query.id, text="Тип чата выбран и записан")
    try:
        await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                            reply_markup=get_interests_keyboard())
    except MessageNotModified:
        pass


@dp.callback_query_handler(lambda c: c.data == 'town')
async def process_callback_town(callback_query: types.CallbackQuery):
    await Form.waiting_for_town.set()
    await bot.send_message(callback_query.from_user.id, "Введите интересующий город")


@dp.message_handler(state=Form.waiting_for_town)
async def process_town(message: types.Message, state: FSMContext):
    update_interest(message.from_user.id, 'interest_town', message.text)
    await message.reply("Город выбран и записан")
    await state.finish()
    try:
        await bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1,
                                            reply_markup=get_interests_keyboard())
    except MessageNotModified:
        pass
