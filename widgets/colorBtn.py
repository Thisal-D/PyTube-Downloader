import customtkinter as ctk


class ColorBtn(ctk.CTkButton):
    def __init__(self, 
                 master=None,
                 height=1,
                 width=1,
                 fg_color=None,
                 bg_color=None,
                 corner_radius=0,
                 hover=False,
                 text="",
                 font=None,
                 text_color=None,
                 border_width=0,
                 ):
        super().__init__(master=master, height=height, width=width, fg_color=fg_color,border_width=border_width,text_color=text_color,
                         bg_color=bg_color, corner_radius=corner_radius, hover=hover, text=text, font=font)
        self.height = height
        self.width = width
        self.bind("<Enter>", self.react)
        self.bind("<Leave>", self.react_back)
    
    
    def react(self, e):
        self.configure(width=self.cget("width")+4,
                       height=self.cget("height")+4)
        self.grid(pady=8, padx=2)
        
        
    def react_back(self, e):
        self.configure(width=self.cget("width")-4,
                       height=self.cget("height")-4)
        self.grid(pady=10, padx=4)
        
        
    def set_clicked(self):
        self.configure(state="disabled")
        self.unbind("<Enter>")
        self.unbind("<Leave>")
        self.set_unclicked_before_btn()
        
        
    def set_unclicked_before_btn(self):
        for widget in self.master.winfo_children():
            if type(widget) == ColorBtn and widget!=self:
                if widget.cget("width") > self.width:
                    widget.bind("<Enter>", widget.react)
                    widget.bind("<Leave>", widget.react_back)
                    widget.configure(width=self.width, height=self.height)
                    widget.grid(pady=10, padx=4)
                    widget.configure(state="normal")