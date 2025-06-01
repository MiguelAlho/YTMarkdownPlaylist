import os
import json

def generate_html(playlist_metadata, output_dir):
    html_file = os.path.join(output_dir, f"p_{playlist_metadata['playlist_id']}_summary.html")

    with open(html_file, "w") as f:
        # Write HTML header
        f.write("<html>\n<head>\n")
        f.write(f"<title>{playlist_metadata['title']}</title>\n")
        f.write("<style>\n")
        f.write("body { font-family: Arial, sans-serif; line-height: 1.6; display: flex; flex-direction: column; height: 100vh; margin: 0; }\n")
        f.write(".header { background-color: #333; color: white; padding: 10px; text-align: center; }\n")
        f.write(".content { display: flex; flex: 1; flex-direction: row; }\n")
        f.write(".left-column { width: 20%; padding: 10px; background-color: #f9f9f9; overflow-y: auto; height: 80vh; }\n")
        f.write(".middle-column { width: 40%; padding: 10px; display: flex; flex-direction: column; }\n")
        f.write(".video-player { height: 315px; margin-bottom: 10px; }\n")
        f.write(".video-description { overflow-y: auto; background-color: #f1f1f1; padding: 10px; }\n")
        f.write(".right-column { width: 40%; padding: 10px; background-color: #f9f9f9; overflow-y: auto; height: 80vh; }\n")
        f.write(".video { margin-bottom: 20px; }\n")
        f.write(".thumbnail { max-width: 100%; height: auto; }\n")
        f.write(".transcript-block { cursor: text; padding: 5px; }\n")
        f.write(".transcript { white-space: pre-wrap; cursor: text; }\n")
        f.write(".highlighted { background-color: #d3f9d8; }\n")
        f.write(".copy-button { margin-top: 10px; padding: 5px 10px; background-color: #007bff; color: white; border: none; cursor: pointer; }\n")
        f.write(".copy-button:hover { background-color: #0056b3; }\n")
        f.write(".transcript-header { display: flex; justify-content: space-between; align-items: center; }\n")
        f.write(".transcript-header h2 { margin: 0; }\n")
        f.write("</style>\n")
        f.write("</head>\n<body>\n")

        # Top header bar with playlist title
        f.write("<div class='header'>\n")
        f.write(f"<h1>{playlist_metadata['title']}</h1>\n")
        f.write("</div>\n")

        # Content area with three columns
        f.write("<div class='content'>\n")

        # Left column: Playlist video list
        f.write("<div class='left-column'>\n")
        for index, video in enumerate(playlist_metadata['videos'], start=1):
            f.write(f"<p>{index}. <a href='#' onclick='showVideo(\"{video['video_id']}\")'>{video['title']}</a></p>\n")
        f.write("</div>\n")

        # Middle column: Video player and metadata
        f.write("<div class='middle-column'>\n")
        f.write("<div class='video-player' id='video-player'>\n")
        f.write("<h2>Select a video to play</h2>\n")
        f.write("</div>\n")
        f.write("<div class='video-description' id='video-description'>\n")
        f.write("<h2>Video Description</h2>\n")
        f.write("<p>Select a video to view its description.</p>\n")
        f.write("</div>\n")
        f.write("</div>\n")

        # Right column: Transcript
        f.write("<div class='right-column'>\n")
        f.write("<div id='transcript'>\n")
        f.write("<div class='transcript-header'>\n")
        f.write("<h2>Transcript</h2>\n")
        f.write("<button class='copy-button' onclick='copySelectedBlocks()'>Copy Selected Blocks</button>\n")
        f.write("</div>\n")
        f.write("<p>Select a video to view its transcript.</p>\n")
        f.write("</div>\n")
        f.write("</div>\n")

        f.write("</div>\n")

        # Add JavaScript for interactivity
        f.write("<script>\n")
        f.write("function showVideo(videoId) {\n")
        f.write("  const videoPlayer = document.getElementById('video-player');\n")
        f.write("  const transcript = document.getElementById('transcript');\n")
        f.write("  const videoDescription = document.getElementById('video-description');\n")
        f.write("  const video = playlistVideos.find(v => v.video_id === videoId);\n")
        f.write("  videoPlayer.innerHTML = `<h2>${video.title}</h2><iframe width='100%' height='315' src='https://www.youtube.com/embed/${video.video_id}' frameborder='0' allowfullscreen></iframe>`;\n")
        f.write("  videoDescription.innerHTML = `<h2>Video Description</h2><p>${video.description}</p>`;\n")
        f.write("  const transcriptHeader = `<div class='transcript-header'><h2>Transcript</h2><button class='copy-button' onclick='copySelectedBlocks()'>Copy Selected Blocks</button></div>`;\n")
        f.write("  const formattedTranscript = (video.transcript || 'No transcript available.').replace(/\\n/g, ' ');\n")
        f.write("  transcript.innerHTML = transcriptHeader + `<p>${formattedTranscript}</p>`;\n")
        f.write("}\n")

        f.write("function toggleSelection(block) {\n")
        f.write("  block.classList.toggle('selected');\n")
        f.write("}\n")

        f.write("function copySelectedBlocks() {\n")
        f.write("  const highlightedSpans = document.querySelectorAll('.highlighted');\n")
        f.write("  const markdown = Array.from(highlightedSpans).map(span => `* ${span.textContent}`).join('\\n');\n")
        f.write("  navigator.clipboard.writeText(markdown).then(() => alert('Copied to clipboard!'));\n")
        f.write("}\n")

        f.write("function highlightSelection() {\n")
        f.write("  const selection = window.getSelection();\n")
        f.write("  if (!selection.isCollapsed) {\n")
        f.write("    const range = selection.getRangeAt(0);\n")
        f.write("    const span = document.createElement('span');\n")
        f.write("    span.classList.add('highlighted');\n")
        f.write("    range.surroundContents(span);\n")
        f.write("    selection.removeAllRanges();\n")
        f.write("  }\n")
        f.write("}\n")

        f.write("document.getElementById('transcript').addEventListener('mouseup', highlightSelection);\n")

        f.write("const playlistVideos = ")
        f.write(json.dumps(playlist_metadata['videos']))
        f.write(";\n")
        f.write("</script>\n")

        # Write HTML footer
        f.write("</body>\n</html>")

    return html_file