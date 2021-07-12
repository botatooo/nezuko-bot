import os
import sqlite3

from os.path import abspath, join
from dotenv import load_dotenv, find_dotenv

import discord
from discord.ext import commands

load_dotenv(find_dotenv())

DEFAULT_PREFIX = os.getenv('PREFIX') or '.'
DB_FILENAME = os.getenv('DB_FILE') or 'nezuko.sql'

conn = sqlite3.connect(DB_FILENAME)


def create_prefix_table():
    print('Creating "PREFIXES" table...')
    try:
        conn.execute('''CREATE TABLE PREFIXES
             (PREFIX TEXT PRIMARY KEY     NOT NULL,
             GUILD_ID           TEXT    NOT NULL);''')
        conn.commit()
    except sqlite3.OperationalError:
        pass


def add_prefix(guild_id: int, prefix: str):
    try:
        conn.execute(f'INSERT INTO PREFIXES (GUILD_ID,PREFIX) \
                VALUES ({int(guild_id)}, "{str(prefix)}")')
        conn.commit()
        print('add', conn.cursor().fetchall())
    except sqlite3.OperationalError:
        create_prefix_table()
        add_prefix(guild_id=guild_id, prefix=prefix)


def update_prefix(guild_id: int, new_prefix: str):
    try:
        conn.execute(
            f'UPDATE PREFIXES SET PREFIX = "{str(new_prefix)}" WHERE GUILD_ID = {int(guild_id)}'
        )
        conn.commit()
        print('update', conn.cursor().fetchall())
    except sqlite3.OperationalError:
        add_prefix(guild_id=guild_id, prefix=new_prefix)


def delete_prefix(guild_id: int):
    try:
        conn.execute(f'DELETE FROM PREFIXES WHERE GUILD_ID = {int(guild_id)}')
        conn.commit()
        print('delete', conn.cursor().fetchall())
    except sqlite3.OperationalError:
        pass


def get_prefix(guild_id: int):
    try:
        cursor = conn.execute(
            f'SELECT PREFIX FROM PREFIXES WHERE GUILD_ID = {int(guild_id)}')
        try:
            print('AAAAAAAAAAAAAAAAAAAA')
            prefix = cursor.fetchone()[0]
        except TypeError:
            prefix = DEFAULT_PREFIX
    except sqlite3.OperationalError:
        prefix = DEFAULT_PREFIX
    print('get', cursor.fetchall())
    return prefix


#print(conn.execute('SELECT * from PREFIXES').fetchall())
