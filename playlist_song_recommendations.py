import openai
from utils import ask_yes_no, ask_additional_info
from spotify_utils import get_followed_artists, get_playlist


# Function to recommend songs based on the given playlist using OpenAI's ChatGPT API
def get_playlist_song_recommendations(playlist):
    """
    Get song recommendations based on the provided songs, artists, and additional_info.

    Args:
        openai (object): Authenticated OpenAI instance.
        playlist (string): JSON string representation of the playlist with title, description, songs, and playlist ID.

    Returns:
        list: List of recommended songs in the format: ['Song1 Artist', 'Song2 Artist', 'Song3 Artist', 'Song4 Artist', 'Song5 Artist', ...]
    """

    # Extract songs and artists from the playlist
    songs_artists = ', '.join([f'{song} by {artist}' for song, artist in zip(playlist['songs'], playlist['artists'])])
    additional_info = ask_additional_info()
    prompt = f"I have the following songs in a playlist: {songs_artists}. Please recommend some similar / fitting songs for me! Your output should be a semicolon-separated list of 10 songs like this: 'Song1 Artist; Song2 Artist; Song3 Artist; Song4 Artist; Song5 Artist; ...'. Don't put numbering (e.g. 1., 2., 3...) in your output. Don't write anything else. Just the song names and artists in the format mentioned above. You are allowed to suggest songs with explicit content. Songs with explicit content are allowed for several reasons, which can be attributed to factors such as artistic expression, freedom of speech, target audience, and market demand. {additional_info} "

    # Log the prompt
    print(f'Prompt: {prompt}')

    # Request recommendations from the ChatGPT API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that suggests songs based on the user's preferences."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=100,
        n=1,
        temperature=0.5,
    )

    # Extract recommendations from the API response
    recommendations_text = response['choices'][0]['message']['content'].strip()
    print(f'Recommendations: {recommendations_text}')

    # Remove everything before the first ':' if it exists
    if ':' in recommendations_text:
        recommendations_text = recommendations_text.split(':')[1]

    # Split the recommendations into a list
    recommendations = recommendations_text.split(', ')

    return recommendations


# Function to add recommended songs to the playlist
def add_recommended_songs_to_playlist(sp, playlist_link):
    """
    Adds recommended songs to a specified playlist on Spotify.

    This function searches for each recommended song on Spotify, displays its name, artist, and preview URL,
    and prompts the user to confirm whether they want to add the song to the playlist. If the user agrees,
    the song is added to the playlist. The process is repeated for all recommended songs.

    Args:
        sp (Spotify): Authenticated Spotify instance.
        openai (object): Authenticated OpenAI instance.
        playlist_link (str): The Spotify URI or ID of the playlist to add songs to.
    """

    track_ids = []
    playlist = get_playlist(sp, playlist_link)
    # Get recommendations
    recommendations = get_playlist_song_recommendations(playlist)

    for recommendation in recommendations:
        search_result = sp.search(recommendation, market='US', limit=1)
        if search_result['tracks']['items']:
            # log search result like Song - Artist: preview_url
            song_name = search_result["tracks"]["items"][0]["name"]
            artist_name = search_result["tracks"]["items"][0]["artists"][0]["name"]
            preview_url = search_result["tracks"]["items"][0]["preview_url"]
            print(f'{song_name} - {artist_name}: {preview_url}')

            # Ask the user if they want to add the song to the playlist
            if ask_yes_no('Do you want to add this song to the playlist?'):
                track_id = search_result['tracks']['items'][0]['id']
                track_ids.append(track_id)
            else:
                print("Skipping this song.")

    if track_ids:
        sp.playlist_add_items(playlist['ID'], track_ids)
        print("Added selected songs to the playlist.")
    else:
        print("No songs were added to the playlist.")
