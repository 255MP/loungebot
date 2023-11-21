from api import lounge
import asyncio
import common_utils
import config
import discord
import discord_common_utils
from discord.ext import commands


class Public(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="requestname",
                      description="Request a name change"
                                  + "\n\n"
                                  + "!requestname <new name>"
                                  + "\n\n"
                                  + "example: !requestname 255mp",
                      brief="Request a name change")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        guild: discord.Guild = ctx.guild
        if not guild.id == config.get_lounge_guild_id():
            return

        parameters: list = common_utils.split_comma(args)
        if not parameters:
            message: str = ""
            message += "```"
            message += "!requestname <new name>"
            message += "\n\n"
            message += "example: !requestname 255mp"
            message += "```"
        else:
            message: str = await self.request_player_name_change(ctx.author.id, parameters)
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

                return \
                    {
                        "has_parameters": True,
                        "player_name": player_name
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
                        "message": "please provide a name"
                    }

    @staticmethod
    async def request_player_name_change(discord_user_id: int, parameters: list) -> str:
        result: dict = Public.parse_parameters(parameters)
        if result["has_parameters"]:
            player_name: str = result["player_name"]
            json_response: dict = await lounge.retrieve_player_by_discord_user_id(discord_user_id);
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "it appears your discord is not tied to your lounge profile"

            other_player: dict = await lounge.retrieve_player_by_name(player_name)
            if other_player["status"] != "failed":
                text = other_player["results"][0]["player_name"]
                if text:
                    return "another player already has the name " + player_name
        else:
            return result["message"]


async def main():
    print(await Public.request_player_name_change(["255MP"]))


if __name__ == "__main__":
    asyncio.run(main())
