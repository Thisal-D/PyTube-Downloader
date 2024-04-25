import tkinter as tk


def validate_color(color: str):
    try:
        normal, hover = color.split(",")
        try:
            tk.Button(fg=normal, bg=hover)
            return True
        except Exception as error:
            print(f"@1 > validateColor.py : {error}")
            return False
    except Exception as error:
        print(f"@2 > validateColor.py : {error}")
        return False
