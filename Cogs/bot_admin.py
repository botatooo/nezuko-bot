import discord
from discord.ext import commands


class BotAdminCog(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="say",
                      aliases=["send", "echo"],
                      usage="<message>",
                      description="Make me say something")
    async def say(self, ctx: commands.Context, *, message: str):
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False)
        await ctx.send(message, allowed_mentions=allowed_mentions)

    @commands.command(name="dm",
                      aliases=['pm'],
                      usage="<member> <message>",
                      description="Make me send a dm to someone.")
    @commands.is_owner()
    async def dm(self, ctx: commands.Context, member: discord.Member, *,
                 message: str):
        embed = discord.Embed(description=message)
        embed.set_author(name=f'{member}', icon_url=f'{member.avatar_url}')
        embed.set_footer(text=f'Sent to {member}')

        await member.send(message)
        await ctx.send(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(BotAdminCog(client))
