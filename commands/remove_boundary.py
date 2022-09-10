from api import lounge
import asyncio
import common_utils
import config
import discord
import discord_common_utils
from discord.ext import commands


class Administrator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="removerank",
                      aliases=["removeranking",
                               "removedivision",
                               "removeboundary",
                               "deleterank",
                               "deleteranking",
                               "deletedivision",
                               "deleteboundary"],
                      description="Removes a rank from a particular ladder"
                                  + "\n\n"
                                  + "!removerank <rt/ct>, <division name>"
                                  + "\n\n"
                                  + "example: !removerank rt, Wood",
                      brief="Removes a rank from a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_admin(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("removerank is an admin command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!removerank <rt/ct>, <division name>"
                message += "\n\n"
                message += "example: !removerank rt, Wood"
                message += "```"
            else:
                message: str = await self.remove_ladder_boundary(parameters)
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

                error = "no rank name found"
                boundary_name: str = parameters[1]
                if not boundary_name:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_type": ladder_type,
                        "boundary_name": boundary_name
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
    async def remove_ladder_boundary(parameters: list) -> str:
        result: dict = Administrator.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_type: str = result["ladder_type"]
            boundary_name: str = result["boundary_name"]
            json_response: dict = await lounge.remove_ladder_boundary(ladder_type, boundary_name)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "rank not found"
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
                    return "rank not found"
        else:
            return result["message"]


async def main():
    print(await Administrator.remove_ladder_boundary(["rt", "Wood"]))


if __name__ == "__main__":
    asyncio.run(main())
