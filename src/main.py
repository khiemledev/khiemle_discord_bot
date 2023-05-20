import random

import discord
from discord.ext import commands

from utils import bot_utils, config_utils, logger_utils

config = config_utils.get_config()


class KhiemLeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        self.config = config
        self.logger = logger_utils.get_logger()

        super().__init__(
            command_prefix=commands.when_mentioned_or(
                config.discord.command_prefix,
            ),
            intents=intents,
        )

    async def setup_hook(self):
        await bot_utils.load_cogs(self)
        await self.tree.sync()
        self.logger.info("App commands synced")

    async def on_ready(self):
        self.logger.info("Bot is ready")
        channel = discord.utils.get(
            self.get_all_channels(),
            name=config.discord.bot_log_channel,
        )
        if channel is None:
            self.logger.info(
                'Channel "%s" not found', config.discord.bot_log_channel
            )
            return

        message = random.choice(config.discord.bot_ready_messages)
        await channel.send(message)

    async def close(self):
        self.logger.info("Bot is shutting down")
        channel = discord.utils.get(
            self.get_all_channels(),
            name=config.discord.bot_log_channel,
        )
        if not channel:
            self.logger.info(
                'Channel "%s" not found', config.discord.bot_log_channel
            )
            return

        message = random.choice(config.discord.bot_close_messages)
        await channel.send(message)

    async def on_command_error(
        self,
        ctx: commands.Context,
        exception: commands.CommandError,
    ):
        self.logger.exception(exception)
        resp_embed = discord.Embed(
            title=config.discord.bot_command_error_message,
            description=f"```{exception}```",
            color=discord.Color.red(),
        )
        await ctx.send(embed=resp_embed)


def main():
    bot = KhiemLeBot()
    bot.run(config.discord.bot_token)


if __name__ == "__main__":
    main()
