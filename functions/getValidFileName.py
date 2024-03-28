import os


def getValidFileName(path):
    splited = path.split(".")
    file_name ,extenstion = ".".join(splited[0:-1]),splited[-1]
    generate_file_name = file_name
    i = 2
    while os.path.exists(generate_file_name+"."+extenstion):
        generate_file_name = file_name + " ({})".format(i)
        i += 1
    return generate_file_name + "." + extenstion