
from cv2 import circle
import numpy as np
import cv2 as cv

img = cv.imread('shapes_crop.png')
imgGrey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
canny = cv.Canny(imgGrey,125,175)
ret, thrash = cv.threshold(canny, 240, 255, cv.THRESH_BINARY)
contours, hierarchy = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

# Skusal som napisat kod, co by detekoval kruhy, ale nefunguje to najlepsie
#
# circles = cv.HoughCircles(imgGrey, cv.HOUGH_GRADIENT, 2, 30, param1=50, param2=30, minRadius=0, maxRadius=100)
# detected_circles = np.uint16(np.around(circles))
# for (x, y, r) in detected_circles[0, :]:
#     cv.circle(img, (x, y), r, (0, 0, 0), 2)
for contour in contours:
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True) #zjednodusi geometriu kontur, cim urobi geometrickke udaje menej zsumene
    cv.drawContours(img, [approx], 0, (0, 0, 0), 2)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    if len(approx) <= 12 and cv.arcLength(contour, True) > 50:
        nazov = str(len(approx)) + "Uholnik"
        cv.putText(img, nazov, (x, y), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0))
    else:
        cv.putText(img, 'Kruh', (x, y), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0))

blank = np.zeros(img.shape, dtype='uint8')
cv.drawContours(blank,contours, -1, (0,0,255), 2)
cv.imshow('contures', blank)
cv.imshow('shapes', img)
cv.waitKey(0)
cv.destroyAllWindows()