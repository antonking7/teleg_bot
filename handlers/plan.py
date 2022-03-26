from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot, dp, BotDB
from handlers import constants
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from keyboards import inlinekeyboard
import logging
import datetime


class FSMtimetable(StatesGroup):
    dateplans = State()
    timeplans = State()
    activity = State()


# Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands=constants.cons_comand_load, state=None)
async def cmd_load(message: types.Message, state: FSMContext):
    await message.reply(constants.cons_msg_load_date,
                        reply_markup=inlinekeyboard.create_calendar(year=None, month=None))
    # if inlinekeyboard.callback_data_calc:
    #     async with state.proxy() as data:
    #         data['dateplans'] = message.text
    #     await bot.send_message(message.from_user.id, str(data["dateplans"]) )
    # await FSMtimetable.dateplans.set()


@dp.callback_query_handler(inlinekeyboard.callback_data_calc.filter(_action="DAY"))
async def vote_up_cb_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(callback_data)
    curr = datetime.datetime(int(callback_data["year"]), int(callback_data["month"]), int(callback_data["day"]))
    await query.message.edit_text("Вы выбрали %s" % (curr.strftime("%d.%m.%Y")))
    await FSMtimetable.dateplans.set()
    async with state.proxy() as data:
        data['dateplans'] = curr.strftime("%d-%m-%Y")
        logging.info(data['dateplans'])
    await FSMtimetable.next()
    await bot.send_message(chat_id=query.message.chat.id, text=constants.cons_msg_load_time)
    await query.answer()


# Ответы от пользователя и записываем в память
# @dp.message_handler(state=FSMtimetable.dateplans)
async def load_date(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['dateplans'] = message.text
    await FSMtimetable.next()
    await message.reply(constants.cons_msg_load_time)


# @dp.message_handler(state=FSMtimetable.timeplans)
async def load_time(message: types.Message, state: FSMContext):
    logging.info(message.text)
    async with state.proxy() as data:
        data['timeplans'] = message.text
        logging.info(data['timeplans'])
    await FSMtimetable.next()
    await message.reply(constants.cons_msg_load_activity)


# @dp.message_handler(state=FSMtimetable.activity)
async def load_activity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['activity'] = message.text
        logging.info(data['timeplans'])
    member = message.from_user.id
    async with state.proxy() as data:
        date_ = data['dateplans']
        time_ = data['timeplans']
        # time_ = time.strftime(time_,"%H:%M")
        activity_ = data['activity']
        logging.info(date_)
        logging.info(time_)
        logging.info(activity_)
    if (BotDB.get_user_id(user_id=member)):
        BotDB.add_record(user_id=member, date=date_, time=time_, activity=activity_)
        await message.reply("✅ Запись успешно внесена!")
    else:
        BotDB.add_user(user_id=member)
        BotDB.add_record(user_id=member, date=date_, time=time_, activity=activity_)
        await message.reply("✅ Запись успешно внесена!")

    await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply(constants.cons_msg_canсel)


# Регистрируем хендлеры
def register_hndlr_plans(dp: Dispatcher):
    # dp.callback_query_handler(call_back())
    dp.register_message_handler(cmd_load, Text(equals=constants.cons_comand_load), state=None)
    dp.register_message_handler(cancel_handler, state="*",
                                commands=constants.cons_comand_canсel)  # Text(equals=constants.cons_comand_load) cons_comand_load
    dp.register_message_handler(cancel_handler, Text(equals=constants.cons_comand_canсel, ignore_case=True), state="*")
    dp.register_message_handler(load_date, state=FSMtimetable.dateplans)
    dp.register_message_handler(load_time, state=FSMtimetable.timeplans)
    dp.register_message_handler(load_activity, state=FSMtimetable.activity)
    # dp.register_message_handler(cancel_handler, state="*", commands=constants.cons_comand_canсel)
    # dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state= "*")
