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

    @commands.command(name="listclass",
                      description="Shows a list of classes for a particular ladder"
                                  + "\n\n"
                                  + "!listclass <rt/ct>"
                                  + "\n\n"
                                  + "example: !listclass rt",
                      brief="Shows a list of classes for a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("listclass is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!listclass <rt/ct>"
                message += "\n\n"
                message += "example: !listclass rt"
                message += "```"
            else:
                message: str = await self.retrieve_ladder_classes(parameters)
            await discord_common_utils.send_message(ctx, message)

    @staticmethod
    def parse_parameters(parameters: list) -> dict:
        if parameters:
            try:
                ladder_id: int = int(config.get_lounge_webservice_dictionary(str(parameters[0]).lower()))
                if not ladder_id or ladder_id < 0:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_id": ladder_id
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
    async def retrieve_ladder_classes(parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_id: int = result["ladder_id"]
            json_response: dict = await lounge.retrieve_ladder_class(ladder_id)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "class list not found"
            else:
                text = ""
                for result in json_response["results"]:
                    text += result["ladder_class_name"]
                    text += ", "
                    if result["minimum_mmr"] and result["maximum_mmr"]:
                        text += "{}-{}".format(result["minimum_mmr"],  result["maximum_mmr"])
                    elif result["minimum_mmr"]:
                        text += "above {}".format(result["minimum_mmr"])
                    elif result["maximum_mmr"]:
                        text += "below {}".format(result["maximum_mmr"])
                    else:
                        text += "unknown"
                    text += ", "
                    text += result["color"]
                    text += "\n"
                if text:
                    return text
                else:
                    return "class list not found"
        else:
            return result["message"]


async def main():
    print(await Updater.retrieve_ladder_classes(["rt"]))


if __name__ == "__main__":
    asyncio.run(main())
