import os
import sys
from dotenv import load_dotenv, find_dotenv
from os.path import splitext, join

import discord
from discord.ext import commands

from utils import db

# Get .env
load_dotenv(find_dotenv())

token = os.getenv('TOKEN')
prefix = os.getenv('PREFIX')
owner_ids = [int(id) for id in os.getenv('OWNER_IDS').split(',')]


# Server Prefix
def get_prefix(bot: commands.Bot, message: discord.Message):
    guild_id = message.guild.id
    prefix = db.get_prefix(guild_id=guild_id)
    return prefix


# Intents
intents = discord.Intents.default()
intents.members = True  #pylint: disable=assigning-non-slot

# The bot
client = commands.Bot(command_prefix=get_prefix,
                      intents=intents,
                      owner_ids=owner_ids)

# Load cogs
if __name__ == '__main__':
    try:
        client.load_extension('jishaku')
        print('Loaded cog: jishaku')
    except commands.errors.ExtensionNotFound:
        print('Jishaku not found.', 'Use ``pipenv install`` to install it.')

    COG_DIRECTORY = os.path.join(os.path.split(__file__)[0], 'Cogs')

    for cog in os.listdir(COG_DIRECTORY):
        if cog.endswith('.py'):
            client.load_extension(f'Cogs.{splitext(cog)[0]}')
            print(f'Loaded cog: {splitext(cog)[0]}')
        elif cog.lower() in ['commands', 'events']:
            for specific_cog in os.listdir(join(COG_DIRECTORY, cog)):
                if specific_cog.endswith('.py'):
                    client.load_extension(
                        f'Cogs.{cog}.{splitext(specific_cog)[0]}')
                    print(f'Loaded cog: {cog}.{splitext(specific_cog)[0]}')


@client.event
async def on_ready():
    await client.wait_until_ready()
    print('''
NNNNNNNN        NNNNNNNN                                                          kkkkkkk
N:::::::N       N::::::N                                                          k:::::k
N::::::::N      N::::::N                                                          k:::::k
N:::::::::N     N::::::N                                                          k:::::k
N::::::::::N    N::::::N     eeeeeeeeeeee     zzzzzzzzzzzzzzzzz uuuuuu    uuuuuu  k:::::k    kkkkkkk   ooooooooooo
N:::::::::::N   N::::::N   ee::::::::::::ee   z:::::::::::::::z u::::u    u::::u  k:::::k   k:::::k  oo:::::::::::oo
N:::::::N::::N  N::::::N  e::::::eeeee:::::ee z::::::::::::::z  u::::u    u::::u  k:::::k  k:::::k  o:::::::::::::::o
N::::::N N::::N N::::::N e::::::e     e:::::e zzzzzzzz::::::z   u::::u    u::::u  k:::::k k:::::k   o:::::ooooo:::::o
N::::::N  N::::N:::::::N e:::::::eeeee::::::e      z::::::z     u::::u    u::::u  k::::::k:::::k    o::::o     o::::o
N::::::N   N:::::::::::N e:::::::::::::::::e      z::::::z      u::::u    u::::u  k:::::::::::k     o::::o     o::::o
N::::::N    N::::::::::N e::::::eeeeeeeeeee      z::::::z       u::::u    u::::u  k:::::::::::k     o::::o     o::::o
N::::::N     N:::::::::N e:::::::e              z::::::z        u:::::uuuu:::::u  k::::::k:::::k    o::::o     o::::o
N::::::N      N::::::::N e::::::::e            z::::::zzzzzzzz  u:::::::::::::::u k::::::k k:::::k  o:::::ooooo:::::o
N::::::N       N:::::::N  e::::::::eeeeeeee   z::::::::::::::z  u:::::::::::::::u k::::::k  k:::::k o:::::::::::::::o
N::::::N        N::::::N   ee:::::::::::::e  z:::::::::::::::z   uu::::::::uu:::u k::::::k   k:::::k oo:::::::::::oo
NNNNNNNN         NNNNNNN     eeeeeeeeeeeeee  zzzzzzzzzzzzzzzzz     uuuuuuuu  uuuu kkkkkkkk    kkkkkkk  ooooooooooo'''
         )
    print(
        f'Logged in as {client.user.name} ({client.user.id}) and active in {len(client.guilds)} guilds.',
        f'\nDiscord.PY version: {discord.__version__} | Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
    )
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name='with Tajiro and Zenitsu'))


client.run(token)
