# simpleYT2mp3
Simple YouTube App that will download a YouTube Video (or Playlist) and extract it into mp3 audio files.

The inspiration to the App was to be able to download a YouTube video and extract it to a mp3 file to load onto a device for listening to while traveling where there was limited Internet connections. For those long trips, I could listen to the technical videos and keep up to date on the technical discussions where Video was not as important.

Note - this could be used to extract any Youtube Video to mp3 and this includes music tracks that are copyrighted. All Rights are Reserved and you should consider the legal implications of extracting audio from artists. We should support our artistic music artists.

Usage:
python3 main.py --url "https://www.youtube.com/watch?v=JGwWNGJdvx8&list=PLMC9KNkIncKvYin_USF1qoJQnIyMAfRxl" -n 2

The application takes two switches:
--url or -url = this is the url of the YouTube Playlist. if none is provided then it will default to the playlist in the example above.
--n or -n = this is the number of items from the playlist to extract, if none is provided then it will extract every item from the playlist.
 
