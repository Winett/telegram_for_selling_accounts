from aiogram import types
from loader import bot
from loader import dp
from data.config import *
from data.db import Mongodb
from handlers.users.keyboards import *
from aiogram.dispatcher.filters import Text

user_db = Mongodb('Telegram', 'users')
acc_db = Mongodb('Telegram', 'accounts')
back = types.InlineKeyboardMarkup()
back.add(types.InlineKeyboardButton('Назад', callback_data='back_main'))



@dp.callback_query_handler(Text(startswith='buy '))
async def buy_items(callback_query: types.CallbackQuery):
    # print(callback_query.data)
    item_id = callback_query.data.split()[-1]
    item = acc_db.find_data({'item_id': int(item_id)})
    user = user_db.find_data({'user_id': callback_query.from_user.id})
    balance = user['balance']
    if balance >= price[item['project']]:
        await callback_query.message.answer(f'Вы успешно купили аккаунт! Ниже представлены все данные от него\nСервис: {item["project"]}\nЛогин: <code>{item["login"]}</code>\nПароль: <code>{item["password"]}</code>', parse_mode=types.ParseMode.HTML)
        acc_db.delete_data({'item_id': int(item_id)})
        user_db.update_data({'user_id': user['user_id']}, {'balance': balance - price[item['project']]})
    else:
        await callback_query.message.answer(f'Opss...\nУвы, но вам не хватает средств на балансе, пожалуйста, пополните баланс')

    # await callback_query.message.edit_text(f"{item['about']}\nСтоимость {price[item['project']]}₽")



@dp.callback_query_handler(Text(startswith='refresh'))
async def refresh_acc(callback_query: types.CallbackQuery):
    button, about = gen_item_keyboard(callback_query.data.split()[-1])
    await callback_query.message.edit_text(f'Аккаунт: {callback_query.data.split()[-1]}\nОписание: {about}\nЦена: {price[callback_query.data.split()[-1]]}₽')
    await callback_query.message.edit_reply_markup(button)


@dp.callback_query_handler(lambda callback_query: True)
async def callback_inline(callback_query: types.CallbackQuery):
    # print(callback_query.data)
    # print(callback_query)
    # data = callback_query.message.text
    # print(data)
    if callback_query.data == 'profile':
        await callback_query.message.edit_text(f'🤖Имя: {callback_query.from_user.first_name}\n⚙️Ваш Telegram id: {callback_query.from_user.id}\n💰Баланс: {user_db.find_data({"user_id": callback_query.from_user.id})["balance"]}₽', reply_markup=back)
    # await callback_query.message.edit_text('Ok')
    elif callback_query.data == 'back_main':
        await callback_query.message.edit_text(f'Добро пожаловать в бота по продаже аккаунтов в соц. сетях!\n'
                         '<pre>Выберите что вам нужно из нижепредложенного</pre>', parse_mode=types.ParseMode.HTML, reply_markup=gen_main_keyboard())

    elif callback_query.data == 'buy_item':
        await callback_query.message.edit_text(f'Выберите товар из предложенного: ', reply_markup=gen_category_keyboard())

    elif callback_query.data in services:
        buttons, about = gen_item_keyboard(callback_query.data)
        await callback_query.message.edit_text(f'Аккаунт: {callback_query.data}\nОписание: {about}\nЦена: {price[callback_query.data.split()[-1]]}₽', reply_markup=buttons)

    elif callback_query.data in ['next', 'previous']:
        if callback_query.data == 'next':
            await callback_query.message.edit_text('Выберите понравившийся аккаут: ', reply_markup=gen_category_keyboard())

    elif callback_query.data.isdigit():
        await callback_query.message.edit_reply_markup(buy_item(callback_query.data))

