from re import I
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import BotDB
import config

storage = MemoryStorage()

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

BotDB = BotDB('assistent.db')