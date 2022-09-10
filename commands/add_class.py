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

    @commands.command(name="addclass",
                      description="Adds a new class to a particular ladder"
                                  + "\n\n"
                                  + "!addclass <rt/ct>, <class name>, <minimum mmr>"
                                  + "\n\n"
                                  + "example: !addclass rt, Class Y, 250"
                                  + "\n"
                                  + "         !addclass rt, Class Y, null"
                                  + "\n"
                                  + "         <minimum mmr> can be any number greater than 0 or null",
                      brief="Adds a new class to a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_admin(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("addclass is an admin command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!addclass <rt/ct>, <class name>, <minimum mmr>"
                message += "\n\n"
                message += "example: !addclass rt, Class Y, 250"
                message += "\n"
                message += "         !addclass rt, Class Y, null"
                message += "\n"
                message += "         <minimum mmr> can be any number greater than 0 or null"
                message += "```"
            else:
                message: str = await self.add_ladder_class(parameters)
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

                error = "no class name found"
                class_name: str = parameters[1]
                if not class_name:
                    raise ValueError

                if parameters[2] == "null" or parameters[2] == "none":
                    minimum_mmr: int = None
                else:
                    error = "invalid minimum mmr"
                    minimum_mmr: int = int(parameters[2])
                    if minimum_mmr < 0:
                        raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_type": ladder_type,
                        "class_name": class_name,
                        "minimum_mmr": minimum_mmr
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
    async def add_ladder_class(parameters: list) -> str:
        result: dict = Administrator.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_type: str = result["ladder_type"]
            class_name: str = result["class_name"]
            minimum_mmr: int = result["minimum_mmr"]
            json_response: dict = await lounge.add_ladder_class(ladder_type, class_name, minimum_mmr)
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
                    text += "\n"
                if text:
                    return text
                else:
                    return "class list not found"
        else:
            return result["message"]


async def main():
    print(await Administrator.add_ladder_class(["rt", "Class Y", "250"]))


if __name__ == "__main__":
    asyncio.run(main())
