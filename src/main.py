import random
from typing import Any, List, Mapping, Optional

import discord
from discord.ext import commands
from discord.ext.commands import Command

from utils import bot_utils, config_utils, logger_utils

config = config_utils.get_config()


class BotHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(
        self,
        mapping: Mapping[Optional[commands.Cog], List[Command[Any, ..., Any]]],
    ):
        embed = discord.Embed(
            title="Danh sách các command của bot",
            color=discord.Color.blue(),
        )
        for cog, _commands in mapping.items():
            if cog is None:
                continue

            command_signatures = []
            for command in _commands:
                # Get the command signature
                signature = self.get_command_signature(command)

                # Get the command description
                description = command.help or "Không có mô tả command"

                # Get the argument descriptions
                arg_descs = []
                for param in command.clean_params.values():
                    arg_desc = param.annotation or "Không có mô tả argument"
                    if not isinstance(arg_desc, str):
                        arg_desc = arg_desc.__name__
                    arg_descs.append(f"{param.name}: {arg_desc}")
                if len(arg_descs):
                    arg_descs = "\n".join(["- " + a for a in arg_descs])
                else:
                    arg_descs = "No argument required"

                # Add the command description to the list
                command_signatures.append(
                    (f"{signature}\n{description}\n" f"Arguments: {arg_descs}")
                )

            if command_signatures:
                cog_name = cog.qualified_name
                embed.add_field(
                    name=cog_name,
                    value="\n\n".join(command_signatures),
                    inline=False,
                )

        await self.get_destination().send(embed=embed)


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
            help_command=BotHelpCommand(),
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
        self.logger.error(str(exception))
        if isinstance(exception, commands.CommandNotFound):
            return

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
