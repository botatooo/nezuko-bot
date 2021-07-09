import discord
from discord.ext import commands


class onMessageEdit(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message,
                              after: discord.Message):
        await self.client.process_commands(after)


def setup(bot: commands.Bot):
    bot.add_cog(onMessageEdit(bot))
