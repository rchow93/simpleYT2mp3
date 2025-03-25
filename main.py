import os
import yt_dlp
import argparse

downloaded_count = 0


def download_youtube_playlist(playlist_url, download_path, limit, output_format, cookies_file=None):
    global downloaded_count
    downloaded_count = 0

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best' if output_format == 'm4a' else 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'ignoreerrors': True,  # Continue on download errors
        'quiet': False,
        'verbose': True,  # More detailed output for troubleshooting
    }

    # Add cookies if provided
    if cookies_file and os.path.exists(cookies_file):
        print(f"Using cookies from {cookies_file}")
        ydl_opts['cookiefile'] = cookies_file

    # Add postprocessor for MP3 conversion if needed
    if output_format == 'mp3':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    # Add progress hooks
    def progress_hook(d):
        global downloaded_count
        if d['status'] == 'finished':
            if 'filename' in d:
                print(f'Conversion completed for: {d["filename"]}')
            downloaded_count += 1
            if limit > 0 and downloaded_count >= limit:
                raise yt_dlp.utils.DownloadError('Reached the desired number of downloads.')

    ydl_opts['progress_hooks'] = [progress_hook]

    # First extract playlist info without downloading
    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
        try:
            info = ydl.extract_info(playlist_url, download=False)
            if 'entries' in info:
                total_videos = len(info['entries'])
                print(f"Found {total_videos} videos in playlist")

                # Apply limit if specified
                if limit > 0 and limit < total_videos:
                    print(f"Will download {limit} of {total_videos} videos")
                else:
                    print(f"Will download all {total_videos} videos")
            else:
                print("URL doesn't appear to be a playlist")
                return
        except Exception as e:
            print(f"Error extracting playlist info: {e}")
            return

    # Now download the videos
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([playlist_url])
            print(f"Downloaded {downloaded_count} videos successfully")
        except yt_dlp.utils.DownloadError as e:
            if "Reached the desired number of downloads" in str(e):
                print(f"Stopped after downloading {downloaded_count} videos as requested")
            else:
                print(f"Download error: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download YouTube playlist videos as audio files.')
    parser.add_argument('-url', '--url', type=str, required=True,
                        help='YouTube playlist URL')
    parser.add_argument('-n', '--n', type=int, default=0,
                        help='Number of items to download from the playlist (0 = all, default)')
    parser.add_argument('-f', '--format', type=str, choices=['m4a', 'mp3'], default='mp3',
                        help='Output file format (m4a or mp3)')
    parser.add_argument('-c', '--cookies', type=str, default=None,
                        help='Path to cookies file for authenticated access')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='Output directory (default is current directory)')

    args = parser.parse_args()

    # Set download path
    if args.output:
        download_path = args.output
    else:
        download_path = '/saved'

    os.makedirs(download_path, exist_ok=True)
    print(f"Files will be saved to: {download_path}")

    # Download the playlist
    download_youtube_playlist(args.url, download_path, args.n, args.format, args.cookies)

    # Final cleanup step to remove any remaining .webm files
    for file in os.listdir(download_path):
        if file.endswith('.webm'):
            file_path = os.path.join(download_path, file)
            os.remove(file_path)
            print(f'Deleted incomplete file: {file_path}')

    print(f"Process completed. Audio files converted to {args.format.upper()}")
