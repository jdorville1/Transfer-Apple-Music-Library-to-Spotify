import sys
import urllib.parse
import webbrowser
import requests
import cosine_similarity
import xml.etree.ElementTree as ET
import constant
from time import sleep
from exceptions import ResponseException


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
        return self.name + "\t[" + self.artist + "]\t" + self.album

    def __repr__(self):
        return self.__str__()


class SpotifyLogin:
    def __init__(self):
        self._token = self.generate_spotify_token()

    def generate_spotify_token(self):
        # have the user enter the spotify token, granting the needed permissions.
        msg = constant.OAUTH_TOKEN_PROMPT
        print(msg)
        sleep(0)
        webbrowser.open("https://developer.spotify.com/console/put-current-user-saved-tracks/", 0, True)
        token = ""
        while not token:
            token = input("OAuth Token (Press Q to exit): ")
            if token.lower() == 'q':
                sys.exit()
        return token

    def get_token(self):
        return self._token


class SongTransfer:
    def __init__(self):
        self.song_list = self.get_apple_library()
        self._spotify_token = SpotifyLogin().get_token()
        self._not_found = []

    def get_xml_file(self):
        xml_file = input("Path to XML library file: ")
        try:
            tree = ET.parse(xml_file)
            return tree
        except FileNotFoundError:
            print("File not found. ")
            sys.exit()

    def get_apple_library(self) -> [AppleMusicSong]:
        # parse the Library.xml file
        tree = self.get_xml_file()
        root = tree.getroot()
        track_list = root.find('dict').find('dict')
        songs = []
        # if the properties being grabbed match the properties we can compare against in the Spotify API,
        # then we add the values to the song's instance properties.
        for track_info in range(1, len(track_list), 2):
            song = AppleMusicSong()
            for key in range(0, len(track_list[track_info]), 2):
                if track_list[track_info][key].text in constant.TRACK_PROPERTY_MAP:
                    attr = constant.TRACK_PROPERTY_MAP[track_list[track_info][key].text]
                    attr_val = SongTransfer.string_cleanup(attr, track_list[track_info][key + 1].text)
                    setattr(song, attr, attr_val)
            songs.append(song)

        return songs

    @classmethod
    def string_cleanup(cls, attr, attr_val):
        # strip song names of 'feat', used in Apple Music songs, but not by Spotify (which instead lists featured
        # artists with the main artist, as opposed to in the song title).
        if attr == 'name':
            return attr_val.replace("feat. ", "").replace("&", "")
        elif attr == 'artist':
            return attr_val.replace("&", "")  # this throws off Spotify search function
        elif attr == 'release_date':  # xml lists times as well. Just grab the dates for Spotify comparison.
            return attr_val.split('T')[0]
        elif attr == 'album':  # more strings not used in Spotify formats
            attr_val = attr_val.split(' - Single')[0]
            attr_val = attr_val.split('(feat.')[0]
            return attr_val
        else:
            return attr_val

    def transfer_songs(self):
        for song in self.song_list:
            self.get_spotify_song(song)
        self.generate_songs_not_found_table()

    def get_spotify_song(self, song: AppleMusicSong):
        query = urllib.parse.quote_plus(song.name + " " + song.artist)
        url = constant.SEARCH_FOR_SONG.format(query)
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self._spotify_token)
            }
        )

        data = response.json()
        if response.status_code != 200:
            raise ResponseException(data['error']['status'], data['error']['message'])

        most_similar_id = self.get_spotify_id(data, song)

        if most_similar_id == '':
            self._not_found.append(song)
        else:
            self.add_song_to_library(most_similar_id)

    def get_spotify_id(self, data, song):
        """
        For the tracks obtained from Spotify API, generates score based on similar title and artist names, calculated
        by cosine similarity. Then, if the album, as well as track number, song duration, and album release date match
        across the iTunes Library song and the current song being checked, the score increases.
        """
        most_similar_id, most_similar_score = '', 0.0
        apple_track_text = song.name + song.album + song.artist

        for track in data['tracks']['items']:
            score = 0.0
            spotify_track_text = track['name'] + track['album']['name']
            for artist in track['artists']:
                spotify_track_text += artist['name']

            score += cosine_similarity.get_cosine(cosine_similarity.text_to_vector(spotify_track_text),
                                                  cosine_similarity.text_to_vector(apple_track_text)) * 3

            score += (track['track_number'] == song.track_number)
            score += (track['album']['total_tracks'] == song.track_count)
            score += (track['duration_ms'] == song.duration)
            score += (track['album']['release_date'] == song.release_date) * 2

            if score > most_similar_score:
                most_similar_score = score
                most_similar_id = track['id']
        return most_similar_id

    def add_song_to_library(self, song_id):
        url = constant.SAVE_TRACK_CALL.format(song_id)
        response = requests.put(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self._spotify_token)
            }
        )

    def generate_songs_not_found_table(self):
        print('\n' * 5)
        print("The following tracks could not be found on Spotify. Try searching for them within the app: ")
        print('-' * 80)

        for song in self._not_found:
            print("Track: ", song.name)
            print("Artist(s):", song.artist)
            print("Album: ", song.album)
            print('-' * 80)


def main():
    st = SongTransfer()
    st.transfer_songs()

if __name__ == '__main__':
    main()


#
# class TestSuite(unittest.TestCase):
#     def setUp(self) -> None:
#         self.st = SongTransfer()
#
#
#     def test_get_spotify_song(self):
#         self.song = SongTransfer().song_list[3]
#         self.st.get_spotify_song()
#
#         # pass an apple music song
#         # test we get good/bad spotify response
#         # format string for each item in the response
#             # grab properties we need (basically same as constant apple music ones)
#         # test cosine similarity see which is best
#         # whichever has best, return that one to save it to the library
#         # TODO: also append them to playlists
#
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
