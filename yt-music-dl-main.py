#!/usr/bin/env python3


#pseudo code:
# 1. Paste URL
# 2. Convert URL to mp3
# 3. Option for file directory
# 4. Save mp3 or m4a to file path
# 
# Additional Features (WIP):
# 1. Playlist wide download (yt_dlp allows that
# so i'll prolly just tweak the main code)
# 2. Prompt user of playlist link (give
# user the option to cancel or continue)


#MAIN

def download_audio(video_url, save_path, no_playlist):
    import yt_dlp
    ydl_opts = {
         'noplaylist': no_playlist,
         'format': 'bestaudio/best',
         'outtmpl': save_path + '/%(title)s.%(ext)s',  # Save path and file name
         'postprocessors': [{  # Post-process to convert to MP3
             'key': 'FFmpegExtractAudio',
             'preferredcodec': 'mp3',  # Convert to mp3
             'preferredquality': '0',  # '0' means best quality, auto-determined by source
         }]
     }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
         ydl.download([video_url])

while True:
    yt_link = input("Paste YT link or playlist link here:\n") 
    save_path = input("Input desired file path:\n")

    if "list=" in yt_link:
        choice = input("This is a playlist link, download all? (y/n):\n")
        if choice.lower() == 'y':
            no_playlist = False
        else:
            no_playlist = True
    else:
        no_playlist = True

    download_audio(yt_link, save_path, no_playlist)
    again = input("Want to download another? (y/n):\n")
    if again.lower() == 'n':
        break




#create a loop function to continue the script otherwise give exit function
        
    


