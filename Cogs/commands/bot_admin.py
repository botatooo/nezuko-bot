import os

import discord
from discord.ext import commands

TOKEN = os.getenv('TOKEN')


class BotAdminCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name='say',
                      aliases=['send', 'echo'],
                      usage='<message>',
                      description='Make me say something')
    async def say(self, ctx: commands.Context, *, message: str):
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False)
        await ctx.send(message, allowed_mentions=allowed_mentions)
        await ctx.message.delete(delay=2)

    @commands.command(name='dm',
                      aliases=['pm'],
                      usage='<member> <message>',
                      description='Make me send a dm to someone.')
    @commands.is_owner()
    async def dm(self, ctx: commands.Context, member: discord.Member, *,
                 message: str):
        embed = discord.Embed(description=message)
        embed.set_author(name=f'{member}', icon_url=f'{member.avatar_url}')
        embed.set_footer(text=f'Sent to {member}')

        await member.send(message)
        await ctx.reply(embed=embed)

    @commands.command(name='status',
                      aliases=['setstatus', 'set_status'],
                      usage='<online|dnd|idle|invisible>',
                      description='Set the current status to something.')
    @commands.is_owner()
    async def status(self, ctx: commands.Context, status: str):
        if status.lower() in [
                'dnd', 'do_not_disturb', 'idle', 'invisible', 'offline',
                'online'
        ]:
            await self.client.change_presence(
                status=getattr(discord.Status, status.lower()))
        else:
            await ctx.reply('That is not a status.')

    @commands.command(
        name='activity',
        aliases=['setactivity', 'set_activity'],
        usage='<playing|listening|watching|competing> <name> [url]',
        description='Set the current activity to something.')
    @commands.is_owner()
    async def activity(self, ctx: commands.Context, activity: str, name: str):
        if activity.lower() in [
                'playing',
                'listening',
                'watching',
                'competing',
        ]:
            await self.client.change_presence(activity=discord.Activity(
                name=name,
                type=getattr(discord.ActivityType, activity.lower())))
        elif activity.lower() == 'streaming':
            await ctx.reply('Streaming not supported.')
        else:
            await ctx.reply('That is not an activity.')

    @commands.command(name='restart',
                      aliases=['reboot'],
                      description='Reboot the bot.')
    @commands.is_owner()
    async def restart(self, ctx: commands.Context):
        await ctx.bot.logout()
        await ctx.bot.login(TOKEN)


def setup(client: commands.Bot):
    client.add_cog(BotAdminCog(client))
