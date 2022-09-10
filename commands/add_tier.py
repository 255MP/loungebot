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

    @commands.command(name="addtier",
                      description="Adds a new tier to a particular ladder"
                                  + "\n\n"
                                  + "!addtier <rt/ct>, <tier name>"
                                  + "\n\n"
                                  + "example: !addtier rt, Tier 10",
                      brief="Adds a new tier to a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_admin(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("addtier is an admin command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!addtier <rt/ct>, <tier name>"
                message += "\n\n"
                message += "example: !addtier rt, Tier 10"
                message += "```"
            else:
                message: str = await self.add_ladder_tier(parameters)
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

                error = "no tier name found"
                tier_name: str = parameters[1]
                if not tier_name:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_type": ladder_type,
                        "tier_name": tier_name
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
    async def add_ladder_tier(parameters: list) -> str:
        result: dict = Administrator.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_type: str = result["ladder_type"]
            tier_name: str = result["tier_name"]
            json_response: dict = await lounge.add_ladder_tier(ladder_type, tier_name)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "tier not found"
            else:
                text = ", ".join([result["tier"] for result in json_response["results"]])
                if text:
                    return text
                else:
                    return "tier not found"
        else:
            return result["message"]


async def main():
    print(await Administrator.add_ladder_tier(["rt", "Top 25"]))


if __name__ == "__main__":
    asyncio.run(main())
