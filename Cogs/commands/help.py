from random import randint

import discord
from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name='help',
                      usage='[commandName]',
                      description='Display the help message.',
                      aliases=['h', '?'])
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def help(self, ctx, commandName: str = None):

        commandName2 = None
        stop = False

        if commandName is not None:
            for command in self.client.commands:
                if command.name == commandName.lower():
                    commandName2 = command
                    break
                else:
                    for alias in command.aliases:
                        if alias == commandName.lower():
                            commandName2 = alias
                            stop = True
                            break
                        if stop is True:
                            break

            if commandName2 is None:
                await ctx.channel.send('No command found!')
            else:
                embed = discord.Embed(
                    title=f'{commandName2.name.title()} Command',
                    description='',
                    color=discord.Color.blurple())
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.add_field(name='Name',
                                value=commandName2.name,
                                inline=False)
                aliases = commandName2.aliases
                aliasList = ''
                if len(aliases) > 0:
                    for alias in aliases:
                        aliasList += alias + ', '
                    aliasList = aliasList[:-2]
                    embed.add_field(name='Aliases', value=aliasList)
                else:
                    embed.add_field(name='Aliases', value='None', inline=False)

                if commandName2.usage is None:
                    embed.add_field(name='Usage', value='None', inline=False)
                else:
                    embed.add_field(
                        name='Usage',
                        value=
                        f'{self.client.command_prefix}{commandName2.name} {commandName2.usage}',
                        inline=False)
                embed.add_field(name='Description',
                                value=commandName2.description,
                                inline=False)
                await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Help',
                description=
                f'{self.client.command_prefix}help [commandName], display the help list or the help data for a specific command.',
                color=randint(0, 0xffffff))
            embed.set_thumbnail(url=self.client.user.avatar_url)
            for command in self.client.commands:
                embed.add_field(name=command.name,
                                value=command.description
                                if command.description else 'No description',
                                inline=False)
            await ctx.channel.send(embed=embed)


def setup(client: commands.Bot):
    client.remove_command('help')
    client.add_cog(HelpCog(client))
