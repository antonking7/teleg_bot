from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from create_bot import dp
from handlers import constants
import datetime
import calendar
import locale
import logging

callback_data_calc = CallbackData("voit", "_action", 'year', 'month', 'day')


def create_calendar(year=None, month=None):
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    # data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboards = InlineKeyboardMarkup()
    # Первая строка будет Месяц и Год
    # row = []
    # установка родной локали, чтобы название месяца Python стал выводить кириллицей
    locale.setlocale(locale.LC_ALL, "")
    frst_row_name = calendar.month_name[month] + " " + str(year)
    keyboards.add(InlineKeyboardButton(frst_row_name,
                                       callback_data=callback_data_calc.new(_action="IGNORE", year=year, month=month,
                                                                            day=0)))
    # row.append(InlineKeyboardButton(text=frst_row_name, callback_data=data_ignore))
    # keyboards_list.append(row)
    # keyboards.add(row)
    # Вторая строка дни недели
    row = []
    for day in ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]:
        row.append(InlineKeyboardButton(day,
                                        callback_data=callback_data_calc.new(_action="IGNORE", year=year, month=month,
                                                                             day=0)))
    keyboards.row(*row)
    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if (day == 0):
                row.append(InlineKeyboardButton(" ", callback_data=callback_data_calc.new(_action="IGNORE", year=year,
                                                                                          month=month, day=0)))
            else:
                row.append(InlineKeyboardButton(str(day), callback_data=callback_data_calc.new(_action="DAY", year=year,
                                                                                               month=month,
                                                                                               day=day)))

        keyboards.row(*row)
    # Последний ряд кнопок переключение месяца вперед или назад
    row = []
    row.append(InlineKeyboardButton("<",
                                    callback_data=callback_data_calc.new(_action="PREV-MONTH", year=year, month=month,
                                                                         day=day)))
    row.append(InlineKeyboardButton(" ", callback_data=callback_data_calc.new(_action="IGNORE", year=year, month=month,
                                                                              day=0)))
    row.append(InlineKeyboardButton(">",
                                    callback_data=callback_data_calc.new(_action="NEXT-MONTH", year=year, month=month,
                                                                         day=day)))
    keyboards.row(*row)

    return keyboards


# Ловим ответ от календаря и обрабатываем его
@dp.callback_query_handler(callback_data_calc.filter(_action="IGNORE"))
async def vote_up_cb_handler(query: CallbackQuery, callback_data: dict):
    logging.info(callback_data)
    # await query.message.edit_text("Итого: ")
    await query.answer()


# Ловим ответ от календаря и обрабатываем его
@dp.callback_query_handler(callback_data_calc.filter(_action="PREV-MONTH"))
async def vote_up_cb_handler(query: CallbackQuery, callback_data: dict):
    logging.info(callback_data)
    curr = datetime.datetime(int(callback_data["year"]), int(callback_data["month"]), 1)
    pre = curr - datetime.timedelta(days=1)
    await query.message.edit_text(constants.cons_msg_load_date,
                                  reply_markup=create_calendar(int(pre.year), int(pre.month)))
    await query.answer()


@dp.callback_query_handler(callback_data_calc.filter(_action="NEXT-MONTH"))
async def vote_up_cb_handler(query: CallbackQuery, callback_data: dict):
    logging.info(callback_data)
    curr = datetime.datetime(int(callback_data["year"]), int(callback_data["month"]), 1)
    ne = curr + datetime.timedelta(days=31)
    await query.message.edit_text(constants.cons_msg_load_date,
                                  reply_markup=create_calendar(int(ne.year), int(ne.month)))
    # await query.message.edit_text("Итого: ")
    await query.answer()

# @dp.callback_query_handler(callback_data_calc.filter(_action="DAY"))
# async def vote_up_cb_handler(query: CallbackQuery, callback_data: dict):
#     logging.info(callback_data)
#     curr = datetime.datetime(int(callback_data["year"]), int(callback_data["month"]), 1)
#     await query.answer('ПОЙМАЛ КНОПКУ', show_alert=True)
