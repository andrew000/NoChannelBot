import asyncio
import contextlib
import json

import aiosqlite
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.utils.exceptions import TelegramAPIError
from aiogram.utils.markdown import hcode, hbold

from config import DB_URL, dp, CHANNEL_BOT_ID
from core.callbacks.clb_unban_channel import UNBAN_CHANNEL_CB
from core.db.utils import dict_factory
from core.models.group import GroupSettings


@dp.throttled(rate=2)
async def messages(msg: Message):
    if not msg.sender_chat or msg.from_user.id != CHANNEL_BOT_ID:
        return

    async with aiosqlite.connect(DB_URL) as db:
        db.row_factory = dict_factory
        async with db.execute("SELECT settings FROM groups WHERE id = ?", (msg.chat.id,)) as cursor:
            query = await cursor.fetchone()

            if not query:
                return

    query = json.loads(query.get('settings'))
    group_settings: GroupSettings = GroupSettings.parse_obj(query)

    if group_settings.ban_channels is True:
        if (await msg.chat.get_member(msg.bot.id)).is_chat_admin():
            async with aiosqlite.connect(DB_URL) as db:
                async with db.execute("SELECT EXISTS(SELECT chat_id, sender_chat_id "
                                      "FROM whitelist WHERE chat_id = ? AND sender_chat_id = ?)",
                                      (msg.chat.id, msg.sender_chat.id)) as cursor:
                    query = await cursor.fetchone()

            if query[0] == 0:  # SENDER_CHAT is not whitelisted
                try:
                    await msg.chat.ban_sender_chat(sender_chat_id=msg.sender_chat.id)
                    await msg.reply(f"❗️ Слать сообщения от имени каналов в этой группе — {hbold('ЗАПРЕЩЕНО')}\n"
                                    "\n"
                                    f"🔨 Канал {hcode(msg.sender_chat.id)} забанен",
                                    reply_markup=InlineKeyboardMarkup(
                                        inline_keyboard=[[
                                            InlineKeyboardButton(text="⚪️ Разбанить канал",
                                                                 callback_data=UNBAN_CHANNEL_CB.new(
                                                                     sender_chat_id=msg.sender_chat.id))]]),
                                    parse_mode=ParseMode.HTML)

                except Exception as exc:
                    print(messages.__name__, exc, type(exc).mro())

                await asyncio.sleep(30)

                with contextlib.suppress(TelegramAPIError):
                    await msg.delete()
