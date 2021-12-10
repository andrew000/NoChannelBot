import json

import aiosqlite
from aiogram.types import Message

from config import DB_URL, dp
from core.db.utils import dict_factory
from core.models.group import GroupSettings


@dp.throttled(rate=2)
async def cmd_enable_ch_ban(msg: Message):
    async with aiosqlite.connect(DB_URL) as db:
        db.row_factory = dict_factory
        async with db.execute("SELECT settings FROM groups WHERE id = ?", (msg.chat.id,)) as cursor:
            query = await cursor.fetchone()
            if not query:
                return

            query = json.loads(query.get('settings'))
            group_settings: GroupSettings = GroupSettings.parse_obj(query)

        group_settings.ban_channels = True
        await db.execute("UPDATE groups SET settings = ? WHERE id = ?", (group_settings.json(), msg.chat.id))
        await db.commit()

        await msg.reply("🟢 Бан каналов включён")


@dp.throttled(rate=2)
async def cmd_disable_ch_ban(msg: Message):
    async with aiosqlite.connect(DB_URL) as db:
        db.row_factory = dict_factory
        async with db.execute("SELECT settings FROM groups WHERE id = ?", (msg.chat.id,)) as cursor:
            query = await cursor.fetchone()
            if not query:
                return

            query = json.loads(query.get('settings'))
            group_settings: GroupSettings = GroupSettings.parse_obj(query)

        group_settings.ban_channels = False
        await db.execute("UPDATE groups SET settings = ? WHERE id = ?", (group_settings.json(), msg.chat.id))
        await db.commit()

        await msg.reply("🔴 Бан каналов выключён")
