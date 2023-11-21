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

    @commands.command(name="strike",
                      aliases=["addstrikes",
                               "addstrike"],
                      description="Adds strikes to a particular ladder player"
                                  + "\n\n"
                                  + "!strike <rt/ct>, <player's name>, <amount>"
                                  + "\n\n"
                                  + "example: !strike rt, 255mp, 2"
                                  + "\n"
                                  + "         !strike rt, 255mp, super255mp, 200"
                                  + "\n\n"
                                  + "important: <amount> can be positive/negative number",
                      brief="Adds strikes to a particular ladder player")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        guild: discord.Guild = ctx.guild
        if not guild.id == config.get_lounge_guild_id():
            return

        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("strike is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!strike <rt/ct>, <player's name>, <amount>"
                message += "\n\n"
                message += "example: !strike rt, 255mp, 2"
                message += "\n"
                message += "         !strike rt, 255mp, super255mp, 200"
                message += "\n\n"
                message += "important: <amount> can be positive/negative number"
                message += "```"
                await discord_common_utils.send_message(ctx, message)
            else:
                message: discord.Message = ctx.message
                await message.delete()
                message: str = await self.add_ladder_multiple_player_strikes(parameters)
                await discord_common_utils.send_message(ctx, message)

    @staticmethod
    def parse_multiple_parameters(parameters: list) -> dict:
        error: str = ""
        if parameters:
            try:
                error = "invalid ladder id"
                ladder_type: str = config.get_lounge_webservice_dictionary(str(parameters[0]).lower())
                if not ladder_type:
                    raise ValueError

                error = "no player names found"
                player_names = ",".join(parameters[1:len(parameters)-1])

                error = "invalid strikes"
                strikes: int = int(parameters[len(parameters) - 1])

                return \
                    {
                        "has_parameters": True,
                        "ladder_type": ladder_type,
                        "player_names": player_names,
                        "strikes": strikes
                    }
            except (ValueError, IndexError):
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
    def parse_response(ladder_name: str, json_response: dict):
        if json_response["status"] == "failed":
            if json_response["reason"]:
                return json_response["reason"]
            else:
                return "player not found"
        else:
            text = ""
            for result in json_response["results"]:
                text += ladder_name
                text += " - "
                text += str(result["player_name"])
                text += ", strikes: "
                text += str(result["strikes"])
                text += "/"
                text += str(result["max_strikes"])
                if result["strikes"] >= result["max_strikes"]:
                    text += " *(max strikes exceeded)*"
                text += "\n"
            if text:
                return text
            else:
                return "player not found"

    @staticmethod
    async def add_ladder_multiple_player_strikes(parameters: list) -> str:
        result: dict = Updater.parse_multiple_parameters(parameters)
        if result["has_parameters"]:
            ladder_type: str = result["ladder_type"]
            player_names: str = result["player_names"]
            strikes: int = result["strikes"]
            json_response: dict = await lounge.add_ladder_player_strikes(ladder_type, player_names, strikes)
            return Updater.parse_response(str(parameters[0]).lower(), json_response)
        else:
            return result["message"]


async def main():
    print(await Updater.add_ladder_multiple_player_strikes(["rt",  "255MP", "2"]))


if __name__ == "__main__":
    asyncio.run(main())
