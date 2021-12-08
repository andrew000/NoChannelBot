from aiogram.types import Message

from config import dp


@dp.throttled(rate=2)
async def cmd_unban(msg: Message):
    if not msg.reply_to_message:
        await msg.reply("Необходимо ответить на сообщение канала, который нужно разбанить")
        return

    elif not msg.reply_to_message.sender_chat:
        await msg.reply("Необходимо ответить на сообщения канала, а не пользователя")
        return

    elif msg.reply_to_message.from_user.id != 777000:
        await msg.reply("Необходимо ответить на сообщения канала, а не анонимного админа")
        return

    try:
        await msg.chat.unban_sender_chat(msg.reply_to_message.sender_chat.id)
        await msg.answer(f"Канал {msg.reply_to_message.sender_chat.mention} разбанен!")

    except Exception as exc:
        print(cmd_unban.__name__, exc, type(exc).mro())
