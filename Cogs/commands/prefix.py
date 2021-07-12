import discord
from discord.ext import commands

from utils.checks import is_owner_or_has_perm  # pylint: disable=import-error
from utils import db  # pylint: disable=import-error


class PrefixCog(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name='prefix',
                      aliases=['p'],
                      usage='<prefix>',
                      description='Change server\'s prefix.')
    @commands.guild_only()
    @is_owner_or_has_perm('manage_guild')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def prefix(self, ctx: commands.Context, prefix: str):
        db.update_prefix(guild_id=int(ctx.guild.id), new_prefix=prefix)
        await ctx.send(f'Changed server prefix to "{prefix}".')


def setup(client: commands.Bot):
    client.add_cog(PrefixCog(client))
