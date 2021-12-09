import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth


class SpotifySongs:
    def __init__(self):
        self.song_uris = []
        self.SPOTIFY_REDIRECT_URL = "http://example.com"
        self.sp = self.__authenticate()
        self.user_id = self.sp.current_user()["id"]

    def __authenticate(self):
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                                                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                                                                redirect_uri=self.SPOTIFY_REDIRECT_URL,
                                                                scope="playlist-modify-private",
                                                                show_dialog=True,
                                                                cache_path="token.txt"))
        except EOFError:
            print("Sorry problem with authentication")
            exit()
        return self.sp

    def get_song_uris(self, songs, year):
        for song in songs:
            result = self.sp.search(q=f"track:{song} year: {year}", type="track")
            try:
                self.song_uris.append(result["tracks"]["items"][0]["uri"])
            except IndexError:
                print(f"😔 Sorry couldn't find {song} on spotify!")

    def create_playlist(self, date):
        playlist_id = self.sp.user_playlist_create(user=self.user_id, name=f"{date} Billboard 100", public=False)['id']
        self.sp.playlist_add_items(playlist_id=playlist_id, items=self.song_uris)
        print(f"Playlist {date} Billboard 100 created in your spotify, here is your playlist id: {playlist_id}")
