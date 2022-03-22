from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import  types , Dispatcher
from handlers import constants



b_timetable = KeyboardButton(constants.button_timetable)
b_edit_timetable = KeyboardButton(constants.button_edit_timetable)

kb_person = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_person.add(b_timetable).insert(b_edit_timetable)