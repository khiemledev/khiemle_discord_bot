from discord.ext import commands


class General(commands.Cog, name="general"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ping_bot")
    async def ping_bot(self, ctx: commands.Context):
        """Ping the bot"""
        await ctx.interaction.response.send_message(
            f"`Pong! {round(self.bot.latency * 1000)}ms`",
        )


async def setup(bot: commands.Bot):
    cog = General(bot)
    await bot.add_cog(cog)
    cmd_names = [cmd.name for cmd in cog.get_commands()]
    bot.logger.info(f"Loaded extension '{cog.qualified_name}'")
    bot.logger.info(f"Commands of '{cog.qualified_name}: {cmd_names}'")
