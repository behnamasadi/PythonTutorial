import requests
from PIL import Image
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your Spotify API credentials
client_id = '7f7a4081a0234b49bced2e5d7a847a8a'
client_secret = 'ac2f801e60dd45aaa88b355b8f6d57c7'
redirect_uri = 'http://localhost:4002'

# Define the scope of access
scope = 'user-library-read'

# Authenticate and get a token
auth_manager = SpotifyOAuth(
    client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Fetch the saved tracks

# Authentication and setup
scope = 'user-library-read'
auth_manager = SpotifyOAuth(
    client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)


def save_album_cover(track, index):
    # Get the URL of the album cover, using the largest size
    album_url = track['album']['images'][0]['url']
    response = requests.get(album_url)  # Download the image
    # Open the image from the downloaded content
    img = Image.open(BytesIO(response.content))
    # Create a filename for the image
    filename = f"track_{index+1}_{track['name'].replace('/', '')}.png"
    img.save(filename)  # Save the image as a PNG file
    print(f"Saved album cover for {track['name']} as {filename}")


def get_saved_tracks_with_covers():
    results = sp.current_user_saved_tracks()
    index = 0
    print(index=0)
    while results:
        for item in results['items']:
            track = item['track']
            save_album_cover(track, index)
            index += 1
        if results['next']:
            results = sp.next(results)
        else:
            results = None


def get_artist_genres(artist_id):
    artist_info = sp.artist(artist_id)
    return artist_info['genres']


def get_saved_tracks_with_genres():
    results = sp.current_user_saved_tracks()
    tracks_with_genres = []
    while results:
        for item in results['items']:
            track = item['track']
            # Assuming we take the first artist for genre
            artist_id = track['artists'][0]['id']
            genres = get_artist_genres(artist_id)
            track_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'genres': genres
            }
            tracks_with_genres.append(track_info)
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return tracks_with_genres


# Example usage
if __name__ == '__main__':
    tracks_info = get_saved_tracks_with_genres()
    for track in tracks_info:
        print(
            f"Track: {track['name']}, Artist: {track['artist']}, Album: {track['album']}, Genres: {', '.join(track['genres'])}")


# # Example usage
# if __name__ == '__main__':
#     get_saved_tracks_with_covers()
