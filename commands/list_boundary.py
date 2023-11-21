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

    @commands.command(name="listrank",
                      aliases=["listranks",
                               "listranking", "listrankings",
                               "listdivision", "listdivisions",
                               "listboundary", "listboundaries"],
                      description="Shows a list of ranks for a particular ladder"
                                  + "\n\n"
                                  + "!listrank <rt/ct>"
                                  + "\n\n"
                                  + "example: !listrank rt",
                      brief="Shows a list of ranks for a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        guild: discord.Guild = ctx.guild
        if not guild.id == config.get_lounge_guild_id():
            return

        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("listrank is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!listrank <rt/ct>"
                message += "\n\n"
                message += "example: !listrank rt"
                message += "```"
            else:
                message: str = await self.retrieve_ladder_boundaries(parameters)
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
    async def retrieve_ladder_boundaries(parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_type: str = result["ladder_type"]
            json_response: dict = await lounge.retrieve_ladder_boundary(ladder_type)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "rank list not found"
            else:
                text = ""
                for result in json_response["results"]:
                    text += result["ladder_boundary_name"]
                    text += ", "
                    if result["minimum_lr"] and result["maximum_lr"]:
                        text += "{}-{}".format(result["minimum_lr"],  result["maximum_lr"])
                    elif result["minimum_lr"]:
                        text += "above {}".format(result["minimum_lr"])
                    elif result["maximum_lr"]:
                        text += "0-{}".format(result["maximum_lr"])
                    else:
                        text += "unknown"
                    text += ", "
                    text += result["color"]
                    text += ", "
                    text += "<" + result["emblem"] + ">"
                    text += "\n"
                if text:
                    return text
                else:
                    return "rank list not found"
        else:
            return result["message"]


async def main():
    print(await Updater.retrieve_ladder_boundaries(["rt"]))


if __name__ == "__main__":
    asyncio.run(main())
