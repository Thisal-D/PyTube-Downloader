import customtkinter as ctk

def getWindowScale(widget):
    return 1/ctk.ScalingTracker.get_widget_scaling(widget)