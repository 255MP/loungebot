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

    @commands.command(name="removeplacement",
                      aliases=["deleteplacement"],
                      description="Removes a placement from a particular ladder"
                                  + "\n\n"
                                  + "!removeplacement <rt/ct>, <division name>"
                                  + "\n\n"
                                  + "example: !removeplacement rt, Wood",
                      brief="Removes a placement from a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_admin(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("removeplacement is an admin command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!removeplacement <rt/ct>, <division name>"
                message += "\n\n"
                message += "example: !removeplacement rt, Wood"
                message += "```"
            else:
                message: str = await self.remove_ladder_placement(parameters)
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
                placement_name: str = parameters[1]
                if not placement_name:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_type": ladder_type,
                        "placement_name": placement_name
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
    async def remove_ladder_placement(parameters: list) -> str:
        result: dict = Administrator.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_type: str = result["ladder_type"]
            placement_name: str = result["placement_name"]
            json_response: dict = await lounge.remove_ladder_placement(ladder_type, placement_name)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "rank not found"
            else:
                text = ""
                for result in json_response["results"]:
                    text += result["ladder_placement_name"]
                    text += ", "
                    if result["base_mmr"]:
                        text += "Base MMR: {}".format(result["base_mmr"]) + ", "
                    if result["base_lr"]:
                        text += "Base LR: {}".format(result["base_lr"])
                    text += "\n"
                if text:
                    return text
                else:
                    return "rank not found"
        else:
            return result["message"]


async def main():
    print(await Administrator.remove_ladder_placement(["rt", "Wood"]))


if __name__ == "__main__":
    asyncio.run(main())
