import os
import threading
import webbrowser
from typing import Any, Dict
import customtkinter as ctk
from PIL import Image
from utils import (
    GitHubUtility,
    JsonUtility,
    FileUtility,
    ImageUtility,
)
from services import ThemeManager
from settings import ThemeSettings
from .contributor_profile_widget import ContributorProfileWidget


class AboutPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None):

        super().__init__(
            master=master,
            fg_color=ThemeSettings.settings["root"]["fg_color"]["normal"]
        )

        self.name_title_label = ctk.CTkLabel(
            master=self,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text="Name"
        )
        self.dash1_label = ctk.CTkLabel(
            master=self,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text=":"
        )
        self.name_label = ctk.CTkLabel(
            master=self,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text=""
        )

        self.version_title_label = ctk.CTkLabel(
            master=self,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text="Version"
        )
        self.dash2_label = ctk.CTkLabel(
            master=self,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text=":"
        )
        self.version_label = ctk.CTkLabel(
            master=self,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text=""
        )

        self.site_title_label = ctk.CTkLabel(
            master=self,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text="Site"
        )
        self.dash3_label = ctk.CTkLabel(
            master=self,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text=":"
        )
        self.site_button = ctk.CTkButton(
            master=self,
            fg_color=ThemeSettings.settings["root"]["fg_color"]["normal"],
            hover=False,
            width=1,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text=""
        )

        self.contributors_title_label = ctk.CTkLabel(
            master=self,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text="Contributors"
        )
        self.dash4_label = ctk.CTkLabel(
            master=self,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text=":"
        )
        self.contributors_status_label = ctk.CTkLabel(
            master=self,
            text_color=ThemeSettings.settings["settings_panel"]["text_color"],
            text="Loading..."
        )
        self.contributors_frame = ctk.CTkScrollableFrame(
            fg_color=ThemeSettings.settings["root"]["fg_color"]["normal"],
            master=self
        )

        self.disclaimer_label = ctk.CTkLabel(
            master=self,
            justify="left",
            text="",
            text_color=ThemeSettings.settings["settings_panel"]["warning_color"]["normal"]
        )

        self.app_info: Dict = JsonUtility.read_from_file("data\\info.json")
        self.place_widgets()
        self.configure_values()
        self.set_accent_color()
        self.bind_events()
        ThemeManager.register_widget(self)
        
    def configure_values(self):
        self.name_label.configure(text=self.app_info["name"])
        self.version_label.configure(text=self.app_info["version"])
        self.site_button.configure(text=self.app_info["site"], command=lambda: webbrowser.open(self.app_info["site"]))
        self.disclaimer_label.configure(text="•  " + self.app_info["disclaimer"])
        threading.Thread(target=self.configure_contributors_info, daemon=True).start()

    def update_contributors_info(self, contributors_data):
        # retrieve links of contributors as list[dict] -> GitHub.com
        # iterate contributors list[dict] and generate
        self.app_info["contributors"] = {}
        for i, contributor_data in enumerate(contributors_data):
            self.app_info["contributors"][i] = {
                "profile_url": contributor_data["profile_url"],
                "user_name": contributor_data["user_name"]
            }

    def configure_contributors_info(self):
        # retrieve contributors data from GitHub repo as list[dict]
        contributors_data = GitHubUtility.get_contributors_data()
        # if it success -> return Dict
        # if it fails -> return None
        if contributors_data is not None:
            # if old contributors data list length is different from new contributors data list length,
            # that means contributors data is changed
            if len(self.app_info["contributors"]) != len(contributors_data):
                # if contributors data is changed, call update_contributors_info function to update old data dict
                self.update_contributors_info(contributors_data)

        # place forget the loading label
        self.contributors_status_label.place_forget()
        # place frame for show  contributors info
        self.contributors_frame.place(x=160, y=200, relwidth=1)

        # iterate through contributors
        profile_images_directory = "assets//profile images//"
        row = 0
        for i in self.app_info["contributors"].keys():
            contributor = self.app_info["contributors"][i]
            # check if profile image saved or if not create image path
            # check profile image is already downloaded if it's not download profile image right now
            if contributor.get("profile_images_paths", None) is not None:
                profile_images_paths = contributor["profile_images_paths"]
            else:
                profile_normal_image_path = FileUtility.sanitize_filename(f"{contributor["profile_url"]}-normal.png")
                profile_normal_image_path = profile_images_directory + profile_normal_image_path

                profile_hover_image_path = FileUtility.sanitize_filename(f"{contributor["profile_url"]}-hover.png")
                profile_hover_image_path = profile_images_directory + profile_hover_image_path
                profile_images_paths = (
                    FileUtility.get_available_file_name(profile_normal_image_path),
                    FileUtility.get_available_file_name(profile_hover_image_path)
                )
                # update images path
                self.app_info["contributors"][i]["profile_images_paths"] = profile_images_paths
            
            # check if profile image is already downloaded if it's not download profile image
            if not os.path.exists(profile_images_paths[0]):
                try:
                    # download image from GitHub
                    ImageUtility.download_image(
                        image_url=f"{contributor["profile_url"]}.png",
                        output_image_path=profile_images_paths[0]
                    )
                    # add corner radius to download image
                    profile_image = Image.open(profile_images_paths[0])
                    profile_image = ImageUtility.create_image_with_rounded_corners(
                        image=profile_image,
                        radius=int(profile_image.width/2),
                    )
                    profile_image.save(profile_images_paths[0])
                    profile_image.close()
                except Exception as error:
                    print(f"about_panel.py : {error}")
            # check if  hover profile image is already generated if not generate
            if not os.path.exists(profile_images_paths[1]) and os.path.exists(profile_images_paths[0]):
                profile_image = Image.open(profile_images_paths[0])
                profile_image_hover = ImageUtility.create_image_with_rounded_corners(
                    ImageUtility.create_image_with_hover_effect(
                        image=profile_image,
                        intensity_increase=40
                    ),
                    radius=int(profile_image.width/2)
                )
                profile_image_hover.save(profile_images_paths[1])

            if os.path.exists(profile_images_paths[1]) and os.path.exists(profile_images_paths[0]):
                # create contributor
                ContributorProfileWidget(
                    master=self.contributors_frame,
                    width=35,
                    height=35,
                    user_name=contributor["user_name"],
                    profile_url=contributor["profile_url"],
                    profile_images_paths=profile_images_paths,
                ).grid(
                    row=row,
                    pady=0,
                    padx=(0, 0, 0)
                )
                row += 2

        # save info to json
        JsonUtility.write_to_file("data\\info.json", self.app_info)

    def bind_events(self):
        self.site_button.bind("<Enter>", lambda event: self.site_button.configure(
            text_color=ThemeSettings.settings["root"]["accent_color"]["hover"]))
        self.site_button.bind("<Leave>", lambda event: self.site_button.configure(
            text_color=ThemeSettings.settings["root"]["accent_color"]["normal"]))

    def set_accent_color(self):
        self.name_label.configure(text_color=ThemeSettings.settings["root"]["accent_color"]["normal"])
        self.version_label.configure(text_color=ThemeSettings.settings["root"]["accent_color"]["normal"])
        self.site_button.configure(text_color=ThemeSettings.settings["root"]["accent_color"]["normal"])

    def update_accent_color(self):
        self.set_accent_color()

    def reset_widgets_colors(self):
        ...

    def place_widgets(self):
        self.name_title_label.place(x=50, y=50)
        self.dash1_label.place(x=140, y=50)
        self.name_label.place(x=170, y=50)

        self.version_title_label.place(x=50, y=100)
        self.dash2_label.place(x=140, y=100)
        self.version_label.place(x=170, y=100)

        self.site_title_label.place(x=50, y=150)
        self.dash3_label.place(x=140, y=150)
        self.site_button.place(x=165, y=150)

        self.contributors_title_label.place(x=50, y=200)
        self.dash4_label.place(x=140, y=200)
        self.contributors_status_label.place(x=170, y=200)

        self.disclaimer_label.place(x=50, rely=1, y=-60)
