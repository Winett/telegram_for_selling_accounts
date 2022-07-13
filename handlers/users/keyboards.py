from data.config import *
from data.db import Mongodb
from loader import dp
from aiogram import types
from random import randint
import json

acc_db = Mongodb('Telegram', 'accounts')

def gen_main_keyboard():

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.insert(types.InlineKeyboardButton(text='Профиль👤', callback_data='profile'))
    keyboard.insert((types.InlineKeyboardButton(text='Купить🛒', callback_data='buy_item')))
    # for category in services:
    #     number_of_item = acc_db.count_of_data({'project': category})
    #     button_text = f'{category} - {number_of_item} шт'
    #     keyboard.insert(types.InlineKeyboardButton(text=button_text, callback_data=category))
    return keyboard

def gen_category_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for category in services:
        text = f'{category} - {acc_db.count_of_data({"project": category})} шт'
        keyboard.insert(types.InlineKeyboardButton(text=text, callback_data=category))
        # buttons.append(types.InlineKeyboardButton(text=text, callback_data=category))
    # keyboard.inline_keyboard = keyboard.add(buttons), [types.InlineKeyboardButton(text='Назад', callback_data='back_main')]
    keyboard.row(types.InlineKeyboardButton(text='Назад', callback_data='back_main'))
    return keyboard


def gen_item_keyboard(category):
    keyboard = types.InlineKeyboardMarkup()

    data = acc_db.find_data({'project': category}, multiple=True)
    data = [r for r in data]
    len_of_data = len(data)
    random_data = data[randint(0, len_of_data - 1)]
    # print(str(random_data["_id"]))
    keyboard.row(types.InlineKeyboardButton(text=f'Купить!', callback_data=f'{random_data["item_id"]}'))
    keyboard.row(types.InlineKeyboardButton(text='Обновить', callback_data=f'refresh {category}'))
    return keyboard, random_data['about']

def buy_item(item_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Купить', callback_data=f'buy {item_id}'))
    return keyboard

