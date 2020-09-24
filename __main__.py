#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import telebot
import os
bot = telebot.TeleBot(token='1326919079:AAF0E9OTSd1_tKgbWyxL6md_B2lrVQISDq0')


def create_comment(ticket_id, comment):
    login = 'api.bot'
    password = 'kondrikova22@'
    server = 'https://wrf.intraservice.ru/'
    url = server + 'api/task/' + str(ticket_id)
    payload = {
        'Comment': comment,
        'StatusId': 31,
        'IsPrivateComment': False
    }
    a = requests.put(url=url, auth=(login, password), json=payload)
    print(a.status_code, print(a.text), a, a.headers)

def getname(telegram_id):
    bot.send_message(chat_id=telegram_id, text='Как вас зовут?')




@bot.message_handler()
def chek_comment(message):
    if message.reply_to_message:
        ticket_id = message.reply_to_message.text
        ticket_id = int(((str(ticket_id).split('🙀 Новая заявка: ')[1]).split('\n'))[0])
        comment = message.text
        return create_comment(ticket_id, comment)

@bot.message_handler(commands=['start'])
def hello(message):
    telegram_id = message.chat.id
    bot.send_message(chat_id=telegram_id,
                     text='Привет, друг 🖐. Я бот, \nкоторый помогает следить за заявками Intraservise\n'
                          'Давай знакомиться', )
    if os.path.exists(telegram_id):
        bot.send_message(chat_id=telegram_id, text='+')
    else:
        user = {
            'name': 'User',
            'phone':
        }

bot.polling()
