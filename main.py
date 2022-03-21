from aiogram.utils import executor
from create_bot import dp
from handlers import personal_actions, constants, plan


async def on_start(_):
	print(constants.cons_on_start)
personal_actions.register_hndlr_clnt(dp)
plan.register_hndlr_plans(dp)


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True, on_startup=on_start)
