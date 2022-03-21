from re import I
from tkinter import Button
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from handlers import constants

b_timetable = KeyboardButton(constants.button_timetable)

kb_person = ReplyKeyboardMarkup()
kb_person.add(1)