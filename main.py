import argparse
from utils import create_outputs_directory, log, save_json_file, format_duration
from download import download_playlist_metadata
import yt_dlp
import json
import os
import requests
from urllib.parse import urlparse
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from yt_dlp.utils import parse_qs
from html_generator import generate_html

def source_playlist_metadata(args, outputs_dir):
    # Extract playlist ID from the URL
    parsed_url = urlparse(args.playlist_url)
    log(f"Parsed URL: {parsed_url}", args.silent)  # Debugging log

    # Extract playlist ID from the URL manually
    query_string = parsed_url.query
    query_params = {param.split('=')[0]: param.split('=')[1] for param in query_string.split('&') if '=' in param}
    playlist_id = query_params.get('list')
    log(f"Manually parsed playlist ID: {playlist_id}", args.silent)  # Debugging log
    if not playlist_id:
        log(f"Invalid playlist URL: {args.playlist_url}", args.silent)
        return None

    metadata_file = os.path.join(outputs_dir, playlist_id, f"p_{playlist_id}_metadata.json")
    if not os.path.exists(metadata_file):
        log(f"Metadata file not found: {metadata_file}", args.silent)
        return None

    with open(metadata_file, "r") as f:
        return json.load(f)

def generate_markdown(playlist_metadata, output_dir):
    markdown_file = os.path.join(output_dir, f"p_{playlist_metadata['playlist_id']}_summary.md")

    with open(markdown_file, "w") as f:
        # Write playlist details
        f.write(f"# {playlist_metadata['title']}\n\n")
        f.write(f"**Description:** {playlist_metadata['description']}\n\n")
        f.write(f"**Total Length:** {playlist_metadata['total_length_formatted']}\n\n")
        f.write(f"**Video Count:** {playlist_metadata['video_count']}\n\n")

        # Write video details
        for video in playlist_metadata['videos']:
            f.write(f"## [{video['title']}](https://www.youtube.com/watch?v={video['video_id']})\n\n")
            f.write(f"**Description:** {video['description']}\n\n")
            f.write(f"**Duration:** {video['length_formatted']}\n\n")
            f.write(f"![Thumbnail](./{video['video_id']}_thumbnail.webp)\n\n")
            if video.get('transcript'):
                f.write(f"**Transcript:**\n\n{video['transcript']}\n\n")

    return markdown_file

def main():
    parser = argparse.ArgumentParser(description="Process a YouTube playlist and generate metadata and markdown files.")
    parser.add_argument("playlist_url", help="The URL or ID of the YouTube playlist to process.")
    parser.add_argument("--silent", action="store_true", help="Run the script in silent mode without logging to the console.")
    parser.add_argument("--generate-markdown-only", action="store_true", help="Generate markdown from existing metadata without downloading data.")

    args = parser.parse_args()

    outputs_dir = create_outputs_directory()
    log(f"Outputs directory created at: {outputs_dir}", args.silent)

    if args.generate_markdown_only:
        playlist_metadata = source_playlist_metadata(args, outputs_dir)
        if not playlist_metadata:
            return
    else:
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

        playlist_metadata = download_playlist_metadata(ydl, playlist_info, playlist_dir, args)

        # Save metadata to a JSON file in the playlist subfolder
        metadata_file = os.path.join(playlist_dir, f"p_{playlist_metadata['playlist_id']}_metadata.json")
        save_json_file(playlist_metadata, metadata_file, args.silent)

    # Generate markdown file
    markdown_file = generate_markdown(playlist_metadata, os.path.join(outputs_dir, playlist_metadata['playlist_id']))
    log(f"Markdown file generated at: {markdown_file}", args.silent)

    # Generate HTML file
    html_file = generate_html(playlist_metadata, os.path.join(outputs_dir, playlist_metadata['playlist_id']))
    log(f"HTML file generated at: {html_file}", args.silent)

if __name__ == "__main__":
    main()