from typing import List

from aiogram.dispatcher.filters import CommandStart, BoundFilter
from aiogram.types import Message, BotCommand, BotCommandScopeAllPrivateChats, \
    BotCommandScopeAllChatAdministrators, BotCommandScopeAllGroupChats, ContentType

from config import dp, DEVELOPERS
from core.cmds.cmd_ch_ban import cmd_enable_ch_ban, cmd_disable_ch_ban
from core.cmds.cmd_check_adm import cmd_check_adm
from core.cmds.cmd_start import cmd_start
from core.cmds.cmd_unban import cmd_unban
from core.cmds.messages import messages


class ChatAdminAndDevFilter(BoundFilter):
    key = 'user_id'

    def __init__(self, user_id: List):
        self.user_id = user_id

    async def check(self, msg: Message) -> bool:
        return (await msg.chat.get_member(msg.from_user.id)).is_chat_admin() or msg.from_user.id in self.user_id


def bind_filters():
    dp.filters_factory.bind(ChatAdminAndDevFilter, event_handlers=[dp.message_handlers])

    return True


def register_commands_handlers():
    dp.register_message_handler(cmd_start, CommandStart())
    dp.register_message_handler(cmd_enable_ch_ban, ChatAdminAndDevFilter(DEVELOPERS), commands='enable_ch_ban')
    dp.register_message_handler(cmd_disable_ch_ban, ChatAdminAndDevFilter(DEVELOPERS), commands='disable_ch_ban')
    dp.register_message_handler(cmd_check_adm, ChatAdminAndDevFilter(DEVELOPERS), commands='check_adm')
    dp.register_message_handler(cmd_unban, ChatAdminAndDevFilter(DEVELOPERS), commands='ch_unban')


def register_messages_handlers():
    dp.register_message_handler(messages, content_types=[
        ContentType.TEXT, ContentType.AUDIO, ContentType.DOCUMENT, ContentType.GAME, ContentType.PHOTO,
        ContentType.STICKER, ContentType.VIDEO, ContentType.VIDEO_NOTE, ContentType.VOICE, ContentType.CONTACT,
        ContentType.LOCATION, ContentType.VENUE, ContentType.POLL, ContentType.DICE])


def register_errors_handlers():
    ...


async def set_commands():
    await dp.bot.set_my_commands(commands=[
        BotCommand('start', 'Начало начал')
    ], scope=BotCommandScopeAllPrivateChats())

    await dp.bot.set_my_commands(commands=[
        BotCommand('start', 'Начало начал')
    ], scope=BotCommandScopeAllGroupChats())

    await dp.bot.set_my_commands(commands=[
        BotCommand('start', 'Начало начал'),
        BotCommand('enable_ch_ban', 'Включить бан каналов'),
        BotCommand('disable_ch_ban', 'Выключить бан каналов'),
        BotCommand('check_adm', 'Проверка работоспособности'),
        BotCommand('ch_unban', 'Разбанить канал')
    ], scope=BotCommandScopeAllChatAdministrators())
