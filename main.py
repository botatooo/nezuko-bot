import os
import sys
import json
from os.path import splitext

import discord
from discord.ext import commands

# Get configuration.jsonc
with open('configuration.json', 'r') as config:
    data = json.load(config)
    token = data['token']
    prefix = data['prefix']
    owner_ids = data['owner_ids']

# Intents
intents = discord.Intents.default()
intents.members = True

# The bot
client = commands.Bot(prefix, intents=intents, owner_ids=owner_ids)

# Load cogs
if __name__ == '__main__':
    try:
        client.load_extension('jishaku')
    except commands.errors.ExtensionNotFound:
        print('Jishaku not found.',
              'Use `pip install -r requirements.txt` to install it.')

    for filename in os.listdir('Cogs'):
        if splitext(filename)[1] == '.py':
            client.load_extension(f'Cogs.{splitext(filename)[0]}')


@client.event
async def on_ready():
    print('''
NNNNNNNN        NNNNNNNN                                                         kkkkkkkk
N:::::::N       N::::::N                                                         k::::::k
N::::::::N      N::::::N                                                         k::::::k
N:::::::::N     N::::::N                                                         k::::::k
N::::::::::N    N::::::N    eeeeeeeeeeee     zzzzzzzzzzzzzzzzzuuuuuu    uuuuuu   k:::::k    kkkkkkk ooooooooooo
N:::::::::::N   N::::::N  ee::::::::::::ee   z:::::::::::::::zu::::u    u::::u   k:::::k   k:::::koo:::::::::::oo
N:::::::N::::N  N::::::N e::::::eeeee:::::ee z::::::::::::::z u::::u    u::::u   k:::::k  k:::::ko:::::::::::::::o
N::::::N N::::N N::::::Ne::::::e     e:::::e zzzzzzzz::::::z  u::::u    u::::u   k:::::k k:::::k o:::::ooooo:::::o
N::::::N  N::::N:::::::Ne:::::::eeeee::::::e      z::::::z    u::::u    u::::u   k::::::k:::::k  o::::o     o::::o
N::::::N   N:::::::::::Ne:::::::::::::::::e      z::::::z     u::::u    u::::u   k:::::::::::k   o::::o     o::::o
N::::::N    N::::::::::Ne::::::eeeeeeeeeee      z::::::z      u::::u    u::::u   k:::::::::::k   o::::o     o::::o
N::::::N     N:::::::::Ne:::::::e              z::::::z       u:::::uuuu:::::u   k::::::k:::::k  o::::o     o::::o
N::::::N      N::::::::Ne::::::::e            z::::::zzzzzzzz u:::::::::::::::uuk::::::k k:::::k o:::::ooooo:::::o
N::::::N       N:::::::N e::::::::eeeeeeee   z::::::::::::::z u:::::::::::::::uk::::::k  k:::::ko:::::::::::::::o
N::::::N        N::::::N  ee:::::::::::::e  z:::::::::::::::z  uu::::::::uu:::uk::::::k   k:::::koo:::::::::::oo
NNNNNNNN         NNNNNNN    eeeeeeeeeeeeee  zzzzzzzzzzzzzzzzz    uuuuuuuu  uuuukkkkkkkk    kkkkkkk ooooooooooo'''
         )
    print(
        f'Logged in as {client.user.name} ({client.user.id}) and active in {len(client.guilds)} guilds.\n',
        f'Discord.PY version: {discord.__version__} | Python version: {sys.version}'
    )
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name='with Tajiro and Zenitsu'))


client.run(token)
