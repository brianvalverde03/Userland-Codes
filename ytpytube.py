import os
import re
from pytubefix import YouTube, Playlist

# Function to clean up the title and remove unwanted content
def clean_title(title):
    title = re.sub(r'[^\w\s]', '', title).strip()  # Remove special characters
    title = re.sub(r'\bASMR\b', '', title, flags=re.IGNORECASE)  # Remove 'ASMR' or 'asmr'
    title = re.sub(r'\s+', ' ', title)  # Replace multiple spaces with a single space
    return title

# Function to get a list of already downloaded files
def get_downloaded_files(output_path):
    downloaded_files = set()
    for file_name in os.listdir(output_path):
        if file_name.endswith(".mp3"):
            downloaded_files.add(file_name)
    return downloaded_files

# Function to download MP3 from YouTube video URL
def download_mp3(video_url, output_path, downloaded_files, new_downloads):
    try:
        yt = YouTube(video_url)
        creator_name = yt.author

        # Modify the author name for specific creators
        if creator_name == "Ceres Fauna Ch. hololive-EN":
            creator_name = "Fauna"
        elif creator_name == "Dude That's Wholesome":
            creator_name = "DTW"
        elif creator_name == "YourgirlfriendASMR":
            creator_name = "YgASMR"
        elif creator_name == "Solar Girl ASMR":
            creator_name = "SGASMR"
        elif creator_name == "Stronny Cuttles Ch. VAllure":
            creator_name = "Stronny"

        cleaned_title = clean_title(yt.title)
        new_filename = f"{creator_name} - {cleaned_title}.mp3"
        new_filename = re.sub(r'\s+', ' ', new_filename).strip()  # Ensure single spacing

        # Skip if the file already exists
        if new_filename in downloaded_files:
            return  # Silent skip if the file is already downloaded

        # Download the audio
        video = yt.streams.filter(only_audio=True).first()
        mp3_file = video.download(output_path=output_path)
        output_file_path = os.path.join(output_path, new_filename)
        os.rename(mp3_file, output_file_path)  # Rename after download
        new_downloads.append(new_filename)

    except Exception as e:
        print(f"Error downloading {video_url}: {str(e)}")

# Function to download MP3 files from a YouTube playlist URL
def download_playlist_mp3(output_path):
    try:
        playlist_url = "https://youtube.com/playlist?list=PL8SV5EpQTe_oz7d5y72wrBemfVLkByzqL&si=KdwnsZSiPcR2p10a"
        playlist = Playlist(playlist_url)

        # Get already downloaded files
        downloaded_files = get_downloaded_files(output_path)
        new_downloads = []

        # Iterate through the playlist
        for video_url in playlist.video_urls:
            download_mp3(video_url, output_path, downloaded_files, new_downloads)

        if new_downloads:
            print("Finished downloading the following new files:")
            for file in new_downloads:
                print(f" - {file}")
        else:
            print("No new files were downloaded.")
    except Exception as e:
        print(f"Error accessing playlist {playlist_url}: {str(e)}")

# Specify the output path
output_directory = "/Downloads/asmr"  # Update this path
download_playlist_mp3(output_directory)

