import os
import subprocess
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from pytube import YouTube, Playlist
import threading

# Global variables
downloading = False
yt = None

def download_video():
    global downloading, yt
    if downloading:
        return  # Return if download is already in progress

    url = enter_url.get()
    resolution = resolutions_var.get()

    def download_process():
        global downloading, yt
        downloading = True
        status_label.pack(pady=("10p", "5p"))
        stop_download_button.pack(pady=("10p", "5p"))

        try:
            download_playlist(url, resolution) if 'playlist' in url.lower() else download_single_video(url, resolution)
            print("Download process completed.")
        except Exception as e:
            status_label.configure(text=f"Error: {str(e)}", text_color="white", fg_color="red")

        downloading = False

    threading.Thread(target=download_process).start()

def download_playlist(url, resolution):
    pl = Playlist(url)
    output_path = os.path.join("/home/theonlyerror/Downloads/", "playlist_videos")
    os.makedirs(output_path, exist_ok=True)
    print(f"Downloading playlist with {len(pl.video_urls)} videos...")
    for i, video_url in enumerate(pl.video_urls):
        if not downloading:  # Check if stop button pressed
            break

        download_single_video_helper(video_url, resolution, output_path, i, len(pl.video_urls))

    print("Playlist download complete.")

def download_single_video(url, resolution):
    output_path = os.path.join("/home/theonlyerror/Downloads/", "single_video")
    os.makedirs(output_path, exist_ok=True)
    download_single_video_helper(url, resolution, output_path)

def download_single_video_helper(video_url, resolution, output_path, i=None, total=None):
    global yt

    yt = YouTube(video_url, on_progress_callback=on_progress)
    stream = yt.streams.filter(res=resolution, progressive=True).first()

    if stream:
        video_path = stream.download(output_path=output_path)
        audio_codec = "Unknown"  # Placeholder for audio codec
        if i is not None and total is not None:
            status_label.configure(text=f"Downloaded {i + 1} / {total} videos! Audio Codec: {audio_codec}", text_color="white", fg_color="green")
        else:
            status_label.configure(text=f"Downloaded! Audio Codec: {audio_codec}", text_color="white", fg_color="green")
    else:
        status_label.configure(text=f"No stream found for resolution {resolution}", text_color="white", fg_color="red")

def stop_download():
    global downloading, yt
    downloading = False
    if yt:
        yt.streams.first().download(cancel=True)
    status_label.configure(text="Download Stopped", text_color="white", fg_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = (bytes_downloaded / total_size) * 100
    progress_bar.set(int(percentage_of_completion))
    progress_label.configure(text=f"{int(percentage_of_completion)}%")

root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root.title("Welcome To Youtube Downloader")
root.geometry("720x480")
root.minsize(720, 480)
root.maxsize(1000, 720)

content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

url_label = ctk.CTkLabel(content_frame, text="Drop Your Video URL Here: ")
enter_url = ctk.CTkEntry(content_frame, width=400, height=40)
url_label.pack(pady=("10p", "5p"))
enter_url.pack(pady=("10p", "5p"))

download_button = ctk.CTkButton(content_frame, text="Download", command=download_video)
download_button.pack(pady=("10p", "5p"))

stop_download_button = ctk.CTkButton(content_frame, text="Stop Download", command=stop_download)
stop_download_button.pack(pady=("10p", "5p"))

resolutions = ["720p", "360p"]
resolutions_var = ctk.StringVar()
resolution_combobox = ttk.Combobox(content_frame, values=resolutions, textvar=resolutions_var)
resolution_combobox.pack(pady=("10p", "5p"))
resolution_combobox.set("720p")

progress_label = ctk.CTkLabel(content_frame, text="0%")
progress_bar = ctk.CTkProgressBar(content_frame, width=400)
progress_bar.set(0)

status_label = ctk.CTkLabel(content_frame, text="")

copy_right = ctk.CTkLabel(content_frame, text="© 2024 Abdallah Mousa. All Rights Reserved")
copy_right.pack(side=ctk.BOTTOM, pady=("10p", "5p"))

root.mainloop()