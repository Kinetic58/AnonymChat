import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

ADMIN_ID = 'adm'
API_TOKEN = 'token'
DATABASE = 'Anonym_message_users'
MESSAGE_DATA = 'anonym_message_all'
QUEUE_DATA = 'users_in_queue'
TABLE = 'table_for_user'
CURRENCY_DATABASE = 'data_currency'
REGISTER_DB = 'database_premium'
INTEREST = 'database_interests'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.ERROR)