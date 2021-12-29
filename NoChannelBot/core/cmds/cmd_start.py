from aiogram.types import Message, ParseMode
from aiogram.utils.markdown import hbold

from config import dp


@dp.throttled(rate=2)
async def cmd_start(msg: Message):
    await msg.reply(f"🚀 Скажи {hbold('НЕТ 🖕')} долбоёбам, которые пишут от имени канала.\n"
                    f"\n"
                    f"❗️ Для работы нужна админка с разрешением ограничиввать пользователей ❗️\n"
                    f"/check_adm - проверить работоспособность\n"
                    f"\n"
                    f""
                    f"/enable_ch_ban - Включить бан каналов\n"
                    f"/disable_ch_ban - Выключить бан каналов\n"
                    f"\n"
                    f"/whitelist - Добавить канал в белый список\n"
                    f"/blacklist - Убрать канал из белого списка",
                    parse_mode=ParseMode.HTML)
