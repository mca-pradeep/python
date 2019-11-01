# import os
# import tempfile
# import subprocess
#
# def ocr(path):
#     temp = tempfile.NamedTemporaryFile(delete=False)
#
#     process = subprocess.Popen(['pytesseract', path, temp.name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     process.communicate()
#     print (temp);
#     with open(temp.name + '.txt', 'r') as handle:
#         contents = handle.read()
#
#     #os.remove(temp.name + '.txt')
#     #os.remove(temp.name)
#
#     return contents
#
# str = ocr('../image.jpg')
# print(str)

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
print(pytesseract.image_to_string(Image.open('../image.jpg')))
