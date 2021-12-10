import json

import aiosqlite
from aiogram.types import Message

from config import DB_URL, dp
from core.db.utils import dict_factory
from core.models.group import GroupSettings


@dp.throttled(rate=2)
async def messages(msg: Message):
    if not msg.sender_chat:
        return

    if msg.from_user.id != 777000:
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
            try:
                await msg.chat.ban_sender_chat(sender_chat_id=msg.sender_chat.id, until_date=group_settings.until_date)
                await msg.reply("❗️ Слать сообщения от имени каналов в этой группе - ЗАПРЕЩЕНО")

            except Exception as exc:
                print(messages.__name__, exc, type(exc).mro())
