from utils import ImageUtility
from PIL import Image

image_path = "assets\\profile images\\https~~~github.com~Thisal-D-normal.png"

ImageUtility.create_image_with_hover_effect(
    image=Image.open(image_path),
    intensity_increase=50
).save("2.png")