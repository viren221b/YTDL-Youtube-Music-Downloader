#!/usr/bin/env python3

#pseudo code:
# 1. Paste URL
# 2. Convert URL to mp3
# 3. Option for file directory
# 4. Save mp3 or m4a to file path
#
# Additional Features (Done):
# 1. Playlist wide download (yt_dlp allows that
# so i'll prolly just tweak the main code)
# 2. Prompt user of playlist link (give
# user the option to cancel or continue)
#
# Additional Features pt.2(WIP):
# 1. Add loading bars for processes that doesn't have
# logs.
# 2. Add prompt for user errors like non-existent
# directories.


#MAIN

# ruff: noqa: I001
import itertools
import sys
import os
import threading
import time
import yt_dlp

def spinner(stop_event, message="Fetching info"):
    for char in itertools.cycle('|/-\\'):
        if stop_event.is_set():
            break
        sys.stdout.write(f'\r{message}... {char}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r                        \r')
    sys.stdout.flush()

def download_audio(video_url, save_path, no_playlist, split_chapters, format_choice):
    if split_chapters:
        postprocessors = [
            #ffmpeg extract audio, split and preffered codec for download
            {'key': 'FFmpegExtractAudio', 'preferredcodec': format_choice.lower(), 'preferredquality': '0'},
            {'key': 'FFmpegSplitChapters'}
        ]
        outtmpl = {
            #Save path for default download and split download
            'default': save_path + '/%(title)s/%(title)s.%(ext)s',
            'chapter': save_path + '/%(title)s/%(section_title)s.%(ext)s'
        }
        #audio format
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
    yt_link = input("\nPaste YT link or playlist link here:\n")

    while True:
        save_path = input("\nInput desired file path:\n")
        if os.path.exists(save_path):
            break
        create = input("\nFile path doesn't exist, create it? (y/n):\n")
        if create.lower() in ('y', ''):
            os.makedirs(save_path)
            break

    format_choice = input("\nChoose format (mp3/m4a):\n")

    stop = threading.Event()
    t = threading.Thread(target=spinner, args=(stop,))
    t.start()

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(yt_link, download=False)
    except yt_dlp.utils.DownloadError:
        print("\ninvalid or unsupported URL, please try again.\n")
        continue
    finally:
        stop.set()
        t.join()

    if "list=" in yt_link:
        choice = input("\nThis is a playlist link, download all? (y/n):\n")
        if choice.lower() in ('y', ''):
            no_playlist = False
        else:
            no_playlist = True
    else:
        no_playlist = True

    if info.get('chapters'):
        choice = input("\nThis video has chapters, want to split it? (y/n):\n")
        if choice.lower() in ('y', ''):
            split_chapters = True
        else:
            split_chapters = False
    else:
        split_chapters = False

    #create a loop function to continue the script otherwise give exit function
    download_audio(yt_link, save_path, no_playlist, split_chapters, format_choice)
    again = input("\nWant to download another? (y/n):\n")
    if again.lower() == 'n':
        break