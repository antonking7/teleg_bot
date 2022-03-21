from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from db import BotDB
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

BotDB = BotDB('assistent.db')