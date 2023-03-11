from api import lounge
import asyncio
import common_utils
import discord
import discord_common_utils
from discord.ext import commands


class Public(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="changecontroller",
                      description="Change player's controller"
                                  + "\n\n"
                                  + "!changecontroller <controller name: gcn, classic, ccp, wiiwheel, nunchuk, none>"
                                  + "\n\n"
                                  + "example: !changecontroller gcn",
                      brief="Update player's controller")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        parameters: list = common_utils.split_comma(args)
        if not parameters:
            message: str = ""
            message += "```"
            message += "!changecontroller <controller name: gcn, classic, ccp, wiiwheel, nunchuk, none>"
            message += "\n\n"
            message += "example: !changecontroller gcn"
            message += "```"
        else:
            message: str = await self.update_player_controller(ctx.author.id, parameters)
        await discord_common_utils.send_message(ctx, message)

    @staticmethod
    def parse_parameters(parameters: list) -> dict:
        error: str = ""
        if parameters:
            try:
                error = "invalid controller name, use either: gcn, classic, ccp, wiiwheel, nunchuk, none"
                controller_name: str = parameters[0]
                if not controller_name:
                    raise ValueError
                if not (controller_name == "gcn" or controller_name == "classic" or controller_name == "ccp"
                        or controller_name == "wiiwheel" or controller_name == "nunchuk" or controller_name == "none"):
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "controller_name": controller_name
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
    async def update_player_controller(discord_user_id: int, parameters: list) -> str:
        result: dict = Public.parse_parameters(parameters)
        if result["has_parameters"]:
            controller_name: str = result["controller_name"]
            json_response: dict = await lounge.retrieve_player_by_discord_user_id(discord_user_id)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return "<@!" + str(discord_user_id) + "> cannot change controller because " + \
                                                     "the discord account is not tied to " + \
                                                     "site lounge profile";
                else:
                    return None
            else:
                json_response: dict = await lounge.update_player_controller(discord_user_id, controller_name)
                if json_response["status"] == "failed":
                    if json_response["reason"]:
                        return json_response["reason"]
                    else:
                        return "player or controller not found"
                else:
                    return "<@!" + str(discord_user_id) + "> controller has been updated to " + controller_name
        else:
            return result["message"]


async def main():
    print(await Public.update_player_controller(311022748753330176, ["wiiwheel"]))


if __name__ == "__main__":
    asyncio.run(main())
