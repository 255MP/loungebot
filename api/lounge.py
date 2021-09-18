import config
import json
import requests


async def add_ladder_boundary(ladder_id: int, boundary_name: str, minimum_lr: int, color: str,
                              emblem: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "boundary_name": boundary_name,
                "minimum_lr": minimum_lr,
                "color": color,
                "emblem": emblem,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderboundary.php"
        response: requests.Response = requests.put(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_ladder_boundary(ladder_id: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderboundary.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_ladder_boundary(ladder_id: int, boundary_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "boundary_name": boundary_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderboundary.php"
        response: requests.Response = requests.delete(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_class(ladder_id: int, class_name: str, minimum_mmr: int, color: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "class_name": class_name,
                "minimum_mmr": minimum_mmr,
                "color": color,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderclass.php"
        response: requests.Response = requests.put(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_ladder_class(ladder_id: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderclass.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_ladder_class(ladder_id: int, class_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "class_name": class_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderclass.php"
        response: requests.Response = requests.delete(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_event(ladder_id: int, event_data: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "event_data": event_data,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/laddereventratingcalc.php"
        response: requests.Response = requests.post(url, headers={"content-type": "application/json"}, params=params)
        print(response.text)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_ladder_event(event_id: int) -> dict:
    try:
        params: dict = \
            {
                "event_id": event_id,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderevent.php"
        response: requests.Response = requests.delete(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_player_award(ladder_id: int, player_names: str, award: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "player_names": player_names,
                "award": award,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayerawardpenalty.php"
        response: requests.Response = requests.post(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_player_penalty(ladder_id: int, player_names: str, penalty: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "player_names": player_names,
                "penalty": penalty,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayerawardpenalty.php"
        response: requests.Response = requests.post(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_player(ladder_id: int, player_name: str, placement_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "player_name": player_name,
                "placement_name": placement_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayer.php"
        response: requests.Response = requests.post(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_ladder_player(ladder_id: int, player_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "player_name": player_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayer.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_ladder_player(ladder_id: int, player_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "player_name": player_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayer.php"
        response: requests.Response = requests.delete(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_placement(ladder_id: int, placement_name: str, base_mmr: int, base_lr: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "placement_name": placement_name,
                "base_mmr": base_mmr,
                "base_lr": base_lr,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplacement.php"
        response: requests.Response = requests.put(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_ladder_placement(ladder_id: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplacement.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_ladder_placement(ladder_id: int, placement_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "placement_name": placement_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplacement.php"
        response: requests.Response = requests.delete(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_player(player_name: str, discord_user_id: int) -> dict:
    try:
        params: dict = \
            {
                "player_name": player_name,
                "discord_user_id": discord_user_id,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/player.php"
        response: requests.Response = requests.post(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_players() -> dict:
    try:
        params: dict = \
            {
                "all": 1,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/player.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_player_by_name(player_name: str) -> dict:
    try:
        params: dict = \
            {
                "player_name": player_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/player.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_player_by_discord_user_id(discord_user_id: str) -> dict:
    try:
        params: dict = \
            {
                "discord_user_id": discord_user_id,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/player.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_player(player_name: str) -> dict:
    try:
        params: dict = \
            {
                "player_name": player_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/player.php"
        response: requests.Response = requests.delete(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def update_player_discord(player_name: str, discord_user_id: int) -> dict:
    try:
        params: dict = \
            {
                "player_name": player_name,
                "discord_user_id": discord_user_id,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/player.php"
        response: requests.Response = requests.put(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def update_player_flag(player_name: str, country_flag: str) -> dict:
    try:
        params: dict = \
            {
                "player_name": player_name,
                "country_flag": country_flag,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/player.php"
        response: requests.Response = requests.put(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def update_player_name(player_name: str, player_new_name: str) -> dict:
    try:
        params: dict = \
            {
                "player_name": player_name,
                "player_new_name": player_new_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/player.php"
        response: requests.Response = requests.put(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_player_strikes(ladder_id: int, player_names: str, strikes: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "player_names": player_names,
                "strikes": strikes,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayerstrikes.php"
        response: requests.Response = requests.put(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception as e:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_ladder_max_strikes(ladder_id: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayerstrikes.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_tier(ladder_id: int, tier_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "tier_name": tier_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/laddertier.php"
        response: requests.Response = requests.post(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_ladder_tier(ladder_id: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/laddertier.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_ladder_tier(ladder_id: int, tier_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_id": ladder_id,
                "tier_name": tier_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/laddertier.php"
        response: requests.Response = requests.delete(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}
