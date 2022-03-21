import config
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo_send(message : types.message):
	await message.answer(message.text)

executor.start_polling(dp)
