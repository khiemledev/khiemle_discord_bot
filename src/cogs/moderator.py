import asyncio
from typing import List, Literal, TypedDict

import discord
from discord import app_commands
from discord.ext import commands


class VoteType(TypedDict):
    message_id: int
    voting_type: Literal["kick", "ban"]
    member: discord.Member


class Moderator(commands.Cog, name="moderator"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voting_list: List[VoteType] = []

    @commands.hybrid_command(
        name="vote_kick",
        description="Vote to kick a member",
    )
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

        # Check if bot has permission to kick members
        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.send(
                "Tui hog có quyền kick member ời bạn ơi :(",
            )
            return

        # Check if member is already in the voting list
        in_voting = [e for e in self.voting_list if e["member"] == member]
        if len(in_voting):
            await ctx.send(f"{member.mention} đang trong poll vote rồi.")
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

                {ctx.author.mention} Để hủy poll này, react ❌.
            """,
            color=discord.Color.blue(),
        )
        message = await ctx.send(embed=resp_embed)
        # Add reactions to the message
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await message.add_reaction("❌")

        def check(
            reaction: discord.Reaction,
            user: discord.User,
        ) -> bool:
            # Stop the poll if the user who started the poll reacts with ❌
            return (
                reaction.message.id == message.id
                and user == ctx.author
                and reaction.emoji == "❌"
            )

        voting_idx = None
        try:
            # Add voting to the list
            voting_idx = len(self.voting_list)
            self.voting_list.append(
                {
                    "message_id": message.id,
                    "voting_type": "kick",
                    "member": member,
                }
            )

            await self.bot.wait_for(
                "reaction_add",
                check=check,
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            pass
        finally:
            # Get the updated message with reactions
            message = await message.channel.fetch_message(message.id)

            # Count the number of yes and no votes
            yes_votes = 0
            no_votes = 0
            for reaction in message.reactions:
                if reaction.emoji == "❌":
                    # Check if poll was closed by the user who started the poll
                    async for user in reaction.users():
                        if user == ctx.author:
                            msg = discord.Embed(
                                title="Poll đã bị hủy",
                                description="""
                                    Poll đã bị hủy bởi người tạo poll.
                                """,
                                color=discord.Color.red(),
                            )
                            await message.edit(embed=msg)
                            await message.clear_reactions()
                            return

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

            # Remove voting from the list
            if voting_idx is not None:
                self.voting_list.pop(voting_idx)

    @commands.hybrid_command(
        name="vote_ban",
        description="Vote to ban a member",
    )
    # @commands.bot_has_permissions(kick_members=True)
    @app_commands.describe(member="Member to be banned")
    @app_commands.describe(reason="Reason why member are being banned")
    async def vote_ban(
        self,
        ctx: commands.Context,
        member: discord.Member,
        reason: str = None,
        timeout: float = 60.0,
    ):
        if member == self.bot.user:
            await ctx.send("Non, sao mà ban được em =))")
            return

        if member.id == ctx.author.id:
            await ctx.send("Sao bạn lại tự ban chính mình zậy =(")
            return

        if member.guild_permissions.administrator:
            msg = "Không thể ban được admin bạn ơi, bạn muốn đảo chính hả :("
            await ctx.send(msg)
            return

        # Check if bot has permission to kick members
        if not ctx.guild.me.guild_permissions.kick_members:
            await ctx.send(
                "Tui hog có quyền ban member ời bạn ơi :(",
            )
            return

        # Check if member is already in the voting list
        in_voting = [e for e in self.voting_list if e["member"] == member]
        if len(in_voting):
            await ctx.send(f"{member.mention} đang trong poll vote rồi.")
            return

        # Get member list not include the bots
        members = [mem for mem in ctx.guild.members if mem.bot is False]

        # Send a message to the channel asking users to vote
        resp_embed = discord.Embed(
            title="Vote ban member",
            description=f"""
                Có nên ban {member.mention} ko ae?
                Lý do: {reason or 'Hổng có lý do'}
                React like 👍 để ban, 👎 để không ban.

                **Lưu ý: User bị ban sẽ không thể được mời lại vào server
                trừ khi được xóa khỏi blacklist**

                Cái poll này sẽ hết hạn sau {timeout} giây.
                Nếu như hết hạn mà chưa đạt điều kiện thì sẽ không kích.

                Điều kiện ban như sau:
                  - Số up vote nhiều hơn down vote
                  - Số up vote phải hơn 1 nửa số thành viên trong server
                  (không tính bot)

                Số thành viên: {len(members)}
                Up vote để bị ban: {len(members) // 2}

                {ctx.author.mention} Để hủy poll này, react ❌.
            """,
            color=discord.Color.blue(),
        )
        message = await ctx.send(embed=resp_embed)
        # Add reactions to the message
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await message.add_reaction("❌")

        def check(
            reaction: discord.Reaction,
            user: discord.User,
        ) -> bool:
            # Stop the poll if the user who started the poll reacts with ❌
            return (
                reaction.message.id == message.id
                and user == ctx.author
                and reaction.emoji == "❌"
            )

        voting_idx = None
        try:
            # Add voting to the list
            voting_idx = len(self.voting_list)
            self.voting_list.append(
                {
                    "message_id": message.id,
                    "voting_type": "ban",
                    "member": member,
                }
            )

            await self.bot.wait_for(
                "reaction_add",
                check=check,
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            pass
        finally:
            # Get the updated message with reactions
            message = await message.channel.fetch_message(message.id)

            # Count the number of yes and no votes
            yes_votes = 0
            no_votes = 0
            for reaction in message.reactions:
                if reaction.emoji == "❌":
                    # Check if poll was closed by the user who started the poll
                    async for user in reaction.users():
                        if user == ctx.author:
                            msg = discord.Embed(
                                title="Poll đã bị hủy",
                                description="""
                                    Poll đã bị hủy bởi người tạo poll.
                                """,
                                color=discord.Color.red(),
                            )
                            await message.edit(embed=msg)
                            await message.clear_reactions()
                            return

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
                    await member.ban(
                        reason=reason or "Bạn bị ban bởi vote kick poll."
                    )
                    await ctx.send(f"{member.mention} đã bị ban khỏi server.")
                except discord.Forbidden as err:
                    self.bot.logger.exception(err)
                    await ctx.send(
                        f"Tui hog có quyền để ban {member.mention} :_("
                    )
            else:
                await ctx.send(
                    f"Poll vote ban {member.mention} không đạt điều kiện.",
                )

            # Remove voting from the list
            if voting_idx is not None:
                self.voting_list.pop(voting_idx)


async def setup(bot: commands.Bot) -> None:
    cog = Moderator(bot)
    await bot.add_cog(cog)
    cmd_names = [cmd.name for cmd in cog.get_commands()]
    bot.logger.info(f"Loaded extension '{cog.qualified_name}'")
    bot.logger.info(f"Commands of '{cog.qualified_name}: {cmd_names}'")
