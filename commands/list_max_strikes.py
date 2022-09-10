from api import lounge
import asyncio
import common_utils
import config
import discord
import discord_common_utils
import json
import requests
from discord.ext import commands


class Updater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="maxstrikes",
                      aliases=["listmaxstrikes"],
                      description="Shows a list of players with the max strike limit for a particular ladder"
                                  + "\n\n"
                                  + "!maxstrikes <rt/ct>"
                                  + "\n\n"
                                  + "example: !maxstrikes rt",
                      brief="Shows a list of players with the max strike limit for a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("maxstrikes is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!maxstrikes <rt/ct>"
                message += "\n\n"
                message += "example: !maxstrikes rt"
                message += "```"
            else:
                message: str = await self.retrieve_max_strikes(parameters)
            await discord_common_utils.send_message(ctx, message)

    @staticmethod
    def parse_parameters(parameters: list) -> dict:
        if parameters:
            try:
                ladder_type: str = config.get_lounge_webservice_dictionary(str(parameters[0]).lower())
                if not ladder_type:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_type": ladder_type
                    }
            except (ValueError, IndexError):
                return \
                    {
                        "has_parameters": False,
                        "message": "invalid ladder id"
                    }
        else:
            return \
                    {
                        "has_parameters": False,
                        "message": "no parameters found"
                    }

    @staticmethod
    async def retrieve_max_strikes(parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_type: str = result["ladder_type"]
            json_response: dict = await lounge.retrieve_ladder_max_strikes(ladder_type)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "max strikes list not found"
            else:
                text = ""
                for result in json_response["results"]:
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
                    return "max strikes list not found"
        else:
            return result["message"]


async def main():
    print(await Updater.retrieve_max_strikes(["rt"]))


if __name__ == "__main__":
    asyncio.run(main())
