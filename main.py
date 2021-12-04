# Internal
import config
from commands import add_boundary
from commands import add_class
from commands import add_event
from commands import add_ladder_award
from commands import add_ladder_mmr
from commands import add_ladder_penalty
from commands import add_ladder_player
from commands import add_placement
from commands import add_player
from commands import add_strikes
from commands import add_tier
from commands import list_boundary
from commands import list_class
from commands import list_max_strikes
from commands import list_mismatch
from commands import list_placement
from commands import list_tiers
from commands import reload_config
from commands import remove_boundary
from commands import remove_class
from commands import remove_event
from commands import remove_ladder_player
from commands import remove_placement
from commands import remove_player
from commands import remove_tier
from commands import restore_event
from commands import retrieve_ladder_player
from commands import retrieve_ladder_player_game_counter
from commands import retrieve_player
from commands import update_player_discord_user_id
from commands import update_player_flag
from commands import update_player_name
from customization.loungebot import LoungeBot
from discordevent import display_name_update

# Third party
import discord
from discord.ext import commands
import logging

# Configure logging
logging.basicConfig(filename="log/error.log", format='%(asctime)s %(message)s')

# Configure bot
intents = discord.Intents.default()
intents.members = True
bot = LoungeBot(command_prefix="!",
                case_insensitive=True,
                intents=intents,
                allowed_mentions=discord.AllowedMentions.none())


# Bot events
@bot.event
async def on_ready():
    print(bot.user.name + " locked and loaded!")


@bot.event
async def on_command_error(ctx: discord.ext.commands.Context, error: Exception):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        return
    raise error


# Register bot commands
bot.add_cog(add_boundary.Administrator(bot))
bot.add_cog(add_class.Administrator(bot))
bot.add_cog(add_event.Updater(bot))
bot.add_cog(add_ladder_award.Updater(bot))
bot.add_cog(add_ladder_mmr.Updater(bot))
bot.add_cog(add_ladder_penalty.Updater(bot))
bot.add_cog(add_ladder_player.Updater(bot))
bot.add_cog(add_placement.Administrator(bot))
bot.add_cog(add_player.Updater(bot))
bot.add_cog(add_strikes.Updater(bot))
bot.add_cog(add_tier.Administrator(bot))
bot.add_cog(list_boundary.Updater(bot))
bot.add_cog(list_class.Updater(bot))
bot.add_cog(list_max_strikes.Updater(bot))
bot.add_cog(list_mismatch.Updater(bot))
bot.add_cog(list_tiers.Updater(bot))
bot.add_cog(list_placement.Updater(bot))
bot.add_cog(reload_config.Administrator(bot))
bot.add_cog(remove_boundary.Administrator(bot))
bot.add_cog(remove_class.Administrator(bot))
bot.add_cog(remove_event.Updater(bot))
bot.add_cog(remove_ladder_player.Updater(bot))
bot.add_cog(remove_placement.Administrator(bot))
bot.add_cog(remove_player.Updater(bot))
bot.add_cog(remove_tier.Administrator(bot))
bot.add_cog(restore_event.Updater(bot))
bot.add_cog(retrieve_ladder_player.Updater(bot))
bot.add_cog(retrieve_ladder_player_game_counter.Updater(bot))
bot.add_cog(retrieve_player.Updater(bot))
bot.add_cog(update_player_discord_user_id.Updater(bot))
bot.add_cog(update_player_flag.Administrator(bot))
bot.add_cog(update_player_name.Updater(bot))


# Register bot events
bot.add_cog(display_name_update.Bot(bot))


# Start the bot
if config.discord_login_token():
    bot.run(config.discord_login_token())
else:
    print("invalid discord token")
