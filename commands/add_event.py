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

    @commands.command(name="addevent",
                      description="Adds a new event to a particular ladder"
                                  + "\n\n"
                                  + "!addevent <rt/ct>, <data>"
                                  + "\n\n"
                                  + "example: !addevent rt, "
                                  + "{\"races\":12,\"format\":\"6\",\"tier\":\"Tier 3\",\"teams\":[...]]}"
                                  + "\n\n"
                                  + "important: only use this command if Updater Bot is down",
                      brief="Adds a new event to a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("addevent is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!addevent <rt/ct>, <data>"
                message += "\n\n"
                message += "example: !addevent rt, {\"races\":12,\"format\":\"6\",\"tier\":\"Tier 3\",\"teams\":[...]]}"
                message += "\n\n"
                message += "important: only use this command if Updater Bot is down"
                message += "```"
            else:
                message: str = await self.add_ladder_event(parameters)
            await discord_common_utils.send_message(ctx, message)

    @staticmethod
    def parse_parameters(parameters: list) -> dict:
        error: str = ""
        if parameters:
            try:
                temp_parameters = parameters.copy()
                error = "invalid ladder id"
                ladder_type: str = int(config.get_lounge_webservice_dictionary(str(temp_parameters[0])))
                if not ladder_type:
                    raise ValueError
                temp_parameters.pop(0)

                error = "no event data found"
                event_data: str = ', '.join(temp_parameters)
                if not event_data:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "ladder_type": ladder_type,
                        "event_data": event_data
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
    async def add_ladder_event(parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            ladder_type: str = result["ladder_type"]
            event_data: str = result["event_data"]
            json_response: dict = await lounge.add_ladder_event(ladder_type, event_data)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "event not found"
            else:
                text = ""
                if len(json_response["results"]) > 0:
                    text += "event " + str(json_response["results"][0]["event_id"]) + " has been added"
                if text:
                    return text
                else:
                    return "event not found"
        else:
            return result["message"]


async def main():
    print(await Updater.add_ladder_event(["rt",
                                          '{"races":12,"format":"6","tier":"Tier 3","teams":[{"players":[{'
                                          '"full_gain_loss":true,"subbed_out":true,"multiplier":1,"player_id":30,'
                                          '"races":6,"score":15},{"multiplier":1,"player_id":1041,"races":12,'
                                          '"score":13},{"subbed_in":true,"multiplier":1,"player_id":281,"races":6,'
                                          '"score":319},{"multiplier":1,"player_id":232,"races":12,"score":17},'
                                          '{"multiplier":1,"player_id":820,"races":12,"score":23},{"multiplier":1,'
                                          '"player_id":857,"races":12,"score":27},{"multiplier":1,"player_id":115,'
                                          '"races":12,"score":19}]},{"players":[{"multiplier":1,"player_id":323,'
                                          '"races":12,"score":29},{"multiplier":1,"player_id":1995,"races":12,'
                                          '"score":50},{"multiplier":1,"player_id":1347,"races":12,"score":55},'
                                          '{"multiplier":1,"player_id":1533,"races":12,"score":23},'
                                          '{"gain_loss_prevented":true,"multiplier":1,"player_id":349,"races":12,'
                                          '"score":59},{"multiplier":1,"player_id":2231,"races":12,"score":80}]}]}']))


if __name__ == "__main__":
    asyncio.run(main())
