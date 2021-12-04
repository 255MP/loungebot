from api import lounge
import asyncio
import common_utils
import config
import discord
import discord_common_utils
from discord.ext import commands


class Updater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="place",
                      aliases=["placement",
                               "addladderplayer"],
                      description="Adds a player to a particular ladder"
                                  + "\n\n"
                                  + "!place <rt/ct>, <player's name>, <placement name>"
                                  + "\n\n"
                                  + "example: !place rt, 255mp, Wood"
                                  + "\n\n"
                                  + "important: <player's name> must exist when running the command retrieveplayer"
                                  + "\n"
                                  + "           <placement name> can be obtained using !listplacement",
                      brief="Adds a player to a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("place is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!place <rt/ct>, <player's name>, <placement name>"
                message += "\n\n"
                message += "example: !place rt, 255mp, Wood"
                message += "\n\n"
                message += "important: <player's name> must exist when running the command retrieveplayer"
                message += "\n"
                message += "           <placement name> can be obtained using !listplacement"
                message += "```"
            else:
                message: str = await self.add_ladder_player(parameters)
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

                error = "invalid player name"
                player_name: str = parameters[1]
                if not player_name:
                    raise ValueError

                error = "invalid placement name"
                placement_name: str = str(parameters[2])

                return \
                    {
                        "has_parameters": True,
                        "ladder_id": ladder_id,
                        "player_name": player_name,
                        "placement_name": placement_name
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
    async def add_ladder_player(parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_id: int = result["ladder_id"]
            player_name: str = result["player_name"]
            placement_name: str = result["placement_name"]
            json_response: dict = await lounge.add_ladder_player(ladder_id, player_name, placement_name)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "player not found"
            else:
                text = json_response["results"][0]["player_name"]
                if json_response["results"][0]["current_mmr"] is not None:
                    text += ", MMR: " + str(json_response["results"][0]["current_mmr"])
                    text += " (" + json_response["results"][0]["current_class"] + ")"
                if json_response["results"][0]["current_lr"] is not None:
                    text += ", LR: " + str(json_response["results"][0]["current_lr"])
                    text += " (" + json_response["results"][0]["current_division"] + ")"
                if json_response["results"][0]["penalties"] is not None:
                    text += ", Award/Penalties: " + str(json_response["results"][0]["penalties"])
                if text:
                    return text
                else:
                    return "player not found"
        else:
            return result["message"]


async def main():
    print(await Updater.add_ladder_player(["rt", "255MP", "Bronze"]))


if __name__ == "__main__":
    asyncio.run(main())
