import sys
import webbrowser
import json
import requests
import unittest
import xml.etree.ElementTree as ET

from constant import SAVE_TRACK_CALL, TRACK_PROPERTY_MAP, OAUTH_TOKEN_PROMPT
from time import sleep

# /Users/julian/Documents/GitHub/Transfer-Apple-Music-Library-to-Spotify/Library.xml

class AppleMusicSong:
    def __init__(self):
        self.track_id = 0
        self.name = ""
        self.artist = ""
        self.album = ""
        self.duration = 0
        self.track_number = 0
        self.track_count = 0
        self.release_date = ""

    def __str__(self):
        # TODO: Remove
        return self.name + "\t[" + self.artist + "]\t" + self.album + "\n"

    def __repr__(self):
        return self.__str__()


class SpotifyLogin:
    def __init__(self):
        self._token = self.get_spotify_token()

    def get_spotify_token(self):
        msg = OAUTH_TOKEN_PROMPT
        print(msg)
        sleep(2)
        # webbrowser.open("https://developer.spotify.com/console/put-current-user-saved-tracks/", 0, True)
        token = ""
        while not token:
            token = input("OAuth Token (Press Q to exit): ")
            if token.lower() == 'q':
                sys.exit()
        return token


class SongTransfer:
    def __init__(self):
        self.song_list = self.get_apple_library()

    def get_xml_file(self):
        xml_file = input("Path to XML library file: ")
        try:
            tree = ET.parse(xml_file)
            return tree
        except FileNotFoundError:
            print("File not found. ")
            sys.exit()

    def get_apple_library(self) -> [AppleMusicSong]:
        tree = self.get_xml_file()
        root = tree.getroot()
        # initialize the dictionaries and set the values to none
        # then iterate over the dict:
        track_list = root.find('dict').find('dict')
        # iterate over track_list to get track_info ([0] is key, [1] is the dict for track info)
        songs = []
        for track_info in range(1, len(track_list), 2):
            song = AppleMusicSong()
            for key in range(0, len(track_list[track_info]), 2):
                if track_list[track_info][key].text in TRACK_PROPERTY_MAP:
                    attr = TRACK_PROPERTY_MAP[track_list[track_info][key].text]
                    attr_val = SongTransfer.string_cleanup(attr, track_list[track_info][key + 1].text)
                    setattr(song, attr, attr_val)
            songs.append(song)

        return songs

    @classmethod
    def string_cleanup(cls, attr, attr_val):
        # strip song names of 'feat', used in Apple Music songs, but not by Spotify (which instead lists featured
        # artists with the main artist, as opposed to in the song title).
        if attr == 'name':
            return attr_val.replace("feat. ", "")
        elif attr == 'release_date':  # xml lists times as well. Just grab the dates for Spotify comparison.
            return attr_val.split('T')[0]
        elif attr == 'album':  # more strings not used in Spotify formats
            attr_val = attr_val.split(' - Single')[0]
            attr_val = attr_val.split('(feat.')[0]
            return attr_val
        else:
            return attr_val

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
    st = SongTransfer()
    print(st.song_list)


#
# class TestSuite(unittest.TestCase):
#     def setUp(self) -> None:
#         self.st = SongTransfer()
#
#     def test_get_spotify_song(self):
#         pass
#
#     # def test_add_song_to_library(self):
#     #     song_uri = "1Adwhpmwhz1CSi7E7QTwIC"
#     #     song = SongTransfer()
#     #     self.assertEqual(song.add_song_to_library(song_uri), 200)
#
#     # def test_get_apple_library(self):
#     #     self.assertEqual(self.st.get_apple_library(), 252)
#
#
