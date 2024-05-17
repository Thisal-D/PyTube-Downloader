# PyTube Downloader

[Download .exe for Windows](https://github.com/Thisal-D/PyTube-Downloader/releases/tag/v1.0.2)

PyTube Downloader is a user-friendly application that allows users to download YouTube videos with ease. It features a simple and intuitive user interface, making the downloading process straightforward for all users.

---

## Features

- **Easy Downloading:** Download YouTube videos effortlessly by pasting the video URL into the application.
- **Playlist Downloading:** Download entire playlists using just the playlist URL.
- **Format Selection:** Choose from various video and audio formats for downloading.
- **Progress Tracking:** Track the download progress within the application.
- **Simultaneous Downloads:** Download multiple YouTube videos simultaneously, saving time and increasing efficiency. Users have full control over the number of simultaneous downloads, allowing for a personalized downloading experience.
- **Automatic Download with Predefined Settings** Users can set predefined download settings such as preferred video quality, audio format, download location, and more. Once a YouTube URL is added, the video/playlist will load and then start to download automatically according to these predefined settings.
  - *In playlist auto download mode, if any video fails to load, it will be ignored, and the download will continue with the remaining videos.*
- **Dynamic Folder Organization:** Automatically organize downloaded files into separate directories based on factors such as video quality, file type (audio or video), and playlist name, ensuring efficient and structured storage.
  - **Quality-Based Folder Structure:** Create distinct folders for downloads categorized by their quality settings, allowing users to easily locate and manage files based on their desired resolution or bitrate.
  - **Type-Specific Directories:** Customize folder organization to segregate audio and video files into their respective folders, providing a clear distinction between different media types.
  - **Playlist-Centric Folders:** Automatically create folders named after the channel and playlist, making it easier to find and manage downloaded content based on specific playlists.
- **System Tray Icon Mode:** Minimize the application to the system tray for unobtrusive operation.
- **Theme Customization:** Personalize your experience with the ability to switch between dark and light themes. Additionally, customize the accent color to suit your preferences, creating a visually pleasing interface tailored to your style.
- **Scaling Preferences:** Users can scale the application interface from 100% to 200% (step 1%), adjusting the size of widgets and elements for better readability and usability.
- **Auto Reload Failed Videos:** Automatically attempts to reload a video up to 5 times if it fails to load. Users can enable or disable this feature, ensuring a more seamless downloading experience even with intermittent connectivity issues.
- **Auto Retry Failed Downloads:** Automatically retries a failed download up to 5 times. This feature ensures that temporary issues such as network interruptions do not prevent successful downloading, enhancing reliability and user experience.

---

### Dark Theme

![0](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/03821a3b-264a-4f8a-ad56-142352d9d9be)
![1](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/fc3475e7-5b62-486b-bbe6-fda589e2dc37)
![2](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/7f0df26e-4452-4b73-ae47-e05db7276095)
![3](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/221bb327-00f9-4077-9a18-9b1d7b89982e)
![4](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/03388570-a9fd-40e6-a673-ce9eaed7245c)
![5](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/b26e701d-0445-4397-80c4-107565651934)
![6](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/3a83d2c8-85c3-4247-8a9f-28e36e94359e)
![7](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/3617f5d2-59a8-4b07-b79e-bb0cee0258ac)
![8](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/8d21672d-0b9c-4ee3-b526-13fa30ac9bd1)
![9](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/b9dbf091-32b5-4fa6-8173-7a6f02f83165)

---

## Technologies Used

- **Programming Language:** 
  - Python
- **Frameworks/Libraries:** 
  - tkinter
  - customtkinter
  - pytube
  - pillow
  - pyautogui
  - pystray
  - pyperclip

---

## How to Use

1. Clone the repository to your local machine.
2. Install the necessary dependencies (if any, run **dependencies_installer.py**).
3. Run the application (``main.py``).
4. Paste the YouTube video/playlist URL into the designated field.
5. Choose the download mode: video/playlist.
6. Choose the desired format.
7. Click the download button to initiate the download process.
8. Monitor the download progress within the application.
9. Enjoy your downloaded YouTube video!

---

## Project Structure
project_folder/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── data/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── general.json<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── appearance.json<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── info.json<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── assets/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── main icon/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── icon.ico<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── ui images/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── info.png<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── default thumbnail.png<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── profile images/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── temp/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── thumbnails/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── settings/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── \_\_init\_\_.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── appearance_settings.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── general_settings.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── utils/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── \_\_init\_\_.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── download_info_utility.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── file_utility.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── git_hub_utility.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── gui_utils.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── image_utility.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── json_utility.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── settings_validate_utility.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── value_convert_utility.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── widgets/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── \_\_init\_\_.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── components/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── \_\_init\_\_.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── thumbnail_button.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── accent_color_button.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── appearance_panel.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── network_panel.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── downloads_panel.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── about_panel.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── navigation_panel.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── contributor_profile_widget.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── core_widgets/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── \_\_init\_\_.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── alert_window.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── context_menu.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── setting_panel.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── tray_menu.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── play_list/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── \_\_init\_\_.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── play_list.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── added_play_list.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── downloading_play_list.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── downloaded_play_list.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── video/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── \_\_init\_\_.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── video.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── added_video.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── downloading_video.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── downloaded_video.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── services/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── \_\_init\_\_.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── theme_manager.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── load_manager.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── download_manager.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── loading_indicate_manager.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── app.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;└── main.py<br>

---

## Contribution

Contributions to this project are welcome! Feel free to fork the repository, make improvements, and submit pull requests.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This application is intended for personal use only. Please respect YouTube's terms of service and the rights of content creators when downloading videos.

---

## Contributors

- [<img src="https://github.com/childeyouyu.png?size=25" width="25">](https://github.com/childeyouyu) [youyu](https://github.com/childeyouyu)
- [<img src="https://github.com/Navindu21.png?size=25" width="25">](https://github.com/Navindu21) [Navindu Pahasara](https://github.com/Navindu21)
- [<img src="https://github.com/sooryasuraweera.png?size=25" width="25">](https://github.com/sooryasuraweera) [Soorya Suraweera](https://github.com/sooryasuraweera)
