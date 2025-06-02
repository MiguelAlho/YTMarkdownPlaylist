def generate_confluence_markdown(playlist_metadata, output_dir):
    import os
    confluence_file = os.path.join(output_dir, f"p_{playlist_metadata['playlist_id']}_summary.confluence.md")
    with open(confluence_file, "w", encoding="utf-8") as f:
        # Playlist title
        f.write(f"# {playlist_metadata['title']}\n\n")
        
        # Page Properties Table
        f.write("| Property | Value |\n")
        f.write("|---|---|\n")
        f.write(f"| Description | {playlist_metadata['description']} |\n")
        f.write(f"| Total Length | {playlist_metadata['total_length_formatted']} |\n")
        f.write(f"| Video Count | {playlist_metadata['video_count']} |\n")
        f.write(f"| Link | [YouTube Playlist](https://www.youtube.com/playlist?list={playlist_metadata['playlist_id']}) |\n\n")
        
        # Ordered list of video links
        f.write("## Video List\n\n")
        for idx, video in enumerate(playlist_metadata['videos'], 1):
            anchor = f"video-{idx}"
            f.write(f"{idx}. [{video['title']}](#{anchor})\n")

        f.write("\n---\n\n")
        f.write("\n## Videos\n\n")
        for idx, video in enumerate(playlist_metadata['videos'], 1):
            f.write(f"---\n")
            anchor = f"video-{idx}"
            f.write(f"<a id=\"{anchor}\"></a>\n")
            video_url = f"https://www.youtube.com/watch?v={video['video_id']}"
            f.write(f"### [{video['title']}]({video_url})\n\n")
            f.write(f"{video_url}\n\n")
            f.write(f"**Description:** {video['description']}\n\n")
            f.write(f"**Duration:** {video['length_formatted']}\n\n")
            
            # Transcript (if available)
            if video.get('transcript'):
                transcript_oneline = video['transcript'].replace('\n', ' ')
                f.write(f"**Transcript:**\n\n{transcript_oneline}\n\n")
    return confluence_file
