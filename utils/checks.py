import json

import discord
from discord.ext import commands

with open('configuration.json', 'r', encoding='utf-8') as config:
    data = json.load(config)
    owner_ids = data['owner_ids']


def is_bot_admin_or_has_perm(permission):

    def predicate(ctx):
        global owner_ids
        return (int(ctx.message.author.id) in owner_ids) or hasattr(
            ctx.message.author.guild_permissions, permission.lower())

    return commands.check(predicate)
