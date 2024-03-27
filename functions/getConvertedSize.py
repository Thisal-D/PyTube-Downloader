#convert data to len 3 
def getConvertedSize(s,with_decimal):
    datas = ["B","KB","MB","GB","TB","PB","EB"]
    index= 0
    
    while len(str(int(s))) > 3 and (index+1) < len(datas) :
        s = s /1024
        index += 1
    if with_decimal > 0:
        val = str(round(s,with_decimal)) + " " + datas[index]
    else:
        val = str(int(s)) + " " + datas[index]
    return val
