from api import lounge
import asyncio
import discord
import discord_common_utils
from discord.ext import commands


class Updater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="listmismatch",
                      aliases=["listmismatchs", "listmismatches"],
                      description="Shows a list of discrepancies/mismatches for Discord and the Lounge iste"
                                  + "\n\n"
                                  + "!listmismatch"
                                  + "\n\n"
                                  + "example: !listmismatch",
                      brief="Shows a list of discrepancies/mismatches for Discord and the Lounge iste")
    async def exec(self, ctx: discord.ext.commands.Context, *, args: str = None):
        if not (discord_common_utils.is_lounge_updater(ctx.author.roles)
                or discord_common_utils.is_owner(ctx.author.id)):
            message: discord.message.Message = await ctx.send("listmismatch is an updater command")
            await asyncio.sleep(3)
            await message.delete()
        else:
            message: str = await self.determine_mismatch(ctx)
            await discord_common_utils.send_message(ctx, message)

    @staticmethod
    async def determine_mismatch(ctx: discord.ext.commands.Context) -> str:
        guild: discord.Guild = ctx.guild
        if not guild:
            return "this command only works in the server"

        json_response: dict = await lounge.retrieve_players()
        if json_response["status"] == "failed":
            if json_response["reason"]:
                return json_response["reason"]
            else:
                return "unlinked discord user list not found"
        else:
            text = ""

            # missing discord id
            for result in json_response["results"]:
                if not result["discord_user_id"]:
                    text += result["player_name"] + " is missing a Discord ID"
                    text += "\n"

            # unlinked users with roles
            discord_user_id_map: dict = dict({})
            missing_discord_user_id_map: dict = dict({})
            for result in json_response["results"]:
                player_name: str = str(result["player_name"]).lower().replace(" ", "")
                if result["discord_user_id"]:
                    discord_user_id: int = int(result["discord_user_id"])
                    discord_user_id_map[str(discord_user_id)] = result["player_name"]
                else:
                    missing_discord_user_id_map[player_name] = result["player_name"]

            members: list[discord.Member] = guild.members
            member: discord.Member
            for member in members:
                role: discord.Role
                is_ladder_player: bool = False
                for role in member.roles:
                    if "Placement" not in role.name and "Request" not in role.name and \
                            ("RT" in role.name or "CT" in role.name):
                        is_ladder_player = True

                if is_ladder_player and not discord_user_id_map.get(str(member.id)):
                    text += member.mention + " has roles but their discord id is not found on the Lounge site"
                    discord_display_name = str(member.display_name).lower().replace(" ", "")
                    if missing_discord_user_id_map.get(discord_display_name):
                        text += " - possible match: " + missing_discord_user_id_map.get(discord_display_name)
                    text += "\n"

            # name does not match
            for result in json_response["results"]:
                player_name: str = str(result["player_name"]).lower().replace(" ", "")
                if result["discord_user_id"]:
                    discord_user_id: int = int(result["discord_user_id"])
                    member: discord.Member = guild.get_member(discord_user_id)
                    if member:
                        discord_display_name = str(member.display_name).lower().replace(" ", "")
                        if player_name != discord_display_name:
                            text += str(member.display_name)
                            text += " name does not match the Lounge site: "
                            text += str(result["player_name"])
                            text += " <@!" + str(discord_user_id) + ">"
                            text += "\n"

            discord_user_name_map: dict = dict({})
            for result in json_response["results"]:
                player_name: str = str(result["player_name"]).lower().replace(" ", "")
                if result["discord_user_id"]:
                    discord_user_id: int = int(result["discord_user_id"])
                    discord_user_name_map[player_name] = discord_user_id

            # discord does not match
            Updater.determine_discord_mismatch(guild, json_response)

            # multiple account to single discord
            Updater.determine_multiple_account_to_single_discord(json_response)

            # ladder role with no matching discord id
            Updater.determine_ladder_role_with_no_matching_discord_id(guild, json_response)

            if text:
                return text
            else:
                return "no mismatch found"

    @staticmethod
    def determine_discord_mismatch(guild: discord.Guild, json_response: dict) -> str:
        text = ""

        discord_user_name_map: dict = dict({})
        for result in json_response["results"]:
            player_name: str = str(result["player_name"]).lower().replace(" ", "")
            if result["discord_user_id"]:
                discord_user_id: int = int(result["discord_user_id"])
                discord_user_name_map[player_name] = discord_user_id

        members: list[discord.Member] = guild.members
        member: discord.Member
        for member in members:
            role: discord.Role
            is_ladder_player: bool = False
            for role in member.roles:
                if "Placement" not in role.name and ("RT" in role.name or "CT" in role.name):
                    is_ladder_player = True
            discord_display_name = str(member.display_name).lower().replace(" ", "")
            if is_ladder_player and discord_user_name_map.get(discord_display_name) \
                    and discord_user_name_map.get(discord_display_name) != member.id:
                text += member.mention + " discord does not match the Lounge site: "
                text += discord_display_name + " <@!" + str(discord_user_name_map.get(discord_display_name)) + ">"
                text += "\n"

        return text

    @staticmethod
    def determine_multiple_account_to_single_discord(json_response: dict) -> str:
        text = ""

        discord_user_id_map: dict = dict({})
        for result in json_response["results"]:
            if result["discord_user_id"]:
                discord_user_id: int = int(result["discord_user_id"])
                if discord_user_id_map.get(discord_user_id):
                    text += "<@!" + str(discord_user_id) + "> is mapped to multiple Lounge site: "
                    text += discord_user_id_map.get(discord_user_id)
                    text += ", "
                    text += result["player_name"]
                    text += "\n"
                else:
                    discord_user_id_map[str(discord_user_id)] = result["player_name"]

        return text

    @staticmethod
    def determine_ladder_role_with_no_matching_discord_id(guild: discord.Guild, json_response: dict) -> str:
        text = ""

        discord_user_name_map: dict = dict({})
        for result in json_response["results"]:
            player_name: str = str(result["player_name"]).lower().replace(" ", "")
            if result["discord_user_id"]:
                discord_user_id: int = int(result["discord_user_id"])
                discord_user_name_map[player_name] = discord_user_id

        members: list[discord.Member] = guild.members
        member: discord.Member
        for member in members:
            role: discord.Role
            is_ladder_player: bool = False
            for role in member.roles:
                if "Placement" not in role.name and ("RT" in role.name or "CT" in role.name):
                    is_ladder_player = True
            discord_display_name = str(member.display_name).lower().replace(" ", "")
            if is_ladder_player and discord_user_name_map.get(discord_display_name) \
                    and discord_user_name_map.get(discord_display_name) != member.id:
                text += member.mention + " discord does not match the Lounge site: "
                text += discord_display_name + " <@!" + str(discord_user_name_map.get(discord_display_name)) + ">"
                text += "\n"

        return text
