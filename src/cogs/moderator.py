import asyncio

import discord
from discord import app_commands
from discord.ext import commands


class Moderator(commands.Cog, name="moderator"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="vote_kick")
    # @commands.bot_has_permissions(kick_members=True)
    @app_commands.describe(member="Member to be kicked")
    @app_commands.describe(reason="Reason why member are being kicked out")
    async def vote_kick(
        self,
        ctx: commands.Context,
        member: discord.Member,
        reason: str = None,
        timeout: float = 60.0,
    ):
        if member == self.bot.user:
            await ctx.send("Non, sao mà kích được em =))")
            return

        if member.id == ctx.author.id:
            await ctx.send("Sao bạn lại tự kick chính mình zậy =(")
            return

        if member.guild_permissions.administrator:
            msg = "Không thể kick được admin bạn ơi, bạn muốn đảo chính hả :("
            await ctx.send(msg)
            return

        # check if bot has permission to kick members
        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.send(
                "Tui hog có quyền kick member ời bạn ơi :(",
            )
            return

        # Get member list not include the bots
        members = [mem for mem in ctx.guild.members if mem.bot is False]

        # Send a message to the channel asking users to vote
        resp_embed = discord.Embed(
            title="Vote kick member",
            description=f"""
                Có nên kích {member.mention} ko ae?
                Lý do: {reason or 'Hổng có lý do'}
                React like 👍 để kich, 👎 để không kích.

                Cái poll này sẽ hết hạn sau {timeout} giây.
                Nếu như hết hạn mà chưa đạt điều kiện thì sẽ không kích.

                Điều kiện kích như sau:
                  - Số up vote nhiều hơn down vote
                  - Số up vote phải hơn 1 nửa số thành viên trong server
                  (không tính bot)

                Số thành viên: {len(members)}
                Up vote để bị kích: {len(members) // 2}
            """,
            color=discord.Color.blue(),
        )
        message = await ctx.send(embed=resp_embed)
        # Add reactions to the message
        await message.add_reaction("👍")
        await message.add_reaction("👎")

        def check(
            _: discord.Reaction,
            __: discord.User,
        ) -> bool:
            return False

        try:
            await self.bot.wait_for(
                "reaction_add",
                check=check,
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            # Get the updated message with reactions
            message = await message.channel.fetch_message(message.id)

            # Count the number of yes and no votes
            yes_votes = 0
            no_votes = 0
            for reaction in message.reactions:
                if reaction.emoji == "👍":
                    yes_votes = (
                        reaction.count - 1
                    )  # Subtract 1 to exclude the bot's own reaction
                elif reaction.emoji == "👎":
                    no_votes = (
                        reaction.count - 1
                    )  # Subtract 1 to exclude the bot's own reaction

            # Check if the vote passes (50% or more yes votes)
            if yes_votes >= len(members) // 2 and yes_votes > no_votes:
                try:
                    await member.kick(
                        reason=reason or "Bạn bị kích bởi vote kick poll."
                    )
                    await ctx.send(f"{member.mention} đã bị kích khỏi server.")
                except discord.Forbidden as err:
                    self.bot.logger.exception(err)
                    await ctx.send(
                        f"Tui hog có quyền để kích {member.mention} :_("
                    )
            else:
                await ctx.send(
                    f"Poll vote kích {member.mention} không đạt điều kiện.",
                )


async def setup(bot: commands.Bot) -> None:
    cog = Moderator(bot)
    await bot.add_cog(cog)
    cmd_names = [cmd.name for cmd in cog.get_commands()]
    bot.logger.info(f"Loaded extension '{cog.qualified_name}'")
    bot.logger.info(f"Commands of '{cog.qualified_name}: {cmd_names}'")
