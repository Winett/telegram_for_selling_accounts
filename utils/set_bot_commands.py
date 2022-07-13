from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустить бота'), # пока добавляем только одну команду
            types.BotCommand('buy_account', 'Купить аккаунт'),
        ]
    )

async def set_admin_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('add_account', 'Добавить аккаунт')
        ]
    )