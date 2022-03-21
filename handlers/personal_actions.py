from re import I
from aiogram import  types, Dispatcher
from create_bot import dp, bot
from handlers import constants


# @dp.message_handler()
async def cmd_start(message : types.message):
	await bot.message.answer(constants.cons_com_start)

def register_hndlr_clnt(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands=['/strat', '/help'])