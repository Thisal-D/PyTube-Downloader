import pytube


def to_dict(data) -> list[dict]:
    data_list = []
    for d in data:
        data_list.append(
            {value.split("=")[0]: value.split("=")[1] for value in str(d)[9:-1].replace('"', "").split(" ")})
    return data_list


def get_supported_download_types(video_streams: pytube.StreamQuery) -> list[dict]:
    data = to_dict(video_streams.all())

    support_download_types = []
    for stream_type in data:
        if stream_type["type"] == "video":
            try:
                file_size = video_streams.get_by_resolution(stream_type["res"]).filesize
                download_info = {stream_type["res"]: file_size}
                if download_info not in support_download_types:
                    support_download_types.append(download_info)
            except Exception:
                pass

    try:
        audio_stream = video_streams.get_audio_only()
        file_size = audio_stream.filesize
        audio_bit_rate = f"{str(int(audio_stream.bitrate / 1024))}kbps"
        support_download_types.append({audio_bit_rate: file_size})
    except Exception:
        pass

    return support_download_types
