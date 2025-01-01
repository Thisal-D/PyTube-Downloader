from .history_object import HistoryObject
from PIL import Image
from tkinter import PhotoImage
from services import ThemeManager
from utils import ImageUtility, FileUtility


class HistoryVideo(HistoryObject):
    default_thumbnail_dark_normal: PhotoImage = None
    default_thumbnail_dark_hover: PhotoImage = None
    
    default_thumbnail_light_normal: PhotoImage = None
    default_thumbnail_light_hover: PhotoImage = None
    
    default_thumbnail_path_light = "assets\\ui images\\video-light.png"
    default_thumbnail_path_dark = "assets\\ui images\\video-dark.png"

    def __init__(self, length, **kwargs):
        self.length = length
        
        super().__init__(**kwargs)
    
    def get_default_thumbnail(self):
        if HistoryVideo.default_thumbnail_dark_normal is None:
            thumbnail_image_light = Image.open(HistoryVideo.default_thumbnail_path_light)
            thumbnail_image_dark = Image.open(HistoryVideo.default_thumbnail_path_dark)
            
            image_width = thumbnail_image_light.width
            corner_radius = int(image_width / 18)
           
            thumbnail_image_light_hover = ImageUtility.create_image_with_hover_effect(thumbnail_image_light, intensity_increase=-50)
            thumbnail_image_dark_hover = ImageUtility.create_image_with_hover_effect(thumbnail_image_dark, intensity_increase=50)
            
            thumbnail_image_light_normal = ImageUtility.create_image_with_rounded_corners(thumbnail_image_light, radius=corner_radius)
            thumbnail_image_dark_normal = ImageUtility.create_image_with_rounded_corners(thumbnail_image_dark, radius=corner_radius)
            thumbnail_image_light_hover = ImageUtility.create_image_with_rounded_corners(thumbnail_image_light_hover, radius=corner_radius)
            thumbnail_image_dark_hover = ImageUtility.create_image_with_rounded_corners(thumbnail_image_dark_hover, radius=corner_radius)
            
            thumbnail_size_for_video_history_object = (
                int(self.width) - 5,
                int((self.width/ 16*9))
            )
            thumbnail_image_light_normal = ImageUtility.resize_image(
                image=thumbnail_image_light_normal,
                new_size=thumbnail_size_for_video_history_object
            )
            thumbnail_image_dark_normal = ImageUtility.resize_image(
                image=thumbnail_image_dark_normal,
                new_size=thumbnail_size_for_video_history_object
            )
            thumbnail_image_light_hover = ImageUtility.resize_image(
                image=thumbnail_image_light_hover,
                new_size=thumbnail_size_for_video_history_object
            )
            thumbnail_image_dark_hover = ImageUtility.resize_image(
                image=thumbnail_image_dark_hover,
                new_size=thumbnail_size_for_video_history_object
            )
        
            thumbnail_image_path_light_normal = FileUtility.get_available_file_name("temp\\thumbnails\\history.png")
            thumbnail_image_light_normal.save(thumbnail_image_path_light_normal)
            
            thumbnail_image_path_dark_normal = FileUtility.get_available_file_name("temp\\thumbnails\\history.png")
            thumbnail_image_dark_normal.save(thumbnail_image_path_dark_normal)
            
            thumbnail_image_path_light_hover = FileUtility.get_available_file_name("temp\\thumbnails\\history.png")
            thumbnail_image_light_hover.save(thumbnail_image_path_light_hover)
            
            thumbnail_image_path_dark_hover = FileUtility.get_available_file_name("temp\\thumbnails\\history.png")
            thumbnail_image_dark_hover.save(thumbnail_image_path_dark_hover)
            
            HistoryVideo.default_thumbnail_dark_normal = PhotoImage(file=thumbnail_image_path_dark_normal)
            HistoryVideo.default_thumbnail_dark_hover = PhotoImage(file=thumbnail_image_path_dark_hover)
            
            HistoryVideo.default_thumbnail_light_normal = PhotoImage(file=thumbnail_image_path_light_normal)        
            HistoryVideo.default_thumbnail_light_hover = PhotoImage(file=thumbnail_image_path_light_hover)
        
        self.configure_default_thumbnails()

    def configure_default_thumbnails(self):
        if ThemeManager.current_theme_mode == "Dark":
            self.thumbnail_normal = HistoryVideo.default_thumbnail_dark_normal
            self.thumbnail_hover = HistoryVideo.default_thumbnail_dark_hover
        else:
            self.thumbnail_normal = HistoryVideo.default_thumbnail_light_normal
            self.thumbnail_hover = HistoryVideo.default_thumbnail_light_hover
        
        self.thumbnail_button.configure(image=self.thumbnail_normal)