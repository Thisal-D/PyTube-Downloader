import sqlite3
from utils import (
    DataBaseUtility, 
    DateTimeUtility,
    FileUtility
)
import os
from typing import Callable
# from widgets.video import DownloadedVideo
# from widgets.play_list import DownloadedPlayList


class HistoryManager:
    
    videos_history_data = []
    playlists_history_data = []
    data_base_dir = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\PyTube Downloader"
    # data_base_dir = "history"
    data_base_name = "history.db"
    data_base = f"{data_base_dir}\\{data_base_name}"
    connection = None
    cursor = None
    max_history = 40
    video_history_change_callback = None
    playlist_history_change_callback = None
    
    @staticmethod
    def initialize(
        video_history_change_callback: Callable = None, 
        playlist_history_change_callback: Callable = None) -> None:
        
        HistoryManager.video_history_change_callback = video_history_change_callback
        HistoryManager.playlist_history_change_callback = playlist_history_change_callback
        
        if not DataBaseUtility.is_data_base_exists(HistoryManager.data_base):
            DataBaseUtility.create_data_base(HistoryManager.data_base_dir, HistoryManager.data_base_name)
            DataBaseUtility.create_table(
                HistoryManager.data_base, 
                "videos", 
                "no INTEGER PRIMARY KEY AUTOINCREMENT, channel TEXT, title TEXT, url TEXT, thumbnail_normal_path TEXT, thumbnail_hover_path TEXT, video_length INTEGER, download_date TEXT"
            )
            DataBaseUtility.create_table(
                HistoryManager.data_base, 
                "playlists", 
                "no INTEGER PRIMARY KEY AUTOINCREMENT, channel TEXT, title TEXT, url TEXT, thumbnail_normal_path TEXT, thumbnail_hover_path TEXT, video_count INTEGER, download_date TEXT"
            )
        
        HistoryManager.connection = sqlite3.connect(HistoryManager.data_base, check_same_thread=False)
        HistoryManager.cursor = HistoryManager.connection.cursor()
        
        HistoryManager.initialize_history()
        
    @staticmethod
    def initialize_history():
        # SQL query to fetch the last 50 rows based on the primary key (no)
        sql_videos = "SELECT * FROM videos"
        sql_playlists = "SELECT * FROM playlists"
        
        # Fetch the data from videos and playlists tables
        HistoryManager.videos_history_data = HistoryManager.cursor.execute(sql_videos).fetchall()
        HistoryManager.playlists_history_data = HistoryManager.cursor.execute(sql_playlists).fetchall()
        
        if len(HistoryManager.videos_history_data) > HistoryManager.max_history:
            HistoryManager.videos_history_data = HistoryManager.videos_history_data[len(HistoryManager.videos_history_data) - HistoryManager.max_history::]
            
        if len(HistoryManager.playlists_history_data) > HistoryManager.max_history:
            HistoryManager.playlists_history_data = HistoryManager.playlists_history_data[len(HistoryManager.playlists_history_data) - HistoryManager.max_history::]
        
        HistoryManager.videos_history_data = HistoryManager.videos_history_data[::-1]
        HistoryManager.playlists_history_data = HistoryManager.playlists_history_data[::-1]
            
    @staticmethod
    def save_video_to_history(video):#: DownloadedVideo):        
        channel = video.channel
        title = video.video_title
        url = video.video_url
        thumbnail_normal_path = video.history_normal_thumbnail_image_path
        thumbnail_hover_path = video.history_hover_thumbnail_image_path
        video_length = video.length
        download_date = DateTimeUtility.get_current_date_time()
        
        """
        HistoryManager.videos_history_data.insert(0, (None, channel, title, url, thumbnail_normal_path, thumbnail_hover_path, video_length, download_date))
        if len(HistoryManager.videos_history_data) > HistoryManager.max_history:
             HistoryManager.videos_history_data =  HistoryManager.videos_history_data[0:HistoryManager.max_history]
        """
        
        sql = "Insert into videos (channel, title, url, thumbnail_normal_path, thumbnail_hover_path, video_length, download_date) values (?, ?, ?, ?, ?, ?, ?)"
        HistoryManager.cursor.execute(sql, (channel, title, url, thumbnail_normal_path, thumbnail_hover_path, video_length, download_date))
        HistoryManager.connection.commit()
        
        HistoryManager.video_history_change_callback(0, channel, title, url, thumbnail_normal_path, thumbnail_hover_path, video_length, download_date)
        
    @staticmethod
    def save_playlist_to_history(playlist):#: DownloadedPlayList):        
        channel = playlist.channel
        title = playlist.playlist_title
        url = playlist.playlist_url
        thumbnail_normal_path = playlist.downloading_videos[0].history_normal_thumbnail_image_path
        thumbnail_hover_path = playlist.downloading_videos[0].history_hover_thumbnail_image_path
        video_count = playlist.playlist_original_video_count
        download_date = DateTimeUtility.get_current_date_time()
        
        """
        HistoryManager.playlists_history_data.insert(0, (None, channel, title, url, thumbnail_normal_path, thumbnail_hover_path, video_count, download_date))
        if len(HistoryManager.playlists_history_data) > HistoryManager.max_history:
             HistoryManager.playlists_history_data =  HistoryManager.playlists_history_data[0:HistoryManager.max_history]
        """
        
        sql = "Insert into playlists (channel, title, url, thumbnail_normal_path, thumbnail_hover_path, video_count, download_date) values (?, ?, ?, ?, ?, ?, ?)"
        HistoryManager.cursor.execute(sql, (channel, title, url, thumbnail_normal_path, thumbnail_hover_path, video_count, download_date))
        HistoryManager.connection.commit()
        
        HistoryManager.playlist_history_change_callback(0, channel, title, url, thumbnail_normal_path, thumbnail_hover_path, video_count, download_date)
        
    @staticmethod
    def maintain_history(table: str) -> None:
        sql_count = f"SELECT COUNT(*) FROM {table}"
        HistoryManager.cursor.execute(sql_count)
        total_rows = HistoryManager.cursor.fetchone()[0]

        if total_rows > HistoryManager.max_history:
            rows_to_delete = total_rows - HistoryManager.max_history
            sql_delete = f"DELETE FROM {table} WHERE no IN (SELECT no FROM {table} ORDER BY no ASC LIMIT ?)"
            HistoryManager.cursor.execute(sql_delete, (rows_to_delete,))
            HistoryManager.connection.commit()

    @staticmethod
    def clear_invalid_history() -> None:
        HistoryManager.maintain_history("videos")
        HistoryManager.maintain_history("playlists")
         
        videos_history_req_thumbnails = HistoryManager.cursor.execute("SELECT thumbnail_normal_path, thumbnail_hover_path FROM videos").fetchall()
        playlists_history_req_thumbnails = HistoryManager.cursor.execute("SELECT thumbnail_normal_path, thumbnail_hover_path FROM playlists").fetchall()

        required_thumbnails = ["this directory is necessary"]
        for thumbnail in videos_history_req_thumbnails + playlists_history_req_thumbnails:
            required_thumbnails.append(thumbnail[0].split("/")[-1])
            required_thumbnails.append(thumbnail[1].split("/")[-1])
        
        for required_thumbnail in required_thumbnails:
            print(required_thumbnail)
        FileUtility.delete_files(directory="history\\thumbnails", files_to_keep=required_thumbnails)
        
