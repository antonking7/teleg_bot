from aiogram import  types, Dispatcher
from create_bot import dp, bot
from handlers import constants
from keyboards import percon_kb

# @dp.message_handler()
async def cmd_start(message : types.message):
    # await message.delete()
	await bot.send_message(message.from_user.id, constants.cons_msg_start, reply_markup=percon_kb.kb_person)
async def cmd_timetable(message : types.message):
    # await message.delete()
	await bot.send_message(message.from_user.id, constants.cons_msg_timetable)



def register_hndlr_clnt(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands=[constants.cons_comand_start, constants.cons_comand_help])
    dp.register_message_handler(cmd_timetable, commands=[constants.cons_comand_timetable])