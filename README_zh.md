![Language](https://img.shields.io/badge/Language-中文-red) [![English](https://img.shields.io/badge/Language-English-blue)](README.md)

# PyTube Downloader


&nbsp; &nbsp;[![Download PyTube Downloader](https://a.fsdn.com/con/app/sf-download-button)](https://sourceforge.net/projects/pytube-downloader/files/latest/download)

&nbsp; &nbsp;[![Download PyTube Downloader](https://img.shields.io/sourceforge/dm/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download) [![Download PyTube Downloader](https://img.shields.io/sourceforge/dw/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download) [![Download PyTube Downloader](https://img.shields.io/sourceforge/dt/pytube-downloader.svg)](https://sourceforge.net/projects/pytube-downloader/files/latest/download)

[下载适用于 Windows 的 .exe](https://sourceforge.net/p/pytube-downloader)

---

**PyTube Downloader 是一个简单、用户友好的应用程序，帮助您轻松下载 YouTube 视频或整个播放列表。您可以选择多种视频和音频格式，包括从 144p 到 8K 的各种分辨率。它还允许您一次下载多个视频，节省时间。**

---

## 特点

- **播放列表下载**： 仅通过播放列表 URL 下载整个播放列表。
- **格式选择**： 从各种视频和音频格式中选择下载，从 144p 到 8K。
- **下载进度跟踪**： 在应用程序内跟踪下载进度。
- **同时下载**： 同时下载多个 YouTube 视频，节省时间并提高效率。用户可以完全控制同时下载的数量，允许个性化的下载体验。
- **默认设置的自动下载**： 用户可以设置默认的下载设置，如首选视频质量、音频格式、下载位置等。添加 YouTube URL 后，视频/播放列表将- **加载并根据这些默认设置自动下载。
  - 在播放列表自动下载模式下，如果有任何视频无法加载，将被忽略它们继续下载剩余的视频。
- **动态文件夹组织**： 根据视频质量、文件类型（音频或视频）和播放列表名称等因素，自动将下载的文件组织到单独的目录中，确保有效和结构化的存储。
- **多语言支持**： 可以使用您喜欢的语言享受该应用程序，支持多种语言。

  - 当前支持语言:
    | 语言         | 贡献者       |
    | --------------| ------------ |
    | `English` (英文)         | -            |
    | `中文` | [<img src="https://github.com/childeyouyu.png?size=25" width="25">](https://github.com/childeyouyu) |
    | `සිංහල` (僧伽罗语) | [<img src="https://github.com/Navindu21.png?size=25" width="25">](https://github.com/Navindu21) |

  - **帮助我们 [``改进当前语言``](LANGUAGE_CONTRIBUTION_GUIDE_zh.md/#improve-current-language-issues) 和 [``添加新语言``](LANGUAGE_CONTRIBUTION_GUIDE_zh.md/#adding-a-new-language) 到此应用程序。**
- **快捷键**： 使用常见任务的快捷键来控制应用程序。

---

## 快速入门指南

1. 将仓库克隆到本地计算机。
    - 使用以下命令克隆仓库：
      
      ```bash
      git clone https://github.com/Thisal-D/PyTube-Downloader.git
      ```
2. 下载 FFmpeg
   - 访问 [FFmpeg 网站](https://ffmpeg.org/download.html) 并下载适合您操作系统的版本。
   - 解压下载的文件并找到 ffmpeg.exe 文件。 (`ffmpeg\bin\ffmpeg.exe`)
   - 将 ffmpeg.exe 复制到应用程序目录中的 ffmpeg 文件夹。 (`Pytube-Downloader\ffmpeg\`)
3. 安装依赖：:
    - 如果应用程序需要依赖，运行以下脚本安装它们：
     
      ```bash
      python dependencies_installer.py
      ```
4. 运行应用程序：
    - 通过运行以下命令启动应用程序：
      
      ```bash
      python main.py
      ```
5. 粘贴 YouTube URL：
    - 将您要下载的 YouTube 视频或播放列表的 URL 粘贴到指定的输入框中。
6. 选择下载模式：
    - 选择您是要下载单个视频还是整个播放列表。
7. 选择格式：
    - 从可用选项中选择所需的格式（例如，MP4、MP3）。
8. 启动下载：
    - 点击下载按钮开始下载过程。
9. 监控进度：
    - 在应用程序界面中查看下载进度。
10. 享受您的视频：
    - 下载完成后，在输出目录中找到文件并享受您的 YouTube 视频或音频！

---

## 使用的技术

- **编程语言：** 
  - Python
- **Python 库：** 
  - tkinter
  - customtkinter
  - pytube
  - pytubefix
  - pillow
  - pyautogui
  - pystray
  - pyperclip
- **依赖：**
  - FFMPEG

---

## 项目结构

查看 [**项目结构**](PROJECT_STRUCTURE.md) 指南，了解文件夹组织和代码布局。

---

## 暗黑主题预览

![0](./readme%20assets/zh-0.png)
![1](./readme%20assets/zh-1.png)
![2](./readme%20assets/zh-2.png)
![3](./readme%20assets/zh-3.png)
![4](./readme%20assets/zh-4.png)
![5](./readme%20assets/zh-5.png)
![6](./readme%20assets/zh-6.png)
![7](./readme%20assets/zh-7.png)
![8](./readme%20assets/zh-8.png)
![9](./readme%20assets/zh-9.png)


---

## Star 历史

<picture> 
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Thisal-D/PyTube-Downloader&type=Date&theme=dark"> 
    <img src="https://api.star-history.com/svg?repos=Thisal-D/PyTube-Downloader&type=Date&theme=light" > 
</picture> 

---

## 使用方法

1. 将仓库克隆到您的本地机器。
2. 安装必要的依赖项（如有，运行 **dependencies_installer.py**）。
3. 运行应用程序（``main.py``）。
4. 将 YouTube 视频/播放列表 URL 粘贴到指定字段中。
5. 选择下载模式: 视频/播放列表。
6. 选择所需的格式。
7. 点击下载按钮以启动下载过程。
8. 在应用

## 贡献

欢迎对此项目进行贡献！请随意分叉存储库，进行改进，并提交拉取请求。

---

## 许可证

本项目根据 MIT 许可证授权 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

---

## 免责声明

本应用仅供个人使用。请尊重 YouTube 的服务条款和内容创建者的权利。

---

## 贡献者

- [<img src="https://github.com/childeyouyu.png?size=25" width="25">](https://github.com/childeyouyu) [youyu](https://github.com/childeyouyu)
- [<img src="https://github.com/Navindu21.png?size=25" width="25">](https://github.com/Navindu21) [Navindu Pahasara](https://github.com/Navindu21)
- [<img src="https://github.com/sooryasuraweera.png?size=25" width="25">](https://github.com/sooryasuraweera) [Soorya Suraweera](https://github.com/sooryasuraweera)