import tesserocr
from PIL import Image
image=Image.open('D:\PycharmProjects\AllProjects\VerificationCode\code.jpg')
# result=tesserocr.image_to_text(image)
# print(result)
image.show()