import os
import sys
import json
from os.path import splitext

import discord
from discord.ext import commands

# Get configuration.jsonc
with open('configuration.jsonc', 'r') as config:
    data = json.load(config)
    token = data['token']
    prefix = data['prefix']
    owner_ids = data['owner_ids']

# Intents
intents = discord.Intents.default()
# The bot
client = commands.Bot(prefix, intents=intents, owner_ids=owner_ids)

# Load cogs
if __name__ == '__main__':
    try:
        client.load_extension('jishaku')
    except commands.errors.ExtensionNotFound:
        print('Jishaku not found.',
              'Use `pip install -r requirements.txt` to install it.')

    for item in os.listdir('Cogs'):
        if os.path.isfile(item):
            if splitext(item)[1] == '.py':
                client.load_extension(f'Cogs.{splitext(item)[0]}')
        elif os.path.isdir(item):
            for filename in os.listdir(os.path.join('Cogs', item)):
                if splitext(item)[1] == '.py':
                    client.load_extension(
                        f'Cogs.{item}.{splitext(filename)[0]}')


@client.event
async def on_ready():
    print(
        f'Logged in as {client.user.name} ({client.user.id}) and active in {len(client.guilds)} guilds.'
    )
    print(
        f'Discord.PY version: {discord.__version__} | Python version: {sys.version}'
    )
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.competing, name='with Tajiro and Zenitsu'))


client.run(token)
