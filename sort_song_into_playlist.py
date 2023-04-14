import json

import openai
from spotify_utils import get_users_playlists, get_song_info
from openai_utils import estimate_tokens
from utils import ask_additional_info


# Function to handle sorting a song into a playlist
def sort_song_into_playlist(sp):
    """
    Handle user input for sorting a song into a playlist.

    Args:
        sp (Spotify): Authenticated Spotify instance.
    """

    # Get user input for the song
    user_input = input("Enter a link to a song or the name / artist: ")
    song = get_song_info(sp, user_input)

    # Get all user-created playlists as a JSON string
    playlists = get_users_playlists(sp)

    # Ask the user for additional information
    additional_info = ask_additional_info()

    prompt = get_prompt(song, playlists, additional_info)
    # Check if the prompt is too long (max 4097 tokens)
    max_tokens = 4097
    prompt_tokens = estimate_tokens(prompt)

    while prompt_tokens >= max_tokens:
        # Reduce the number of playlists
        playlists = json.loads(playlists)[:-1]
        playlists = json.dumps(playlists, indent=2)

        # Generate a new prompt with fewer playlists
        prompt = get_prompt(song, playlists, additional_info)
        prompt_tokens = estimate_tokens(prompt)

        print(f"Prompt is too long ({prompt_tokens} tokens). Trying again with fewer playlists...")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that sorts songs into the most suitable playlists."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=150,
        n=1,
        temperature=0.5,
    )

    recommendations_text = response['choices'][0]['message']['content'].strip()
    print(f"Recommendations: {recommendations_text}")
    recommendations = recommendations_text.split(', ')

    return recommendations


def get_prompt(song, playlists, additional_info):
    prompt = f"I have a song {song} that I want to sort into one of my playlists. Here's the information about my playlists in JSON format: {playlists}. Please provide a top 10 list of which playlist the song fits the most, taking the playlists' names, descriptions, songs, genres, and the general vibe of the playlists into account. {additional_info}"
    return prompt
