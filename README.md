![Language](https://img.shields.io/badge/Language-English-blue) [![Chinese](https://img.shields.io/badge/Language-中文-red)](README_zh.md)

# PyTube Downloader 

&nbsp; &nbsp;[![Download PyTube Downloader](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/pytube-downloader/files/latest/download)

&nbsp; &nbsp;[![Download PyTube Downloader](https://img.shields.io/sourceforge/dm/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download) [![Download PyTube Downloader](https://img.shields.io/sourceforge/dw/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download) [![Download PyTube Downloader](https://img.shields.io/sourceforge/dt/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download)

[Visit to Download .exe for Windows](https://sourceforge.net/p/pytube-downloader)

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

## Project Structure

Check out the [**Project Structure**](PROJECT_STRUCTURE.md) guide to understand the folder organization and code layout.

---

## Dark Theme Preview 

![0](./readme%20assets/en-0.png)
![1](./readme%20assets/en-1.png)
![2](./readme%20assets/en-2.png)
![3](./readme%20assets/en-3.png)
![4](./readme%20assets/en-4.png)
![5](./readme%20assets/en-5.png)
![6](./readme%20assets/en-6.png)
![7](./readme%20assets/en-7.png)
![8](./readme%20assets/en-8.png)
![9](./readme%20assets/en-9.png)

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