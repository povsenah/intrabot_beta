#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import telebot
import json
import os
bot = telebot.TeleBot(token='1326919079:AAF0E9OTSd1_tKgbWyxL6md_B2lrVQISDq0')


def check_ticket_status(ticket_id):
    login = 'api.bot'
    password = 'kondrikova22@'
    server = 'https://wrf.intraservice.ru/'
    url = server + 'api/task/' + str(ticket_id)
    payload = {
        'fields': 'Id,Name,StatusId'
    }
    a = requests.get(url=url, auth=(login, password), json=payload)
    print(a.status_code)
    b = json.loads(a.text)
    print(b['Task']['StatusId'], b['Task']['StatusName'])
    return b['Task']['StatusId']


def create_comment(ticket_id, comment):
    login = 'api.bot'
    password = 'kondrikova22@'
    server = 'https://wrf.intraservice.ru/'
    url = server + 'api/task/' + str(ticket_id)
    payload = {
        'Comment': comment,
        'StatusId': check_ticket_status(ticket_id),
        'IsPrivateComment': False
    }
    a = requests.put(url=url, auth=(login, password), json=payload)
    print(a.status_code, print(a.text))

def create_task():
    login = 'api.bot'
    password = 'kondrikova22@'
    server = 'https://wrf.intraservice.ru/'
    url = server + 'api/task/'
    description = 'Test '
    payload = {
        'ServiceId': 19,
        'StatusId': 31,
        'Description': description,
        'TypeId': 1008,
        'PriorityId': 11
    }
    a = requests.post(url=url, auth=(login, password), json=payload)

# create_task()
@bot.message_handler()
def chek_comment(message):
    if message.reply_to_message:
        ticket_id = message.reply_to_message.text
        ticket_id = int(((str(ticket_id).split('🙀 Новая заявка: ')[1]).split('\n'))[0])
        comment = message.text
        return create_comment(ticket_id, comment)
#
# @bot.message_handler(commands=['start'])
# def hello(message):
#     telegram_id = message.chat.id
#     bot.send_message(chat_id=telegram_id,
#                      text='Привет, друг 🖐. Я бот, \nкоторый помогает следить за заявками Intraservise\n'
#                           'Давай знакомиться', )
#     if os.path.exists(telegram_id):
#         bot.send_message(chat_id=telegram_id, text='+')
#     else:
#         user = {
#             'name': 'User',
#             'phone':
#         }
#
bot.polling()
