from .getValidFileName import getValidFileName
from .removeInvalidCharts import removeInvalidChars
from urllib import request
import tkinter
from PIL import Image, ImageDraw


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def getHoverThumbnail(thumbnail_download_path):
    thumbnail_hover_temp = Image.open(thumbnail_download_path)
    thumbnail_hover_path = ".".join(thumbnail_download_path.split(".")[0:-1]) + "-hover." + thumbnail_download_path.split(".")[-1] 
    thumbnail_hover_temp = thumbnail_hover_temp.convert("RGB")
    thumbnail_hover_data = thumbnail_hover_temp.getdata()
    thumbnail_hover_data_list = []
    for item in thumbnail_hover_data:
        item = list(item)
        for index ,i in enumerate(item):
            if i+30  < 256 :
                item[index] = i+30
            else:
                item[index] = 255
        thumbnail_hover_data_list.append(tuple(item))
        
    thumbnail_hover_temp.putdata(thumbnail_hover_data_list)
    #thumbnail_hover_temp.save(thumbnail_hover_path)
    thumbnail_hover_corner_rounded = add_corners(thumbnail_hover_temp,6)
    thumbnail_hover_corner_rounded.save(thumbnail_hover_path)
    thumbnail_hover = tkinter.PhotoImage(file = thumbnail_hover_path)
    return thumbnail_hover


def getThumbnail(video):
    thumbnail_url = video.thumbnail_url
    thumbnail_download_path = getValidFileName("./temp/" + removeInvalidChars(thumbnail_url) + ".png")
    request.urlretrieve(thumbnail_url, thumbnail_download_path)
    
    thumbnail_temp = Image.open(thumbnail_download_path)
    print(thumbnail_temp.width)
    print(thumbnail_temp.height)
    if round(thumbnail_temp.width/4*3) <= 480:
        thumbnail_temp = thumbnail_temp.resize((113, 64),Image.Resampling.LANCZOS).crop((0,8,113,56)).resize((113,64))
    else:
        thumbnail_temp = thumbnail_temp.resize((113,64),Image.Resampling.LANCZOS)#.crop((0,7,110,55))
    #else:
    #    thumbnail_temp = thumbnail_temp.resize((103, 58),Image.Resampling.LANCZOS).crop((0,7,110,55)).resize((97,55))
    thumbnail_temp_corner_rounded = add_corners(thumbnail_temp,6)
    thumbnail_temp_corner_rounded.save(thumbnail_download_path)
    thumbnail = tkinter.PhotoImage(file=thumbnail_download_path)
    return thumbnail, getHoverThumbnail(thumbnail_download_path)

    
def getThumbnails(video):
    return getThumbnail(video)
