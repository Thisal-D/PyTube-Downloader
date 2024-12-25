import os
class scan():
    def __init__(self ,path:str):
        path = path + "/"
        files_or_folders = os.listdir(path)
        files = []
        folders = []
        file_sizes = [] 
        file_count = 0
        folder_count = 0
        total_size = 0
        index = 0 
        files_and_sizes = {}
        while index < len(files_or_folders):
            try:
                file_or_folder = path + files_or_folders[index]
                if os.path.isfile(file_or_folder):
                    files.append(file_or_folder)
                    size_of_file = os.path.getsize(file_or_folder)
                    files_and_sizes[file_or_folder] = str(size_of_file) + " bytes"
                    total_size += size_of_file
                    file_sizes.append(str(size_of_file) + " bytes")
                    file_count += 1
                elif os.path.isdir(file_or_folder):
                    folders.append(file_or_folder)
                    folder_count += 1
                    files_or_folders += [(files_or_folders[index]  + "/" + file_folder_temp) for file_folder_temp in os.listdir(file_or_folder)]
            except Exception as error :
                pass
            index += 1

        self.file_count = file_count
        self.folder_count = folder_count
        self.files = files
        self.folders = folders
        self.file_sizes = file_sizes
        self.files_and_sizes = files_and_sizes
        self.total_size = str(total_size) + " bytes"

    
    
    
files = [file for file in scan("F:\\Codes\\Python\\PyTube Downloader\\PyTube Downloader 2.1.3").files if file.endswith(".py") or file.endswith(".json") and not file.endswith("counter.py") and "test" not in file] 

lines = 0
words = 0
characters = 0
for file in files:
    for line in open(file, "r", encoding="utf-8"):
        lines += 1
        words += len(line.split())
        characters += len(line)
        

print("Lines: " + str(lines))
print("Words: " + str(words))
print("Characters: " + str(characters))

input()
    