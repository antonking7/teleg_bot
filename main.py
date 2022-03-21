import config
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import datetime

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

from db import BotDB
BotDB = BotDB('assistent.db')

@dp.message_handler()
async def echo_send(message : types.message):
	# await message.answer(message.text)
	await message.answer(datetime.today())

executor.start_polling(dp)
