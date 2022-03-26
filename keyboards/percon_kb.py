from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers import constants


b_timetable = KeyboardButton(constants.button_timetable)
b_get_news = KeyboardButton(constants.button_get_news)
b_edit_timetable = KeyboardButton(constants.button_edit_timetable)

kb_person = ReplyKeyboardMarkup(resize_keyboard=True)
kb_person.add(b_get_news).add(b_timetable).insert(b_edit_timetable)
