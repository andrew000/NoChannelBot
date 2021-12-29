from sqlite3 import IntegrityError

import aiosqlite
from aiogram.types import CallbackQuery, ParseMode
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import TelegramAPIError
from aiogram.utils.markdown import hcode

from config import DB_URL, dp

UNBAN_CHANNEL_CB: CallbackData = CallbackData("unban_channel", "sender_chat_id")


@dp.throttled(rate=5)
async def clb_unban_channel(clb: CallbackQuery):
    sender_chat_id = UNBAN_CHANNEL_CB.parse(clb.data).get("sender_chat_id")

    async with aiosqlite.connect(DB_URL) as db:
        try:
            await db.execute("INSERT INTO whitelist (chat_id, sender_chat_id) VALUES (?, ?)",
                             (clb.message.chat.id, sender_chat_id))
            await db.commit()

            await clb.message.chat.unban_sender_chat(int(sender_chat_id))

            await clb.answer(f"🟢 Канал {sender_chat_id} добавлен в белый список", show_alert=True)
            await clb.message.edit_text(f"🟢 Канал {hcode(sender_chat_id)} добавлен в белый список",
                                        parse_mode=ParseMode.HTML)

        except IntegrityError:
            await clb.answer(f"🟡 Канал {sender_chat_id} уже в белом списке", show_alert=True)
            await clb.message.edit_text(f"🟡 Канал {hcode(sender_chat_id)} уже в белом списке",
                                        parse_mode=ParseMode.HTML)

        except TelegramAPIError:
            await clb.answer(f"🟡 Произошла непредвиденная ошибка", show_alert=True)
            await clb.message.edit_text(f"🟡 Произошла непредвиденная ошибка, по которой бот не смог разбанить канал "
                                        f"{hcode('sender_chat_id')}.\n"
                                        f"\n"
                                        f"Проверьте есть ли у бота нужные права",
                                        parse_mode=ParseMode.HTML)
