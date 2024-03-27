import customtkinter as ctk
import tkinter

class customBtn(ctk.CTkButton):
    def __init__(self ,text ,image_normal ,image_hover ,image_clicked ,**kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.image_normal = tkinter.PhotoImage(file=image_normal)
        self.image_hover = tkinter.PhotoImage(file=image_hover)
        self.image_clicked = tkinter.PhotoImage(file=image_clicked)
        self.set_normal()
        
    def set_normal(self):
        self.configure(state="normal")
        self.configure(image=self.image_normal ,text=self.text)
    
        def _button_normal(e):
            self.configure(image=self.image_normal ,text=self.text)
            
        def _button_hover(e):
            self.configure(image=self.image_hover ,text=self.text)
        self.bind("<Enter>" ,_button_hover)
        self.bind("<Leave>" ,_button_normal)
            
    def set_clicked(self):
        self.configure(state="disabled")
        self.configure(image=self.image_clicked ,text=self.text)
        
        def _button_normal(e):
            self.configure(image=self.image_clicked ,text=self.text)
        def _button_hover(e):
            self.configure(image=self.image_clicked ,text=self.text)
        self.bind("<Enter>" ,_button_hover)
        self.bind("<Leave>" ,_button_normal)