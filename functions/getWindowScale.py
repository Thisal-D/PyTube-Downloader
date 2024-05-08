import customtkinter as ctk


def get_window_scale(widget):
    return 1 / ctk.ScalingTracker.get_widget_scaling(widget)
