import openai
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Function to authenticate Spotify and return the authenticated instance
def authenticate_spotify(client_id, client_secret, redirect_uri, scope):
    """
    Authenticate with the Spotify API.

    Parameters:
    client_id (str): Your Spotify client ID
    client_secret (str): Your Spotify client secret
    redirect_uri (str): The redirect URI for your application
    scope (str): The scope of the authentication request (e.g. 'playlist-modify-public user-follow-read user-follow-modify')

    Returns:
    sp (spotipy.Spotify): An authenticated Spotify instance
    """
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))
    return sp


# Function to authenticate OpenAI API
def authenticate_openai(api_key):
    """
    Authenticate with the OpenAI API.

    Parameters:
    api_key (str): Your OpenAI API key

    Returns:
    None
    """
    openai.api_key = api_key
