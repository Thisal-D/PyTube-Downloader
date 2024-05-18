import os
import threading
import webbrowser
from typing import Any, Dict
import random
import customtkinter as ctk
from PIL import Image
from utils import (
    GitHubUtility,
    JsonUtility,
    FileUtility,
    ImageUtility,
)
from services import ThemeManager, LanguageManager
from settings import (
    AppearanceSettings,
)
from .contributor_profile_widget import ContributorProfileWidget


class AboutPanel(ctk.CTkFrame):
    def __init__(
            self,
            master: Any = None):

        super().__init__(
            master=master,
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"]
        )

        self.name_title_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text="Name"
        )
        self.dash1_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text=":"
        )
        self.name_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text=""
        )

        self.version_title_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text="Version"
        )
        self.dash2_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text=":"
        )
        self.version_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text=""
        )

        self.site_title_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text="Site"
        )
        self.dash3_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text=":"
        )
        self.site_button = ctk.CTkButton(
            master=self,
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            hover=False,
            anchor="w",
            corner_radius=0,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text=""
        )

        self.contributors_title_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text="Contributors"
        )
        self.dash4_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text=":"
        )
        self.contributors_status_label = ctk.CTkLabel(
            master=self,
            text_color=AppearanceSettings.settings["settings_panel"]["text_color"],
            text="Loading..."
        )
        self.contributors_frame = ctk.CTkScrollableFrame(
            scrollbar_fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            fg_color=AppearanceSettings.settings["root"]["fg_color"]["normal"],
            master=self
        )

        self.disclaimer_label = ctk.CTkLabel(
            master=self,
            justify="left",
            text="",
            text_color=AppearanceSettings.settings["settings_panel"]["warning_color"]["normal"]
        )
        self.contribute_data_retrieve_status = None
        self.app_info: Dict = JsonUtility.read_from_file("data\\info.json")
        self.place_widgets()
        self.set_widgets_fonts()
        self.set_widgets_texts()
        self.set_widgets_sizes()
        self.configure_values()
        self.set_widgets_accent_color()
        self.bind_widgets_events()

        ThemeManager.register_widget(self)
        LanguageManager.register_widget(self)
        
    def configure_values(self):
        self.name_label.configure(text=self.app_info["name"])
        self.version_label.configure(text=self.app_info["version"])
        self.site_button.configure(text=self.app_info["site"], command=lambda: webbrowser.open(self.app_info["site"]))
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
        # randomly choose to update info :D
        if random.choice((False,) * 15 + (True,)*5):
            # delete old profile images
            FileUtility.delete_files("assets//profile images//", ["this directory is necessary"])
            self.app_info["contributors"] = {}
            
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
        else:
            if len(self.app_info["contributors"]) == 0:
                self.contribute_data_retrieve_status = "Failed"
                self.contributors_status_label.configure(
                    text=LanguageManager.data["contribute_data_retrieve_fail"],
                    text_color=AppearanceSettings.settings["settings_panel"]["warning_color"]["normal"]
                )
                
        if len(self.app_info["contributors"]) != 0:
            # place forget the loading label
            self.contributors_status_label.grid_forget()
            # place frame for show  contributors info
            self.contributors_frame.grid(
                row=3,
                column=2,
                pady=(16 * AppearanceSettings.settings["scale_r"], 0),
                sticky="w",
                columnspan=10,
            )
        self.contribute_data_retrieve_status = "Success"
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

    def bind_widgets_events(self):
        self.site_button.bind("<Enter>", lambda event: self.site_button.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["hover"]))
        self.site_button.bind("<Leave>", lambda event: self.site_button.configure(
            text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"]))

    def set_widgets_accent_color(self):
        self.name_label.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
        self.version_label.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])
        self.site_button.configure(text_color=AppearanceSettings.settings["root"]["accent_color"]["normal"])

    def update_widgets_accent_color(self):
        self.set_widgets_accent_color()

    def update_widgets_colors(self):
        """Update colors for the widgets."""

    def place_widgets(self):
        scale = AppearanceSettings.settings["scale_r"]
        pady = 16 * scale
        self.name_title_label.grid(row=0, column=0, padx=(100, 0), pady=(50, 0), sticky="w")
        self.dash1_label.grid(row=0, column=1, padx=(30, 30), pady=(50, 0), sticky="w")
        self.name_label.grid(row=0, column=2, pady=(50, 0), sticky="w")

        self.version_title_label.grid(row=1, column=0, padx=(100, 0), pady=(pady, 0), sticky="w")
        self.dash2_label.grid(row=1, column=1, padx=(30, 30), pady=(pady, 0), sticky="w")
        self.version_label.grid(row=1, column=2, pady=(pady, 0), sticky="w")

        self.site_title_label.grid(row=2, column=0, padx=(100, 0), pady=(pady, 0), sticky="w")
        self.dash3_label.grid(row=2, column=1, padx=(30, 30), pady=(pady, 0), sticky="w")
        self.site_button.grid(row=2, column=2, pady=(pady, 0), sticky="w")
        self.site_button.configure(width=20)

        self.contributors_title_label.grid(row=3, column=0, padx=(100, 0), pady=(pady, 0), sticky="nw")
        self.dash4_label.grid(row=3, column=1, padx=(30, 30), pady=(pady, 0), sticky="nw")
        self.contributors_status_label.grid(row=3, column=2, pady=(pady, 0), sticky="w")
        self.disclaimer_label.place(x=100, rely=1, y=-60 * scale)

    def set_widgets_sizes(self):
        scale = AppearanceSettings.settings["scale_r"]
        self.contributors_frame.configure(height=200 * scale, width=500 * scale)
        self.contributors_frame._scrollbar.grid_forget()

    def set_widgets_texts(self):
        self.name_title_label.configure(text=LanguageManager.data["name"])
        self.version_title_label.configure(text=LanguageManager.data["version"])
        self.site_title_label.configure(text=LanguageManager.data["site"])
        self.contributors_title_label.configure(text=LanguageManager.data["contributors"])
        if self.contribute_data_retrieve_status == "failed":
            self.contributors_status_label.configure(text=LanguageManager.data["contribute_data_retrieve_fail"])
        elif self.contribute_data_retrieve_status is None:
            self.contributors_status_label.configure(text=LanguageManager.data["loading"])
        self.disclaimer_label.configure(text="  " + LanguageManager.data["disclaimer"])

    def update_widgets_text(self):
        self.set_widgets_texts()

    def set_widgets_fonts(self):
        scale = AppearanceSettings.settings["scale_r"]
        title_font = ("Segoe UI", 13 * scale, "bold")
        self.name_title_label.configure(font=title_font)
        self.dash1_label.configure(font=title_font)
        self.name_label.configure(font=title_font)

        self.version_title_label.configure(font=title_font)
        self.dash2_label.configure(font=title_font)
        self.version_label.configure(font=title_font)

        self.site_title_label.configure(font=title_font)
        self.dash3_label.configure(font=title_font)
        self.site_button.configure(font=title_font)

        self.contributors_title_label.configure(font=title_font)
        self.dash4_label.configure(font=title_font)
        self.contributors_status_label.configure(font=title_font)

        value_font = ("Segoe UI", 13 * scale, "normal")
        self.disclaimer_label.configure(font=value_font)
