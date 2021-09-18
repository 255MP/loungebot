from api import lounge
import asyncio
import common_utils
import discord
import discord_common_utils
from discord.ext import commands


class Updater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addplayer",
                      description="Adds a player to the site"
                                  + "\n\n"
                                  + "!addplayer <player's name>, <discord id>"
                                  + "\n\n"
                                  + "example: !addplayer 255mp, <@!311022748753330176>",
                      brief="Adds a player to the site")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("addplayer is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!addplayer <player's name>, <discord id>"
                message += "\n\n"
                message += "example: !addplayer 255mp, <@!311022748753330176>"
                message += "```"
            else:
                message: str = await self.add_player(parameters)
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

                error = "no discord id found"
                discord_user_id: int = int(parameters[1].replace("<", "")
                                                        .replace("@", "")
                                                        .replace("!", "")
                                                        .replace(">", ""))
                if not discord_user_id:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "player_name": player_name,
                        "discord_user_id": discord_user_id
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
    async def add_player(parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            player_name: str = result["player_name"]
            discord_user_id: int = result["discord_user_id"]
            json_response: dict = await lounge.add_player(player_name, discord_user_id)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "unable to add player"
            else:
                text = "player added " + json_response["results"][0]["player_name"]
                if json_response["results"][0]["discord_user_id"]:
                    text += " <@!" + json_response["results"][0]["discord_user_id"] + ">"
                if text:
                    return text
                else:
                    return "unable to add player"
        else:
            return result["message"]


async def main():
    print(await Updater.add_player(["Top 1", "12345678901"]))


if __name__ == "__main__":
    asyncio.run(main())
