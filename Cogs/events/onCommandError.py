import sys
import traceback

from discord.ext import commands


class OnCommandErrorCog(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context,
                               error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                f'This command ({ctx.command}) is missing the "{error.param}" argument.'
            )
        elif isinstance(error, commands.TooManyArguments):
            await ctx.reply('Too many arguments have been specified.')
        elif isinstance(error, commands.MessageNotFound):
            await ctx.reply(f'The message {error.argument} was not found.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply(f'The member {error.argument} was not found.')
        elif isinstance(error, commands.GuildNotFound):
            await ctx.reply(f'The guild {error.argument} was not found.')
        elif isinstance(error, commands.UserNotFound):
            await ctx.reply(f'The user {error.argument} was not found.')
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.reply(f'The channel {error.argument} was not found.')
        elif isinstance(error, commands.ChannelNotReadable):
            await ctx.reply(
                f'I don\' have permission to access the channel {error.argument}.'
            )
        elif isinstance(error, commands.BadColourArgument):
            await ctx.reply(f'{error.argument} is not a valid color.')
        elif isinstance(error, commands.RoleNotFound):
            await ctx.reply(f'The role {error.argument} was not found.')
        elif isinstance(error, commands.BadInviteArgument):
            await ctx.reply(
                f'The invite {error.argument} is invalid or expired.')
        elif isinstance(error, commands.EmojiNotFound):
            await ctx.reply(f'The emoji {error.argument} was not found.')
        elif isinstance(error, commands.PartialEmojiConversionFailure):
            await ctx.reply(
                f'The emoji {error.argument} does match the correct emoji format.'
            )
        elif isinstance(error, commands.BadBoolArgument):
            await ctx.reply(f'The boolean {error.argument} is not convertible.')
        elif isinstance(error, commands.BadArgument):
            await ctx.reply('Failed to parse or convert one of the arguments.')
        elif isinstance(error, commands.BadUnionArgument):
            await ctx.reply(
                f'The union {error.param} failed to be converted by {", ".join(error.converters)}.'
            )
        elif isinstance(error, commands.UnexpectedQuoteError):
            await ctx.reply(
                f'The quote {error.quote} was found inside a non-quoted string.'
            )
        elif isinstance(error, commands.InvalidEndOfQuotedStringError):
            await ctx.reply(
                f'A space was expected after the closing quote but got {error.char} instead.'
            )
        elif isinstance(error, commands.ExpectedClosingQuoteError):
            await ctx.reply(
                f'A quote character was expected but found {error.char} instead.'
            )
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.reply('Failed to parse arguments')
        elif isinstance(error, commands.UserInputError):
            await ctx.reply('An error occured reguarding User Input.')
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.reply(
                f'This command ({ctx.command}) only works inside of Private Messages.'
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply(
                f'This command ({ctx.command}) does not work inside of Private Messages.'
            )
        elif isinstance(error, commands.NotOwner):
            await ctx.reply(
                f'This command ({ctx.command}) is reserved to bot owners.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(
                f'You are missing the required permissions to run this command. ({", ".join(error.missing_perms)})'
            )
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.reply(
                f'You are missing the permissions required to run this command. ({", ".join(error.missing_perms)})'
            )
        elif isinstance(error, commands.MissingRole):
            await ctx.reply(
                f'You are missing the role required to run this command. ({error.missing_role})'
            )
        elif isinstance(error, commands.BotMissingRole):
            await ctx.reply(
                f'I am missing the role required to run this command. ({error.missing_role})'
            )
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.reply(
                'You need to have at least 1 role to run this command.')
        elif isinstance(error, commands.BotMissingAnyRole):
            await ctx.reply(
                'I need to have at least 1 role to run this command.')
        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.reply(
                'You need to be in an NSFW channel to run this command.')
        elif isinstance(error, commands.CheckAnyFailure):
            await ctx.reply(
                f'Multiple checks have failed: ```py\n{error.errors}```.')
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply('A check has failed.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.reply(f'This command ({ctx.command}) has been disabled.')
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply(
                f'An exception was raised: ```py\n{error.original}```')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(
                f'You are on a cooldown (type: {error.cooldown.type}). You can retry again after {round(error.retry_after, 1)} seconds.'
            )
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.reply(
                f'Too many people are running this command ({error.number}). Try again later.'
            )
        elif isinstance(error, commands.ConversionError):
            await ctx.reply(
                f'The "{error.converter}" converter has failed. Message this to the bot owner: ```py\n{error.original}```'
            )
        elif isinstance(error, commands.CommandError):
            await ctx.reply(
                'There\'s been an error while executing this command.')
        else:
            print(f'Ignoring exception in command {ctx.command}:',
                  file=sys.stderr)
            traceback.print_exception(type(error),
                                      error,
                                      error.__traceback__,
                                      file=sys.stderr)


def setup(client):
    client.add_cog(OnCommandErrorCog(client))
