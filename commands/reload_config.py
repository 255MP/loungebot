import asyncio
import config
import discord
import discord_common_utils
from discord.ext import commands


class Administrator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reloadconfig")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_admin(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("reloadconfig is an admin command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            config.reload_config()
            message: discord.message.Message = await ctx.send("LoungeBot configuration has been reloaded.")
            await asyncio.sleep(3)
            await message.delete()


async def main():
    config.reload_config();


if __name__ == "__main__":
    asyncio.run(main())
