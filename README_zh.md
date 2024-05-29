# PyTube Downloader

- `v1.0.3` [下载适用于 Windows 的 .exe](https://sourceforge.net/p/pytube-downloader)

---

PyTube 下载器是一款用户友好的应用程序，使用户能够轻松下载 YouTube 视频。它具有简单直观的用户界面，使下载过程对所有用户来说都非常简单。

---

## 特点

- **轻松下载:** 只需将视频 URL 粘贴到应用程序中，即可轻松下载 YouTube 视频。
- **播放列表下载:** 使用播放列表 URL 下载整个播放列表。
- **格式选择:** 选择各种视频和音频格式进行下载。
- **进度跟踪:** 在应用程序中跟踪下载进度。
- **同时下载:** 同时下载多个 YouTube 视频，节省时间并提高效率。用户可以完全控制同时下载的数量，允许个性化的下载体验。
- **使用预定义设置自动下载:** 用户可以设置预定义的下载设置，如首选视频质量、音频格式、下载位置等。一旦添加了 YouTube URL，视频/播放列表将加载并根据这些预定义设置自动开始下载。
  - *在播放列表自动下载模式下，如果某个视频加载失败，它将被忽略，下载将继续剩余的视频。*
- **动态文件夹组织:** 根据视频质量、文件类型（音频或视频）和播放列表名称等因素自动将下载的文件组织到不同的目录中，确保高效且结构化的存储。
  - **基于质量的文件夹结构:** 为下载的文件创建按质量设置分类的不同文件夹，允许用户根据所需的分辨率或比特率轻松定位和管理文件。
  - **类型特定目录:** 自定义文件夹组织，将音频和视频文件分开到各自的文件夹中，清楚地区分不同的媒体类型。
  - **以播放列表为中心的文件夹:** 自动创建以频道和播放列表命名的文件夹，使基于特定播放列表的下载内容更容易找到和管理。
- **系统托盘图标模式:** 最小化应用程序到系统托盘以进行不干扰操作。
- **主题自定义:** 通过在深色和浅色主题之间切换个性化您的体验。此外，自定义强调色以适应您的偏好，创建符合您风格的视觉愉悦界面。
- **缩放首选项:** 用户可以将应用程序界面从 100% 缩放到 200%（步长 1%），调整小部件和元素的大小以提高可读性和可用性。
- **自动重新加载失败的视频:** 如果视频加载失败，最多尝试重新加载 5 次。用户可以启用或禁用此功能，确保即使在间歇性连接问题下也能更无缝地下载。
- **自动重试失败的下载:** 自动重试失败的下载最多 5 次。此功能确保由于网络中断等临时问题不会阻止成功下载，增强可靠性和用户体验。
- **多语言支持:** 使用多语言支持，以您喜欢的语言享受应用程序。
  - 当前支持语言:
    | 语言         | 贡献者       |
    | --------------| ------------ |
    | English (英文)        | -            |
    | 中文 | [<img src="https://github.com/childeyouyu.png?size=25" width="25">](https://github.com/childeyouyu) |
    | සිංහල (僧伽罗语) | [<img src="https://github.com/Navindu21.png?size=25" width="25">](https://github.com/Navindu21) |
 
  - **帮助我们 [``改进当前语言``](LANGUAGE_CONTRIBUTION_GUIDE_zh.md/#improve-current-language-issues) 和 [``添加新语言``](LANGUAGE_CONTRIBUTION_GUIDE_zh.md/#adding-a-new-language) 到此应用程序。**

---

## 查看 - 深色主题

![0](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/b2079262-0d1c-4bd0-9b33-7cc16c9173ce)
![7](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/7aea8c67-669f-4ee6-af45-7ea6e3b92019)
![8](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/b209e21d-afe0-4dd6-a776-95a1fc0a1062)
![9](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/5402f15b-ec81-4abc-b4ed-9d8c389ac03f)
![10](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/1d197f08-77eb-4e3e-85e2-450de5497db1)
![11](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/6aa20ae2-fe27-4d32-9997-590fe6453c38)
![12](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/4e30da72-b615-4d3a-baac-a986965ab8f9)
![13](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/2741bc3d-8b9a-4763-b4ee-987b0476015e)
![14](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/a85491e9-189c-4e60-ad51-3c4241931e0a)
![15](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/4c87c165-1b32-4053-99b6-f3087cf145e8)
![16](https://github.com/Thisal-D/PyTube-Downloader/assets/93121062/6d192edb-999b-4fdd-838b-0e2ecddf2df1)

---

## 使用的技术

- **编程语言:** 
  - Python
- **框架/库:** 
  - tkinter
  - customtkinter
  - pytube
  - pillow
  - pyautogui
  - pystray
  - pyperclip

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
