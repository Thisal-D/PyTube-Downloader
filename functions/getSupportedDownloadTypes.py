import pytube


def toDict(data):
    data_list = []    
    for d in data:
        data_list.append({value.split("=")[0]:value.split("=")[1] for value in str(d)[9:-1].replace('"',"").split(" ")})
    return data_list


def getSupportedDownloadTypes(video_streams: pytube.StreamQuery):
    supportedDownloadTypes = []
    data = toDict(video_streams.all())
    for type_info in data:
        if type_info["type"] == "video":
            try:
                file_size = video_streams.get_by_resolution(type_info["res"]).filesize
                download_info = {type_info["res"] : file_size}
                if download_info not in supportedDownloadTypes:
                    supportedDownloadTypes.append(download_info)
            except:
                #print("Error :",type_info["res"])
                pass
    try:
        audio_only = video_streams.get_audio_only()
        file_size = audio_only.filesize
        bitrate = str(int((audio_only.bitrate)/1024)) + "kbps"
        supportedDownloadTypes.append({bitrate: file_size})
    except:
        pass
        #print("Error :","Audio")
    return supportedDownloadTypes