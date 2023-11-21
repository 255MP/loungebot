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

    @commands.command(name="addplacement",
                      description="Adds a new placement to a particular ladder"
                                  + "\n\n"
                                  + "!addplacement <rt/ct>, <placement name>, <base mmr>, <base lr>"
                                  + "\n\n"
                                  + "example: !addplacement rt, Wood, 250, 250",
                      brief="Adds a new placement to a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        guild: discord.Guild = ctx.guild
        if not guild.id == config.get_lounge_guild_id():
            return

        if not (discord_common_utils.is_lounge_admin(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("addplacement is an admin command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!addplacement <rt/ct>, <placement name>, <base mmr>, <base lr>"
                message += "\n\n"
                message += "example: !addplacement rt, Wood, 250, 250"
                message += "```"
            else:
                message: str = await self.add_ladder_placement(parameters)
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

                error = "no placement name found"
                placement_name: str = parameters[1]
                if not placement_name:
                    raise ValueError

                error = "invalid base mmr"
                base_mmr: int = int(parameters[2])
                if base_mmr < 0:
                    raise ValueError

                error = "invalid base lr"
                base_lr: int = int(parameters[3])
                if base_lr < 0:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_type": ladder_type,
                        "placement_name": placement_name,
                        "base_mmr": base_mmr,
                        "base_lr": base_lr
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
    async def add_ladder_placement(parameters: list) -> str:
        result: dict = Administrator.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_type: str = result["ladder_type"]
            placement_name: str = result["placement_name"]
            base_mmr: int = result["base_mmr"]
            base_lr: int = result["base_lr"]
            json_response: dict = await lounge.add_ladder_placement(ladder_type, placement_name, base_mmr, base_lr)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "placement list not found"
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
                    return "placement list not found"
        else:
            return result["message"]


async def main():
    print(await Administrator.add_ladder_placement(["rt", "Wood", "250", "250"]))


if __name__ == "__main__":
    asyncio.run(main())
