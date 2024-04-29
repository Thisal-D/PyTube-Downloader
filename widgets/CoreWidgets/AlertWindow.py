import customtkinter as ctk
from PIL import Image
from services import ThemeManager


class AlertWindow(ctk.CTk):
    def __init__(
            self,
            error_msg: str = "Something went wrong,,.!",
            button_text: str = "ok"):

        super().__init__(fg_color=ThemeManager.theme_settings["alert_window"]["fg_color"]["normal"])
        self.minsize(450, 130)
        self.maxsize(450, 130)
        self.resizable(False, False)
        self.geometry(f"{450}x{120}+{int(self.winfo_screenwidth()/2-225)}+{int(self.winfo_screenheight()/2-60)}")
        
        self.info_image = ctk.CTkImage(Image.open("src\\info.png"), size=(60, 60))
        self.iconbitmap("src\\icon.ico")
        self.title("PytubeDownloader : Something went wrong..!")

        self.info_image_label = ctk.CTkLabel(
            master=self,
            text="",
            image=self.info_image
        )
        self.info_image_label.pack(side="left", fill="y", padx=(30, 10))
        
        self.error_msg_label = ctk.CTkLabel(
            master=self,
            text=error_msg,
            text_color=ThemeManager.theme_settings["alert_window"]["msg_color"]["normal"],
            font=("Arial", 13, "bold")
        )
        self.error_msg_label.pack(pady=(20, 15), padx=(0, 30))

        self.button = ctk.CTkButton(
            border_width=2,
            border_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            master=self,
            hover_color=ThemeManager.theme_settings["root"]["accent_color"]["hover"],
            command=self.close_error_window,
            text=button_text,
            fg_color=ThemeManager.theme_settings["root"]["accent_color"]["normal"],
            width=120
        )
        self.button.pack(side="right",  padx=40)
        
    def show(self):
        self.mainloop()

    def close_error_window(self):
        self.destroy()
