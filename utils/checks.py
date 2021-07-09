import os

import discord
from discord.ext import commands

owner_ids = [int(id) for id in os.getenv('OWNER_IDS').split(',')]


def is_bot_admin_or_has_perm(permission):

    def predicate(ctx):
        global owner_ids
        return (int(ctx.message.author.id) in owner_ids) or hasattr(
            ctx.message.author.guild_permissions, permission.lower())

    return commands.check(predicate)
