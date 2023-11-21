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

    @commands.command(name="restoreevent",
                      aliases=["undeleteevent"],
                      description="Restores a deleted event from a particular ladder"
                                  + "\n\n"
                                  + "!restoreevent <event_id>"
                                  + "\n\n"
                                  + "example: !restoreevent 1"
                                  + "\n\n"
                                  + "important: this can be used to restore deleted penalties, awards, or events",
                      brief="Restores a deleted event from a particular ladder")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        guild: discord.Guild = ctx.guild
        if not guild.id == config.get_lounge_guild_id():
            return

        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("restoreevent is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            parameters: list = common_utils.split_comma(args)
            if not parameters:
                message: str = ""
                message += "```"
                message += "!restoreevent <event_id>"
                message += "\n\n"
                message += "example: !restoreevent 1"
                message += "\n\n"
                message += "important: this can be used to restore deleted penalties, awards, or events"
                message += "```"
            else:
                message: str = await self.restore_ladder_event(parameters)
            await discord_common_utils.send_message(ctx, message)

    @staticmethod
    def parse_parameters(parameters: list) -> dict:
        error: str = ""
        if parameters:
            try:
                error = "invalid event id"
                event_id: int = int(parameters[0])
                if event_id < 0:
                    raise ValueError

                return \
                    {
                        "has_parameters": True,
                        "event_id": event_id
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
    async def restore_ladder_event(parameters: list) -> str:
        result: dict = Updater.parse_parameters(parameters)
        if result["has_parameters"]:
            event_id: int = result["event_id"]
            json_response: dict = await lounge.restore_ladder_event(event_id)
            if json_response["status"] == "failed":
                if json_response["reason"]:
                    return json_response["reason"]
                else:
                    return "event not found"
            else:
                text = "event " + str(event_id) + " has been restored"
                if text:
                    return text
                else:
                    return "event not found"
        else:
            return result["message"]


async def main():
    print(await Updater.restore_ladder_event(["10"]))


if __name__ == "__main__":
    asyncio.run(main())
