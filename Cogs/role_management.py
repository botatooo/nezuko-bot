import discord
from discord.ext import commands


class RoleManagementCog(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name='addrole',
                      aliases=['+role', 'add_role'],
                      usage='<member> <roles...>',
                      description='Add a role to a member.')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def addrole(self, ctx: commands.Context, member: discord.Member, *,
                      roles: discord.abc.Snowflake):
        role_object_list = [ctx.guild.get_role(role) for role in roles]
        await member.add_roles(*role_object_list)
        await ctx.send(f'Added role(s) to {member}. 🎭')

    @commands.command(name='removerole',
                      aliases=['-role', 'remove_role'],
                      usage='<member> <roles...>',
                      description='Remove a role from a member.')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def removerole(self, ctx: commands.Context, member: discord.Member, *,
                         roles: discord.abc.Snowflake):
        if 'all' in roles:
            await member.remove_roles(
                *[role for role in member.roles if role.name != '@everyone'])
            await ctx.send(f'Removed all roles from {member}. 🎭')
            return
        role_object_list = [ctx.guild.get_role(role) for role in roles]
        await member.remove_roles(*role_object_list)
        await ctx.send(f'Removed role(s) to {member}. 🎭')


def setup(client: commands.Bot):
    client.add_cog(RoleManagementCog(client))
