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

    @commands.command(name="removetier",
                      aliases=["deletetier"],
                      description="Removes a tier from a particular ladder"
                                  + "\n\n"
                                  + "!removetier <rt/ct>, <tier name>"
                                  + "\n\n"
                                  + "example: !removetier rt, Tier 10",
                      brief="Removes a tier from a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_admin(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("removetier is an admin command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!removetier <rt/ct>, <tier name>"
                message += "\n\n"
                message += "example: !removetier rt, Tier 10"
                message += "```"
            else:
                message: str = await self.remove_ladder_tier(parameters)
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

                error = "no tier name found"
                tier_name: str = parameters[1]
                if not tier_name:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_id": ladder_id,
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
    async def remove_ladder_tier(parameters: list) -> str:
        result: dict = Administrator.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_id: int = result["ladder_id"]
            tier_name: str = result["tier_name"]
            json_response: dict = await lounge.remove_ladder_tier(ladder_id, tier_name)
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
    print(await Administrator.remove_ladder_tier(["rt", "Top 25"]))


if __name__ == "__main__":
    asyncio.run(main())
