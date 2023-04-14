# GPTify: AI-Powered Music Recommendations

GPTify leverages the power of OpenAI's GPT-3.5-turbo to provide personalized song and artist recommendations based on your current playlists and additional input. Discover new music, manage your playlists, and explore a world of tunes with GPTify!

## Features

- Generate song recommendations for your playlists based on the existing songs, artists, and any additional information provided.
- Sort a song into a suitable playlist based on its attributes.
- Discover new artists based on artists you are following
- Add recommended songs to your existing playlists.

## Installation

1. Clone the repository:

```
git clone https://github.com/stickerdaniel/GPTifyGPTify.git
```

2. Install the required dependencies:

```
cd GPTify
pip install -r requirements.txt
```

## Usage

1. Set up the necessary API keys in `config.py`:
```python
OPENAI_API_KEY = 'your_openai_api_key'
SPOTIPY_CLIENT_ID = 'your_spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'your_spotify_client_secret_here'
```
2. Run the main program:
```python 
python main.py
```
3. Authenticate with Spotify and start exploring music recommendations.
