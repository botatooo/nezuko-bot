import discord
from discord.ext import commands


class BotManagementCog(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name='shutdown',
                      usage='',
                      description='Shuts down the bot.')
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context):
        print('Shutting down bot.')
        await ctx.send('Shutting down bot.')
        await self.client.change_presence(status=discord.Status.offline)
        await self.client.close()


def setup(client: commands.Bot):
    client.add_cog(BotManagementCog(client))
