import customtkinter as ctk


class ColorBtn(ctk.CTkButton):
    def __init__(self, 
                 master,
                 height,
                 width,
                 fg_color,
                 bg_color,
                 corner_radius,
                 hover,
                 text,
               
                 ):
        super().__init__(master=master, height=height, width=width, fg_color=fg_color,
                         bg_color=bg_color, corner_radius=corner_radius, hover=hover, text=text,
                        )
        
        self.bind("<Enter>", self.react)
        self.bind("<Leave>", self.react_back)
    
    
    def react(self, e):
        self.configure(width=self.cget("width")+4,
                       height=self.cget("height")+4)
        self.place(x=int(self.place_info()["x"])-2,
                   y=int(self.place_info()["y"])-2,)
        
        
    def react_back(self, e):
        self.configure(width=self.cget("width")-4,
                       height=self.cget("height")-4)
        self.place(x=int(self.place_info()["x"])+2,
                   y=int(self.place_info()["y"])+2,)
        
        
    def set_clicked(self):
        self.configure(state="disabled")
        self.unbind("<Enter>")
        self.unbind("<Leave>")
        self.set_unclicked_before_btn()
        
        
    def set_unclicked_before_btn(self):
        for widget in self.master.winfo_children():
            if type(widget) == ColorBtn and widget!=self:
                if widget.cget("width") > 30:
                    widget.bind("<Enter>", widget.react)
                    widget.bind("<Leave>", widget.react_back)
                    widget.configure(width=30, height=30)
                    widget.place(y=int(widget.place_info()["y"])+2, x=int(widget.place_info()["x"])+2)
                    widget.configure(state="normal")