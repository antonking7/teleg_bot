from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,CallbackQuery,ReplyKeyboardRemove
from aiogram import  Dispatcher
from aiogram.utils.callback_data import CallbackData
from create_bot import dp, bot
import datetime
import calendar
import locale 
import logging

callback_data_calc = CallbackData("voit","_action",'year','month','day')

def create_calendar(year=None, month=None):
    now = datetime.datetime.now()
    if year == None:
        year = now.year
    if  month == None:
         month = now. month
    # data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboards = InlineKeyboardMarkup()
    keyboards_list = []
#Первая строка будет Месяц и Год
    # row = []
# установка родной локали, чтобы название месяца Python стал выводить кириллицей
    locale.setlocale(locale.LC_ALL, "")  
    frst_row_name = calendar.month_name[month]+" "+str(year)
    keyboards.add(InlineKeyboardButton(frst_row_name, callback_data=callback_data_calc.new(_action="IGNORE",year=year,month=month,day=0)))
    # row.append(InlineKeyboardButton(text=frst_row_name, callback_data=data_ignore))
    # keyboards_list.append(row)
    # keyboards.add(row)
#Вторая строка дни недели
    row=[]
    for day in ["ПН","ВТ","СР","ЧТ","ПТ","СБ","ВС"]:
         row.append(InlineKeyboardButton(day,callback_data=callback_data_calc.new(_action="IGNORE",year=year,month=month,day=0)))
    keyboards.row(*row)
    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(" ",callback_data=callback_data_calc.new(_action="IGNORE",year=year,month=month,day=0)))
            else:
                row.append(InlineKeyboardButton(str(day),callback_data=callback_data_calc.new(_action="DAY",year=year,month=month,day=day)))#createcallback_data_calc("DAY",year,month,day)))
        keyboards.row(*row)
#Последний ряд кнопок переключение месяца вперед или назад
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=callback_data_calc.new(_action="PREV-MONTH",year = year,month=month,day=day))) 
    row.append(InlineKeyboardButton(" ",callback_data=callback_data_calc.new(_action="IGNORE",year = year,month=month,day=0)))
    row.append(InlineKeyboardButton(">",callback_data=callback_data_calc.new(_action="NEXT-MONTH",year = year,month=month,day=day)))
    keyboards.row(*row)
   

    return keyboards   

# def process_calendar_selection():
#     ret_data = (True,None)
    # curr = datetime.datetime(int(callback_data['year']), int(callback_data['month']), 1)
    # if callback_data['_action'] == "IGNORE":
    #     bot.answer_callback_query(callback_query_id= callback.from_user.id)
    # elif callback_data['_action'] == "DAY":
         
    # elif action == "PREV-MONTH":
    #     pre = curr - datetime.timedelta(days=1)
    #     bot.edit_message_text(text=query.message.text,
    #         chat_id=query.message.chat_id,
    #         message_id=query.message.message_id,
    #         reply_markup=create_calendar(int(pre.year),int(pre.month)))
    # elif action == "NEXT-MONTH":
    #     ne = curr + datetime.timedelta(days=31)
    #     bot.edit_message_text(text=query.message.text,
    #         chat_id=query.message.chat_id,
    #         message_id=query.message.message_id,
    #         reply_markup=create_calendar(int(ne.year),int(ne.month)))
    # else:
    #     bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
    #     # UNKNOWN
    # return ret_data



#Ловим ответ от календаря и обрабатываем его
@dp.callback_query_handler(callback_data_calc.filter(_action="IGNORE"))
async def vote_up_cb_handler(query: CallbackQuery, callback_data: dict):
    logging.info(callback_data)
    # await query.message.edit_text("Итого: ")
    await query.answer()

@dp.callback_query_handler(callback_data_calc.filter(_action="DAY"))
async def vote_up_cb_handler(query: CallbackQuery, callback_data: dict):
    logging.info(callback_data)
    curr = datetime.datetime(int(callback_data["year"]), int(callback_data["month"]), int(callback_data["day"]))
    await query.message.edit_text("Вы выбрали %s:" % (curr.strftime("%d/%m/%Y")))
    await query.answer('ПОЙМАЛ КНОПКУ', show_alert=True)


@dp.callback_query_handler(callback_data_calc.filter(_action=["PREV-MONTH","DAY","NEXT-MONTH"]))
async def vote_up_cb_handler(query: CallbackQuery, callback_data: dict):
    logging.info(callback_data)
    curr = datetime.datetime(int(callback_data["year"]), int(callback_data["month"]), 1)
    await query.answer('ПОЙМАЛ КНОПКУ', show_alert=True)
    # await bot.edit_message_text(f'You voted up! Now you have votes.',
    #                             query.from_user.id,
    #                             query.message.message_id)
# # @dp.callback_query_handler(callback_data_calc.filter(_action=["IGNORE", "NEXT-MONT","DAY","NEXT-MONTH"]))
# async def call_back(callback : CallbackQuery, callback_data: dict):
#     # selected,date = process_calendar_selection()
#     logging.info(callback_data)
#     await bot.edit_message_text(f'You voted up! Now you have  votes.',
#                                 callback_data.from_user.id,
#                                 callback_data.message.message_id)
    # if selected:
    # await bot.edit_message_text(f"Вы выбрали %s  {callback_data['day']}  '/' {callback_data['month']}  '/' {callback_data['year']}",
    #                             callback_data.from_user.id,
    #                             callback_data.message.message_id,
    #                             reply_markup=ReplyKeyboardRemove())
    # await bot.send_message(chat_id=callback.from_user.id,text=f"Вы выбрали %s  {callback_data['day']}  '/' {callback_data['month']}  '/' {callback_data['year']}", reply_markup=ReplyKeyboardRemove())
    # await bot.answer_callback_query()
    # else:
        #  bot.answer_callback_query(callback_query_id=callback.from_user.id, show_alert=True)
   


def register_callback_inkeybtn(dp : Dispatcher):
    dp.callback_query_handler(vote_up_cb_handler, callback_data_calc.filter(_action=["IGNORE", "PREV-MONTHT","DAY","NEXT-MONTH"]))