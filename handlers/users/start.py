from aiogram import types
from loader import bot
from loader import dp
from data.config import *
from data.db import Mongodb
import json
from os import remove
from utils.set_bot_commands import set_admin_commands
from handlers.users.keyboards import *
from random import randint
# from handlers.users.callback_query import *


user_db = Mongodb('Telegram', 'users')
acc_db = Mongodb('Telegram', 'accounts')


@dp.message_handler(commands=['start', 'about'])
async def command_start(msg: types.Message):
    await msg.answer(f"Привет {msg.from_user.first_name}")
    user_id = msg.from_user.id
    if user_id in admins_id:
        await msg.answer(f'Команды для админа бота:\n'
                         f'/statistic   Посмотреть статистику\n')
        await set_admin_commands(dp)
    is_exist_user = user_db.find_data({'user_id': msg.from_user.id})
    # print(is_exist_user)
    if is_exist_user == None:
        user_db.insert_one_data({'name': msg.from_user.first_name, 'user_id': msg.from_user.id, 'balance': 0})
        await msg.answer(f'Добро пожаловать в бота по продаже аккаунтов в соц. сетях!\n'
                         f'<pre>Нажмите на </pre>/menu', parse_mode=types.ParseMode.HTML, reply_markup=gen_main_keyboard())
    else:
        await msg.answer(f'{msg.from_user.first_name}, Добро пожаловать в бота по продаже аккаунтов в соц. сетях!\n'
                         f'<pre>Нажмите на </pre>/menu', parse_mode=types.ParseMode.HTML,  reply_markup=gen_main_keyboard())
        # await msg.answer(f':basketball:', parse_mode=types.ParseMode.HTML)


@dp.message_handler(user_id=admins_id, content_types=['file', 'document'])
async def get_file(msg):
    global acc_db
    file_id = msg.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = file_path.split('/')[-1]
    file_format = file_name.split('.')[-1]
    await bot.download_file(file_path, f"{file_name}")
    if file_format == 'json':
        with open(file_name) as file_with_data:
            data = json.load(file_with_data)
        try:
            for dat in data:
                dat['item_id'] = randint(100000, 1000000000000)
                acc_db.insert_one_data(dat)
        except:
            acc_db.insert_one_data(data)
        # acc_db = Mongodb('Telegram', 'accounts')
        await msg.answer('Данные успешно добавлены!')
    else:
        await msg.answer('Отправьте файл в формате JSON')

    remove(file_name)


@dp.message_handler(user_id=admins_id, commands=['statistic'])
async def statistic(msg: types.Message):
    message = ''
    for project in services:
        data = acc_db.count_of_data({'project': project})
        message += f'{project}: {data}\n'

    await msg.answer(message)




