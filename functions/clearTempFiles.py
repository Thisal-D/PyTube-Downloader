import os


def clear_temp_files(temp_directory: str) -> None:
    for file in os.listdir(temp_directory):
        try:
            if file != 'this directory is necessary':
                os.remove(f"{temp_directory}\\{file}")
        except Exception as error:
            print("@1 clearTemp.py :", error)
            pass
