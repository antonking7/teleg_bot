from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio
from db import BotDB
import config
import logging
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,CallbackQuery
from aiogram.utils.callback_data import CallbackData


logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

loop = asyncio.get_event_loop()
bot = Bot(token=config.BOT_TOKEN, loop=loop, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

BotDB = BotDB('assistent.db')
