from pathlib import Path

from discord.ext import commands


async def load_cogs(bot: commands.Bot):
    """
    The code in this function is executed whenever the bot will start.
    """
    # get current path of the file
    path = Path(__file__).parent.parent / "cogs"
    for file in path.glob("**/*.py"):
        extension = file.stem
        try:
            await bot.load_extension(f"cogs.{extension}")
            bot.logger.info(f"Loaded extension '{extension}'")
        except Exception as e:
            exception = f"{type(e).__name__}: {e}"
            bot.logger.error(
                f"Failed to load extension {extension}\n{exception}"
            )
