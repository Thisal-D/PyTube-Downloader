from .Video import Video
import customtkinter as ctk
import pytube
import threading
import time
from pytube import request as pytube_request
from functions.passIt import passIt
from functions.getConvertedSize import getConvertedSize
from functions.getValidFileName import getValidFileName
from functions.removeInvalidCharts import removeInvalidChars
from functions.createDownloadDirectory import createDownloadDirectory


class downloadingVideo(Video):
    def __init__(self, master,
                 border_width=None,
                 width=None,
                 height=None,
                 download_quality=None,
                 download_type=None,
                 title=None,
                 channel=None,
                 thumbnails=(None,None),
                 loading_done = True,
                 video_stream_data: pytube.StreamQuery = None,
                 url=None,
                 channel_url=None,
                 
                 bg_color=None,
                 fg_color=None,
                 text_color=None,
                 theme_color=None,
                 hover_color=None,
                 special_color=None,
                 
                 downloaded_callback_function=None,
                 download_directory = ""):
        
        self.download_pause_req = False
        self.downloaded_callback_function = downloaded_callback_function
        self.download_quality = download_quality
        self.download_type = download_type
        self.video_stream_data = video_stream_data
        self.download_directory = download_directory
        super().__init__(master=master, border_width=border_width, theme_color=theme_color,hover_color=hover_color,
                         channel_url=channel_url, width=width,
                         fg_color=fg_color, bg_color=bg_color, height=height ,url=url, text_color=text_color,
                         thumbnails=thumbnails, title=title, channel=channel, loading_done=loading_done, special_color=special_color)
        self.set_state()
        threading.Thread(target=self.redownload_video).start()
        
        
    def create_widgets(self):
        super().create_widgets()
        
        self.info_frame = ctk.CTkFrame(self, height=self.height-4, bg_color=self.fg_color, fg_color=self.fg_color)
    
        self.download_progress_bar = ctk.CTkProgressBar(master=self.info_frame,
                                                        bg_color=self.fg_color,
                                                        height=8)
             
        self.download_progress_label = ctk.CTkLabel(master=self.info_frame,
                                                    text="",
                                                    font=("arial", 12, "bold"),
                                                    bg_color=self.fg_color,
                                                    fg_color=self.fg_color,
                                                    text_color=self.text_color)
        
        self.download_percentage_label = ctk.CTkLabel(master=self.info_frame,
                                                      text="",
                                                      font=("arial", 12, "bold"),
                                                      bg_color=self.fg_color,
                                                      fg_color=self.fg_color,
                                                      text_color=self.text_color)
        
        self.download_type_label = ctk.CTkLabel(master=self.info_frame,
                                          text="",
                                          font=("arial", 12, "normal"),
                                          bg_color=self.fg_color,
                                          fg_color=self.fg_color,
                                          text_color=self.text_color)
        
        self.net_speed_label = ctk.CTkLabel(master=self.info_frame,
                                            text="",
                                            font=("arial", 12, "normal"),
                                            bg_color=self.fg_color,
                                            fg_color=self.fg_color,
                                            text_color=self.text_color)
        
        self.status_label = ctk.CTkLabel(master=self.info_frame,
                                         text="",
                                         font=("arial", 12, "bold"),
                                         bg_color=self.fg_color,
                                         fg_color=self.fg_color,
                                         )
        
        self.redownload_btn = ctk.CTkButton(self ,text="⟳", 
                                            width=15 ,height=15,
                                            font=("arial", 20,"normal"),
                                            command = self.redownload_video,
                                            fg_color=self.fg_color,
                                            bg_color=self.fg_color,
                                            hover=False,
                                            )
        #  ⏯ ↺ ↻ ⏵ ⏸ ▷
        self.pause_resume_button = ctk.CTkButton(self ,text="⏸", 
                                                 width=15 ,height=15,
                                                 font=("arial", 20,"normal"),
                                                 command = self.pause_downloading,
                                                 fg_color=self.fg_color,
                                                 bg_color=self.fg_color,
                                                 hover=False,
                                                 )
        
    
    def place_widgets(self):
        self.thumbnail_btn.place(x=5, y=2, relheight=1, height=-4, width=int((self.height-4)/9*16))
        self.title_label.place(x=130, y=4, height=20, relwidth=0.5, width=-150)
        self.channel_label.place(x=130, y=24, height=20, relwidth=0.5, width=-150)
        self.url_label.place(x=130, y=44, height=20, relwidth=0.5, width=-150)
        
        self.pause_resume_button.place(y=22, relx=1, x=-80)
        self.info_frame.place(relx=0.5, y=2)
        
        self.download_progress_label.place(relx=0.25, anchor="n", y=4)
        self.download_progress_label.configure(height=20)
        self.download_percentage_label.place(relx=0.75, anchor="n", y=4)
        self.download_percentage_label.configure(height=20)
        self.download_progress_bar.place(relwidth=1, y=30)
        self.download_type_label.place(relx=0.115, anchor="n", y=40)
        self.download_type_label.configure(height=20)
        self.net_speed_label.place(relx=0.445, anchor="n", y=40)
        self.net_speed_label.configure(height=20)
        self.status_label.place(relx=0.775, anchor="n", y=40)
        self.status_label.configure(height=20)
        

    def set_theme(self):
        super().set_theme()
        self.download_progress_bar.configure(progress_color=self.theme_color)
        self.status_label.configure(text_color=self.theme_color)
        self.redownload_btn.configure(text_color=self.theme_color)
        self.pause_resume_button.configure(text_color=self.theme_color)
        
    def redownload_video(self):
        self.set_pause_btn()
        self.redownload_btn.place_forget()
        self.pause_resume_button.place(y=22, relx=1, x=-80)
        self.net_speed_label.configure(text="0.0 B/s")
        self.download_progress_bar.set(0)
        self.download_percentage_label.configure(text="0.0 %")
        self.status_label.configure(text="Downloading", text_color=self.theme_color)
        threading.Thread(target=self.download_video).start()
    
    
    def set_redownload(self):
        self.pause_resume_button.place_forget()
        self.redownload_btn.place(y=22, relx=1, x=-80)
    
    
    def configure_widget_sizes(self, e):
        self.remove_btn.place(x=self.winfo_width()-24,y=4)
        self.info_frame.configure(width=self.winfo_width()/2-100)
        
    def set_state(self):
        self.thumbnail_btn.configure(state="normal")
        self.channel_label.configure(state="normal")
    
    def set_status(self, status):
        if status=="Failed":
            self.status_label.configure(text_color=self.special_color)
        self.status_label.configure(text=status)
        
        
    def download_video(self):
        try:
            createDownloadDirectory(self.download_directory)
        except BufferError:
            pass
        
        self.downloaded_bytes = 0
        self.download_file_name = self.download_directory + "\\" + removeInvalidChars(self.channel + " - " + self.title)
        try:
            self.download_type_label.configure(text=self.download_type + " : "+self.download_quality)
            if self.download_type == "Video":
                stream = self.video_stream_data.get_by_resolution(self.download_quality)
                self.download_file_name += ".mp4"
            else:
                stream = self.video_stream_data.get_audio_only()
                self.download_file_name += ".mp3"
            self.total_bytes = stream.filesize
            self.converted_total_bytes = getConvertedSize(self.total_bytes,2)
            self.download_file_name = getValidFileName(self.download_file_name)
            self.set_download_progress()
        except Exception as error:
            self.set_redownload()
            self.set_status("Failed")
        
        print(self.download_file_name)
        try:
            with open(self.download_file_name,"wb") as self.video_file :
                stream =  pytube_request.stream(stream.url)
                count = 0
                while 1:
                    try:
                        time_s = time.time()
                        if self.download_pause_req:
                            if count == 0:
                                self.pause_resume_button.configure(command=self.resume_downloading)
                                self.set_status("Paused")
                                self.set_resume_btn()
                                count = 1
                            time.sleep(0.3)
                            continue
                        self.pause_resume_button.configure(command=self.pause_downloading)
                        count = 0
                        chunk = next(stream, None)
                        time_e = time.time()
                        if chunk:
                            self.video_file.write(chunk)
                            self.net_speed_label.configure(text=getConvertedSize(((self.downloaded_bytes + len(chunk)) - self.downloaded_bytes)/(time_e-time_s),1)+"/s")
                            self.downloaded_bytes += len(chunk)
                            self.set_download_progress()
                        else:
                            if self.downloaded_bytes == self.total_bytes:
                                self.set_status("Downloaded")
                                try:
                                    self.downloaded_callback_function(self)
                                    self.kill()
                                except Exception as error:
                                    print(error)
                                break
                            else:
                                self.set_redownload()
                                self.set_status("Failed")
                                break
                    except Exception as error:
                        self.set_redownload()
                        self.set_status("Failed")
                        break
        except Exception as error:
            self.set_redownload()
            self.set_status("Failed")


    def set_resume_btn(self):
        #  ⏯ ↺ ↻ ⏵ ⏸ ▷
        self.pause_resume_button.configure(text="▷")


    def set_pause_btn(self):
        #  ⏯ ↺ ↻ ⏵ ⏸ ▷
        self.pause_resume_button.configure(text="⏸")
        

    def pause_downloading(self):
        self.pause_resume_button.configure(command=passIt)
        self.set_status("Pausing")
        self.download_pause_req = True
        
    
    def resume_downloading(self):
        self.pause_resume_button.configure(command=passIt)
        self.set_status("Downloading")
        self.download_pause_req = False
        self.set_pause_btn()
        
    
    def set_download_progress(self):
        percentage = self.downloaded_bytes/self.total_bytes
        self.download_progress_bar.set(percentage)
        self.download_percentage_label.configure(text=str(round(percentage*100,2))+" %")
        self.download_progress_label.configure(text=f"{getConvertedSize(self.downloaded_bytes,2)} / {self.converted_total_bytes}")
        
        
    def download_done(self):
        self.downloaded_callback_function(self)
        
        
    