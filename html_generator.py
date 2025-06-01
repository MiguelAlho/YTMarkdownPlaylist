import os
import json
from jinja2 import Template

def generate_html(playlist_metadata, output_dir):
    html_template = """
    <html>
    <head>
        <title>{{ playlist_metadata.title }}</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; display: flex; flex-direction: column; height: 100vh; margin: 0; }
            .header { background-color: #333; color: white; padding: 10px; text-align: center; }
            .content { display: flex; flex: 1; flex-direction: row; }
            .left-column { width: 20%; padding: 10px; background-color: #f9f9f9; overflow-y: auto; height: 80vh; }
            .middle-column { width: 40%; padding: 10px; display: flex; flex-direction: column; }
            .video-player { height: 315px; margin-bottom: 10px; }
            .video-description { overflow-y: auto; background-color: #f1f1f1; padding: 10px; }
            .right-column { width: 40%; padding: 10px; background-color: #f9f9f9; overflow-y: auto; height: 80vh; }
            .video { margin-bottom: 20px; }
            .thumbnail { max-width: 100%; height: auto; }
            .transcript { white-space: pre-wrap; cursor: text; }
            .highlighted { background-color: #d3f9d8; }
            .copy-button { margin-top: 10px; padding: 5px 10px; background-color: #007bff; color: white; border: none; cursor: pointer; }
            .copy-button:hover { background-color: #0056b3; }
            .transcript-header { display: flex; justify-content: space-between; align-items: center; }
            .transcript-header h2 { margin: 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{{ playlist_metadata.title }}</h1>
        </div>
        <div class="content">
            <div class="left-column">
                {% for video in playlist_metadata.videos %}
                    <p>{{ loop.index }}. <a href="#" onclick="showVideo('{{ video.video_id }}')">{{ video.title }}</a></p>
                {% endfor %}
            </div>
            <div class="middle-column">
                <div class="video-player" id="video-player">
                    <h2>Select a video to play</h2>
                </div>
                <div class="video-description" id="video-description">
                    <h2>Video Description</h2>
                    <p>Select a video to view its description.</p>
                </div>
            </div>
            <div class="right-column">
                <div id="transcript">
                    <div class="transcript-header">
                        <h2>Transcript</h2>
                        <button class="copy-button" onclick="copySelectedBlocks()">Copy Selected Blocks</button>
                    </div>
                    <p>Select a video to view its transcript.</p>
                </div>
            </div>
        </div>
        <script>
            const playlistVideos = {{ playlist_metadata.videos | tojson }};
            function showVideo(videoId) {
                const videoPlayer = document.getElementById('video-player');
                const transcript = document.getElementById('transcript');
                const videoDescription = document.getElementById('video-description');
                const video = playlistVideos.find(v => v.video_id === videoId);
                videoPlayer.innerHTML = `<h2>${video.title}</h2><iframe width='100%' height='315' src='https://www.youtube.com/embed/${video.video_id}' frameborder='0' allowfullscreen></iframe>`;
                videoDescription.innerHTML = `<h2>Video Description</h2><p>${video.description}</p>`;
                const transcriptHeader = `<div class='transcript-header'><h2>Transcript</h2><button class='copy-button' onclick='copySelectedBlocks()'>Copy Selected Blocks</button></div>`;
                const formattedTranscript = (video.transcript || 'No transcript available.').replace(/\\n/g, ' ');
                transcript.innerHTML = transcriptHeader + `<p>${formattedTranscript}</p>`;
            }
            function copySelectedBlocks() {
                const highlightedSpans = document.querySelectorAll('.highlighted');
                const markdown = Array.from(highlightedSpans).map(span => `* ${span.textContent}`).join('\\n');
                navigator.clipboard.writeText(markdown).then(() => alert('Copied to clipboard!'));
            }
            function highlightSelection() {
                const selection = window.getSelection();
                if (!selection.isCollapsed) {
                    const range = selection.getRangeAt(0);
                    const span = document.createElement('span');
                    span.classList.add('highlighted');
                    range.surroundContents(span);
                    selection.removeAllRanges();
                }
            }
            document.getElementById('transcript').addEventListener('mouseup', highlightSelection);
        </script>
    </body>
    </html>
    """

    template = Template(html_template)
    rendered_html = template.render(playlist_metadata=playlist_metadata)

    html_file = os.path.join(output_dir, f"p_{playlist_metadata['playlist_id']}_summary.html")
    with open(html_file, "w") as f:
        f.write(rendered_html)

    return html_file