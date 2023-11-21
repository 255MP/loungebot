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

    @commands.command(name="addrank",
                      aliases=["addranking",
                               "adddivision",
                               "addboundary"],
                      description="Adds a new rank to a particular ladder"
                                  + "\n\n"
                                  + "!addrank <rt/ct>, <division name>, <minimum lr>, <hex color>, <url to emblem>"
                                  + "\n\n"
                                  + "example: !addrank rt, Wood, 250, #663300, https://i.imgur.com/ETxn48m.png"
                                  + "\n"
                                  + "         !addrank rt, Wood, null, #663300, https://i.imgur.com/ETxn48m.png"
                                  + "\n"
                                  + "         <minimum lr> can be any number greater than 0 or null"
                                  + "\n\n"
                                  + "important: <emblem> must be 100x100 px",
                      brief="Adds a new rank to a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        guild: discord.Guild = ctx.guild
        if not guild.id == config.get_lounge_guild_id():
            return

        if not (discord_common_utils.is_lounge_admin(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("addrank is an admin command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!addrank <rt/ct>, <division name>, <minimum lr>, <hex color>, <url to emblem>"
                message += "\n\n"
                message += "example: !addrank rt, Wood, 250, #663300, https://i.imgur.com/ETxn48m.png"
                message += "\n"
                message += "         !addrank rt, Wood, null, #663300, https://i.imgur.com/ETxn48m.png"
                message += "\n"
                message += "         <minimum lr> can be any number greater than 0 or null"
                message += "\n\n"
                message += "important: <emblem> must be 100x100 px"
                message += "```"
            else:
                message: str = await self.add_ladder_boundary(parameters)
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

                if parameters[2] == "null" or parameters[2] == "none":
                    minimum_lr: int = None
                else:
                    error = "invalid minimum lr"
                    minimum_lr: int = int(parameters[2])
                    if minimum_lr < 0:
                        raise ValueError

                error = "invalid hex color"
                color: str = parameters[3]
                if len(color) != 7:
                    raise ValueError

                error = "no emblem found"
                emblem: str = parameters[4]
                if not emblem:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_type": ladder_type,
                        "boundary_name": boundary_name,
                        "minimum_lr": minimum_lr,
                        "color": color,
                        "emblem": emblem
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
    async def add_ladder_boundary(parameters: list) -> str:
        result: dict = Administrator.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_type: str = result["ladder_type"]
            boundary_name: str = result["boundary_name"]
            minimum_lr: int = result["minimum_lr"]
            color: str = result["color"]
            emblem: str = result["emblem"]
            json_response: dict = await lounge.add_ladder_boundary(ladder_type, boundary_name, minimum_lr, color, emblem)
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
    print(await Administrator.add_ladder_boundary(["rt", "Wood", "250", "#ff00ff", "/lounge/images/wood.png"]))


if __name__ == "__main__":
    asyncio.run(main())
