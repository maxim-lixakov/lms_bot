import telebot
import config
from telebot import types
from user import User

USERS = {}
bot = telebot.TeleBot(config.TOKEN)


def check_user(message):
    if USERS[message.chat.id]["login"] == " " or USERS[message.chat.id]["password"] == " ":
        return True
    return False


def create_keyboard(list_):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(text=a, callback_data=a) for a in list_]
    keyboard.add(*buttons)
    return keyboard


@bot.callback_query_handler(func=lambda x: True)
def callback_query(callback_query_):
    message = callback_query_.message
    text = callback_query_.data
    if text == "password":
        bot.send_message(message.chat.id, "Отправьте пароль следующим образом:\n"
                                          "password: ")
    if text == "login":
        bot.send_message(message.chat.id, "Отправьте логин следующим образом:\n"
                                          "login: ")


@bot.message_handler(commands=['start'])
def start_command(message, text="login", answer="Здравствутей! Для работы, необходимо авторизироваться на сайте"):
    if message.chat.id not in USERS:
        USERS[message.chat.id] = {"login": " ", "password": " "}
    keyboard = create_keyboard([text])
    bot.send_message(
        message.chat.id,
        answer, reply_markup=keyboard,
    )


@bot.message_handler(content_types=["text"])
def password_message(message):
    if "password:" in message.text.lower():
        USERS[message.chat.id]["password"] = message.text[9:].strip()
        if check_user(message):
            start_command(message)
    elif "login:" in message.text.lower():
        USERS[message.chat.id]["login"] = message.text[7:].strip()
        if check_user(message):
            start_command(message, text="password", answer="Продолжение авторизации")
    if not check_user(message):
        user = User(USERS[message.chat.id]["login"], USERS[message.chat.id]["password"], message.chat.id)
        bot.send_message(message.chat.id, user.lms_auth())


bot.polling(none_stop=True)
