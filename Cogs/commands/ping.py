import time

import discord
from discord.ext import commands


class PingCog(commands.Cog):
    def __init__(self, client: commands.bot):
        self.client = client

    @commands.command(name='ping',
                      usage='',
                      description='Display the bot\'s ping.')
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def ping(self, ctx):
        embed = discord.Embed(title='Measuring...')

        before = time.monotonic()
        message = await ctx.reply(embed=embed)
        ping = (time.monotonic() - before) * 1000

        embed.title = None
        embed.add_field(name='Ping', value=f'{int(ping)}ms')
        embed.add_field(name='Heartbeat',
                        value=f'{round(self.client.latency, 3)} seconds')

        await message.edit(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(PingCog(bot))
