from jproperties import Properties
from pathlib import Path
import json

config = Properties()


def discord_login_token() -> str:
    if config.get("discord.token"):
        return config.get("discord.token").data
    else:
        return ""


def bot_owner_discord_user_id() -> int:
    if config.get("bot.owner.discord.user.id"):
        return int(config.get("bot.owner.discord.user.id").data)
    else:
        return ""


def get_lounge_webservice() -> str:
    if config.get("lounge.webservice"):
        return config.get("lounge.webservice").data
    else:
        return ""


def get_lounge_webservice_api_token() -> str:
    if config.get("lounge.webservice.api.token"):
        return config.get("lounge.webservice.api.token").data
    else:
        return ""


def get_lounge_webservice_dictionary(key: str) -> str:
    if config.get("lounge.webservice.dictionary"):
        dictionary: dict = json.loads(config.get("lounge.webservice.dictionary").data)
        try:
            return dictionary[key]
        except KeyError:
            return None
    else:
        return ""


def reload_config():
    with open(Path(__file__).parent / "config/config.properties", "rb") as config_properties:
        selector = Properties()
        selector.load(config_properties)
        with open(Path(__file__).parent / selector.get("config.file").data, "rb") as config_file:
            config.load(config_file)


reload_config()
