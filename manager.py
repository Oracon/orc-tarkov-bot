from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument


class Manager(commands.Cog):
    """Manage the bot"""

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        # await self.bot.wait_until_ready()
        print(f"{self.bot.user} is Online!")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please send all Arguments. Type !help 'command' to see the 'command' arguments.")
        
        elif isinstance(error, CommandNotFound):
            await ctx.send("This command does not exist. Type !help to see all commands.")
        
        else:
            raise error


def setup(bot):
    bot.add_cog(Manager(bot))