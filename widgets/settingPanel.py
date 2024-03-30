from typing import Any, Tuple
import customtkinter as ctk
from .colorBtn import ColorBtn
from functions.saveSettings import saveSettings
import json

class settingPanel(ctk.CTkFrame):
    
    def __init__(self,master=None,
                 fg_color=None,
                 bg_color=None,
                 text_color=None,
                 theme_color=None,
                 app_theme_colors=[],
                 call_back=None):
        
        self.call_back = call_back
        self.theme_color = theme_color
        super().__init__(master=master, fg_color=fg_color, bg_color=bg_color)
        
        
        self.color_scheme_frame = ctk.CTkFrame(master=self, fg_color=fg_color, bg_color=bg_color, 
                                               border_width=2, width=500, height=50)
        self.color_scheme_frame.place(x=10, y=50)
        
        self.color_scheme_label = ctk.CTkLabel(master=self.color_scheme_frame, fg_color=fg_color, bg_color=bg_color, 
                                               font=("arial", 14, "bold"), text="Color Scheme    :   ")
        self.color_scheme_label.place(y=12, x=10)
        
        x_ = 150
        for app_theme_color in app_theme_colors:
            btn = ColorBtn(master=self.color_scheme_frame, width=30, height=30, hover=False, 
                                fg_color=app_theme_color, bg_color=fg_color, corner_radius=10, text='')
            btn.configure(command=lambda btn_=btn,color=app_theme_color,:self.save_theme_color(btn_,color))
            btn.place(y=10,x=x_)
            if app_theme_color == theme_color:
                btn.react("E")
                btn.set_clicked()
                btn.set_unclicked_before_btn()
            x_+=34

        self.configure_theme_color()

            
    def save_theme_color(self,btn: ColorBtn, theme_color):
        if self.theme_color != theme_color:
            self.theme_color = theme_color
            btn.set_clicked()
            btn.set_unclicked_before_btn()
            file = "./settings/theme.json";
            theme_settings = json.loads(open(file, "r").read())
            theme_settings["app_theme_color"] = theme_color
            saveSettings(file,theme_settings)
            self.configure_theme_color()
            
            self.call_back(theme_color)
        
        
    def configure_theme_color(self):
        self.color_scheme_frame.configure(border_color=self.theme_color)
        self.color_scheme_label.configure(text_color=self.theme_color)