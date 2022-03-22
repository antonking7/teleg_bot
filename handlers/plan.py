from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot, dp
from handlers import constants
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from keyboards import inlinekeyboard
class FSMtimetable(StatesGroup):
    dateplans = State()
    timeplans = State()
    activity  = State()


#Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands=constants.cons_comand_load, state=None)
async def cmd_load(message : types.Message): 
    await message.reply(constants.cons_msg_load_date, reply_markup=inlinekeyboard.create_calendar(year=None, month=None))
    # await FSMtimetable.dateplans.set()


#Ответы от пользователя и записываем в память
# @dp.message_handler(state=FSMtimetable.dateplans)
async def load_date(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dateplans'] = message.text
    await FSMtimetable.next()
    await message.reply(constants.cons_msg_load_time)


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
def register_hndlr_plans(dp : Dispatcher):
    # dp.callback_query_handler(call_back())
    dp.register_message_handler(cmd_load, commands=constants.cons_comand_load, state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=constants.cons_comand_canсel)
    dp.register_message_handler(cancel_handler, Text(equals=constants.cons_comand_canсel, ignore_case=True), state= "*")
    dp.register_message_handler(load_date, state=FSMtimetable.dateplans)
    dp.register_message_handler(load_time, state=FSMtimetable.timeplans)
    dp.register_message_handler(load_activity, state=FSMtimetable.activity)
    # dp.register_message_handler(cancel_handler, state="*", commands=constants.cons_comand_canсel)
    # dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state= "*")