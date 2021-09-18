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

    @commands.command(name="award",
                      aliases=["addaward",
                               "addreward",
                               "addladderaward",
                               "addladderreward"],
                      description="Adds an award to a particular ladder player"
                                  + "\n\n"
                                  + "!award <rt/ct>, <player's name>, <amount>"
                                  + "\n\n"
                                  + "example: !award rt, 255mp, 200"
                                  + "\n"
                                  + "         !award rt, 255mp, super255mp, 200"
                                  + "\n\n"
                                  + "important: <amount> must be a positive number",
                      brief="Adds an award to a particular ladder player")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("award is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!award <rt/ct>, <player's name>, <amount>"
                message += "\n\n"
                message += "example: !award rt, 255mp, 200"
                message += "\n"
                message += "         !award rt, 255mp, super255mp, 200"
                message += "\n\n"
                message += "important: <amount> must be a positive number"
                message += "```"
                await discord_common_utils.send_message(ctx, message)
            else:
                message: str = await self.add_ladder_multiple_player_award(parameters)
                await discord_common_utils.send_message(ctx, message)

    @staticmethod
    def parse_multiple_parameters(parameters: list) -> dict:
        error: str = ""
        if parameters:
            try:
                error = "invalid ladder id"
                ladder_id: int = int(config.get_lounge_webservice_dictionary(str(parameters[0]).lower()))
                if not ladder_id or ladder_id < 0:
                    raise ValueError

                error = "no player names found"
                player_names = ",".join(parameters[1:len(parameters)-1])

                error = "invalid award amount"
                award: int = int(parameters[len(parameters) - 1])
                if award < 0:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_id": ladder_id,
                        "player_names": player_names,
                        "award": award
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
    def parse_response(json_response: dict):
        if json_response["status"] == "failed":
            if json_response["reason"]:
                return json_response["reason"]
            else:
                return "player not found"
        else:
            text = ""
            for result in json_response["results"]:
                text += result["player_name"]
                if result["current_mmr"] is not None:
                    if int(result["current_mmr"]) < 0:
                        text += ", MMR: Below 0"
                    else:
                        text += ", MMR: " + str(result["current_mmr"])
                    text += " (" + result["current_division"] + ")"
                if result["current_lr"] is not None:
                    text += ", LR: " + str(result["current_lr"])
                    text += " (" + result["current_class"] + ")"
                if result["penalties"] is not None:
                    text += ", Award/Penalties: " + str(result["penalties"])
                text += "\n"
            if text:
                return text
            else:
                return "player not found"

    @staticmethod
    async def add_ladder_multiple_player_award(parameters: list) -> str:
        result: dict = Updater.parse_multiple_parameters(parameters)
        if result["has_parameters"]:
            ladder_id: int = result["ladder_id"]
            player_names: str = result["player_names"]
            award: int = result["award"]
            json_response: dict = await lounge.add_ladder_player_award(ladder_id, player_names, award)
            return Updater.parse_response(json_response)
        else:
            return result["message"]


async def main():
    print(await Updater.add_ladder_multiple_player_award(["rt", "255MP", "500"]))


if __name__ == "__main__":
    asyncio.run(main())
