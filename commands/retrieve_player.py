from api import lounge
import asyncio
import common_utils
import discord
import discord_common_utils
from discord.ext import commands


class Updater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="retrieveplayer",
                      description="Retrieve information about a player on site"
                                  + "\n\n"
                                  + "!retrieveplayer <player's name>"
                                  + "\n\n"
                                  + "example: !retrieveplayer 255mp",
                      brief="Retrieve information about a player on site")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("retrieveplayer is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!retrieveplayer <player's name>"
                message += "\n\n"
                message += "example: !retrieveplayer 255mp"
                message += "```"
            else:
                message: str = await self.retrieve_player(parameters)
            await discord_common_utils.send_message(ctx, message)

    @staticmethod
    def parse_parameters(parameters: list) -> dict:
        error: str = ""
        if parameters:
            try:
                error = "invalid player name"
                player_name: str = parameters[0]
                if not player_name:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "player_name": player_name
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
    async def retrieve_player(parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            player_name: str = result["player_name"]
            json_response: dict = await lounge.retrieve_player_by_name(player_name)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "player not found"
            else:
                text = json_response["results"][0]["player_name"]
                if json_response["results"][0]["discord_user_id"]:
                    text += " <@!" + json_response["results"][0]["discord_user_id"] + ">"
                else:
                    text += " **No Discord ID**"
                if text:
                    return text
                else:
                    return "player not found"
        else:
            return result["message"]


async def main():
    print(await Updater.retrieve_player(["255MP"]))


if __name__ == "__main__":
    asyncio.run(main())
