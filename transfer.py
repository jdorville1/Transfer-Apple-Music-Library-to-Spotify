import secrets
import webbrowser
import json
from importlib import reload
from time import sleep

import requests
import unittest
from constant import SAVE_TRACK_CALL


class AppleMusicLogin:
    pass


class SpotifyLogin:
    def __init__(self):
        self._token = self.get_spotify_token()

    def get_spotify_token(self):
        msg = "A link will open in your browser. Click \"Get Token\" and check the box that says " \
              "\"user-library-modify.\"" \
              "\nIf you would also like to migrate your playlists, check \"playlist-modify-private\" as well.\n\n" \
              "Once you're redirected back to the page, copy the OAuth Token and paste it here. " \
              "Note that this token will expire in ONE HOUR."
        print(msg)
        sleep(2)
        # webbrowser.open("https://developer.spotify.com/console/put-current-user-saved-tracks/", 0, True)
        return input("OAuth Token: ")


class SongTransfer:
    def __init__(self):
        self.song_list = []

    def get_apple_library(self, xml_file):
        pass


    def transfer_songs(self):
        pass

    def get_spotify_song(self):
        pass

    def add_song_to_library(self, song_uri):
        query = SAVE_TRACK_CALL.format(song_uri)
        response = requests.put(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(SpotifyLogin().token)
            }
        )
        return response.status_code

    def generate_songs_not_found_table(self):
        pass

    def resolve_conflicts(self):
        pass

    def print_summary(self):
        pass


if __name__ == '__main__':
    st = SpotifyLogin()
#
# class TestSuite(unittest.TestCase):
#     def setUp(self) -> None:
#         pass
#
#     def test_get_spotify_song(self):
#         pass
#
#     def test_add_song_to_library(self):
#         song_uri = "1Adwhpmwhz1CSi7E7QTwIC"
#         song = SongTransfer()
#         self.assertEqual(song.add_song_to_library(song_uri), 200)
