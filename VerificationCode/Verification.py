# -*- coding:utf-8 -*-
import tesserocr
from PIL import Image
image=Image.open('code.png')
result=tesserocr.image_to_text(image)
print(result)
