def removeInvalidChars(url:str):
    filename = url
    replaces = ["\\","/",":",'"',"?","<",">","|","*"]
    for re in replaces:
        filename = filename.replace(re,"~")
    return filename