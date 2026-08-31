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
import yt_dlp

def download_audio(video_url, save_path, no_playlist, split_chapters, format_choice):
    if split_chapters:
        postprocessors = [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': format_choice.lower(), 'preferredquality': '0'},
            {'key': 'FFmpegSplitChapters'}
        ]
        outtmpl = {
            'default': save_path + '/%(title)s/%(title)s.%(ext)s',
            'chapter': save_path + '/%(title)s/%(section_title)s.%(ext)s'
        }
        ydl_format = 'bestaudio[ext=m4a]/bestaudio/best'
    else:
        postprocessors = [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': format_choice.lower(), 'preferredquality': '0'}
        ]
        outtmpl = save_path +'/%(title)s.%(ext)s'
        ydl_format = 'bestaudio/best'
        
    ydl_opts = {
         'noplaylist': no_playlist,
         'format': ydl_format,
         'outtmpl': outtmpl,
         'postprocessors': postprocessors,
         'verbose': True,
         'writethumbnail': False,
         'keepvideo': False,
     }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
         ydl.download([video_url])

while True:
    yt_link = input("Paste YT link or playlist link here:\n") 
    save_path = input("Input desired file path:\n")
    format_choice = input("Choose format (mp3/m4a):\n")
    
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(yt_link, download=False)
    
    if "list=" in yt_link:
        choice = input("This is a playlist link, download all? (y/n):\n")
        if choice.lower() == 'y':
            no_playlist = False
        else:
            no_playlist = True
    else:
        no_playlist = True

    if info.get('chapters'):
        choice = input("This video has chapters, want to split it? (y/n):\n")
        if choice.lower() == 'y':
            split_chapters = True
        else:
            split_chapters = False
    else:
        split_chapters = False

    #create a loop function to continue the script otherwise give exit function
    download_audio(yt_link, save_path, no_playlist, split_chapters, format_choice)
    again = input("Want to download another? (y/n):\n")
    if again.lower() == 'n':
        break

        
    
