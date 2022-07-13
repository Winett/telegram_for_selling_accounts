from aiogram import types
from typing import Union
from data.db import Mongodb
from loader import dp

acc_db = Mongodb('Telegram', 'accounts')

@dp.message_handler(commands='menu')
async def show_menu(msg: types.Message):
    await list_categories(msg)



async def list_categories(msg: Union[types.Message, types.CallbackQuery], **kwargs): #Union либо одно, либо другое
    markup = categories_keyboard()