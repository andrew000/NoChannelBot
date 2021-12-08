from aiogram.types import Message, ChatMemberAdministrator, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hlink

from config import dp


@dp.throttled(rate=5)
async def cmd_check_adm(msg: Message):
    me = await msg.chat.get_member(msg.bot.id)

    if isinstance(me, ChatMemberAdministrator):
        if me.can_restrict_members:
            await msg.reply("✅ Системы работают нормально!\n"
                            "\n"
                            "Бот готов к работе")

            return

    await msg.reply("❌ У бота нет прав и пока что он не может работать.\n"
                    "\n"
                    "➡️ Чтобы решить проблему - выдайте боту право на ограничение участников.\n"
                    "\n"
                    f"⚠️ {hlink('Инструкция', 'https://telegra.ph/Instrukciya-po-nastrojke-NoChannel-Bot-12-08')} ⚠️",
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton('⚠️ Инструкция ⚠️',
                                              url='https://telegra.ph/Instrukciya-po-nastrojke-NoChannel-Bot-12-08')
                         ]]),
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True)
