🌟**If you find this project helpful, your support by starring it would mean a lot! Your feedback motivates me to keep refining and enhancing it further.** 🚀

Your support means a lot and inspires me to do better with each update. Thank you for taking the time to check out this project! 🥰

---

# PyTube Downloader

[Download .exe for Windows](https://github.com/Thisal-D/PyTube-Downloader/tree/main/Windows%20Installer)

PyTube Downloader is a user-friendly application that allows users to download YouTube videos with ease. It features a simple and intuitive user interface, making the downloading process straightforward for all users.

---

## Features

- **Easy Downloading:** Download YouTube videos effortlessly by pasting the video URL into the application.
- **Playlist Downloading:** Download entire playlists using just the playlist URL.
- **Format Selection:** Choose from various video and audio formats for downloading.
- **Progress Tracking:** Track the download progress within the application.
- **Simultaneous Downloads:** Download multiple YouTube videos simultaneously, saving time and increasing efficiency. Users have full control over the number of simultaneous downloads, allowing for a personalized downloading experience.
- **Automatic Download With Predefined Settings** Users can set predefined download settings such as preferred video quality, audio format, download location, and more. Once a YouTube URL is added, the video will load and then start to download automatically according to these predefined settings.
- **System Tray Icon Mode:** Access the application conveniently from the system tray, providing quick access to essential features and controls without cluttering the desktop. Users can easily minimize the application to the system tray for unobtrusive operation.
- **Theme Customization:** Personalize your experience with the ability to switch between dark and light themes. Additionally, customize the accent color to suit your preferences, creating a visually pleasing interface tailored to your style.

---

### Dark Theme

![1](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/be798646-ccc8-4691-8084-c2f4969e5069)
![2](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/262aa64c-1a42-43a9-b932-620ebc2faa52)
![6](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/7230212f-0948-43f2-80f3-3850b71c36f0)
![3](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/72a1bffd-e4a2-4fef-ba3f-903f1875b6d2)
![4](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/78e3ff84-962e-4b69-8b12-9a93fbea4978)
![5](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/bb01e14e-6ca8-4be0-ba07-c43e64af400a)

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

## Project Structure
project_folder/<br>
│<br>
├── data/<br>
│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── general_settings.json<br>
│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── theme_settings.json<br>
│<br>
├── settings/<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── __init__.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── general_settings.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── theme_settings.py<br>
│<br>
├── assets/<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── icons/<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── icon1.png<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── icon2.png<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── ...<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── photos/<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── photo1.jpg<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── photo2.jpg<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── ...<br>
│<br>
├── utils/<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── __init__.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── utility1.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── utility2.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── ...<br>
│<br>
├── widgets/<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── __init__.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── widget1.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── widget2.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── ...<br>
│<br>
├── managers/<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── __init__.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── theme_manager.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── download_manager.py<br>
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── ...<br>
│<br>
└── services/<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── __init__.py<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── service1.py<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── service2.py<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── ...<br>



## Contributors

- [<img src="https://github.com/childeyouyu.png?size=25" width="25">](https://github.com/childeyouyu) [youyu](https://github.com/childeyouyu)
- [<img src="https://github.com/Navindu21.png?size=25" width="25">](https://github.com/Navindu21) [Navindu Pahasara](https://github.com/Navindu21)
- [<img src="https://github.com/sooryasuraweera.png?size=25" width="25">](https://github.com/sooryasuraweera) [Soorya Suraweera](https://github.com/sooryasuraweera)
