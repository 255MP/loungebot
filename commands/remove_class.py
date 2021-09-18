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

    @commands.command(name="removeclass",
                      aliases=["deleteclass"],
                      description="Removes a class from a particular ladder"
                                  + "\n\n"
                                  + "!removeclass <rt/ct>, <class name>"
                                  + "\n\n"
                                  + "example: !removeclass rt, Class Y",
                      brief="Removes a class from a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_admin(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("removeclass is an admin command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!removeclass <rt/ct>, <class name>"
                message += "\n\n"
                message += "example: !removeclass rt, Class Y"
                message += "```"
            else:
                message: str = await self.remove_ladder_class(parameters)
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

                error = "no class name found"
                class_name: str = parameters[1]
                if not class_name:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_id": ladder_id,
                        "class_name": class_name
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
    async def remove_ladder_class(parameters: list) -> str:
        result: dict = Administrator.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_id: int = result["ladder_id"]
            class_name: str = result["class_name"]
            json_response: dict = await lounge.remove_ladder_class(ladder_id, class_name)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "class not found"
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
                        text += "0-{}".format(result["maximum_mmr"])
                    else:
                        text += "unknown"
                    text += ", "
                    text += result["color"]
                    text += "\n"
                if text:
                    return text
                else:
                    return "class not found"
        else:
            return result["message"]


async def main():
    print(await Administrator.remove_ladder_class(["rt", "Class Y"]))


if __name__ == "__main__":
    asyncio.run(main())
