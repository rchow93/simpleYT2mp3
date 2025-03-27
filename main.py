import os
import yt_dlp
import argparse

downloaded_count = 0

def parse_url(url: str) -> str:
    if 'list=' in url:
        print("Detected playlist URL")
        return 'playlist'
    elif 'watch?v=' in url:
        print("Detected single video URL")
        return 'single'
    else:
        print("URL doesn't appear to be valid")
        return 'unknown'

def download_youtube_playlist(playlist_url, download_path, limit, output_format, cookies_file=None):
    global downloaded_count
    downloaded_count = 0

    url_type = parse_url(playlist_url)

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best' if output_format == 'm4a' else 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'ignoreerrors': True,  # continue if a video is blocked
        'quiet': False,
        'verbose': True,
    }

    if cookies_file and os.path.exists(cookies_file):
        print(f"Using cookies from {cookies_file}")
        ydl_opts['cookiefile'] = cookies_file

    if output_format == 'mp3':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    def progress_hook(d):
        global downloaded_count
        if d['status'] == 'finished':
            downloaded_count += 1
            if limit > 0 and downloaded_count >= limit:
                raise yt_dlp.utils.DownloadError('Reached the desired number of downloads.')

    ydl_opts['progress_hooks'] = [progress_hook]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if url_type == 'playlist':
            print("Processing playlist URL.")
        elif url_type == 'single':
            print("Processing single video URL.")
        else:
            return

        try:
            ydl.download([playlist_url])
            print(f"Downloaded {downloaded_count} video(s) successfully.")
        except yt_dlp.utils.DownloadError as e:
            if "Reached the desired number of downloads" in str(e):
                print(f"Stopped after downloading {downloaded_count} video(s).")
            else:
                print(f"Download error: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download YouTube playlist videos as audio files.')
    parser.add_argument('-url', '--url', type=str, required=True, help='YouTube playlist URL')
    parser.add_argument('-n', '--n', type=int, default=0, help='Number of items to download (0=all)')
    parser.add_argument('-f', '--format', type=str, choices=['m4a', 'mp3'], default='mp3', help='Output format')
    parser.add_argument('-c', '--cookies', type=str, default=None, help='Path to cookies file')
    parser.add_argument('-o', '--output', type=str, default=None, help='Output directory')

    args = parser.parse_args()
    download_path = args.output if args.output else '/saved'
    os.makedirs(download_path, exist_ok=True)
    print(f"Files will be saved to: {download_path}")

    download_youtube_playlist(args.url, download_path, args.n, args.format, args.cookies)

    for file in os.listdir(download_path):
        if file.endswith('.webm'):
            file_path = os.path.join(download_path, file)
            os.remove(file_path)
            print(f"Deleted incomplete file: {file_path}")

    print(f"Process completed. Audio files converted to {args.format.upper()}")