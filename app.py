import datetime
from math import floor
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import argparse

def main():
  GENRES = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']

  parser = argparse.ArgumentParser()
  parser.add_argument('--tempo', type=int, default=random.randint(80,160))
  parser.add_argument('--genre', type=str, default=random.choice(GENRES))
  args = parser.parse_args()

  TAG_TEMPO = args.tempo
  POMODORO_SEC = 25 * 60
  UNTIL_POMODORO = POMODORO_SEC
  GENRE = args.genre

  scope = "user-library-modify playlist-modify-private"

  sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

  playlist_ids = [] 

  recommend = sp.recommendations(seed_genres=[GENRE],  limit=1, min_tempo=(TAG_TEMPO), max_tempo=(TAG_TEMPO + 5), max_duration_ms=min(5*60*1000, UNTIL_POMODORO*1000))

  while UNTIL_POMODORO > floor(2.5*60):

    print( "UNTIL: ", UNTIL_POMODORO)
    print("TEMPO:" , TAG_TEMPO)
    print("GENRE:", GENRE)

    recommend = sp.recommendations(seed_tracks=random.sample( playlist_ids, min(len(playlist_ids), 3) ), seed_genres=[GENRE],  limit=1, min_tempo=(TAG_TEMPO), max_tempo=(TAG_TEMPO + 5), max_duration_ms=min(5*60*1000, UNTIL_POMODORO*1000))

    if len( recommend["tracks"] ) == 0:

      continue

    print(recommend["tracks"][0]["name"], recommend["tracks"][0]["id"])

    features = sp.audio_features(tracks=[recommend["tracks"][0]["id"]])

    # print(features)
    UNTIL_POMODORO -= floor( features[0]["duration_ms"] / 1000 )
    TAG_TEMPO = features[0]["tempo"]

    playlist_ids.append(recommend["tracks"][0]["id"])

    time.sleep(0.1)

  # rest track
  recommend = sp.recommendations(seed_tracks=random.sample( playlist_ids, min(len(playlist_ids), 3) ), seed_genres=[GENRE], limit=1, min_tempo=(TAG_TEMPO - 25), max_tempo=(TAG_TEMPO-15), min_duration_ms=4*60*1000, max_duration_ms=6*60*1000)

  playlist_ids.append(recommend["tracks"][0]["id"])
  print(recommend["tracks"][0]["name"],recommend["tracks"][0]["id"])

  pl = sp.user_playlist_create(user=sp.me()["id"], name=f"POMODORO: {GENRE}, About{round(TAG_TEMPO)}BPM, {datetime.datetime.now().strftime('%Y%m%d')}", public=False)
  sp.playlist_add_items(playlist_id=pl["id"], items=playlist_ids )
  
main()