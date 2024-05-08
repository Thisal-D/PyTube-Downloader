import os

def createDownloadDirectory(path):
    try:
        if not os.path.exists(path):
            sub_paths = path.split("\\")
            for i in range(0, len(sub_paths)):
                sub_path = "\\".join(sub_paths[0:i+1])
                if not os.path.exists(sub_path):
                    os.mkdir(sub_path)
    except Exception:
        raise BufferError("download path errror :/")