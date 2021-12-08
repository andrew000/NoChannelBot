from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from environs import Env

env = Env()
env.read_env()

DEVELOPERS = (382182253, 641848459)

DB_URL = Path('./db') / 'no_channel.db'

bot = Bot(token=env.str('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, no_throttle_error=True)
