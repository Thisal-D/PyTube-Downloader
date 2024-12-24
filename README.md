![Language](https://img.shields.io/badge/Language-English-blue) [![Chinese](https://img.shields.io/badge/Language-中文-red)](README_zh.md)

# PyTube Downloader 

&nbsp; &nbsp;[![Download PyTube Downloader](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/pytube-downloader/files/latest/download)

&nbsp; &nbsp;[![Download PyTube Downloader](https://img.shields.io/sourceforge/dm/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download) [![Download PyTube Downloader](https://img.shields.io/sourceforge/dw/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download) [![Download PyTube Downloader](https://img.shields.io/sourceforge/dt/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download)

&nbsp; &nbsp;`v3.1.1` [Visit to Download .exe for Windows](https://sourceforge.net/p/pytube-downloader)

---


**PyTube Downloader is a simple, user-friendly app that lets you easily download YouTube videos and entire playlists with one click. Choose from a variety of video and audio formats, including resolutions from 144p to 8K quality. It also supports simultaneous downloads, allowing you to save time and download multiple videos at once.**

---

## Features

- **Playlist Downloading:** Download entire playlists using just the playlist URL.
- **Format Selection:** Choose from various video and audio formats for downloading, from `144p` to `8K` quality.
- **Progress Tracking:** Track the download progress within the application.
- **Simultaneous Downloads:** Download multiple YouTube videos simultaneously, saving time and increasing efficiency. Users have full control over the number of simultaneous downloads, allowing for a personalized downloading experience.
- **Automatic Download with Predefined Settings** Users can set predefined download settings such as preferred video quality, audio format, download location, and more. Once a YouTube URL is added, the video/playlist will load and then start to download automatically according to these predefined settings.
  - *In playlist auto download mode, if any video fails to load, it will be ignored, and the download will continue with the remaining videos.*
- **Dynamic Folder Organization:** Automatically organize downloaded files into separate directories based on factors such as video quality, file type (audio or video), and playlist name, ensuring efficient and structured storage.
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

## Quick Start Guide

1. Clone the repository to your local machine.
    - Clone the repository to your local machine using:  
      
        ```bash
        git clone https://github.com/Thisal-D/PyTube-Downloader.git
        ```
2. Download FFmpeg
    - Visit the [FFmpeg website](https://ffmpeg.org/download.html) and download the appropriate version for your operating system.
    - Extract the downloaded files and locate the ffmpeg.exe file. (`ffmpeg\bin\ffmpeg.exe`)
    - Copy ffmpeg.exe into the ffmpeg folder located within the application directory. (`Pytube-Downloader\ffmpeg\`)
3. Install Dependencies:
    - If the application requires dependencies, run the following script to install them:
     
      ```bash
      python dependencies_installer.py
      ```
4. Run the Application:
    - Start the application by running:
      
       ```bash
       python main.py
       ```
5. Paste the YouTube URL:
    - Paste the URL of the YouTube video or playlist you want to download into the designated input field.
6. Select Download Mode:
    - Choose whether you want to download a single video or an entire playlist.
7. Choose Format:
    - Select the desired format (e.g., MP4, MP3) from the available options.
8. Initiate Download:
    - Click the Download button to start the download process.
9. Monitor Progress:
    - Watch the download progress within the application interface.
10. Enjoy Your Video:
    - Once the download is complete, find your file in the output directory and enjoy your YouTube video or audio!

---

## Technologies Used

- **Programming Language:** 
  - Python
- **Python Libraries:** 
  - tkinter
  - customtkinter
  - pytube
  - pytubefix
  - pillow
  - pyautogui
  - pystray
  - pyperclip
- **Dependencies**
  - FFMPEG

---

## Dark Theme Preview 

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