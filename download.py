import os
import requests
from urllib.parse import urlparse
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from utils import log, format_duration

def download_playlist_metadata(ydl, playlist_info, playlist_dir, args):
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

            try:
                # Fetch transcript for the video
                transcript = YouTubeTranscriptApi.get_transcript(video_info.get('id'))
                video_metadata["transcript"] = "\n".join([item['text'] for item in transcript])
            except (TranscriptsDisabled, NoTranscriptFound):
                video_metadata["transcript"] = None
            except Exception as e:
                log(f"Failed to fetch transcript for video {video_info.get('id')}: {e}", args.silent)

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

    return playlist_metadata