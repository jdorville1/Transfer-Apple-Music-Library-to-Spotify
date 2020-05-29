TRACK_PROPERTY_MAP = {'Track ID': 'track_id',
                      'Name': 'name',
                      'Artist': 'artist',
                      'Album': 'album',
                      'Total Time': 'duration',
                      'Track Number': 'track_number',
                      'Track Count': 'track_count',
                      'Release Date': 'release_date'
                      }


# STRINGS:

OAUTH_TOKEN_PROMPT = "A link will open in your browser. Click \"Get Token\" and check the box that says " \
              "\"user-library-modify.\"" \
              "\nIf you would also like to migrate your playlists, check \"playlist-modify-private\" as well.\n\n" \
              "Once you're redirected back to the page, copy the OAuth Token and paste it here. " \
              "Note that this token will expire in ONE HOUR."

SAVE_TRACK_CALL = 'https://api.spotify.com/v1/me/tracks?ids={}'
SAVE_TRACK_SCOPE = 'user-library-modify'
