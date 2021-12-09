from songs import ScrapeSongs
from spotify_integration import SpotifySongs


def main():
    spotify = SpotifySongs()

    date = input("Which date do you want to travel to (after 2000-01-01)? (YYYY-MM-DD): ")
    billboard = ScrapeSongs(date)
    results = billboard.get_songs()
    songs = []
    try:
        songs = [results[index] for index in range(100)]
    except IndexError:
        print("Wrong date")
        choice = input("Do you want to start over (Y/N)? ").lower()
        if choice == 'y':
            main()
        exit()

    year = date.split("-")[0]
    spotify.get_song_uris(songs, year)
    spotify.create_playlist(date)


main()
