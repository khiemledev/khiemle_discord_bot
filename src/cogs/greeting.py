import discord
from discord.ext import commands

from utils.config_utils import get_config

config = get_config()


class Greetings(commands.Cog, name="greetings"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(
            member.guild.channels,
            name=config.discord.welcome_channel,
        )
        if channel is None:
            self.bot.logger.info(
                'Channel "%s" not found',
                config.discord.welcome_channel,
            )
            return

        if channel:
            await channel.send(f"Chào đằng ấy, {member.mention} <3")

    @commands.Cog.listener()
    async def on_member_update(
        self, before: discord.Member, after: discord.Member
    ):
        channel = discord.utils.get(
            after.guild.channels,
            name=config.discord.announcement_channel,
        )
        if channel is None:
            self.bot.logger.info(
                'Channel "%s" not found',
                config.discord.announcement_channel,
            )
            return

        allowed_mentions = discord.AllowedMentions(everyone=True)

        if before.roles != after.roles:
            role_added = set(after.roles) - set(before.roles)
            role_removed = set(before.roles) - set(after.roles)
            if role_added:
                for role in role_added:
                    msg = (
                        f"@everyone {after.mention}, bạn vừa được thăng"
                        f" chức thành {role.mention} <3"
                    )
                    await channel.send(
                        msg,
                        allowed_mentions=allowed_mentions,
                    )
            if role_removed:
                for role in role_removed:
                    msg = (
                        f"@everyone {after.mention}, bạn vừa bị cách"
                        f" chức {role.mention} :(("
                    )
                    await channel.send(
                        msg,
                        allowed_mentions=allowed_mentions,
                    )


async def setup(bot: commands.Bot):
    cog = Greetings(bot)
    await bot.add_cog(cog)
    cmd_names = [cmd.name for cmd in cog.get_commands()]
    bot.logger.info(f"Loaded extension '{cog.qualified_name}'")
    bot.logger.info(f"Commands of '{cog.qualified_name}: {cmd_names}'")
