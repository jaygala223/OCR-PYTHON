try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

import cv2
import numpy as np
from numpy import asarray

def ocr_core(filename):

    """print(type(filename)) #<class 'werkzeug.datastructures.FileStorage'>
    print("filename = ",filename)  #filename =  <FileStorage: 'c.png' ('image/png')"""


    Image_file = Image.open(filename) #opening the image using pillow library
    print("Image_file = ",type(Image_file))
    data = asarray(Image_file) #converting image to an array using numpy
    print("data = ",type(data))
    imgUMat = np.float32(data) #converting that array to float32 type
    print("imgUMat = ",type(imgUMat))
    grayImage = cv2.cvtColor(imgUMat, cv2.COLOR_BGR2GRAY) #converting that image to black and white
    print("grayImage = ",type(grayImage))
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY) #thresholding that image using the threshold as 127
    print("blackAndWhiteImage = ",type(blackAndWhiteImage))
    img = Image.fromarray(blackAndWhiteImage) # converting the processed array into an image using fromarray method
    print("img = ",type(img))
    if img.mode == "F": #the image is in float form because we converted it to float before
        img = img.convert('RGB') #since we converted it to float before we are now converting the color space of the image to RGB
    print("img after converting = ",type(img))
    img.show() # showing the image to the user after it is processed optional
    text = pytesseract.image_to_string(img) #sending the converted image to the pytesseract library for ocr recognition


    """file = cv2.imread(filename,0)
    file = cv2.GaussianBlur(file,(5,5),0)
    grayImage = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)
    x = grayImage
    x = Image.fromarray(x)
    if x.mode == "F": #the image is in float form because we converted it to float before
        x = x.convert('RGB')
    x.show()
    #blackAndWhiteImage = cv2.adaptiveThreshold(file,127,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\cv2.THRESH_BINARY,11,2)
    ret3,blackAndWhiteImage = cv2.threshold(file,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img = Image.fromarray(blackAndWhiteImage)
    if img.mode == "F": #the image is in float form because we converted it to float before
        img = img.convert('RGB')
    img.show()
    text = pytesseract.image_to_string(img)"""

    return text #return that text to app.py
