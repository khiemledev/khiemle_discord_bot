import discord
from discord import app_commands
from discord.ext import commands

from utils import llm_utils


class ChatGPT(commands.Cog, name="chatgpt"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Run ChatGPT when bot is mentioned"""

        if not self.bot.user.mentioned_in(message):
            return

        history = message.channel.history(limit=20)

        messages = []
        async for msg in history:
            messages.append(msg)

        messages = reversed(messages)  # reverse the list, oldest first

        history_strs = []
        for msg in messages:  # skip the last message, which is the mention
            content = msg.content

            # replace mention id with user's name
            for mention in msg.mentions:
                member = discord.utils.get(
                    message.guild.members, id=mention.id
                )
                if member:
                    content = content.replace(
                        f"<@{mention.id}>",
                        f"<{member.name}>",
                    )

            history_strs.append(f"{msg.author.name}: {content}")

        history_str = "\n".join(history_strs[:-1])

        async with message.channel.typing():
            try:
                chatgpt_response = llm_utils.call_chatgpt_bot_mentioned(
                    history=history_str,
                    message=history_strs[-1],
                )
                await message.reply(chatgpt_response)
            except Exception as err:
                self.bot.logger.exception(err)
                await message.reply(
                    "Huhu, em hog biết trả lời sao hết :_(",
                )

    @commands.hybrid_command(
        name="chatgpt",
        description="Run ChatGPT",
    )
    @app_commands.describe(prompt="Prompt to run ChatGPT")
    @app_commands.describe(
        temperature="Temperature to run ChatGPT, higher is more creative",
    )
    async def chatgpt(
        self,
        ctx: commands.Context,
        prompt: str = None,
        temperature: float = 0.9,
    ):
        """Run ChatGPT and return response in text"""

        resp = ctx.interaction.response
        if prompt is None:
            desc = f"{ctx.author.mention} phải có prompt để chạy chứ bạn ơi"
            return await resp.send_message(desc)

        if temperature < 0.0 or temperature > 2.0:
            desc = (
                f"{ctx.author.mention} temperature phải nằm trong khoảng từ 0.0"
                f" đến 2.0 chứ bạn ơi"
            )
            return await resp.send_message(desc)

        await resp.send_message(
            f"{ctx.author.mention} tui đang chạy prompt này nha <3 :\n `{prompt}`",
        )

        try:
            chatgpt_response = llm_utils.call_chatgpt(
                prompt=prompt,
                temperature=temperature,
            )
        except Exception as err:
            self.bot.logger.exception(err)
            resp_msg = f"{ctx.author.mention} ChatGPT bị lỗi rùi =(("
            return await ctx.send(resp_msg)

        desc = f"{chatgpt_response}\n{ctx.author.mention}"
        resp_embed = discord.Embed(
            title="Phản hồi từ ChatGPT <3",
            description=desc,
            color=discord.Color.green(),
        )
        await ctx.send(embed=resp_embed)


async def setup(bot: commands.Bot) -> None:
    cog = ChatGPT(bot)
    await bot.add_cog(cog)
    cmd_names = [cmd.name for cmd in cog.get_commands()]
    bot.logger.info(f"Loaded extension '{cog.qualified_name}'")
    bot.logger.info(f"Commands of '{cog.qualified_name}: {cmd_names}'")
