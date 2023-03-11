import config
import json
import requests


async def add_ladder_boundary(ladder_type: str, boundary_name: str, minimum_lr: int, color: str,
                              emblem: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
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


async def retrieve_ladder_boundary(ladder_type: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderboundary.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_ladder_boundary(ladder_type: str, boundary_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "boundary_name": boundary_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderboundary.php"
        response: requests.Response = requests.delete(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_class(ladder_type: str, class_name: str, minimum_mmr: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "class_name": class_name,
                "minimum_mmr": minimum_mmr,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderclass.php"
        response: requests.Response = requests.put(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_ladder_class(ladder_type: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderclass.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_ladder_class(ladder_type: str, class_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "class_name": class_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderclass.php"
        response: requests.Response = requests.delete(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_event(ladder_type: str, event_data: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
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


async def restore_ladder_event(event_id: int) -> dict:
    try:
        params: dict = \
            {
                "event_id": event_id,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderevent.php"
        response: requests.Response = requests.put(url, headers={"content-type": "application/json"}, params=params)
        print(response.text.strip())
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_player_mmr(ladder_type: str, player_names: str, mmr: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "player_names": player_names,
                "mmr": mmr,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayermmradjustment.php"
        response: requests.Response = requests.post(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_player_award(ladder_type: str, player_names: str, award: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "player_names": player_names,
                "award": award,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayerawardpenalty.php"
        response: requests.Response = requests.post(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_player_penalty(ladder_type: str, player_names: str, penalty: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "player_names": player_names,
                "penalty": penalty,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayerawardpenalty.php"
        response: requests.Response = requests.post(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_player(ladder_type: str, player_name: str, placement_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "player_name": player_name,
                "placement_name": placement_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayer.php"
        response: requests.Response = requests.post(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_ladder_player(ladder_type: str, player_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "player_name": player_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayer.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_ladder_player(ladder_type: str, player_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "player_name": player_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayer.php"
        response: requests.Response = requests.delete(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_placement(ladder_type: str, placement_name: str, base_mmr: int, base_lr: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
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


async def retrieve_ladder_placement(ladder_type: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplacement.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_ladder_placement(ladder_type: str, placement_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
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


async def update_player_controller(discord_user_id: int, game_controller: str) -> dict:
    try:
        params: dict = \
            {
                "discord_user_id": discord_user_id,
                "game_controller": game_controller,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/player.php"
        response: requests.Response = requests.put(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def update_player_discord(player_name: str, new_discord_user_id: int) -> dict:
    try:
        params: dict = \
            {
                "player_name": player_name,
                "new_discord_user_id": new_discord_user_id,
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


async def add_ladder_player_strikes(ladder_type: str, player_names: str, strikes: int) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "player_names": player_names,
                "strikes": strikes,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayerstrikes.php"
        response: requests.Response = requests.put(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception as e:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_ladder_max_strikes(ladder_type: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/ladderplayerstrikes.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def add_ladder_tier(ladder_type: str, tier_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "tier_name": tier_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/laddertier.php"
        response: requests.Response = requests.post(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def retrieve_ladder_tier(ladder_type: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/laddertier.php"
        response: requests.Response = requests.get(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}


async def remove_ladder_tier(ladder_type: str, tier_name: str) -> dict:
    try:
        params: dict = \
            {
                "ladder_type": ladder_type,
                "tier_name": tier_name,
                "code": config.get_lounge_webservice_api_token()
            }
        url: str = config.get_lounge_webservice() + "/api/laddertier.php"
        response: requests.Response = requests.delete(url, headers={"content-type": "application/json"}, params=params)
        return json.loads(response.text.strip())
    except Exception:
        return {"status": "failed", "reason": "unable to connect to lounge api"}
