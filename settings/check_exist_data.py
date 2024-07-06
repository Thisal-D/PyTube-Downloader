import os
from utils import FileCopy


class CheckExistData:
    @staticmethod
    def check_exist_data():

        documents_folder = f'{os.path.expanduser("~/Documents")}\\PyTube Downloader\\'
        if not os.path.exists(documents_folder):
            os.mkdir(documents_folder)
        else:
            FileCopy.file_copy('load')
