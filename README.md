# SimpleYT2MP3

A lightweight command-line tool for downloading YouTube playlists and converting them to audio formats (MP3/M4A). This tool leverages the power of `yt-dlp` to download content from YouTube and then uses FFmpeg to convert to the desired audio format.

## Features

- Download entire YouTube playlists or a specific number of videos
- Convert videos to MP3 or M4A audio formats
- Authenticate with YouTube using browser cookies (required for private/restricted videos)
- Configurable output directory
- Automatic cleanup of temporary files
- Detailed progress feedback
- Error handling with graceful fallbacks

## Requirements

### System Dependencies

- Python 3.6+
- FFmpeg (for audio conversion)

### Python Dependencies

- yt-dlp
- argparse

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rchow93/simpleYT2mp3.git
cd simpleYT2mp3
```

### 2. Set up a Virtual Environment (Recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Required Python Packages

```bash
# Install the required libraries
pip install yt-dlp

# If you want to install all dependencies at once
pip install -r requirements.txt
```

#### Create a requirements.txt file with the following content:

```
yt-dlp>=2023.3.4
```

### 4. Install FFmpeg

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### On Windows:
Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your PATH.

#### On macOS:
```bash
brew install ffmpeg
```

## Cookie Authentication

For private or restricted videos, you'll need to provide YouTube cookies from a logged-in browser session.

### Generating Cookie File Using a Browser Extension (Recommended)

1. Install a cookie export extension:
   - Chrome: "Cookie-Editor" or "Get cookies.txt"
   - Firefox: "Cookie Quick Manager"

2. Steps to export cookies:
   - Navigate to YouTube.com and ensure you're logged in
   - Open the extension
   - Select "Export" and choose "Netscape/cookies.txt format" (NOT JSON format)
   - Save the file as "youtube.cookies"

3. Important: The cookie file must be in Netscape format and begin with:
   ```
   # Netscape HTTP Cookie File
   # http://curl.haxx.se/rfc/cookie_spec.html
   # This is a generated file! Do not edit.
   ```

### Alternative: Using yt-dlp to Extract Cookies

```bash
yt-dlp --cookies-from-browser chrome https://www.youtube.com -o "cookies.txt"
```

Replace `chrome` with your browser of choice (firefox, edge, etc.)

## Usage

### Basic Usage

Download an entire playlist and convert to MP3:

```bash
python main.py --url "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

### Advanced Options

```bash
python main.py --url "https://www.youtube.com/playlist?list=PLAYLIST_ID" \
               --n 5 \                      # Download only 5 videos
               --format mp3 \               # Convert to MP3 (or m4a)
               --cookies youtube.cookies \  # Use authentication
               --output "/path/to/folder"   # Specify output directory
```

### Command Line Arguments

| Argument             | Short | Description                                       | Default                                   |
|----------------------|-------|---------------------------------------------------|-------------------------------------------|
| `--url`              | `-url`| YouTube playlist URL (required)                   | None                                      |
| `--n`                | `-n`  | Number of videos to download (0 = all)            | 0 (all)                                   |
| `--format`           | `-f`  | Output format (mp3 or m4a)                        | mp3                                       |
| `--cookies`          | `-c`  | Path to Netscape-formatted cookies file           | None                                      |
| `--output`           | `-o`  | Output directory                                  | "/mnt/c/Users/Richard Chow/Desktop/Games/staging" |

## Troubleshooting

### Common Issues

1. **Cookie Format Errors**:
   - Ensure your cookie file is in Netscape format, not JSON
   - Check that the file begins with `# Netscape HTTP Cookie File`
   - Try regenerating the cookie file with a browser extension

2. **FFmpeg Not Found**:
   - Ensure FFmpeg is installed and in your PATH
   - Try running `ffmpeg -version` to verify installation

3. **Private Video Errors**:
   - Make sure you're logged into YouTube in the browser used for cookie extraction
   - Check that your cookies are recent (YouTube cookies expire)

4. **Download Failures**:
   - Check your internet connection
   - YouTube may be blocking your IP address (try using a VPN)
   - The video may no longer be available

## Limitations

- Cannot download videos with age restrictions or that require special permissions
- Cookie authentication may stop working if YouTube updates its authentication mechanism
- Download speeds may be throttled by YouTube

## Legal Disclaimer

This tool is for personal use only. Please respect copyright laws and YouTube's Terms of Service. Only download content that you have permission to access and use according to applicable laws and regulations.

## License

[MIT License](LICENSE)