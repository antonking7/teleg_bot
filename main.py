from aiogram.utils import executor
from aiogram import types
from create_bot import dp, loop
from handlers import personal_actions, constants, plan
from keyboards import inlinekeyboard

async def on_start(_):
	print(constants.cons_on_start)

personal_actions.register_hndlr_clnt(dp)
plan.register_hndlr_plans(dp)
inlinekeyboard.register_callback_inkeybtn(dp)



if __name__ == '__main__':
	executor.start_polling(dp, loop=loop, skip_updates=True, on_startup=on_start)
