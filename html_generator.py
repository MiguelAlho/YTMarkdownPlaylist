import os
import json

def generate_html(playlist_metadata, output_dir):
    html_file = os.path.join(output_dir, f"p_{playlist_metadata['playlist_id']}_summary.html")

    with open(html_file, "w") as f:
        # Write HTML header
        f.write("<html>\n<head>\n")
        f.write(f"<title>{playlist_metadata['title']}</title>\n")
        f.write("<style>\n")
        f.write("body { font-family: Arial, sans-serif; line-height: 1.6; display: flex; flex-direction: row; }\n")
        f.write(".left-column { width: 20%; padding: 10px; background-color: #f9f9f9; overflow-y: auto; }\n")
        f.write(".middle-column { width: 60%; padding: 10px; }\n")
        f.write(".right-column { width: 20%; padding: 10px; background-color: #f9f9f9; overflow-y: auto; }\n")
        f.write(".video { margin-bottom: 20px; }\n")
        f.write(".thumbnail { max-width: 100%; height: auto; }\n")
        f.write("</style>\n")
        f.write("</head>\n<body>\n")

        # Left column: Playlist video list
        f.write("<div class='left-column'>\n")
        f.write(f"<h2>{playlist_metadata['title']}</h2>\n")
        for video in playlist_metadata['videos']:
            f.write(f"<p><a href='#' onclick='showVideo(\"{video['video_id']}\")'>{video['title']}</a></p>\n")
        f.write("</div>\n")

        # Middle column: Video player and metadata
        f.write("<div class='middle-column'>\n")
        f.write("<div id='video-player'>\n")
        f.write("<h2>Select a video to play</h2>\n")
        f.write("</div>\n")
        f.write("</div>\n")

        # Right column: Transcript
        f.write("<div class='right-column'>\n")
        f.write("<div id='transcript'>\n")
        f.write("<h2>Transcript</h2>\n")
        f.write("<p>Select a video to view its transcript.</p>\n")
        f.write("</div>\n")
        f.write("</div>\n")

        # Add JavaScript for interactivity
        f.write("<script>\n")
        f.write("function showVideo(videoId) {\n")
        f.write("  const videoPlayer = document.getElementById('video-player');\n")
        f.write("  const transcript = document.getElementById('transcript');\n")
        f.write("  const video = playlistVideos.find(v => v.video_id === videoId);\n")
        f.write("  videoPlayer.innerHTML = `<h2>${video.title}</h2><iframe width='100%' height='315' src='https://www.youtube.com/embed/${video.video_id}' frameborder='0' allowfullscreen></iframe><p><strong>Description:</strong> ${video.description}</p><p><strong>Duration:</strong> ${video.length_formatted}</p>`;\n")
        f.write("  transcript.innerHTML = `<h2>Transcript</h2><p>${video.transcript || 'No transcript available.'}</p>`;\n")
        f.write("}\n")
        f.write("const playlistVideos = ")
        f.write(json.dumps(playlist_metadata['videos']))
        f.write(";\n")
        f.write("</script>\n")

        # Write HTML footer
        f.write("</body>\n</html>")

    return html_file