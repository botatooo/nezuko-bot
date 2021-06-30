import discord
from discord import utils
from discord.ext import commands


class ModerationCog(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    # Clear
    @commands.command(
        name='clear',
        aliases=['purge'],
        usage='[amount=10] [channel]',
        description=
        'Purge messages. If no channel is specified, defaults to current one. If no amount is specified, defaults to 10.'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_message=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def clear(self, ctx: commands.Context, amount=10):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Purged {amount} messages. 🧹')

    # Kick
    @commands.command(name='kick',
                      aliases=['boot', '👢'],
                      usage='<member> [reason=None]',
                      description='Kick a user.')
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def kick(self,
                   ctx: commands.Context,
                   member: discord.Member,
                   *,
                   reason: str = None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member}. 👢')

    # Ban and Unban
    @commands.command(name='ban',
                      aliases=['begone', '404', 'gtfo', '🚪'],
                      usage='<member> [reason=None]',
                      description='Ban a user.')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def ban(self,
                  ctx: commands.Context,
                  member: discord.Member,
                  delete_message_days: int = 0,
                  *,
                  reason: str = None):
        if delete_message_days > 7:
            delete_message_days = 7
        elif delete_message_days < 0:
            delete_message_days = 0
        await member.ban(delete_message_days=delete_message_days, reason=reason)
        await ctx.send(f'Banned {member}. 🚪')

    @commands.command(name='unban',
                      aliases=['bacc', '🔑'],
                      usage='<member> [reason=None]',
                      description='Unban a user.')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def unban(self,
                    ctx: commands.Context,
                    member: discord.User,
                    *,
                    reason: str = None):
        async for banned_user in ctx.guild.bans():
            if banned_user.user == member:
                await banned_user.user.unban(reason=reason)
                await ctx.send(f'Unbanned {member}. 🔑')
                break

    # Mute and Unmute
    @commands.command(name='mute',
                      aliases=['shush', 'shut', 'stfu', '🤫'],
                      usage='<member> [reason=None]',
                      description='Mute a user.')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def mute(self,
                   ctx: commands.Context,
                   member: discord.User,
                   *,
                   reason: str = None):
        muted_role = utils.get(member.guild.roles, name='Muted')
        if not muted_role:
            muted_role = await ctx.guild.create_role(
                name='Muted',
                color=discord.Color(0x242526),
                reason='Creating muted role.')
            for channel in ctx.guild.channels:
                perms = channel.overwrites_for(muted_role)
                perms.send_messages = False
                await channel.set_permissions(muted_role,
                                              overwrite=perms,
                                              reason='Creating muted role.')
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f'Muted {member}. 🤫')

    @commands.command(name='unmute',
                      aliases=['😮'],
                      usage='<member> [reason=None]',
                      description='Unmute a user.')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def unmute(self,
                     ctx: commands.Context,
                     member: discord.User,
                     *,
                     reason: str = None):
        muted_role = utils.get(member.guild.roles, name='Muted')
        await member.remove_roles(muted_role, reason=reason)
        await ctx.send(f'Unmuted {member}. 😮')


def setup(client: commands.Bot):
    client.add_cog(ModerationCog(client))
