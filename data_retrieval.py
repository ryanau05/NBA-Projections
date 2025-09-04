from nba_api.stats.endpoints import playergamelog, playercareerstats
from nba_api.stats.static import players
from nba_api.stats.library.parameters import SeasonAll
import numpy as np
import requests
import unicodedata


def strip_accents(text: str) -> str:                                                #strips name of accents
    normalized = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")

def get_player_info(player_name: str):                                              #retrievs name, id, status
    player_dict = players.get_players()
    name = strip_accents(player_name)
    full_name = "NO PLAYER"
    player_id = -1
    is_active = False

    for player in player_dict:
        if strip_accents(player["full_name"]).lower() == name.lower():
            full_name = player["full_name"]
            player_id = player["id"]
            is_active = player["is_active"]

    return full_name,player_id,is_active

def get_stats(p_id):                                                                #gets career stats sorted by year
    log = playergamelog.PlayerGameLog(player_id = p_id, season=SeasonAll.all).get_data_frames()[0]
    season_dfs = {
    season: group.reset_index(drop=True)
    for season, group in log.groupby("SEASON_ID")}

    return season_dfs

def main():
    print("Please Enter A Player's Full Name: ")
    user_input = input()

    name,p_id,is_active = get_player_info(user_input)
    if name == "NO PLAYER":
        print("Sorry, that player was not found")
        return
    if is_active == False:
        print("Sorry, that player is inactive")
        return

    career_stats = get_stats(p_id)


main()