from api import lounge
import asyncio
import common_utils
import discord
import discord_common_utils
from discord.ext import commands


class Updater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="changediscord",
                      aliases=["changediscordid",
                               "changeplayerdiscord",
                               "changeplayerdiscordid",
                               "updatediscord",
                               "updatediscordid",
                               "updateplayerdiscord",
                               "updateplayerdiscordid"],
                      description="Update a player's Discord ID"
                                  + "\n\n"
                                  + "!changediscord <player's name>, <discord id>"
                                  + "\n\n"
                                  + "example: !changediscord 255mp, <@!311022748753330176>",
                      brief="Update a player's Discord ID")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("changediscord is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!changediscord <player's name>, <discord id>"
                message += "\n\n"
                message += "example: !changediscord 255mp, <@!311022748753330176>"
                message += "```"
            else:
                message: str = await self.update_player_discord(parameters)
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
    async def update_player_discord(parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            player_name: str = result["player_name"]
            discord_user_id: int = result["discord_user_id"]
            json_response: dict = await lounge.update_player_discord(player_name, discord_user_id)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "unable to update player's discord"
            else:
                text = "player discord updated " + json_response["results"][0]["player_name"]
                if json_response["results"][0]["discord_user_id"]:
                    text += " <@!" + json_response["results"][0]["discord_user_id"] + ">"
                else:
                    text += " **No Discord ID**"
                if text:
                    return text
                else:
                    return "unable to update player's discord"
        else:
            return result["message"]


async def main():
    print(await Updater.update_player_discord(["255MP", "123123"]))


if __name__ == "__main__":
    asyncio.run(main())
