import os
import shutil


# 从文档文件夹/data文件夹互相传文件
class FileCopy:
    @staticmethod
    def file_copy(direction: str):
        documents_folder = f'{os.path.expanduser("~/Documents")}\\PyTube Downloader\\'
        current_folder = os.getcwd()
        source_folder = None
        destination_folder = None
        if direction == 'load':
            source_folder = documents_folder
            destination_folder = f'{current_folder}\\data'
        if direction == 'backup':
            source_folder = f'{current_folder}\\data'
            destination_folder = documents_folder

        for item in os.listdir(source_folder):
            source_item = os.path.join(source_folder, item)
            destination_item = os.path.join(destination_folder, item)
            try:
                shutil.copy2(source_item, destination_item)
            except Exception as e:
                print(e)
