import json
from urllib.parse import urlsplit


# Function to get the playlist info from the given playlist link
def get_playlist(sp, playlist_link):
    """
    Get the playlist info from the given playlist link.

    Args:
        sp (Spotify): Authenticated Spotify instance.
        playlist_link (str): URL of the playlist.

    Returns:
        str: JSON string representation of the playlist with title, description, songs, and playlist ID.
    """
    playlist_id = urlsplit(playlist_link).path.split('/')[-1]
    playlist = sp.playlist(playlist_id)
    results = sp.playlist_items(playlist_id)
    songs = []

    for item in results['items']:
        track = item['track']
        song = {
            "name": track['name'],
            "artist": track['artists'][0]['name']
        }
        songs.append(song)

    playlist_json = {
        "playlist": {
            "id": playlist_id,
            "title": playlist['name'],
            "description": playlist['description'],
            "songs": songs
        }
    }

    return json.dumps(playlist_json, indent=2)


# Function to get all user-created playlists
def get_users_playlists(sp):
    """
    Get all user-created playlists.

    Args:
        sp (Spotify): Authenticated Spotify instance.

    Returns:
        str: JSON string representation of an array containing all user-created playlists with title, description, songs, and playlist ID.
    """
    user_playlists = sp.current_user_playlists()
    all_playlists = []

    for playlist_item in user_playlists['items']:
        playlist_link = playlist_item['external_urls']['spotify']
        playlist_json = get_playlist(sp, playlist_link)
        all_playlists.append(json.loads(playlist_json))

    return json.dumps(all_playlists, indent=2)


# Function to get all the artists the user follows
def get_followed_artists(sp):
    """
    Get a list of all artists followed by the user.

    Args:
        sp (Spotify): Authenticated Spotify instance.

    Returns:
        list: A list of followed artist names.
    """
    followed_artists = []
    after = None

    while True:
        response = sp.current_user_followed_artists(after=after)
        if not response['artists']['items']:
            break

        for artist in response['artists']['items']:
            followed_artists.append(artist['name'])

        after = response['artists']['cursors']['after']

        # Break the loop if the 'after' parameter is None
        if after is None:
            break

    print(f'Followed artists: {len(followed_artists)}')
    return followed_artists


# Function to get the song info from the given Spotify track link or name/artist input
def get_song_info(sp, user_input):
    """
    Retrieves the song name, artist, publishing year, and genre from a Spotify track link or name/artist input.

    Args:
        sp (Spotify): Authenticated Spotify instance.
        user_input (str): The Spotify track link or name/artist input.

    Returns:
        dict: A dictionary containing the song name, artist, publishing year, and genre.
    """
    # Initialize dictionary to store song information
    song_info = {}

    if user_input.startswith("https://open.spotify.com/track/"):
        # If the user input is a Spotify track link
        track_id = urlsplit(user_input).path.split('/')[-1]
        track_info = sp.track(track_id)
    else:
        # If the user input is a song name/artist
        search_result = sp.search(user_input, market='US', limit=1)
        track_info = search_result['tracks']['items'][0]

    # log track info
    print(track_info)

    # Get song name and artist
    song_name = track_info['name']
    artist_name = track_info['artists'][0]['name']

    # Get publishing year
    album_id = track_info['album']['id']
    album_info = sp.album(album_id)
    release_date = album_info['release_date']
    publishing_year = release_date[:4]

    # Add song information to dictionary
    song_info['song_name'] = song_name
    song_info['artist_name'] = artist_name
    song_info['publishing_year'] = publishing_year

    return song_info
