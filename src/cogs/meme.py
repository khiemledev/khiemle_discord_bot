import random
from pathlib import Path

import discord
from discord.ext import commands

from utils.config_utils import get_config

config = get_config()


class Meme(commands.Cog, name="meme"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # pre-load memes
        self.memes = []
        meme_dir = Path(config.discord.meme_dir)
        if not meme_dir.is_dir():
            self.bot.logger.error(f"meme_dir '{meme_dir}' is not a directory")
            return

        # get all jpgs or pngs in meme_dir
        for meme in meme_dir.glob("**/*"):
            if not meme.is_file():
                continue
            if meme.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
                continue
            self.memes.append(meme)

        self.bot.logger.info(f"Loaded {len(self.memes)} memes")

    @commands.hybrid_command(name="meme")
    async def meme(self, ctx: commands.Context):
        """Get random meme from folder"""

        if len(self.memes) == 0:
            await ctx.send("No memes found")
            return

        meme = random.choice(self.memes)
        await ctx.send(file=discord.File(meme))


async def setup(bot: commands.Bot):
    cog = Meme(bot)
    await bot.add_cog(cog)
    cmd_names = [cmd.name for cmd in cog.get_commands()]
    bot.logger.info(f"Loaded extension '{cog.qualified_name}'")
    bot.logger.info(f"Commands of '{cog.qualified_name}: {cmd_names}'")
