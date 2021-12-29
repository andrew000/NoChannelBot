from sqlite3 import IntegrityError

import aiosqlite
from aiogram.types import Message, ChatType, ParseMode
from aiogram.utils.exceptions import ChatNotFound, TelegramAPIError
from aiogram.utils.markdown import hcode

from config import dp, CHANNEL_BOT_ID, DB_URL


async def _validate_cmd(msg: Message, command: str) -> int:
    """
    Return `sender_chat_id: int` if validation is OK, else return `0`

    P.S. I don't want use `raise` and `try: except:` statements :)
    """
    if msg.chat.type != ChatType.SUPERGROUP:
        await msg.reply("🔴 Команду можно использовать только в группах")
        return 0

    if msg.reply_to_message and msg.reply_to_message.sender_chat:
        if msg.reply_to_message.from_user.id != CHANNEL_BOT_ID:
            await msg.reply("🔴 Команду можно использовать только для разбана каналов")
            return 0

        else:
            sender_chat_id = msg.reply_to_message.sender_chat.id

    elif sender_chat_id := msg.get_args().split(" ", maxsplit=1)[0]:
        if sender_chat_id.replace('-', '', 1).isdecimal():
            sender_chat_id = int(sender_chat_id)

        else:
            await msg.reply("🔴 Необходимо указать корректное число")
            return 0

        try:
            await msg.bot.get_chat(sender_chat_id)

        except ChatNotFound:
            await msg.reply("🔴 Такого чата не существует или бот ни разу не встречался с таковым")
            return 0

    else:
        await msg.reply("💁‍♂️ Необходимо ответить командой на сообщение канала или указать его ID.\n"
                        "\n"
                        "Если ответить на сообщение канала — бот добавит или удалит его из белого списка в зависимости "
                        f"от команды ({hcode('/whitelist')} | {hcode('/blacklist')}).\n"
                        "\n"
                        "Также можно указать ID канала:\n"
                        f"{hcode(f'/{command} channel_id')}\n"
                        "\n"
                        f"Где {hcode('channel_id')} это цифра, то есть ID канала.",
                        parse_mode=ParseMode.HTML)
        return 0

    return sender_chat_id


@dp.throttled(rate=3)
async def cmd_whitelist(msg: Message):
    if (sender_chat_id := await _validate_cmd(msg, "whitelist")) == 0:
        return

    async with aiosqlite.connect(DB_URL) as db:
        try:
            await db.execute("INSERT INTO whitelist (chat_id, sender_chat_id) VALUES (?, ?)",
                             (msg.chat.id, sender_chat_id))
            await db.commit()

            await msg.chat.unban_sender_chat(sender_chat_id)

        except IntegrityError:
            await msg.reply(f"🟡 Канал {hcode(sender_chat_id)} уже в белом списке",
                            parse_mode=ParseMode.HTML)

        except TelegramAPIError:
            await msg.reply(f"🟡 Произошла непредвиденная ошибка, по которой бот не смог разбанить канал.\n"
                            f"\n"
                            f"Проверьте есть ли у бота нужные права")

        except Exception as exc:
            print(cmd_whitelist.__name__, exc, type(exc).mro())

        else:
            await msg.reply(f"🟢 Канал {hcode(sender_chat_id)} добавлен в белый список чата",
                            parse_mode=ParseMode.HTML)


@dp.throttled(rate=3)
async def cmd_blacklist(msg: Message):
    if (sender_chat_id := await _validate_cmd(msg, "blacklist")) == 0:
        return

    async with aiosqlite.connect(DB_URL) as db:
        await db.execute("DELETE FROM whitelist WHERE chat_id = ? AND sender_chat_id = ?",
                         (msg.chat.id, sender_chat_id))
        await db.commit()

    try:
        await msg.chat.ban_sender_chat(sender_chat_id)
        await msg.reply(f"🟢 Канал {hcode(sender_chat_id)} удалён их белого списка чата",
                        parse_mode=ParseMode.HTML)

    except TelegramAPIError:
        await msg.reply(f"🟡 Произошла непредвиденная ошибка, по которой бот не смог забанить канал.\n"
                        f"\n"
                        f"Проверьте есть ли у бота нужные права")

    except Exception as exc:
        print(cmd_blacklist.__name__, exc, type(exc).mro())
