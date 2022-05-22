import aiosqlite
from aiogram import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.exceptions import TelegramAPIError

from config import DB_URL, dp, DEVELOPERS
from core.db.tables import create_tables
from core.handlers import register_commands_handlers, register_errors_handlers, register_messages_handlers, \
    bind_filters, set_commands, register_callback_query_handlers
from core.middlewares import register_middlewares


async def on_start(dps: Dispatcher):
    async with aiosqlite.connect(DB_URL) as db:
        db.getName()

    await create_tables()
    await set_commands()

    for developer in DEVELOPERS:
        try:
            await dps.bot.send_message(chat_id=developer,
                                       text=f"{(await dps.bot.get_me()).mention} started!",
                                       parse_mode=ParseMode.HTML)

        except TelegramAPIError:
            continue


async def on_shutdown(dps: Dispatcher):
    await dps.storage.close()
    await dps.storage.wait_closed()

    print("End")


def main():
    bind_filters()
    register_commands_handlers()
    register_callback_query_handlers()
    register_messages_handlers()
    register_errors_handlers()

    register_middlewares()

    print('[+]: BOT STARTED')

    executor.start_polling(dp, skip_updates=True, on_startup=on_start, on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
