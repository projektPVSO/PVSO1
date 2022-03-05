import imp
import cv2 as cv
import numpy as np

def rescaleFrame(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)
    return cv.resize(frame,dimensions,interpolation = cv.INTER_AREA)

def translate(img, x, y):
    trans_mat = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, trans_mat, dimensions)

def rotate(img, angle, rotPoint = None):
    (height, width) = img.shape[:2]
    if rotPoint is None:
        rotPoint = (width//2,height//2)
    rot_mat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width,height)
    return cv.warpAffine(img, rot_mat, dimensions)

img = cv.imread('sisi.png')

# Zmeni velkost
img_resized = rescaleFrame(img,0.7)

# Ciernobiele
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

# Rozmaze
blur = cv.GaussianBlur(img,(3,3),cv.BORDER_DEFAULT)

# Zoberie hrany?
canny = cv.Canny(img,125,175)

# Resize 2
resized = cv.resize(img,(500,500),interpolation= cv.INTER_CUBIC)

# Cropping
cropped =  img[50:200,200:400]

# Posunutie
translated = translate(img,100,30)

# Otocit
rotated = rotate(img, 45)

# flip
flip = cv.flip(img,1)

# contury
gray2 = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
canny2 = cv.Canny(gray2,125,175)
contours, hierarchies = cv.findContours(canny2, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
contours2, hierarchies2 = cv.findContours(canny2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours3, hierarchies3 = cv.findContours(canny2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#print(len(contours),len(contours2),len(contours3))

# Zmena farby contur a nakreslenie do prazdneho
blank = np.zeros(img.shape, dtype='uint8')
cv.drawContours(blank,contours, -1, (0,0,255), 2)

# BGR to Hue Saturation Value
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

#BGR to L*a*b
lab = cv.cvtColor(img, cv.COLOR_BGR2Lab)

#BGR to RGB
rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# split
b, g, r = cv.split(img)



cv.imshow('Mnau',img)
cv.imshow('Cat',r)
# cv.imshow('Catg',g)
# cv.imshow('Catb',b)
cv.waitKey(0)

# cap = cv.VideoCapture(0)
# while True:
#     isTrue, frame = cap.read()
#     #frame = cv.Canny(frame,125,175)
#     cv.imshow('Video', frame)
#     if cv.waitKey(20) & 0xFF == ord('d'):
#         break
# cap.release()
# cv.destroyAllWindows()


