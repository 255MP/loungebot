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

    @commands.command(name="removeladderplayer",
                      aliases=["deleteladderplayer"],
                      description="Removes a player from a particular ladder"
                                  + "\n\n"
                                  + "!removeladderplayer <rt/ct>, <player's name>"
                                  + "\n\n"
                                  + "example: !removeladderplayer rt, 255mp",
                      brief="Removes a player from a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("removeladderplayer is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!removeladderplayer <rt/ct>, <player's name>"
                message += "\n\n"
                message += "example: !removeladderplayer rt, 255mp"
                message += "```"
            else:
                message: str = await self.remove_ladder_player(parameters)
            await discord_common_utils.send_message(ctx, message)

    @staticmethod
    def parse_parameters(parameters: list) -> dict:
        error: str = ""
        if parameters:
            try:
                error = "invalid ladder id"
                ladder_id: int = int(config.get_lounge_webservice_dictionary(str(parameters[0]).lower()))
                if not ladder_id or ladder_id < 0:
                    raise ValueError

                error = "invalid player name"
                player_name: str = parameters[1]
                if not player_name:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_id": ladder_id,
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
    async def remove_ladder_player(parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_id: int = result["ladder_id"]
            player_name: str = result["player_name"]
            json_response: dict = await lounge.remove_ladder_player(ladder_id, player_name)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "player not found"
            else:
                text = player_name
                text += " has been removed from the ladder"
                if text:
                    return text
                else:
                    return "player not found"
        else:
            return result["message"]


async def main():
    print(await Updater.remove_ladder_player(["rt", "255MP"]))


if __name__ == "__main__":
    asyncio.run(main())
