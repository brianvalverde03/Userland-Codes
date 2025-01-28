import yt_dlp
import time

# Function to download MP3 with custom user-agent and delay
def download_mp3_with_user_agent_and_delay(video_url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(uploader)s - %(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,  # Suppress output
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',  # Set a common user-agent
        'sleep_interval': 5,  # Add a 5-second delay between requests
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Function to download MP3 from a YouTube playlist
def download_playlist_mp3(output_path):
    try:
        playlist_url = "https://youtube.com/playlist?list=PL8SV5EpQTe_oz7d5y72wrBemfVLkByzqL&si=KdwnsZSiPcR2p10a"
        playlist = yt_dlp.Playlist(playlist_url)

        # Iterate through the playlist and download each video
        for video_url in playlist.video_urls:
            download_mp3_with_user_agent_and_delay(video_url, output_path)
            time.sleep(5)  # Ensure a delay between each download to avoid rate-limiting issues

    except Exception as e:
        print(f"Error accessing playlist {playlist_url}: {str(e)}")

# Specify the output path
output_directory = "/mnt/d/asmr"  # Update this path
download_playlist_mp3(output_directory)

