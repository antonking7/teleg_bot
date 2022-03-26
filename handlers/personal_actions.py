from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from create_bot import bot, BotDB
from handlers import constants
from keyboards import percon_kb
from scrab_news import gest_scrab_news
from datetime import datetime, timedelta
import logging
import json
import time


# @dp.message_handler()
async def cmd_start(message: types.message):
    # await message.delete()
    await bot.send_message(message.from_user.id, constants.cons_msg_start, reply_markup=percon_kb.kb_person)


async def cmd_timetable(message: types.message):
    # await message.delete()
    records = BotDB.get_record(message.from_user.id, datetime.now().strftime("%d-%m-%Y"))
    logging.info(datetime.now().strftime("%d-%m-%Y"))
    logging.info(records)
    if (len(records)):
        answer = f"🕘 Планы на сегодня\n"
        for r in records:
            answer += f" В {r[3]}"
            answer += f" <i>-{r[4]}</i>\n"
        logging.info(answer)
        await bot.send_message(message.from_user.id, answer)
        # await message.reply(answer)
    else:
        await bot.send_message(message.from_user.id, constants.cons_msg_timetable)


async def cmd_get_news(message: types.message):
    await message.answer(constants.cons_msg_wait)

    # Если файла парсинга новостей нет то вызовем метод получения и парсинга новостей
    try:
        with open("news_dict.json") as file:
            news_dict = json.load(file)
    except Exception as ex:
        logging.info("except и вызов gest_scrab_news()")
        gest_scrab_news()
        time.sleep(5)
        with open("news_dict.json") as file:
            news_dict = json.load(file)

    # Если файл есть, но он путой. Вызовем парсер новостей.
    if not news_dict:
        logging.info("json пуст и вызов gest_scrab_news()")
        gest_scrab_news()
        time.sleep(5)
        try:
            with open("news_dict.json") as file:
                news_dict = json.load(file)
        except Exception as ex:
            logging.info("except не удалость прочтитать фай news_dict2.json")
            await message.answer(constants.cons_msg_nofile)
    else:
        # Проверяем время обновления новостей, если прошло более 10 минут, вызываем парсер и обновляем json файл
        now = datetime.now()
        update_time = datetime.strptime(news_dict[0].get("update_time"), "%Y-%m-%d %H:%M:%S.%f")
        if now - update_time > timedelta(minutes=30):
            logging.info("update_time больше 30 минут и вызов gest_scrab_news()")
            gest_scrab_news()
            time.sleep(5)
            try:
                with open("news_dict.json") as file:
                    news_dict = json.load(file)
            except Exception as ex:
                logging.info("except не удалость прочтитать фай news_dict2.json")
                await message.answer(constants.cons_msg_nofile)
    if not news_dict:
        await message.answer(constants.cons_msg_nofile)
    else:
        for news in news_dict:
            title_card = news.get("title")
            url_card = news.get("url")
            descr_card = news.get("discr")
            card = f"{hlink(title_card, url_card)}\n" \
                   f"{descr_card}"
            await message.answer(card)


def register_hndlr_clnt(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=[constants.cons_comand_start, constants.cons_comand_help])
    dp.register_message_handler(cmd_timetable, Text(equals=constants.cons_comand_timetable))  # cons_comand_timetable
    dp.register_message_handler(cmd_get_news, Text(equals=constants.cons_comand_get_news))
