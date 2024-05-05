from tkinter import ttk
import customtkinter as ctk
from pytube import YouTube
import os

def download_video():
    url = enter_url.get()
    resolution = resolutions_var.get()

    progress_label.pack(pady=("10p", "5p"))
    progress_bar.pack(pady=("10p", "5p"))
    status_label.pack(pady=("10p", "5p"))


    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(res=resolution).first()
        # download into specific folder (linux)
        #after the output_path put ur downlload path
        os.path.join("~/Downloads", f"{yt.title}.mp4")
        stream.download(output_path="/home/theonlyerror/Downloads/")
        # download into specific folder (windows)
        # stream.download(output_path="C:/Users/your_user_name/Downloads")
        status_label.configure(text=f"Downloaded!", text_color="white", fg_color="green")

    except Exception as e:
        status_label.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_label.configure(text= str(int(percentage_of_completion)) + "%")
    progress_label.update()

    progress_bar.set(float(percentage_of_completion) / 100)

root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root.title("Welcome To Youtube Downloader")

#set min and max size of the window
root.geometry("720x480")
root.minsize(720, 480)
root.maxsize(1000, 720)

#create a frame
content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

url_label = ctk.CTkLabel(content_frame, text="Drop Your Video URL Here: ")
enter_url = ctk.CTkEntry(content_frame, width=400, height=40)
url_label.pack(pady=("10p", "5p"))
enter_url.pack(pady=("10p", "5p"))


#Download Button
download_button = ctk.CTkButton(content_frame, text="Download", command=download_video)
download_button.pack(pady=("10p", "5p"))

#resolution box
resolutions = ["1080p", "720p", "480p", "360p", "240p", "144p"]
resolutions_var = ctk.StringVar()
resolution_combobox = ttk.Combobox(content_frame, values=resolutions, textvar=resolutions_var)
resolution_combobox.pack(pady=("10p", "5p"))
resolution_combobox.set("720p")

#progress label
progress_label = ctk.CTkLabel(content_frame, text="0%")

#progress bar
progress_bar = ctk.CTkProgressBar(content_frame, width=400)
progress_bar.set(0)


#status label
status_label = ctk.CTkLabel(content_frame, text="")







#Copyright label
copy_right = ctk.CTkLabel(content_frame, text="© 2024 Abdallah Mousa. All Rights Reserved")
copy_right.pack(side=ctk.BOTTOM, pady=("10p", "5p"))
root.mainloop()