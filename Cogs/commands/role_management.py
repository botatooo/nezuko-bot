import discord
from discord.ext import commands

from utils.checks import is_owner_or_has_perm  # pylint: disable=import-error


class RoleManagementCog(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name='addrole',
                      aliases=['+role', 'add_role'],
                      usage='<member> <roles...>',
                      description='Add a role to a member.')
    @commands.guild_only()
    @is_owner_or_has_perm('manage_roles')
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def addrole(self, ctx: commands.Context, member: discord.Member,
                      *roles):
        role_object_list = [
            ctx.message.guild.get_role(int(role)) for role in roles
        ]
        await member.add_roles(*role_object_list)
        await ctx.reply(f'Added role(s) to {member}. 🎭')

    @commands.command(name='removerole',
                      aliases=['-role', 'remove_role'],
                      usage='<member> <roles...>',
                      description='Remove a role from a member.')
    @commands.guild_only()
    @is_owner_or_has_perm('manage_roles')
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def removerole(self, ctx: commands.Context, member: discord.Member,
                         *roles):
        if 'all' in roles:
            await member.remove_roles(
                *[role for role in member.roles if role.name != '@everyone'])
            await ctx.reply(f'Removed all roles from {member}. 🎭')
            return
        role_object_list = [
            ctx.message.guild.get_role(int(role)) for role in roles
        ]
        await member.remove_roles(*role_object_list)
        await ctx.reply(f'Removed role(s) to {member}. 🎭')


def setup(client: commands.Bot):
    client.add_cog(RoleManagementCog(client))
