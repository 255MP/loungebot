from api import lounge
import asyncio
import common_utils
import config
import discord
import discord_common_utils
from discord.ext import commands


class Updater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="changename",
                      aliases=["changeplayername",
                               "updatename",
                               "updateplayername"],
                      description="Update a player's name"
                                  + "\n\n"
                                  + "!changename <player's name>, <player's new name>"
                                  + "\n\n"
                                  + "example: !changename 255mp, super255mp",
                      brief="Update a player's name")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        guild: discord.Guild = ctx.guild
        if not guild.id == config.get_lounge_guild_id():
            return

        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("changename is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!changename <player's name>, <player's new name>"
                message += "\n\n"
                message += "example: !changename 255mp, super255mp"
                message += "```"
            else:
                message: str = await self.update_player_name(ctx, parameters)
            await discord_common_utils.send_message(ctx, message)

    @staticmethod
    def parse_parameters(parameters: list) -> dict:
        error: str = ""
        if parameters:
            try:
                error = "invalid player name"
                player_name: str = parameters[0]
                if not player_name:
                    raise ValueError

                error = "invalid new player name"
                player_new_name: str = parameters[1]
                if not player_new_name:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "player_name": player_name,
                        "player_new_name": player_new_name
                    }
            except (ValueError, IndexError, Exception):
                return \
                    {
                        "has_parameters": False,
                        "message": error
                    }
        else:
            return \
                    {
                        "has_parameters": False,
                        "message": "no parameters found"
                    }

    @staticmethod
    async def update_player_name(ctx: discord.ext.commands.Context, parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            player_name: str = result["player_name"]
            player_new_name: str = result["player_new_name"]
            json_response: dict = await lounge.update_player_name(player_name, player_new_name)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "unable to update player's name"
            else:
                text = "player name updated " + json_response["results"][0]["player_name"]
                if json_response["results"][0]["discord_user_id"]:
                    text += " <@!" + json_response["results"][0]["discord_user_id"] + ">"
                    if ctx:
                        guild: discord.Guild = ctx.guild
                        if guild:
                            try:
                                member: discord.Member = await \
                                    guild.fetch_member(int(json_response["results"][0]["discord_user_id"]))
                                if member:
                                    await member.edit(nick=json_response["results"][0]["player_name"])
                            except (discord.Forbidden, discord.HTTPException, Exception):
                                text += ""
                else:
                    text += " **No Discord ID**"
                if text:
                    return text
                else:
                    return "unable to update player's name"
        else:
            return result["message"]


async def main():
    print(await Updater.update_player_name(None, ["255MP", "SUPER 255MP"]))
    print(await Updater.update_player_name(None, ["SUPER 255MP", "255MP"]))


if __name__ == "__main__":
    asyncio.run(main())
