from api import lounge
import discord
from discord.ext import commands


class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if after.bot:
            return

        guild: discord.Guild = after.guild
        if not guild:
            return

        player: dict = await retrieve_player(after.id)
        if player:
            if player["player_name"] != after.display_name:
                await after.edit(nick=player["player_name"])

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        if after.bot:
            return

        guild: discord.Guild = self.bot.get_guild(387347467332485122)
        if not guild:
            return

        member: discord.Member = guild.get_member(after.id)
        if not member:
            return

        player: dict = await retrieve_player(after.id)
        if player:
            if player["player_name"] != member.display_name or player["player_name"] != after.display_name:
                await member.edit(nick=player["player_name"])

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return

        guild: discord.Guild = member.guild
        if not guild:
            return

        player: dict = await retrieve_player(member.id)
        if player:
            if player["player_name"] != member.display_name:
                await member.edit(nick=player["player_name"])


async def retrieve_player(discord_user_id: str) -> str:
    json_response: dict = await lounge.retrieve_player_by_discord_user_id(discord_user_id)
    if json_response["status"] == "failed":
        if json_response["reason"]:
            return None
        else:
            return None
    else:
        return json_response["results"][0]
