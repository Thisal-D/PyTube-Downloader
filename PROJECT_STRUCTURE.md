# Project Structure

### Pytube Downloader/<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── [_`data/`_](data/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [_`languages/`_](data/languages/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`en.json`](data/languages/en.json)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`zh.json`](data/languages/zh.json)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`si.json`](data/languages/si.json)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `....json`<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `....json`<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `....json`<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`general.json`](data/general.json)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`appearance.json`](data/appearance.json)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`info.json`](data/info.json)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`languages.json`](data/languages.json)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── [_`assets/`_](assets/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [_`main icon/`_](assets/main%20icon/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`64x64.ico`](assets/main%20icon/64x64.ico)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`128x128.ico`](assets/main%20icon/128x128.ico)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`256x256.ico`](assets/main%20icon/256x256.ico)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`512x512.ico`](assets/main%20icon/512x512.ico)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [_`ui images/`_](assets/ui%20images/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`info.png`](assets/ui%20images/info.png)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`playlist-dark.png`](assets/ui%20images/playlist-dark.png)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`playlist-light.png`](assets/ui%20images/playlist-light.png)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`video-dark.png`](assets/ui%20images/video-dark.png)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`video-light.png`](assets/ui%20images/video-light.png)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`default thumbnail.png`](assets/ui%20images/default%20thumbnail.png)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [_`profile images/`_](assets/profile%20images/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── [_`history/`_](history/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [_`thumbnails/`_](history/thumbnails/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── [_`temp/`_](temp/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [_`thumbnails/`_](temp/thumbnails/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── [_`ffmpeg/`_](ffmpeg/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`ffmpeg.exe`](https://ffmpeg.org/download.html)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── [_`settings/`_](settings/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [**`__init__.py`**](settings/__init__.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`appearance_settings.py`](settings/appearance_settings.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`general_settings.py`](settings/general_settings.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── [_`utils/`_](utils/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [**`__init__.py`**](utils/__init__.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`data_base_utility.py`](utils/data_base_utility.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`date_time_utility.py`](utils/date_time_utility.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`download_info_utility.py`](utils/download_info_utility.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`file_utility.py`](utils/file_utility.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`data_retrive_utility.py`](utils/data_retrive_utility.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`gui_utils.py`](utils/gui_utils.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`image_utility.py`](utils/image_utility.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`json_utility.py`](utils/json_utility.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`settings_validate_utility.py`](utils/settings_validate_utility.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`value_convert_utility.py`](utils/value_convert_utility.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── [_`widgets/`_](widgets/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [**`__init__.py`**](widgets/__init__.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [_`components/`_](widgets/components/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [**`__init__.py`**](widgets/components/__init__.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`thumbnail_button.py`](widgets/components/thumbnail_button.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`accent_color_button.py`](widgets/components/accent_color_button.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`contributor_profile_widget.py`](widgets/components/contributor_profile_widget.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [_`setting_panels/`_](widgets/setting_panels/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [**`__init__.py`**](widgets/setting_panels/__init__.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`general_panel.py`](widgets/setting_panels/general_panel.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`appearance_panel.py`](widgets/setting_panels/appearance_panel.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`network_panel.py`](widgets/setting_panels/network_panel.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`downloads_panel.py`](widgets/setting_panels/downloads_panel.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`about_panel.py`](widgets/setting_panels/about_panel.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`navigation_panel.py`](widgets/setting_panels/navigation_panel.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [_`core_widgets/`_](widgets/core_widgets/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [**`__init__.py`**](widgets/core_widgets/__init__.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`alert_window.py`](widgets/core_widgets/alert_window.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`low_level_alert_window.py`](widgets/core_widgets/low_level_alert_window.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`context_menu.py`](widgets/core_widgets/context_menu.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`setting_panel.py`](widgets/core_widgets/setting_panel.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`tray_menu.py`](widgets/core_widgets/tray_menu.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [_`history_widgets/`_](widgets/history_widgets/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [**`__init__.py`**](widgets/history_widgets/__init__.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`history_object.py`](widgets/history_widgets/history_object.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`history_video.py`](widgets/history_widgets/history_video.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`history_playlist.py`](widgets/history_widgets/history_playlist.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`history_panel.py`](widgets/history_widgets/history_panel.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [_`play_list/`_](widgets/play_list/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [**`__init__.py`**](widgets/play_list/__init__.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`play_list.py`](widgets/play_list/play_list.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`added_play_list.py`](widgets/play_list/added_play_list.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`downloading_play_list.py`](widgets/play_list/downloading_play_list.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`downloaded_play_list.py`](widgets/play_list/downloaded_play_list.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [_`video/`_](widgets/video/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [**`__init__.py`**](widgets/video/__init__.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`video.py`](widgets/video/video.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`added_video.py`](widgets/video/added_video.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`downloading_video.py`](widgets/video/downloading_video.py)<br> 
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`downloaded_video.py`](widgets/video/downloaded_video.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── [_`services/`_](services/)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [**`__init__.py`**](services/__init__.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`theme_manager.py`](services/theme_manager.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`load_manager.py`](services/load_manager.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`download_manager.py`](services/download_manager.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`language_manager.py`](services/language_manager.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`loading_indicate_manager.py`](services/loading_indicate_manager.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`video_count_tracker.py`](services/video_count_tracker.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`history_manager.py`](services/history_manager.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`video_convert_manager.py`](services/video_convert_manager.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── [`download_speed_tracker.py`](services/download_speed_tracker.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── [`notification_manager.py`](services/notification_manager.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── [**`app.py`**](app.py)<br>
&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;└── [**`main.py`**](main.py)<br>
