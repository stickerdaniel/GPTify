import openai
from spotify_utils import get_followed_artists
from utils import ask_additional_info, ask_yes_no


# Function to get new artist recommendations using the ChatGPT API
def discover_new_artists(sp):
    """
    Discover new artists based on the provided additional_info.

    Args:
        openai (object): Authenticated OpenAI instance.
        sp (Spotify): Authenticated Spotify instance.
    """

    artists = get_followed_artists(sp)
    additional_info = ask_additional_info()
    prompt = f"I follow these artists: {', '.join(artists)}. Please recommend 20 new artists I might like. Your output should be a semicolon-separated list like this: 'Artist1; Artist2; Artist3; Artist4; Artist5; ...'. Dont put numbering (e.g. 1., 2., 3...) in your output. Dont write anything else. Just the artists in the format mentioned above. {additional_info}"

    # Get recommendations using GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that suggests new artists based on the user's preferences."
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

    recommendations_text = response['choices'][0]['message']['content'].strip()
    recommended_artists = recommendations_text.split('; ')

    for artist_name in recommended_artists:
        # Fetch artist's top songs and display their name and preview link
        results = sp.search(artist_name, type='artist', limit=1)
        if results['artists']['items']:
            artist_id = results['artists']['items'][0]['id']
            top_tracks = sp.artist_top_tracks(artist_id, country='US')
            print(f"\n\nTop songs for {artist_name}:")
            for track in top_tracks['tracks']:
                song_url = track['external_urls']['spotify']
                print(f"{track['name']} - Link: {song_url} - Preview: {track['preview_url']}")

        # Ask the user if they want to follow this artist or not
        artist_link = f"https://open.spotify.com/artist/{artist_id}"

        if ask_yes_no(f'\n{artist_link}\n\nDo you want to follow {artist_name}?'):
            sp.user_follow_artists(ids=[artist_id])
            print(f"Now following {artist_name}.")
        else:
            print(f"Not following {artist_name}.")