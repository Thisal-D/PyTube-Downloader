from .Video import Video
import customtkinter as ctk
import tkinter as tk
import pytube
import threading
import time
from pytube import request as pytube_request
from functions.passIt import passIt
from functions.getConvertedSize import getConvertedSize
from functions.getValidFileName import getValidFileName

class downloadingVideo(Video):
    def __init__(self, master,
                 border_width=None,
                 border_color=None,
                 bg_color=None,
                 fg_color=None,
                 height=None,
                 text_color=None,
                 download_quality=None,
                 download_type=None,
                 title=None,
                 channel=None,
                 thumbnails=(None,None),
                 loading_done = True,
                 video_stream_data: pytube.StreamQuery = None,
                 url=None):
        
        self.download_running = True
        self.download_failed = False
        self.download_completed = False
        self.download_pause_req = False
 
        self.download_quality = download_quality
        self.download_type = download_type
        self.video_stream_data = video_stream_data
        super().__init__(master=master, border_width=border_width, border_color=border_color,
                         fg_color=fg_color, bg_color=bg_color, height=height ,url=url, text_color=text_color,
                         thumbnails=thumbnails, title=title, channel=channel, loading_done=loading_done)
        self.set_state()
        threading.Thread(target=self.download_video).start()
        
        
    def create_widgets(self):
        super().create_widgets()
        
        self.info_frame = ctk.CTkFrame(self ,height=25, bg_color=self.bg_color, fg_color=self.fg_color)
    
    
        self.download_progress_bar = ctk.CTkProgressBar(master=self.info_frame,
                                                      bg_color=self.bg_color,
                                                      width=(self.master.cget("width")-200)/2,
                                                      height=8)
             
        
        self.download_progress_label = ctk.CTkLabel(master=self.info_frame,
                                                     text="",
                                                     font=("arial", 12, "bold"),
                                                     bg_color=self.bg_color,
                                                     fg_color=self.fg_color,
                                                     text_color=self.text_color)

        
        self.download_percentage_label = ctk.CTkLabel(master=self.info_frame,
                                                    text="0.0 %",
                                                    font=("arial", 12, "bold"),
                                                    bg_color=self.bg_color,
                                                    fg_color=self.fg_color,
                                                    text_color=self.text_color)
        
        self.quality_label = ctk.CTkLabel(master=self.info_frame,
                                            text="",
                                            font=("arial", 12, "bold"),
                                            bg_color=self.bg_color,
                                            fg_color=self.fg_color,
                                            text_color=self.text_color)
        
        self.net_speed_label = ctk.CTkLabel(master=self.info_frame,
                                                     text="0.0 B/s",
                                                     font=("arial", 12, "bold"),
                                                     bg_color=self.bg_color,
                                                     fg_color=self.fg_color,
                                                     text_color=self.text_color)
        
        
        self.pause_button_img_normal = tk.PhotoImage(file="./imgs/pause/normal.png")
        self.pause_button_img_hover = tk.PhotoImage(file="./imgs/pause/hover.png")
        self.resume_button_img_normal = tk.PhotoImage(file="./imgs/resume/normal.png")
        self.resume_button_img_hover = tk.PhotoImage(file="./imgs/resume/hover.png")
        self.pause_resume_button = ctk.CTkButton(self ,text="",
                                                image = self.pause_button_img_normal,
                                                width=15 ,height=15,
                                                command = self.pause_downloading,
                                                fg_color=self.fg_color,
                                                bg_color=self.bg_color,
                                                hover_color=self.fg_color)
        self.set_pause_btn()
        
    
    def place_widgets(self):
        self.thumbnail_btn.place(x=5, y=2, relheight=1, height=-4, width=int((self.height-4)/9*16))
        self.title_label.place(x=130, y=4, height=20, relwidth=0.5, width=-150)
        self.channel_label.place(x=130, y=24, height=20, relwidth=0.5, width=-150)
        self.url_label.place(x=130, y=44, height=20, relwidth=0.5, width=-150)
        self.pause_resume_button.place(y=25, relx=1, x=-80)
        self.info_frame.place(relx=0.5, relwidth=0.5, width=-100, y=2, relheight=1, height=-4)
        
        self.download_progress_label.place(relx=0.25, height=20, anchor="n", y=4)
        self.download_percentage_label.place(relx=0.75, height=20, anchor="n", y=4)
        self.download_progress_bar.place(relwidth=1, y=30)
        #self.download_progress_bar.configure(width=self.winfo_width())
        self.quality_label.place(relx=0.25, height=20, anchor="n", y=40)
        self.net_speed_label.place(relx=0.75, height=20, anchor="n", y=40)

    
    def configure_widget_sizes(self, e):
        self.remove_btn.place(x=self.winfo_width()-34,y=2)
        
        
    def set_state(self):
        self.thumbnail_btn.configure(state="normal")
        self.channel_label.configure(state="normal")
        
        
    def download_video(self):
        self.downloaded_bytes = 0
        self.download_file_name = self.channel + " - " + self.title
        try:
            if self.download_type == "video":
                stream = self.video_stream_data.get_by_resolution(self.download_quality)
                self.quality_label.configure(text="Video : "+self.download_quality)
                self.download_file_name += ".mp4"
            else:
                stream = self.video_stream_data.get_audio_only()
                self.quality_label.configure(text="Audio : "+self.download_quality)
                self.download_file_name += ".mp3"
            self.total_bytes = stream.filesize
            self.converted_total_bytes = getConvertedSize(self.total_bytes,2)
            self.download_file_name = getValidFileName(self.download_file_name)
            self.set_download_progress()
        except Exception as error:
            print("Download load :",error)
            
        try:
            with open(self.download_file_name,"wb") as self.video_file :
                stream =  pytube_request.stream(stream.url)
                count = 0
                while 1:
                    time_s = time.time()
                    if self.download_pause_req:
                        if count == 0:
                            self.pause_resume_button.configure(command=self.resume_downloading)
                            self.set_resume_btn()
                            count = 1
                        time.sleep(0.2)
                        continue
                    count = 0
                    chunk = next(stream, None)
                    time_e = time.time()
                    if chunk:
                        self.video_file.write(chunk)
                        self.net_speed_label.configure(text=getConvertedSize(((self.downloaded_bytes + len(chunk)) - self.downloaded_bytes)/(time_e-time_s),1)+"/s")
                        self.downloaded_bytes += len(chunk)
                        self.set_download_progress()
                    else:
                        self.download_completed()
                        break
        except Exception as error:
            print("Downloading :",error)

    
    def set_resume_btn(self):
        self.pause_resume_button.configure(image=self.resume_button_img_normal)
        def pause_resume_btn_enter(e):
            self.pause_resume_button.configure(image=self.resume_button_img_hover)
        def pause_resume_btn_leave(e):
            self.pause_resume_button.configure(image=self.resume_button_img_normal)
        self.pause_resume_button.bind("<Enter>", pause_resume_btn_enter)
        self.pause_resume_button.bind("<Leave>", pause_resume_btn_leave)
        

    def set_pause_btn(self):
        self.pause_resume_button.configure(image=self.pause_button_img_normal)
        def pause_resume_btn_enter(e):
            self.pause_resume_button.configure(image=self.pause_button_img_hover)
        def pause_resume_btn_leave(e):
            self.pause_resume_button.configure(image=self.pause_button_img_normal)
        self.pause_resume_button.bind("<Enter>", pause_resume_btn_enter)
        self.pause_resume_button.bind("<Leave>", pause_resume_btn_leave)
    
    
    def pause_downloading(self):
        self.pause_resume_button.configure(command=passIt)
        self.download_pause_req = True
    
    
    def resume_downloading(self):
        self.pause_resume_button.configure(command=self.pause_downloading)
        self.download_pause_req = False
        self.set_pause_btn()
        
    
    def set_download_progress(self):
        percentage = self.downloaded_bytes/self.total_bytes
        self.download_progress_bar.set(percentage)
        self.download_percentage_label.configure(text=str(round(percentage*100,2))+" %")
        self.download_progress_label.configure(text=f"{getConvertedSize(self.downloaded_bytes,2)} / {self.converted_total_bytes}")