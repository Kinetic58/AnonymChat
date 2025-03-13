from aiogram import types


def get_cancel_button():
    keyboard = types.InlineKeyboardMarkup()
    cancel_button = types.InlineKeyboardButton("Отменить сообщение", callback_data='cancel_message')
    keyboard.add(cancel_button)
    return keyboard


async def back_menu():
    keyboard_main = types.InlineKeyboardMarkup()
    keyboard_main.row(types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu_ru'))
    return keyboard_main


async def rules_menu_key():
    key_rule = types.InlineKeyboardMarkup()
    key_rule.row(types.InlineKeyboardButton('📘 Условия пользования',
                                            url='https://drive.google.com/file/d/1goXbOgT0SsE8FrlwJ_LD4NdFIm_HjzmI/view'))
    key_rule.row(types.InlineKeyboardButton('💳 Тарифы',
                                            url='https://drive.google.com/file/d/13o7lhxONMaOzijwYrFguRaSagI3D5whT/view?usp=sharing'))
    key_rule.row(types.InlineKeyboardButton('🔒 Политика конфиденциальности',
                                            url='https://drive.google.com/file/d/10pm5VAer68HqJH-6uEy-86X9Qk5zI5I_/view'))
    key_rule.row(
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu_ru')
    )

    return key_rule


async def user_menu():
    keyboard_users = types.InlineKeyboardMarkup()
    keyboard_users.row(types.InlineKeyboardButton('🧑‍💼 Профиль', callback_data='profile'))
    keyboard_users.row(types.InlineKeyboardButton('🎉 Условия подписки', callback_data='rules'))
    keyboard_users.row(types.InlineKeyboardButton('ℹ️ Начать поиск', callback_data='start_search'))
    keyboard_users.row(types.InlineKeyboardButton('🛠️ Настройки', callback_data='settings'),
                       types.InlineKeyboardButton('❓ Тех.Поддержка', url='https://t.me/kinetic_manager'))

    return keyboard_users


async def premium_user_menu():
    keyboard_users = types.InlineKeyboardMarkup()
    keyboard_users.row(types.InlineKeyboardButton('🧑‍💼 Профиль', callback_data='profile'))
    keyboard_users.row(types.InlineKeyboardButton('🔎 Поиск', callback_data='prem_ser'))
    keyboard_users.row(types.InlineKeyboardButton('🎮 Игры', callback_data='premium_play'))
    keyboard_users.row(types.InlineKeyboardButton('📝 Регистрация', callback_data='registration'))
    keyboard_users.row(types.InlineKeyboardButton('🌟 Установить интересы', callback_data='userinfo'))
    keyboard_users.row(types.InlineKeyboardButton('🛍️ Магазин', callback_data='shop_currency'),
                       types.InlineKeyboardButton('💰 Баллы', callback_data='count_currency'))
    keyboard_users.row(types.InlineKeyboardButton('🎭 Анонимное сообщение', callback_data='send_anon_message'))
    keyboard_users.row(types.InlineKeyboardButton('🛠️ Настройки', callback_data='settings'),
                       types.InlineKeyboardButton('❓ Тех.Поддержка', url='https://t.me/kinetic_manager'))

    return keyboard_users


async def start_prem_search():
    keyboard_search = types.InlineKeyboardMarkup()
    keyboard_search.row(types.InlineKeyboardButton('ℹ️ Поиск', callback_data='start_search'),
                        types.InlineKeyboardButton('🌟 Premium поиск', callback_data='premium_search'))
    keyboard_search.row(types.InlineKeyboardButton('🌐 Поиск по интересам', callback_data='interesting_search'))
    keyboard_search.row(types.InlineKeyboardButton('🎂 Поиск по возрасту', callback_data='age_search'))
    keyboard_search.row(types.InlineKeyboardButton('🚻 Поиск по полу', callback_data='gender_search'))
    keyboard_search.row(types.InlineKeyboardButton('🌇 Поиск по городу', callback_data='town_search'))
    keyboard_search.row(types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu_ru'))
    return keyboard_search


async def admin_menu():
    keyboard_admin = types.InlineKeyboardMarkup()
    keyboard_admin.row(types.InlineKeyboardButton('👥 Все пользователи', callback_data='all_user'))
    keyboard_admin.row(types.InlineKeyboardButton('🔍 Поиск пользователя', callback_data='search_user'))
    keyboard_admin.row(types.InlineKeyboardButton('💳 Выдача подписки', callback_data='give_subscription'))
    keyboard_admin.row(types.InlineKeyboardButton('📃 Все сообщения', callback_data='all_message'))
    keyboard_admin.row(types.InlineKeyboardButton('🔎 Поиск сообщений', callback_data='search_message'))
    keyboard_admin.row(types.InlineKeyboardButton('🕹️ Активные столы', callback_data='active_table'))
    keyboard_admin.row(types.InlineKeyboardButton('🔍 Поиск стола', callback_data='search_table'))
    keyboard_admin.row(types.InlineKeyboardButton('📣 Рассылка', callback_data='spam'))
    return keyboard_admin


async def game_menu():
    keyboard_game = types.InlineKeyboardMarkup()
    keyboard_game.row(
        types.InlineKeyboardButton('🎁 Сундуки', callback_data='chest'),
        types.InlineKeyboardButton('🎰 Рулетка', callback_data='roulette')
    )
    keyboard_game.row(
        types.InlineKeyboardButton('⬆️⬇️ Больше или меньше', callback_data='random_game')
    )
    keyboard_game.row(
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu_ru')
    )
    return keyboard_game


async def chest_menu():
    keyboard_chest = types.InlineKeyboardMarkup()
    keyboard_chest.row(
        types.InlineKeyboardButton('1️⃣', callback_data='chest_1'),
        types.InlineKeyboardButton('2️⃣', callback_data='chest_2'),
        types.InlineKeyboardButton('3️⃣', callback_data='chest_3')
    )
    return keyboard_chest


async def subs_buy():
    keyboard_subs_curr = types.InlineKeyboardMarkup()
    keyboard_subs_curr.row(
        types.InlineKeyboardButton('🌟 3 дня', callback_data='three_days'),
        types.InlineKeyboardButton('📅 1 месяц', callback_data='subs_month'))
    keyboard_subs_curr.row(
        types.InlineKeyboardButton('🌈 3 месяца', callback_data='subs_3_month'),
        types.InlineKeyboardButton('🎉 Годовая', callback_data='subs_year'))
    keyboard_subs_curr.row(
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu_ru'))
    return keyboard_subs_curr


def cancel_markup():
    markup = types.InlineKeyboardMarkup()
    cancel_button = types.InlineKeyboardButton(text="Отменить рассылку 🚫", callback_data="cancel_spam")
    markup.add(cancel_button)
    return markup


async def greater_or_lower_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton('Больше', callback_data='guess_greater'),
        types.InlineKeyboardButton('Меньше', callback_data='guess_lower')
    )
    return markup


def gender_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Мужчина', callback_data='male'))
    keyboard.add(types.InlineKeyboardButton('Женщина', callback_data='female'))
    return keyboard


def get_interests_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Укажите интересующий пол:', callback_data='gender_none', disabled=True))
    keyboard.add(types.InlineKeyboardButton('Мужчины', callback_data='gender_men'),
                 types.InlineKeyboardButton('Женщины', callback_data='gender_women'))
    keyboard.add(types.InlineKeyboardButton('Укажите интересующий возраст:', callback_data='age_none', disabled=True))
    keyboard.add(types.InlineKeyboardButton('16-21', callback_data='age_16_21'),
                 types.InlineKeyboardButton('22-30', callback_data='age_22_30'),
                 types.InlineKeyboardButton('31-60', callback_data='age_31_60'))
    keyboard.add(types.InlineKeyboardButton('Укажите интересующий город:', callback_data='town'))
    keyboard.add(types.InlineKeyboardButton('Укажите тип чата:', callback_data='chat_none', disabled=True))
    keyboard.add(types.InlineKeyboardButton('Пошлый', callback_data='chat_adult'),
                 types.InlineKeyboardButton('Научный', callback_data='chat_science'))
    keyboard.add(types.InlineKeyboardButton('Детский', callback_data='chat_kids'),
                 types.InlineKeyboardButton('Школьный', callback_data='chat_school'))
    return keyboard
