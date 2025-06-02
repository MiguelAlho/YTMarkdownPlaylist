# YT Markdown Playlist

A MCP experiment to convert a Youtube playlist and meta info into a markdown file and HTML page

## How to Use

### Activate the venv

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### process a playlist

On youtube, grab the playlist link, such as: https://www.youtube.com/playlist?list=PLf38f5LhQtheK16nwnCYFqH23WUUvZfSb

```powershell
python main.py "<playlist url>"
```
