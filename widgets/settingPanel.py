import customtkinter as ctk
from .colorBtn import ColorBtn
from functions.saveSettings import saveSettings
from functions.getThemeSettings import getThemeSettings
from functions.getGeneralSettings import getGeneralSettings
from functions.getConvertedPath import getConvertedPath
import os

class settingPanel(ctk.CTkFrame):
    
    def __init__(self,master=None,
                 fg_color=None,
                 bg_color=None,
                 text_color=None,
                 theme_color_change_call_back=None,
                 directory_change_call_back=None):
        
        self.theme_color_change_call_back = theme_color_change_call_back
        self.theme_settings_file = "./settings/theme.json"
        self.theme_settings =  getThemeSettings()
        
        self.directory_change_call_back = directory_change_call_back
        self.general_settings_file = "./settings/general.json"
        self.general_settings =  getGeneralSettings()
        
        
        
        super().__init__(master=master, fg_color=fg_color, bg_color=bg_color)
    
        
        self.color_scheme_frame = ctk.CTkFrame(master=self, fg_color=fg_color, bg_color=bg_color, 
                                               border_width=2)
        self.color_scheme_frame.place(x=10, y=50,)   
        
        self.color_scheme_label = ctk.CTkLabel(master=self.color_scheme_frame, fg_color=fg_color, bg_color=bg_color, 
                                               font=("arial", 14, "bold"), text="Color Scheme    :    ", height=20)
        self.color_scheme_label.grid(row=0, columnspan=len(self.theme_settings["default_theme_colors"])+2, pady=10)
        
        ctk.CTkLabel(master=self.color_scheme_frame, fg_color=fg_color, bg_color=bg_color, text="").grid(row=1, column=0, padx=4)
        col_ = 1
        for app_theme_color in self.theme_settings["default_theme_colors"]:
            btn = ColorBtn(master=self.color_scheme_frame, width=30, height=30, hover=False, 
                                fg_color=app_theme_color, bg_color=fg_color, corner_radius=10, text='')
            btn.configure(command=lambda btn_=btn,color=app_theme_color,:self.save_theme_color(btn_, color))
            btn.grid(row=1, column=col_, padx=4, pady=10)
            if app_theme_color == self.theme_settings["app_theme_color"]:
                btn.react("E")
                btn.set_clicked()
                btn.set_unclicked_before_btn()
            col_ += 1
        ctk.CTkLabel(master=self.color_scheme_frame, fg_color=fg_color, bg_color=bg_color, text="").grid(row=1, column=col_, padx=4)
        
        
        
        self.theme_mode_frame = ctk.CTkFrame(master=self, fg_color=fg_color, bg_color=bg_color, 
                                        border_width=2)
        self.theme_mode_frame.place(x=420, y=50)
        self.color_mode_label = ctk.CTkLabel(master=self.theme_mode_frame, fg_color=fg_color, bg_color=bg_color, 
                                            font=("arial", 14, "bold"), text="Theme    :    ", height=20)
        self.color_mode_label.grid(row=0, columnspan=5, pady=10)
        ctk.CTkLabel(master=self.theme_mode_frame, fg_color=fg_color, bg_color=bg_color, text="").grid(row=1, column=0, padx=4)
        col_ = 1
        for theme_mode in ["System", "Dark", "Light"]:
            btn = ColorBtn(master=self.theme_mode_frame, width=60, height=30, hover=False, border_width=2, text_color=text_color,
                                fg_color=fg_color, bg_color=bg_color, corner_radius=6, text=theme_mode, font=("arial", 12, "bold"))
            btn.configure(command=lambda btn_=btn,color=theme_mode,:self.save_theme_mode(btn_, color))
            btn.grid(row=1, column=col_, padx=4, pady=10)
            if theme_mode == self.theme_settings["app_theme_mode"]:
                btn.react("E")
                btn.set_clicked()
                btn.set_unclicked_before_btn()
            col_ += 1
        ctk.CTkLabel(master=self.theme_mode_frame, fg_color=fg_color, bg_color=bg_color, text="").grid(row=1, column=4, padx=4)
        

        self.download_path_frame = ctk.CTkFrame(master=self, fg_color=fg_color, bg_color=bg_color,
                                                border_width=2)
        self.download_path_frame.place(x=10, y=200)
        
        self.download_path_label = ctk.CTkLabel(master=self.download_path_frame, fg_color=fg_color, bg_color=bg_color, width=200,
                                                font=("arial", 14, "bold"), text="Download Directory    :    ", height=40)
        self.download_path_label.grid(row=0, column=0, pady=10, padx=10)
        
        self.download_path_btn = ctk.CTkButton(master=self.download_path_frame,
                                               text="📂",
                                               font=("arial", 25, "bold"),
                                               cursor="hand2",
                                               hover=False,
                                               command=self.get_download_directory,
                                               bg_color=fg_color,
                                               fg_color=fg_color, height=40,width=40)
        self.download_path_btn.grid(row=0, column=1, pady=10, padx=10)
        self.download_path_entry = ctk.CTkEntry(master=self.download_path_frame, fg_color=fg_color, bg_color=bg_color, width=610,
                                                font=("arial", 13, "underline"), height=40)
        self.download_path_entry.insert(0, self.general_settings["download_directory"] if self.general_settings["download_directory"]!=False else f"C:\\Users\\{os.getlogin()}\\Downloads\\PyTube Downloader\\")
        self.download_path_entry.grid(row=1, columnspan=2, pady=10, padx=10)
        self.configure_theme_color()
        
 
    def save_theme_color(self,btn: ColorBtn, theme_color):
        if self.theme_settings["app_theme_color"] != theme_color:
            self.theme_settings["app_theme_color"] = theme_color
            btn.set_clicked()
            btn.set_unclicked_before_btn()
            self.theme_settings["app_theme_color"] = theme_color
            saveSettings(self.theme_settings_file,self.theme_settings)
            self.configure_theme_color() 
            self.theme_color_change_call_back(theme_color)
    
    
    def save_theme_mode(self,btn: ColorBtn, theme):
        btn.set_clicked()
        btn.set_unclicked_before_btn()
        self.theme_settings["app_theme_mode"] = theme
        saveSettings(self.theme_settings_file,self.theme_settings)
        self.configure_theme_color() 
        ctk.set_appearance_mode(theme)
                
                
    def configure_theme_color(self):
        self.color_scheme_frame.configure(border_color=self.theme_settings["app_theme_color"])
        self.color_scheme_label.configure(text_color=self.theme_settings["app_theme_color"])
        
        self.theme_mode_frame.configure(border_color=self.theme_settings["app_theme_color"])
        self.color_mode_label.configure(text_color=self.theme_settings["app_theme_color"])
        
        for btn in self.theme_mode_frame.winfo_children():
            if type(btn) == ColorBtn:
                btn.configure(border_color=self.theme_settings["app_theme_color"], text_color=self.theme_settings["app_theme_color"])
                
        self.download_path_frame.configure(border_color=self.theme_settings["app_theme_color"])
        self.download_path_label.configure(text_color=self.theme_settings["app_theme_color"])
        self.download_path_btn.configure(text_color=self.theme_settings["app_theme_color"])
        self.download_path_entry.configure(border_color=self.theme_settings["app_theme_color"], text_color=self.theme_settings["app_theme_color"])
        

    def get_download_directory(self):
        directory = ctk.filedialog.askdirectory()
        if directory != "" and self.general_settings["download_directory"] != directory:
            directory = getConvertedPath(directory)
            self.general_settings["download_directory"] = directory
            saveSettings(self.general_settings_file,self.general_settings)
            self.download_path_entry.delete(0, "end")
            self.download_path_entry.insert(0, directory)
            self.directory_change_call_back(directory)
            