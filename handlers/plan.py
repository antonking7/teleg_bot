from cgitb import text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import  types, Dispatcher
from create_bot import dp
from handlers import constants
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import calendar
import locale 

class FSMtimetable(StatesGroup):
    dateplans = State()
    timeplans = State()
    activity  = State()

def create_callback_data(action,year,month,day):
    """ Create the callback data associated to each button"""
    return ";".join([action,str(year),str(month),str(day)])

def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")

def create_calendar(year=None, month=None):
    now = datetime.datetime.now()
    if year == None:
        year = now.year
    if  month == None:
         month = now. month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboards = InlineKeyboardMarkup()
    keyboards_list = []
#Первая строка будет Месяц и Год
    # row = []
# установка родной локали, чтобы название месяца Python стал выводить кириллицей
    locale.setlocale(locale.LC_ALL, "")  
    frst_row_name = calendar.month_name[month]+" "+str(year)
    row = InlineKeyboardButton(text=frst_row_name, callback_data=data_ignore)
    # row.append(InlineKeyboardButton(text=frst_row_name, callback_data=data_ignore))
    # keyboards_list.append(row)
    keyboards.add(row)
#Вторая строка дни недели
    row=[]
    for day in ["ПН","ВТ","СР","ЧТ","ПТ","СБ","ВС"]:
         row.append(InlineKeyboardButton(text=day,callback_data=data_ignore))
    keyboards.row(*row)
    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(str(day),callback_data=create_callback_data("DAY",year,month,day)))
        keyboards.row(*row)
#Последний ряд кнопок переключение месяца вперед или назад
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=create_callback_data("PREV-MONTH",year,month,day)))
    row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
    row.append(InlineKeyboardButton(">",callback_data=create_callback_data("NEXT-MONTH",year,month,day)))
    keyboards.row(*row)

    return keyboards   

#Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands=constants.cons_comand_load, state=None)
async def cmd_load(message : types.Message): 
    await FSMtimetable.dateplans.set()
    await message.reply(constants.cons_msg_load_date, reply_markup=create_calendar(year=None, month=None))

#Ответы от пользователя и записываем в память
# @dp.message_handler(state=FSMtimetable.dateplans)
async def load_date(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dateplans'] = message.text
    await FSMtimetable.next()
    await message.reply(constants.cons_msg_load_time)

#Ловим ответ от календаря и обрабатываем его
async def call_back(callback : types.CallbackQuery):
    await callback.message.answer('1')
    await callback.answer()

# @dp.message_handler(state=FSMtimetable.timeplans)
async def load_time(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['timeplans'] = message.text
    await FSMtimetable.next()
    await message.reply(constants.cons_msg_load_activity)

# @dp.message_handler(state=FSMtimetable.activity)
async def load_activity(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['activity'] = message.text

    await state.finish()

async def cancel_handler(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply(constants.cons_msg_canсel)



#Регистрируем хендлеры
def register_hndlr_plans(dp : Dispatcher ):
    dp.register_message_handler(cmd_load, commands=constants.cons_comand_load, state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=constants.cons_comand_canсel)
    dp.register_message_handler(cancel_handler, Text(equals=constants.cons_comand_canсel, ignore_case=True), state= "*")
    dp.register_message_handler(load_date, state=FSMtimetable.dateplans)
    dp.callback_query_handler(call_back, Text(startswith='PREV-MONTH'))
    dp.register_message_handler(load_time, state=FSMtimetable.timeplans)
    dp.register_message_handler(load_activity, state=FSMtimetable.activity)
    # dp.register_message_handler(cancel_handler, state="*", commands=constants.cons_comand_canсel)
    # dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state= "*")