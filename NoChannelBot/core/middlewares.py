from sqlite3 import IntegrityError

import aiosqlite
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import ChatType, Message

from config import DB_URL, dp
from core.models.group import GroupModel
from core.models.user import UserModel


class CheckGroupMiddleware(BaseMiddleware):
    """
    Check group in DB
    """

    GROUP_ID_CACHE = set()

    def __init__(self):
        super(CheckGroupMiddleware, self).__init__()

    async def on_process_message(self, msg: Message, _):
        if msg.chat.type != ChatType.SUPERGROUP:
            return

        if msg.chat.id in self.GROUP_ID_CACHE:
            return

        async with aiosqlite.connect(DB_URL) as db:
            async with db.execute("SELECT id FROM groups WHERE id == ?", (msg.chat.id,)) as cursor:
                group = await cursor.fetchone()

            if not group:
                new_group = GroupModel(id=msg.chat.id,
                                       member_count=await msg.chat.get_member_count(),
                                       link=await msg.chat.get_url())
                try:
                    await db.execute("INSERT INTO groups(id, member_count, link, settings) VALUES (?, ?, ?, ?)",
                                     (new_group.id,
                                      new_group.member_count,
                                      new_group.link,
                                      new_group.settings.json()))

                except IntegrityError:
                    await db.execute("UPDATE groups SET member_count = ?, link = ? WHERE id = ?",
                                     (await msg.chat.get_member_count(),
                                      await msg.chat.get_url(),
                                      msg.chat.id))

            else:
                await db.execute("UPDATE groups SET member_count = ?, link = ? WHERE id = ?",
                                 (await msg.chat.get_member_count(),
                                  await msg.chat.get_url(),
                                  msg.chat.id))

            await db.commit()

            self.GROUP_ID_CACHE.add(msg.chat.id)


class CheckUserMiddleware(BaseMiddleware):
    """
    Check user in DB
    """
    USER_ID_CACHE = set()

    def __init__(self):
        super(CheckUserMiddleware, self).__init__()

    async def on_process_message(self, msg: Message, _):  # noqa
        if msg.from_user.id in self.USER_ID_CACHE:
            return

        async with aiosqlite.connect(DB_URL) as db:
            async with db.execute("SELECT id FROM users WHERE id == ?", (msg.from_user.id,)) as cursor:
                user = await cursor.fetchone()

            if not user:
                new_user = UserModel(id=msg.from_user.id,
                                     first_name=msg.from_user.first_name,
                                     last_name=msg.from_user.last_name,
                                     username=msg.from_user.username,
                                     language_code=msg.from_user.language_code)

                try:
                    await db.execute("INSERT INTO users(id, first_name, last_name, username, language_code) "
                                     "VALUES (?, ?, ?, ?, ?)",
                                     (new_user.id,
                                      new_user.first_name,
                                      new_user.last_name,
                                      new_user.username,
                                      new_user.language_code))
                except IntegrityError:
                    await db.execute("UPDATE users SET first_name = ?, last_name = ?, username = ?, language_code = ? "
                                     "WHERE id = ?",
                                     (msg.from_user.first_name,
                                      msg.from_user.last_name,
                                      msg.from_user.username,
                                      msg.from_user.language_code,
                                      msg.from_user.id))
            else:
                await db.execute("UPDATE users SET first_name = ?, last_name = ?, username = ?, language_code = ? "
                                 "WHERE id = ?",
                                 (msg.from_user.first_name,
                                  msg.from_user.last_name,
                                  msg.from_user.username,
                                  msg.from_user.language_code,
                                  msg.from_user.id))

            await db.commit()

            self.USER_ID_CACHE.add(msg.from_user.id)


def register_middlewares():
    dp.middleware.setup(CheckGroupMiddleware())
    dp.middleware.setup(CheckUserMiddleware())
