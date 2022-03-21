from aiogram import  types, Dispatcher
from create_bot import dp
from datetime import datetime


# @dp.message_handler()
async def cmd_start(message : types.message):
	# await message.answer(message.text)
	await message.answer(datetime.today())

def register_hndlr_clnt(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands=['strat', 'help'])