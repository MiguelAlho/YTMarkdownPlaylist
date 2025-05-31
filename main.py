import argparse
from utils import create_outputs_directory, log, save_json_file, format_duration
import yt_dlp
import json
import os
import requests
from urllib.parse import urlparse, parse_qs

def main():
    parser = argparse.ArgumentParser(description="Process a YouTube playlist and generate metadata and markdown files.")
    parser.add_argument("playlist_url", help="The URL or ID of the YouTube playlist to process.")
    parser.add_argument("--silent", action="store_true", help="Run the script in silent mode without logging to the console.")

    args = parser.parse_args()

    outputs_dir = create_outputs_directory()
    log(f"Outputs directory created at: {outputs_dir}", args.silent)

    # Set up yt-dlp options
    ydl_opts = {
        'quiet': args.silent,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(args.playlist_url, download=False)

    # Create a subfolder for the playlist using its ID
    playlist_id = playlist_info.get('id')
    playlist_dir = os.path.join(outputs_dir, playlist_id)
    if not os.path.exists(playlist_dir):
        os.makedirs(playlist_dir)

    # Fetch playlist metadata
    playlist_metadata = {
        "playlist_id": playlist_info.get('id'),
        "title": playlist_info.get('title'),
        "description": playlist_info.get('description'),
        "video_count": len(playlist_info.get('entries', [])),
        "last_updated": None,  # yt-dlp does not provide this directly
        "videos": []
    }

    # Calculate total playlist length
    total_length = sum([entry['duration'] for entry in playlist_info.get('entries', []) if 'duration' in entry])
    playlist_metadata["total_length"] = total_length
    playlist_metadata["total_length_formatted"] = format_duration(total_length)

    for entry in playlist_info.get('entries', []):
        try:
            video_url = entry['url']
            video_info = ydl.extract_info(video_url, download=False)

            # Fetch video metadata
            video_metadata = {
                "video_id": video_info.get('id'),
                "title": video_info.get('title'),
                "description": video_info.get('description'),
                "length": video_info.get('duration'),
                "length_formatted": format_duration(video_info.get('duration')),
                "publish_date": video_info.get('upload_date'),
                "author": video_info.get('uploader'),
                "thumbnail_url": video_info.get('thumbnail'),
                "embed_url": f"https://www.youtube.com/embed/{video_info.get('id')}"
            }

            # Add video metadata to the playlist's videos list
            playlist_metadata["videos"].append(video_metadata)

            # Download and save the thumbnail
            thumbnail_url = video_info.get('thumbnail')
            if thumbnail_url:
                parsed_url = urlparse(thumbnail_url)
                thumbnail_path = parsed_url.path
                thumbnail_extension = thumbnail_path.split('.')[-1]
                thumbnail_file = os.path.join(playlist_dir, f"{video_info.get('id')}_thumbnail.{thumbnail_extension}")

                thumbnail_response = requests.get(thumbnail_url, stream=True)
                if thumbnail_response.status_code == 200:
                    with open(thumbnail_file, 'wb') as f:
                        for chunk in thumbnail_response.iter_content(1024):
                            f.write(chunk)
                    log(f"Thumbnail saved to: {thumbnail_file}", args.silent)
        except Exception as e:
            log(f"Failed to process video {entry['url']}: {e}", args.silent)

    # Save metadata to a JSON file in the playlist subfolder
    metadata_file = os.path.join(playlist_dir, f"p_{playlist_metadata['playlist_id']}_metadata.json")
    save_json_file(playlist_metadata, metadata_file, args.silent)

if __name__ == "__main__":
    main()