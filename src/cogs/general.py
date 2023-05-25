import random

from discord import app_commands
from discord.ext import commands


class General(commands.Cog, name="general"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="ping_bot",
        description="Ping the bot",
    )
    async def ping_bot(self, ctx: commands.Context):
        """Ping the bot"""
        await ctx.interaction.response.send_message(
            f"`Pong! {round(self.bot.latency * 1000)}ms`",
        )

    @commands.hybrid_command(
        name="random_pick",
        description="Pick a random item from a list of items",
    )
    @app_commands.describe(
        items="List of items to pick from, separated by commas",
    )
    async def random_pick(self, ctx: commands.Context, items: str):
        """Pick a random item from a list of items"""

        items = [s.strip() for s in items.split(",")]

        await ctx.reply(
            f"`{random.choice(items)}`",
        )

    @commands.hybrid_command(
        name="random_number",
        description="Choose a random number between min and max",
    )
    @app_commands.describe(min="Minimum number, default to 0")
    @app_commands.describe(max="Maximum number, default to 100")
    async def random_number(
        self,
        ctx: commands.Context,
        min: int = 0,
        max: int = 100,
    ):
        """Choose a random number between min and max"""
        await ctx.reply(
            f"`{random.randint(min, max)}`",
        )


async def setup(bot: commands.Bot):
    cog = General(bot)
    await bot.add_cog(cog)
    cmd_names = [cmd.name for cmd in cog.get_commands()]
    bot.logger.info(f"Loaded extension '{cog.qualified_name}'")
    bot.logger.info(f"Commands of '{cog.qualified_name}: {cmd_names}'")
