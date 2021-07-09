import sys
from pathlib import Path

import discord
from discord import utils
from discord.ext import commands

sys.path.insert(0, Path(__file__).parent.parent.parent.absolute())

from utils.checks import is_bot_admin_or_has_perm  # pylint: disable=import-error


class ModerationCog(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        name='clear',
        aliases=['purge'],
        usage='[amount=10] [channel]',
        description=
        'Purge messages. If no channel is specified, defaults to current one. If no amount is specified, defaults to 10.'
    )
    @commands.guild_only()
    @is_bot_admin_or_has_perm('manage_messages')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def clear(self,
                    ctx: commands.Context,
                    amount=10,
                    channel: discord.TextChannel = None):
        channel = channel if channel else ctx.channel
        await channel.purge(limit=amount + 1)
        msg = await ctx.reply(
            f'Purged {amount} messages in {channel.mention}. 🧹')
        await msg.delete(delay=5)

    @commands.command(name='kick',
                      aliases=['boot', '👢'],
                      usage='<member> [reason=None]',
                      description='Kick a user.')
    @commands.guild_only()  #    @is_bot_admin_or_has_perm('manage_messages')
    @is_bot_admin_or_has_perm('kick_members')
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def kick(self,
                   ctx: commands.Context,
                   member: discord.Member,
                   *,
                   reason: str = None):
        await member.kick(reason=reason)
        await ctx.reply(f'Kicked {member}. 👢')

    @commands.command(name='ban',
                      aliases=['begone', '404', 'gtfo', '🚪'],
                      usage='<member> [reason=None]',
                      description='Ban a user.')
    @commands.guild_only()
    @is_bot_admin_or_has_perm('ban_members')
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def ban(self,
                  ctx: commands.Context,
                  user: discord.User,
                  *,
                  reason: str = None):
        if user not in ctx.guild.members:
            user = await self.client.fetch_user(user.id)
        await ctx.guild.ban(user=user, reason=reason)
        await ctx.reply(f'Banned {user}. 🚪')

    @commands.command(name='unban',
                      aliases=['bacc', '🔑'],
                      usage='<member> [reason=None]',
                      description='Unban a user.')
    @commands.guild_only()
    @is_bot_admin_or_has_perm('ban_members')
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def unban(self,
                    ctx: commands.Context,
                    user_id: int,
                    *,
                    reason: str = None):
        bans = await ctx.guild.bans()
        for banned_user in bans:
            if banned_user.user.id == user_id:
                await ctx.guild.unban(user=banned_user.user, reason=reason)
                user = await self.client.fetch_user(user_id)
                await ctx.reply(f'Unbanned {user}. 🔑')
                break

    # Mute and Unmute
    @commands.command(name='mute',
                      aliases=['shush', 'shut', 'stfu', '🤫'],
                      usage='<member> [reason=None]',
                      description='Mute a user.')
    @commands.guild_only()
    @is_bot_admin_or_has_perm('manage_roles')
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def mute(self,
                   ctx: commands.Context,
                   member: discord.Member,
                   *,
                   reason: str = None):
        muted_role = utils.get(ctx.guild.roles, name='Muted')
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
        await ctx.reply(f'Muted {member}. 🤫')

    @commands.command(name='unmute',
                      aliases=['😮'],
                      usage='<member> [reason=None]',
                      description='Unmute a user.')
    @commands.guild_only()
    @is_bot_admin_or_has_perm('manage_roles')
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def unmute(self,
                     ctx: commands.Context,
                     member: discord.Member,
                     *,
                     reason: str = None):
        muted_role = utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(muted_role, reason=reason)
        await ctx.reply(f'Unmuted {member}. 😮')


def setup(client: commands.Bot):
    client.add_cog(ModerationCog(client))
