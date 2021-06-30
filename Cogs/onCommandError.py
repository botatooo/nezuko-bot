from discord.ext import commands
from discord.ext.commands import MissingPermissions, CheckFailure, CommandNotFound, NotOwner


class OnCommandErrorCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context,
                               error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            day = round(error.retry_after / 86400)
            hour = round(error.retry_after / 3600)
            minute = round(error.retry_after / 60)
            if day > 0:
                await ctx.send(
                    f'You are on a cooldown. ({day} day{"s" if day > 1 else ""})'
                )
            elif hour > 0:
                await ctx.send(
                    f'You are on a cooldown. ({hour} hour{"s" if hour > 1 else ""})'
                )
            elif minute > 0:
                await ctx.send(
                    f'You are on a cooldown. ({minute} minute{"s" if minute > 1 else ""})'
                )
            else:
                await ctx.send(
                    f'You are on a cooldown. ({error.retry_after:.2f} second{"s" if error.retry_after > 1 else ""})'
                )
        elif isinstance(error, CommandNotFound):
            return
        elif isinstance(error, MissingPermissions):
            await ctx.send(error)
        elif isinstance(error, CheckFailure):
            await ctx.send(error)
        elif isinstance(error, NotOwner):
            await ctx.send(error)
        else:
            print(error)


def setup(client):
    client.add_cog(OnCommandErrorCog(client))
