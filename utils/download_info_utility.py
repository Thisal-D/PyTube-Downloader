from typing import List, Dict
import pytube
from .value_convert_utility import ValueConvertUtility


class DownloadInfoUtility:
    @staticmethod
    def sort_download_qualities(qualities_info: List[Dict[str, int]]) -> List[Dict[str, int]]:
        """
        Sort the list of download qualities information based on their keys.

        Args:
            qualities_info (List[Dict[str, int]]): A list of dictionaries containing download qualities information.

        Returns:
            List[Dict[str, int]]: The sorted list of download qualities information.
        """
        video_keys = []
        audio_keys = []

        # Separate video and audio keys
        for data in qualities_info:
            key = list(data.keys())[0]
            if "kbps" in key:
                audio_keys.append(key)
            else:
                video_keys.append(key)

        # Sort video keys in descending order
        for i in range(len(video_keys)):
            for j in range(len(video_keys) - 1):
                if int(video_keys[j][:-1]) < int(video_keys[j + 1][:-1]):
                    video_keys[j], video_keys[j + 1] = video_keys[j + 1], video_keys[j]

        # Combine sorted video and audio keys
        sorted_keys = video_keys + audio_keys

        # Arrange dictionaries based on sorted keys
        sorted_qualities_info = []
        index = 0
        while index < len(sorted_keys):
            for quality_info in qualities_info:
                if list(quality_info.keys())[0] == sorted_keys[index]:
                    sorted_qualities_info.append(quality_info)
                    index += 1
                    if index >= len(sorted_keys):
                        break

        return sorted_qualities_info

    @staticmethod
    def to_dict(data) -> list[dict[str, str]]:
        """
        Convert data to a list of dictionaries.

        Args:
            data: Data to be converted.

        Returns:
            list[dict]: A list of dictionaries.
        """
        data_list = []
        for d in data:
            data_list.append(
                {value.split("=")[0]: value.split("=")[1] for value in str(d)[9:-1].replace('"', "").split(" ")})
        return data_list

    @staticmethod
    def get_supported_download_types(video_streams: pytube.StreamQuery) -> list[dict[str, int]]:
        """
        Get supported download types from video streams.

        Args:
            video_streams (pytube.StreamQuery): video streams.

        Returns:
            list[dict]: A list of supported download types.
        """
        data = DownloadInfoUtility.to_dict(video_streams.all())

        supported_download_types = []
        for stream_type in data:
            if stream_type["type"] == "video":
                try:
                    file_size = video_streams.get_by_resolution(stream_type["res"]).filesize
                    download_info = {stream_type["res"]: file_size}
                    if download_info not in supported_download_types:
                        supported_download_types.append(download_info)
                except Exception as error:
                    print(f"download_info_utility.py : {error}")
                    pass

        try:
            audio_stream = video_streams.get_audio_only()
            file_size = audio_stream.filesize
            audio_bit_rate = f"{str(int(audio_stream.bitrate / 1024))}kbps"
            supported_download_types.append({audio_bit_rate: file_size})
        except Exception as error:
            print(f"download_info_utility.py : {error}")
            pass

        return supported_download_types

    @staticmethod
    def generate_download_options(download_types: List[Dict[str, int]]) -> List[str]:
        """
        Generate download options for CTk combo box based on download types and their sizes.

        Args:
            download_types List[Dict[str, int]]: A dictionary containing download types and their sizes.

        Returns:
            List[str]: A list of combo box values formatted as "type | size".
        """
        download_options = []

        for data_dict in download_types:
            for data_key in data_dict:
                download_options.append(data_key + " | " + ValueConvertUtility.convert_size(data_dict[data_key], 1))

        return download_options

