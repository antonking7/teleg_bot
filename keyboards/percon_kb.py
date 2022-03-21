from pickle import TRUE
from re import I
from tkinter import Button
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from handlers import constants

b_timetable = KeyboardButton(constants.button_timetable)
b_edit_timetable = KeyboardButton(constants.button_edit_timetable)

kb_person = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_person.add(b_timetable).insert(b_edit_timetable)