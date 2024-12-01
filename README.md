![Language](https://img.shields.io/badge/Language-English-blue) [![Chinese](https://img.shields.io/badge/Language-中文-red)](README_zh.md)

# PyTube Downloader 

&nbsp; &nbsp;[![Download PyTube Downloader](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/pytube-downloader/files/latest/download)

&nbsp; &nbsp;[![Download PyTube Downloader](https://img.shields.io/sourceforge/dm/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download) [![Download PyTube Downloader](https://img.shields.io/sourceforge/dw/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download) [![Download PyTube Downloader](https://img.shields.io/sourceforge/dt/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download)

&nbsp; &nbsp;`v2.0.3` [Visit to Download .exe for Windows](https://sourceforge.net/p/pytube-downloader)

---

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
- **Multi-Language Support**: Enjoy the application in your preferred language with support for multiple languages.
  - Currently Support Languages:
    | Language      | Contributors |
    | --------------| ------------ |
    | `English`       | -            |
    | `中文` (Chinese)| [<img src="https://github.com/childeyouyu.png?size=25" width="25">](https://github.com/childeyouyu) |
    | `සිංහල` (Sinhala)| [<img src="https://github.com/Navindu21.png?size=25" width="25">](https://github.com/Navindu21) |

  -  **Help us [``improve current languages``](LANGUAGE_CONTRIBUTION_GUIDE_en.md/#improve-current-language-issues) and [``add new languages``](LANGUAGE_CONTRIBUTION_GUIDE_en.md/#adding-a-new-language) to this application.** 
- **Shortcut Keys**: Take control of the application with  shortcut keys for common tasks.
---

## View - Dark Theme

![0](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/b2079262-0d1c-4bd0-9b33-7cc16c9173ce)
![18](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/e57acd23-cbdc-446e-86ed-b5d08f5ce9e1)
![19](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/fbf086cb-e90c-499e-b63e-9f8a9515c014)
![20](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/6622a7d4-7b23-41b6-abba-4d55ff2d58cd)
![10](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/45a9ff9f-dc56-49a5-b4e0-576e8299a609)
![22](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/ea13e3c1-3397-4af7-ba8e-09cdc0f0eda5)
![23](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/7a8a00f2-6165-4379-8316-51d90b3e0747)
![24](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/53ce24af-6224-4d7b-b1a4-3a52b436ec0d)
![25](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/501763ad-e30f-4916-9a66-f9b8a80f2052)
![26](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/a7d2ca37-289b-41f4-b01f-21cc915f7e0a)
![27](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/1f8b6280-4bd3-469e-aace-12ddc1d645b8)

---

## Star History

<picture> 
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Thisal-D/PyTube-Downloader&type=Date&theme=dark"> 
    <img src="https://api.star-history.com/svg?repos=Thisal-D/PyTube-Downloader&type=Date&theme=light" > 
</picture> 

---

## Technologies Used

- **Programming Language:** 
  - Python
- **Frameworks/Libraries:** 
  - tkinter
  - customtkinter
  - pytube
  - pytubefix
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