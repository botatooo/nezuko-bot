import discord
from discord import utils
from discord.ext import commands


class onGuildChannelCreateCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        muted_role = utils.get(channel.guild.roles, name='Muted')
        if muted_role:
            perms = channel.overwrites_for(muted_role)
            perms.send_messages = False
            await channel.set_permissions(muted_role,
                                          overwrite=perms,
                                          reason='Muted role.')


def setup(client: commands.Bot):
    client.add_cog(onGuildChannelCreateCog(client))
