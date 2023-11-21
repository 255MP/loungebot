import config
import discord
from discord.ext import commands


MAX_MESSAGE_LENGTH: int = 2000


def is_owner(discord_user_id: int) -> bool:
    return discord_user_id == config.bot_owner_discord_user_id()


def is_lounge_admin(roles: list) -> bool:
    return contains_role(roles, ["Lower Tier RT Arbitrator", "Higher Tier RT Arbitrator",
                                 "Lower Tier CT Arbitrator", "Higher Tier CT Arbitrator",
                                 "RT Admin", "CT Admin", "Boss"])


def is_lounge_updater(roles: list) -> bool:
    return contains_role(roles, ["RT Updater", "Lower Tier RT Arbitrator", "Higher Tier RT Arbitrator",
                                 "CT updater", "Lower Tier CT Arbitrator", "Higher Tier CT Arbitrator",
                                 "RT Admin", "CT Admin", "Boss", "Good Boy Bot"])


def contains_role(roles: list, matches: list) -> bool:
    role: discord.Role
    for role in roles:
        match: str
        for match in matches:
            if role.name.lower().replace(" ", "") == match.lower().replace(" ", ""):
                return True
    return False


def get_matching_roles(roles: list, matches: list) -> list:
    match: list = []
    role: discord.Role
    for role in roles:
        match: str
        for match in matches:
            if role.name.lower().replace(" ", "") == match.lower().replace(" ", ""):
                match.append(role)
    return match


async def send_message(ctx: discord.ext.commands.Context, message: str):
    if len(message) > MAX_MESSAGE_LENGTH:
        msg = message
        sub_msgs = []

        while len(msg):
            split_point = msg[:MAX_MESSAGE_LENGTH].rfind('\n')
            if split_point != -1:
                sub_msgs.append(msg[:split_point])
                msg = msg[split_point + 1:]
            else:
                split_point = msg[:MAX_MESSAGE_LENGTH].rfind('. ')
                if split_point != -1:
                    sub_msgs.append(msg[:split_point + 1])
                    msg = msg[split_point + 2:]
                else:
                    sub_msgs.append(msg[:MAX_MESSAGE_LENGTH])
                    msg = msg[MAX_MESSAGE_LENGTH:]

        for send_msg in sub_msgs[:-1]:
            await ctx.send(send_msg, allowed_mentions=discord.AllowedMentions.none())

        message = sub_msgs[-1]

    return await ctx.send(message, allowed_mentions=discord.AllowedMentions.none())
