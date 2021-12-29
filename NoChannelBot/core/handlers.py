from typing import List, Union

from aiogram.dispatcher.filters import CommandStart, BoundFilter
from aiogram.types import Message, BotCommand, BotCommandScopeAllPrivateChats, \
    BotCommandScopeAllChatAdministrators, BotCommandScopeAllGroupChats, ContentType, CallbackQuery

from config import dp, DEVELOPERS
from core.callbacks.clb_unban_channel import clb_unban_channel, UNBAN_CHANNEL_CB
from core.cmds.cmd_ch_ban import cmd_enable_ch_ban, cmd_disable_ch_ban
from core.cmds.cmd_check_adm import cmd_check_adm
from core.cmds.cmd_start import cmd_start
from core.cmds.messages import messages
from core.cmds.restriction_cmds import cmd_whitelist, cmd_blacklist


class ChatAdminAndDevFilter(BoundFilter):
    key = 'user_id'

    def __init__(self, user_id: List):
        self.user_id = user_id

    async def check(self, msg_or_clb: Union[Message, CallbackQuery]) -> bool:
        user_id = msg_or_clb.from_user.id

        if isinstance(msg_or_clb, CallbackQuery):
            chat = msg_or_clb.message.chat

        else:
            chat = msg_or_clb.chat

        return (await chat.get_member(user_id)).is_chat_admin() or user_id in self.user_id


def bind_filters():
    dp.filters_factory.bind(ChatAdminAndDevFilter, event_handlers=[dp.message_handlers])

    return True


def register_commands_handlers():
    dp.register_message_handler(cmd_start, CommandStart())
    dp.register_message_handler(cmd_enable_ch_ban, ChatAdminAndDevFilter(DEVELOPERS), commands='enable_ch_ban')
    dp.register_message_handler(cmd_disable_ch_ban, ChatAdminAndDevFilter(DEVELOPERS), commands='disable_ch_ban')
    dp.register_message_handler(cmd_check_adm, ChatAdminAndDevFilter(DEVELOPERS), commands='check_adm')
    dp.register_message_handler(cmd_whitelist, ChatAdminAndDevFilter(DEVELOPERS), commands='whitelist')
    dp.register_message_handler(cmd_blacklist, ChatAdminAndDevFilter(DEVELOPERS), commands='blacklist')


def register_messages_handlers():
    dp.register_message_handler(messages, content_types=[
        ContentType.TEXT, ContentType.AUDIO, ContentType.DOCUMENT, ContentType.GAME, ContentType.PHOTO,
        ContentType.STICKER, ContentType.VIDEO, ContentType.VIDEO_NOTE, ContentType.VOICE, ContentType.CONTACT,
        ContentType.LOCATION, ContentType.VENUE, ContentType.POLL, ContentType.DICE])


def register_callback_query_handlers():
    dp.register_callback_query_handler(clb_unban_channel, UNBAN_CHANNEL_CB.filter(), ChatAdminAndDevFilter(DEVELOPERS))


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
        BotCommand('whitelist', 'Разбанить канал'),
        BotCommand('blacklist', 'Забанить канал')
    ], scope=BotCommandScopeAllChatAdministrators())
