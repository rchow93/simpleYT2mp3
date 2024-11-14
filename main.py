import os
import yt_dlp
import argparse

downloaded_count = 0

def download_youtube_video(video_url, download_path, n):
    def progress_hook(d):
        global downloaded_count
        if d['status'] == 'finished':
            if 'filename' in d:
                print(f'Conversion completed for: {d["filename"]}')
            downloaded_count += 1
            if downloaded_count >= n:
                raise yt_dlp.utils.DownloadError('Reached the desired number of downloads.')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download YouTube playlist videos as MP3.')
    parser.add_argument('-url', '--url', type=str, default='https://www.youtube.com/watch?v=lwAlGbRmDOU&list=PL-ntK3MOBOs5jO3Yz0HZpITxEtvvOhBNp&index=',
                        help='YouTube playlist URL')
    parser.add_argument('-n', '--n', type=int, default=None,
                        help='Number of items to download from the playlist')

    args = parser.parse_args()
    base_url = args.url
    n = args.n+1
    download_path = 'downloads'
    os.makedirs(download_path, exist_ok=True)

    try:
        if n is None:
            # Download all items in the playlist
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                playlist_info = ydl.extract_info(base_url, download=False)
                if 'entries' in playlist_info:
                    n = len(playlist_info['entries'])
                else:
                    raise ValueError('The provided URL is not a valid playlist.')

        for i in range(1, n + 1):
            video_url = f'{base_url}&index={i}'
            download_youtube_video(video_url, download_path, n)
    except yt_dlp.utils.DownloadError as e:
        print(f'Stopped downloading: {e}')
    except ValueError as e:
        print(f'Error: {e}')

    # Final cleanup step to remove any remaining .webm files
    for file in os.listdir(download_path):
        if file.endswith('.webm'):
            file_path = os.path.join(download_path, file)
            os.remove(file_path)
            print(f'Deleted incomplete file: {file_path}')

    print(f"The first {n} videos have been downloaded and converted to MP3.")

