import aiosqlite

from config import DB_URL

group = """CREATE TABLE IF NOT EXISTS groups
(
id BIGINT NOT NULL PRIMARY KEY,
member_count BIGINT,
link VARCHAR,
settings TEXT
)"""

users = """CREATE TABLE IF NOT EXISTS users
(
id BIGINT NOT NULL PRIMARY KEY,
first_name TEXT NOT NULL,
last_name TEXT,
username TEXT,
language_code TEXT,
ban BOOLEAN NOT NULL DEFAULT FALSE,
active_pm BOOLEAN NOT NULL DEFAULT FALSE
);
"""

whitelist = """CREATE TABLE IF NOT EXISTS whitelist
(
chat_id BIGINT NOT NULL,
sender_chat_id BIGINT NOT NULL,
PRIMARY KEY (chat_id, sender_chat_id)
)"""


async def create_tables():
    async with aiosqlite.connect(DB_URL) as db:
        for table in (group, users, whitelist):
            await db.execute(table)
            await db.commit()
