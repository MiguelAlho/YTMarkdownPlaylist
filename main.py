import argparse
from utils import create_outputs_directory, log, save_json_file
from pytube import Playlist, YouTube
import json
import os

def main():
    parser = argparse.ArgumentParser(description="Process a YouTube playlist and generate metadata and markdown files.")
    parser.add_argument("playlist_url", help="The URL or ID of the YouTube playlist to process.")
    parser.add_argument("--silent", action="store_true", help="Run the script in silent mode without logging to the console.")

    args = parser.parse_args()

    outputs_dir = create_outputs_directory()
    log(f"Outputs directory created at: {outputs_dir}", args.silent)

    playlist = Playlist(args.playlist_url)

    # Create a subfolder for the playlist using its ID
    playlist_id = playlist.playlist_id
    playlist_dir = os.path.join(outputs_dir, playlist_id)
    if not os.path.exists(playlist_dir):
        os.makedirs(playlist_dir)

    # Fetch playlist metadata
    playlist_metadata = {
        "playlist_id": playlist_id,
        "title": playlist.title,
        "description": playlist.description,
        "video_count": len(playlist.video_urls),
        "last_updated": playlist.last_updated,
        "videos": playlist.video_urls
    }

    # Save metadata to a JSON file in the playlist subfolder
    metadata_file = os.path.join(playlist_dir, f"{playlist_id}_metadata.json")
    save_json_file(playlist_metadata, metadata_file, args.silent)

    for video_url in playlist.video_urls:
        video = YouTube(video_url)

        # Fetch video metadata
        video_metadata = {
            "video_id": video.video_id,
            "title": video.title,
            "description": video.description,
            "length": video.length,
            "publish_date": video.publish_date.strftime("%Y-%m-%d") if video.publish_date else None,
            "author": video.author,
            "thumbnail_url": video.thumbnail_url,
            "embed_url": video.embed_url
        }

        # Save video metadata to a JSON file
        video_metadata_file = os.path.join(playlist_dir, f"{video.video_id}_metadata.json")
        save_json_file(video_metadata, video_metadata_file, args.silent)

if __name__ == "__main__":
    main()