import os
import eyed3


def read_and_print_mp3_tags_sorted(directory_path):
    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return

    # Fetch all mp3 files with their full path and last modification time
    mp3_files = [(os.path.join(directory_path, filename), os.stat(os.path.join(directory_path, filename)).st_mtime)
                 for filename in os.listdir(directory_path) if filename.endswith(".mp3")]

    # Sort files based on last modification time in descending order
    mp3_files_sorted = sorted(mp3_files, key=lambda x: x[1], reverse=False)

    # Iterate over sorted files
    for file_path, _ in mp3_files_sorted:
        filename = os.path.basename(file_path)

        # Load the MP3 file
        audiofile = eyed3.load(file_path)

        if audiofile is not None and audiofile.tag is not None:
            # Print filename
            print(f"Filename: {filename}")

            # Extract artist name and song name from the filename
            artist_name, song_name = filename.rsplit('.mp3', 1)[
                0].split(' - ', 1)
            print(f"Artist: {artist_name}")
            print(f"Song Name: {song_name}")

            # Print available ID3 tags
            print(f"Artist (ID3 Tag): {audiofile.tag.artist}")
            print(f"Title (ID3 Tag): {audiofile.tag.title}")
            print(f"Album (ID3 Tag): {audiofile.tag.album}")
            if audiofile.tag.genre:
                print(f"Genre (ID3 Tag): {audiofile.tag.genre.name}")
            print(f"Track Num: {audiofile.tag.track_num}")
            print(f"Album Artist: {audiofile.tag.album_artist}")
            print(f"Year: {audiofile.tag.getBestDate()}")
            # Additional tags like comments
            comments = [comment.text for comment in audiofile.tag.comments]
            if comments:
                print("Comments:", "; ".join(comments))
            print("-" * 40)
        else:
            print(f"No ID3 tag found for {filename}")


# Example usage
music_directory = "/home/behnam/Music/"
read_and_print_mp3_tags_sorted(music_directory)
