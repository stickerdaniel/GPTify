import openai_utils
from authentication import authenticate_spotify, authenticate_openai
from sort_song_into_playlist import sort_song_into_playlist
from playlist_song_recommendations import add_recommended_songs_to_playlist
from discover_new_artists import discover_new_artists
from config import SPOTIFY_CLIENT_ID as client_id, SPOTIFY_CLIENT_SECRET as client_secret, SPOTIFY_REDIRECT_URI as redirect_uri, SPOTIFY_SCOPE as scope, OPENAI_API_KEY as api_key


# Function to display the main menu and execute user-selected options
def main():
    """
    Main function that displays the main menu and handles user input to execute the selected options.
    """

    # Authenticate and create instances
    redirect_uri = 'http://localhost:8080'
    scope = 'playlist-modify-public user-follow-read user-follow-modify'
    sp = authenticate_spotify(client_id, client_secret, redirect_uri, scope)
    authenticate_openai(api_key)

    # Main menu loop
    while True:
        print("\n\n\n### Menu:")
        print("1. Sort song into playlist")
        print("2. Add songs to an existing playlist")
        print("3. Discover new artists")
        print("4. Quit")
        choice = input("Enter your choice (1, 2, 3, or 4): ")

        if choice == '1':
            sort_song_into_playlist(sp)
        elif choice == '2':
            playlist_link = input("Enter the playlist link: ")
            add_recommended_songs_to_playlist(sp, playlist_link)
        elif choice == '3':
            discover_new_artists(sp)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == '__main__':
    main()
