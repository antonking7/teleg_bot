from aiogram import  types, Dispatcher
from create_bot import bot, BotDB
from handlers import constants
from keyboards import percon_kb
import datetime
import logging

# @dp.message_handler()
async def cmd_start(message : types.message):
    # await message.delete()
	await bot.send_message(message.from_user.id, constants.cons_msg_start, reply_markup=percon_kb.kb_person)
async def cmd_timetable(message : types.message):
    # await message.delete()
    records = BotDB.get_record(message.from_user.id, datetime.datetime.now().strftime("%d-%m-%Y")) 
    logging.info(datetime.datetime.now().strftime("%d-%m-%Y"))
    logging.info(records)
    if(len(records)):
        answer = f"🕘 Планы на сегодня\n"
        for r in records:
            answer += f" В {r[3]}"
            answer += f" <i>-{r[4]}</i>\n"
        logging.info(answer)
        await bot.send_message(message.from_user.id, answer)
        # await message.reply(answer)
    else:
	    await bot.send_message(message.from_user.id, constants.cons_msg_timetable)
  




def register_hndlr_clnt(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands=[constants.cons_comand_start, constants.cons_comand_help])
    dp.register_message_handler(cmd_timetable, commands=[constants.cons_comand_timetable])