import asyncpg
from app.core.config import DatabaseConfig, load_database_config

db_config: DatabaseConfig = load_database_config()


async def get_notes(user_id: int) -> list:
    conn = await asyncpg.connect(database=db_config.db.database_name, user=db_config.db.user,
                                 password=db_config.db.password, host=db_config.db.host, port=db_config.db.port)
    query = await conn.fetch(f'SELECT note '
                             'FROM notes '
                             f'WHERE user_id = {user_id}')
    notes = []
    for row in query:
        notes.append(row['note'])
    await conn.close()
    return notes


async def get_user_data(username: str) -> dict:
    conn = await asyncpg.connect(database=db_config.db.database_name, user=db_config.db.user,
                                 password=db_config.db.password, host=db_config.db.host, port=db_config.db.port)
    query = await conn.fetch(f"SELECT username, password FROM users WHERE username = '{username}'")
    result = {}
    for row in query:
        result['username'] = row['username']
        result['password'] = row['password']
    await conn.close()
    return result


async def insert_new_user(username: str, password: str) -> None:
    conn = await asyncpg.connect(database=db_config.db.database_name, user=db_config.db.user,
                                 password=db_config.db.password, host=db_config.db.host, port=db_config.db.port)
    query = await conn.fetch(f"INSERT INTO users (username, password) "
                             f"VALUES ('{username}', '{password}')")
    await conn.close()


async def insert_new_note(user_id: int, note_text: str) -> None:
    conn = await asyncpg.connect(database=db_config.db.database_name, user=db_config.db.user,
                                 password=db_config.db.password, host=db_config.db.host, port=db_config.db.port)
    query = await conn.fetch(f"INSERT INTO notes (user_id, note) "
                             f"VALUES ({user_id}, '{note_text}')")
    await conn.close()


async def get_username_by_id(user_id: int) -> str:
    conn = await asyncpg.connect(database=db_config.db.database_name, user=db_config.db.user,
                                 password=db_config.db.password, host=db_config.db.host, port=db_config.db.port)
    query = await conn.fetch(f"SELECT username "
                             f"FROM users "
                             f"WHERE id = {user_id}")
    await conn.close()
    username = ''
    for row in query:
        username = username.join(row)
    return username
