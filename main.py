'''Page segmentation modes: 
O Orientation and script detection (OSD) only
1 Automatic page segmentation with OSD. ‘
2 Automatic page segmentation, but no OSD, or OCR.
3 Fully automatic page segmentation, but no OSD. (Default)
4 Assume a single column of text of variable sizes.
5 Assume a single uniform block of vertically aligned text.
6 Assume a single uniform block of textJ
7 Treat the image as a single text line.
8 Treat the image as a single word.
9 Treat the image as a single word in a circle.
10 Treat the image as a single character.
11 Sparse text. Find as much text as possible in no particular order.
12 Sparse text with OSD.
13 Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract—specific.'''

import pytesseract
import PIL.Image
import cv2

'''
Setting page seg. setting to 11
ocr engine mode to 3
'''
myconfig = r"--psm 11 --oem 3"

'''Get text from image'''
text = pytesseract.image_to_string(PIL.Image.open("images/nyquil-label.png"), config=myconfig)
print(text)

img = cv2.imread("nyquil-label.png")
height, width, _ = img.shape
boxes = pytesseract.image_to_boxes(img, config=myconfig)
for box in boxes.splitlines():
    box = box.split(" ")
    img = cv2.rectangle(img, (int (box[1]), height - int(box[2])), (int(box[3]), height - int(box[4])), (0, 255, 0), 2 )
cv2.imshow("img", img)
cv2.waitKey(0)