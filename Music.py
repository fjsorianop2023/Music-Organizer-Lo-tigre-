import os
import json
import pygame
from mutagen.mp3 import MP3

pygame.mixer.init()

PLAYLIST_FILE = "playlists.json"

def scan_music_folder(folder_path):
    """Scans the specified folder for music files and retrieves metadata."""
    if not os.path.exists(folder_path):
        print("Folder not found!")
        return []
    
    music_files = []
    for file in os.listdir(folder_path):
        if file.endswith(('.mp3', '.wav')):
            try:
                audio = MP3(os.path.join(folder_path, file))
                duration = int(audio.info.length)
                music_files.append((file, duration))
            except Exception:
                music_files.append((file, "Unknown"))
    
    return music_files

def save_playlists(playlists):
    with open(PLAYLIST_FILE, "w") as file:
        json.dump(playlists, file, indent=4)

def load_playlists():
    if os.path.exists(PLAYLIST_FILE):
        with open(PLAYLIST_FILE, "r") as file:
            return json.load(file)
    return {}
    

def play_song(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    print(f"Now playing: {os.path.basename(file_path)}")
    playback_controls()

def playback_controls():
    """Controls playback: pause, resume, and stop."""
    while True:
        command = input("Enter command (pause/resume/stop): ").strip().lower()
        if command == "pause":
            pygame.mixer.music.pause()
            print("Music paused. Type 'resume' to continue.")
        elif command == "resume":
            pygame.mixer.music.unpause()
            print("Resuming...")
        elif command == "stop":
            pygame.mixer.music.stop()
            print("Playback stopped.")
            return
        else:
            print("Invalid command. Use pause, resume, or stop.")

def play_playlist(playlist_name, playlists, folder_path):
    """Plays the songs in a selected playlist sequentially."""
    if playlist_name not in playlists:
        print("Playlist not found!")
        return
    
    playlist = playlists[playlist_name]
    if not playlist:
        print("Playlist is empty!")
        return
    
    for song in playlist:
        file_path = os.path.join(folder_path, song)
        if not os.path.exists(file_path):
            print(f"File not found: {song}")
            continue
        play_song(file_path)

def manage_playlists(playlists, music_files):
    """Manages playlists by allowing users to create, edit, and delete them."""
    while True:
        print("\nPlaylists:")
        for idx, name in enumerate(playlists.keys(), start=1):
            print(f"{idx}. {name}")
        print("Options: 1. Create 2. Edit 3. Delete 4. View Songs 5. Back")
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            name = input("Enter playlist name: ").strip()
            if name in playlists:
                print("Playlist already exists!")
            else:
                playlists[name] = []
                print("Playlist created.")
        
        elif choice == "2":
            name = input("Enter playlist name to edit: ").strip()
            if name not in playlists:
                print("Playlist not found!")
                continue

            while True:
                print(f"\nEditing Playlist: {name}")
                print(f"Current songs in {name}: {', '.join(playlists[name]) if playlists[name] else 'No songs in this playlist.'}")
                print("Options: 1. Add Song 2. Remove Song 3. Reposition Song 4. Back")
                edit_choice = input("Enter choice: ").strip()

                if edit_choice == "1":
                    print("\nAvailable Songs:")
                    for idx, (file, _) in enumerate(music_files, start=1):
                        print(f"{idx}. {file}")
                    song_choice = input("Enter song number to add: ").strip()
                    if song_choice.isdigit() and 1 <= int(song_choice) <= len(music_files):
                        song_name = music_files[int(song_choice) - 1][0]
                        if song_name not in playlists[name]:
                            playlists[name].append(song_name)
                            print(f"{song_name} added to playlist.")
                        else:
                            print(f"{song_name} is already in the playlist.")
                    else:
                        print("Invalid choice.")
                elif edit_choice == "2":
                    if playlists[name]:
                        song_to_remove = input(f"Enter song name to remove from {name}: ").strip()
                        if song_to_remove in playlists[name]:
                            playlists[name].remove(song_to_remove)
                            print(f"{song_to_remove} removed from playlist.")
                        else:
                            print(f"{song_to_remove} is not in the playlist.")
                    else:
                        print("The playlist is empty. No songs to remove.")
                
                elif edit_choice == "3":
                    if len(playlists[name]) > 1:
                        print(f"Current order: {', '.join(playlists[name])}")
                        song_to_move = input("Enter song name to reposition: ").strip()
                        if song_to_move in playlists[name]:
                            new_position = input(f"Enter the new position (1 to {len(playlists[name])}): ").strip()
                            if new_position.isdigit() and 1 <= int(new_position) <= len(playlists[name]):
                                    playlists[name].remove(song_to_move)
                                    playlists[name].insert(int(new_position) - 1, song_to_move)
                                    print(f"{song_to_move} moved to position {new_position}.")
                            else:
                                print("Invalid position.")
                        else:
                            print(f"{song_to_move} is not in the playlist.")
                    else:
                        print("There are not enough songs to reorder.")
                
                elif edit_choice == "4":
                    break
                else:
                    print("Invalid choice. Please choose again.")
        elif choice == "3":
            name = input("Enter playlist name to delete: ").strip()
            if name in playlists:
                del playlists[name]
                print("Playlist deleted!")
            else:
                print("Playlist not found!")
        
        elif choice == "4":
            view_playlist(playlists)
        
        elif choice == "5":
            save_playlists(playlists)
            break

\

def view_playlist(playlists):
    """Displays the songs in a selected playlist."""
    if not playlists:
        print("No playlists available.")
        return
    print("\nAvailable Playlists:")
    for idx, name in enumerate(playlists.keys(), start=1):
        print(f"{idx}. {name}")

    playlist_choice = input("Enter playlist number to view: ").strip()
    if playlist_choice.isdigit() and 1 <= int(playlist_choice) <= len(playlists):
        playlist_name = list(playlists.keys())[int(playlist_choice) - 1]
        print(f"\nSongs in {playlist_name}:")
        for idx, song in enumerate(playlists[playlist_name], start=1):
            print(f"{idx}. {song}")
    else:
        print("Invalid choice!")
def main():
    print("Welcome to the Music Player!")
    folder_path = input("Enter the music folder path: ").strip()
    music_files = scan_music_folder(folder_path)

    if not music_files:
        print("No music files found!")
        return
    
    playlists = load_playlists()
    playlists = load_playlists()
    
    while True:
        print("\nOptions:")
        print("1. View Music Files")
        print("2. Manage Playlists")
        print("3. View Playlist Songs")
        print("4. Play a Playlist")
        print("5. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            print("\nAvailable Music Files:")
            for idx, (file, duration) in enumerate(music_files, start=1):
                print(f"{idx}. {file} ({duration}s)")
        elif choice == "2":
            manage_playlists(playlists, music_files)
        elif choice == "3":
            view_playlist(playlists)
        elif choice == "4":
            playlist_name = input("Enter the playlist name to play: ").strip()
            play_playlist(playlist_name, playlists, folder_path)
        elif choice == "5":
            save_playlists(playlists)
            print("Goodbye!")
            break

main()