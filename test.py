# -*- coding: utf-8 -*-
"""
This Example will show you how to use register_next_step handler.
"""

import telebot
from telebot import types
import json

API_TOKEN = '<api_token>'

bot = telebot.TeleBot(token='766426216:AAG5lQzCfWNxspmYpYiPt8pSM9kImViqteU')

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.phone = None
        self.chat_id = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Привет, я интработ.
Напиши мне, как тебя зовут? 
""")
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_button = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        markup.add(markup_button)
        msg = bot.reply_to(message, 'Для авторизации отпавь мне свой номер телефона', reply_markup=markup)
        bot.register_next_step_handler(msg, tphone)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def tphone(message):
    try:
        chat_id = message.chat.id
        phone = message.contact.phone_number
        user = user_dict[chat_id]
        user.phone = phone
        user.chat_id = chat_id
        msg = bot.reply_to(message, 'Спасибо')
        print('msg.text: ', msg.text, 'chat_id: ', user.chat_id, 'user name: ', user.name, 'phone: ', user.phone)
        user_conf = {
            'name': user.name,
            'phone': user.phone,
            'chat_id': user.chat_id
        }

        with open(str(user_conf['chat_id']) + '.json', "w", encoding="utf-8") as file:
            json.dump(user_conf, file, ensure_ascii=False)

        with open(str(user_conf['chat_id']) + '.json', encoding="utf-8") as file:
            a = json.load(file)

    except Exception as e:
        print(Exception)
        bot.reply_to(message, e)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

bot.polling()
