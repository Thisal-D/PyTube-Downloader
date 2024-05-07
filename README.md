🌟**If you find this project helpful, your support by starring it would mean a lot! Your feedback motivates me to keep refining and enhancing it further.** 🚀

Your support means a lot and inspires me to do better with each update. Thank you for taking the time to check out this project! 🥰

---

# PyTube Downloader

[Download .exe for Windows](https://github.com/Thisal-D/PyTube-Downloader/tree/main/windows%20installer)

PyTube Downloader is a user-friendly application that allows users to download YouTube videos with ease. It features a simple and intuitive user interface, making the downloading process straightforward for all users.

---

## Features

- **Easy Downloading:** Download YouTube videos effortlessly by pasting the video URL into the application.
- **Playlist Downloading:** Download entire playlists using just the playlist URL.
- **Format Selection:** Choose from various video and audio formats for downloading.
- **Progress Tracking:** Track the download progress within the application.
- **Simultaneous Downloads:** Download multiple YouTube videos simultaneously, saving time and increasing efficiency. Users have full control over the number of simultaneous downloads, allowing for a personalized downloading experience.
- **Automatic Download with Predefined Settings** Users can set predefined download settings such as preferred video quality, audio format, download location, and more. Once a YouTube URL is added, the video will load and then start to download automatically according to these predefined settings.
- **System Tray Icon Mode:** Users can easily minimize the application to the system tray for unobtrusive operation.
- **Theme Customization:** Personalize your experience with the ability to switch between dark and light themes. Additionally, customize the accent color to suit your preferences, creating a visually pleasing interface tailored to your style.
- **Scaling Preferences:** Users can scale the application interface from 100% to 200%, adjusting the size of widgets and elements for better readability and usability.

---

### Dark Theme

![01](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/6db80461-a8a4-4ae4-9ac5-22a591c4ebbe)
![02](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/50ee6014-c9f0-4548-b8fc-5dd9b824ba9f)
![03](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/af0fbdb0-23eb-40f9-951e-084b717de295)
![04](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/e1d85545-b900-43cc-ac27-7710c5bef250)
![06](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/2192be1e-b2bc-4a70-87ed-6c6c15a786cf)
![07](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/39660493-6121-4422-b345-ec2b92249d16)
![08](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/3e4970a2-3e7e-4adb-9fce-5bf4a8f9f62e)
![09](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/c93501bf-4324-415d-879c-4e718978220b)
![10](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/ef0f4deb-0893-4ed1-8c8b-18ab8b8a572c)
![11](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/38b51a50-6435-48f8-807f-4d8437dc634d)
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
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── widget_positions.json<br>
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
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── widget_position_settings.py<br>
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
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── \_\_init\_\_.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── video.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── added_video.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── downloading_video.py<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── downloaded_video.py<br>
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
