import requests
import json
import pandas as pd
import os
from django.conf import settings


class FantasyLeague:
    PLAYERS_FILE_PATH = os.path.join(
        settings.BASE_DIR, "fantasy_news", "static", "fantasy_news", "players.json"
    )

    def __init__(self, league_id):
        self.league_id = league_id
        self.check_and_fetch_players()
        self.players_df = self.load_players_from_file()
        self.rosters_df = self.get_league_rosters()
        self.player_id_to_name = dict(
            zip(self.players_df["player_id"], self.players_df["full_name"])
        )
        self.player_name_to_id = dict(
            zip(self.players_df["full_name"], self.players_df["player_id"])
        )

    def load_players_from_file(self, filename=None):
        filename = filename or FantasyLeague.PLAYERS_FILE_PATH
        with open(filename, "r") as file:
            players = json.load(file)
        return pd.DataFrame(players).T

    def get_league_rosters(self):
        url = f"https://api.sleeper.app/v1/league/{self.league_id}/rosters"
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            print(
                f"Error fetching rosters for league {self.league_id}: {response.status_code}"
            )
            return pd.DataFrame()

    def get_roster_id_for_player(self, player_name):
        player_id = self.player_name_to_id.get(player_name)
        if not player_id:
            print(f"Player ID not found for player: {player_name}")
            return None
        roster_row = self.rosters_df[
            self.rosters_df["players"].apply(lambda x: player_id in x)
        ]
        return roster_row["owner_id"].values[0] if not roster_row.empty else None

    def fetch_owner_info(self, owner_id):
        url = f"https://api.sleeper.app/v1/user/{owner_id}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None

    def get_owner_for_player(self, player_name):
        roster_id = self.get_roster_id_for_player(player_name)
        if not roster_id:
            return None
        owner_info = self.fetch_owner_info(roster_id)
        return owner_info["username"] if owner_info else None

    @staticmethod
    def fetch_players():
        url = "https://api.sleeper.app/v1/players/nfl"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching players: {response.status_code}")
            return None

    @staticmethod
    def save_players_to_file(players, filename=None):
        filename = filename or FantasyLeague.PLAYERS_FILE_PATH
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filename, "w") as file:
            json.dump(players, file)

    def check_and_fetch_players(self):
        if not os.path.exists(FantasyLeague.PLAYERS_FILE_PATH):
            players = FantasyLeague.fetch_players()
            if players:
                FantasyLeague.save_players_to_file(players)
