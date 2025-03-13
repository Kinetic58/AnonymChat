from aiogram.dispatcher.filters.state import StatesGroup, State


class SomeState(StatesGroup):
    UsernameSearch = State()
    SubscriptionUsername = State()
    MessageUsername = State()


class SpamState(StatesGroup):
    waiting_for_message = State()
    waiting_for_input = State()


class TableState(StatesGroup):
    TableSearchUsername = State()


class AnonSMS(StatesGroup):
    wait_username = State()
    wait_sms = State()


class Registration(StatesGroup):
    gender = State()
    age = State()
    city = State()

class Form(StatesGroup):
    waiting_for_town = State()
