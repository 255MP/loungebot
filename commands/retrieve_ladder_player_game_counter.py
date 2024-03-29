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

    @commands.command(name="gamecounter",
                      description="Retrieve information about a particular ladder player's game counter"
                                  + "\n\n"
                                  + "!gamecounter <rt/ct>, <player's name>"
                                  + "\n\n"
                                  + "example: !gamecounter rt, 255mp",
                      brief="Retrieve information about a particular ladder player's game counter")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("gamecounter is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!gamecounter <rt/ct>, <player's name>"
                message += "\n\n"
                message += "example: !gamecounter rt, 255mp"
                message += "```"
            else:
                message: str = await self.retrieve_ladder_player(parameters)
            await discord_common_utils.send_message(ctx, message)

    @staticmethod
    def parse_parameters(parameters: list) -> dict:
        error: str = ""
        if parameters:
            try:
                error = "invalid ladder id"
                ladder_type: str = config.get_lounge_webservice_dictionary(str(parameters[0]).lower())
                if not ladder_type:
                    raise ValueError

                error = "invalid player name"
                player_name: str = parameters[1]
                if not player_name:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_type": ladder_type,
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
                        "message": "no parameters found"
                    }

    @staticmethod
    async def retrieve_ladder_player(parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_type: str = result["ladder_type"]
            player_name: str = result["player_name"]
            json_response: dict = await lounge.retrieve_ladder_player(ladder_type, player_name)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "player not found"
            else:
                text = json_response["results"][0]["player_name"]
                if json_response["results"][0]["game_counter"] is not None:
                    text += ", Game Counter: " + str(json_response["results"][0]["game_counter"])
                if text:
                    return text
                else:
                    return "player not found"
        else:
            return result["message"]


async def main():
    print(await Updater.retrieve_ladder_player(["rt", "255MP"]))


if __name__ == "__main__":
    asyncio.run(main())
