from api import lounge
import asyncio
import common_utils
import discord
import discord_common_utils
import json
import requests
from discord.ext import commands


class Administrator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="changeflag",
                      aliases=["changeplayerflag",
                               "updateflag",
                               "updateplayerflag"],
                      description="Update a player's country flag"
                                  + "\n\n"
                                  + "!changeflag <player's name>, <flag code>"
                                  + "\n\n"
                                  + "example: !changeflag 255mp, us"
                                  + "\n\n"
                                  + "important: <flag code> must match one of the entries in"
                                  + "https://flagcdn.com/en/codes.json",
                      brief="Update a player's country flag")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("changeflag is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!changeflag <player's name>, <flag code>"
                message += "\n\n"
                message += "example: !changeflag 255mp, us"
                message += "\n\n"
                message += "important: <flag code> must match one of the entries in https://flagcdn.com/en/codes.json"
                message += "```"
            else:
                message: str = await self.update_player_flag(parameters)
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

                error = "invalid flag code"
                country_flag_map: dict = Administrator.retrieve_flag_codes()
                country_flag: str = parameters[1]
                if country_flag not in country_flag_map \
                        and country_flag.lower() != "null" \
                        and country_flag.lower() != "none":
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "player_name": player_name,
                        "country_flag": country_flag
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
    @common_utils.timed_lru_cache(86400)
    def retrieve_flag_codes() -> dict:
        response: requests.Response = requests.get("https://flagcdn.com/en/codes.json")
        return json.loads(response.text.strip())

    @staticmethod
    async def update_player_flag(parameters: list) -> str:
        result: dict = Administrator.parse_parameters(parameters)
        if result["has_parameters"]:
            player_name: str = result["player_name"]
            country_flag: str = result["country_flag"]
            json_response: dict = await lounge.update_player_flag(player_name, country_flag)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "unable to update player's flag"
            else:
                text = "player name updated " + json_response["results"][0]["player_name"]
                if json_response["results"][0]["discord_user_id"]:
                    text += " <@!" + json_response["results"][0]["discord_user_id"] + ">"
                else:
                    text += " **No Discord ID**"
                if text:
                    return text
                else:
                    return "unable to update player's flag"
        else:
            return result["message"]


async def main():
    print(await Administrator.update_player_flag(["255MP", "us"]))

if __name__ == "__main__":
    asyncio.run(main())
