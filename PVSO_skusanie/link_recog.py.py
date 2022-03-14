
from tkinter.tix import Tree
from cv2 import circle, sqrt
import numpy as np
import cv2 as cv
import math

def detectConections(lines, tolerance_length, tolerance_coordinates):
    lines_lengths = []
    line_num = 0
    index_number = 0
    linked = []

    # Predpriprava, aby sme spojili ciary, ktore su podobne
    premerged = []
    for line in lines:
        delta_x = line[0][0] - line[0][2]
        delta_y = line[0][1] - line[0][3]
        length = math.sqrt(delta_x**2+delta_y**2)
        fi = int(np.arctan2(delta_y, delta_x) * 180 / np.pi)
        premerged.append((line[0][0],line[0][1],line[0][2],line[0][3],fi,index_number))
        index_number += 1
    

    #Spajanie ciar podla ich uhla a ci su na podobnych suradniciach
    merged = []
    new_line = []
    remove_these = []
    premerged2 = []
    zhoda = True
    break_to_while = False
    #cyklus co sa breakne, ked uz sa ciary nemerguju
    while(zhoda):
        if(break_to_while): #vyrob novy list po tom co si dve mergol
            for line in premerged:
                if (line[5] != remove_these[0] and line[5] != remove_these[1]):
                    premerged2.append(line)
            premerged2.append(new_line)
            premerged = premerged2
            premerged2 = []
        break_to_while = False
        for line in premerged: #zisti ci su nejake mergnutelne
            line_x_mid = (max(line[0], line[2]) - min(line[0], line[2])) / 2
            line_y_mid = (max(line[1], line[3]) - min(line[1], line[3])) / 2
            other_lines = []
            for i in range(len(premerged)):
                if i != line_num:
                    other_lines.append(premerged[i])
            for other in other_lines: #porovnavaj a mergni
                other_x_mid = (max(other[0], other[2]) - min(other[0], other[2])) / 2
                other_y_mid = (max(other[1], other[3]) - min(other[1], other[3])) / 2
                if((line[4] - other[4] < 4 and line[4] - other[4] > -4) and ((line_x_mid - other_x_mid) < 20 or (line_x_mid - other_x_mid) > -20) and ((line_y_mid - other_y_mid) < 20 or (line_y_mid - other_y_mid) > -20)):
                    x_max = max(max(line[0], line[2]),(max(other[0], other[2])))
                    y_max = max(max(line[1], line[3]),(max(other[1], other[3])))
                    x_min = min(min(line[0], line[2]),(min(other[0], other[2])))
                    y_min = min(min(line[1], line[3]),(min(other[1], other[3])))
                    delta_x = x_max - x_min
                    delta_y = y_max - y_min
                    fi = np.arctan2(delta_y, delta_x)
                    new_line = (x_max, y_max, x_min, y_min, int(fi), line[5])
                    remove_these =  (line[5], other[5])
                    break_to_while = True
                    break
            if(break_to_while):
                break
            line_num += 1
        line_num = 0
        if not break_to_while:
            merged = premerged
            break
    

    #Priprava useciek pre dalsie spracovanie
    for line in merged:
        delta_x = line[0][0]- line[0][2]
        delta_y = line[0][1] - line[0][3]
        length = math.sqrt(delta_x**2+delta_y**2)
        lines_lengths.append(((line[0][0],line[0][1]),(line[0][2],line[0][3]),int(length),line_num))
        line_num += 1
    line_num = 0

    # Zlinkuje ktore ciary maju podobnu dlzku (nastavitelne ako presne) a ich suradcnice, kde su spojene
    # Vrati list ciar ktore tvoria tvar, tak mozme predpokladat, ze ide o viacuholnik. nerozozna stvorec od kosostvorca. Bude vediet, ze styri ciary 
    # rovnakej dlzky vytvorili stvoruholnik
    for line_pack in lines_lengths:
        other_lines = []
        for i in range(len(lines_lengths)):
            if i != line_num:
                other_lines.append(lines_lengths[i])
        other_lines_filter1 = []
        for other_line in other_lines:
            if((line_pack[2] - other_line[2] > -tolerance_length) and (line_pack[2] - other_line[2] < tolerance_length)):
                other_lines_filter1.append(other_line)
        for other_line in other_lines_filter1:
            if(line_pack[0][0] - other_line[0][0] > -tolerance_coordinates and line_pack[0][0] - other_line[0][0] < tolerance_coordinates \
                and line_pack[0][1] - other_line[0][1] > -tolerance_coordinates and line_pack[0][1] - other_line[0][1] < tolerance_coordinates):
                   linked.append((line_pack[3],other_line[3]))
            if(line_pack[1][0] - other_line[1][0] > -tolerance_coordinates and line_pack[1][0] - other_line[1][0] < tolerance_coordinates \
                and line_pack[1][1] - other_line[1][1] > -tolerance_coordinates and line_pack[1][1] - other_line[1][1] < tolerance_coordinates):
                   linked.append((line_pack[3],other_line[3]))
        line_num += 1
    return linked

    
                
                
            


img = cv.imread('shapes3.png')
imgGrey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
canny = cv.Canny(imgGrey,125,175)
ret, thrash = cv.threshold(canny, 240, 255, cv.THRESH_BINARY)
contours, hierarchy = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
blank = np.zeros(img.shape, dtype='uint8')

# Skusal som napisat kod, co by detekoval kruhy, ale nefunguje to najlepsie
#
# circles = cv.HoughCircles(imgGrey, cv.HOUGH_GRADIENT, 2, 30, param1=50, param2=30, minRadius=0, maxRadius=100)
# detected_circles = np.uint16(np.around(circles))
# for (x, y, r) in detected_circles[0, :]:
#     cv.circle(img, (x, y), r, (0, 0, 0), 2)

# lines = cv.HoughLines(canny, 1, np.pi/180, 20)
# if lines is not None:
#     for line in lines:
#         rho, theta = line[0]
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a * rho
#         y0 = b * rho
#         x1 = int(x0 + 1000 * -b)
#         y1 = int(y0 + 1000 * a)
#         x2 = int(x0 - 1000 * -b)
#         y2 = int(y0 - 1000 * a)
#         cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
#         cv.line(blank, (x1, y1), (x2, y2), (0, 0, 255), 2)

linesP = cv.HoughLinesP(canny, 1, np.pi/180, 10, None, 25, 40)
if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        cv.line(img, (l[0], l[1]), (l[2], l[3]), (0,i*10,i*10), 3, cv.LINE_AA)
        cv.line(blank, (l[0], l[1]), (l[2], l[3]), (0,i*10,i*10), 3, cv.LINE_AA)
links =  detectConections(linesP,5,7)

# for contour in contours:
#     approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True) #zjednodusi geometriu kontur, cim urobi geometrickke udaje menej zsumene
#     cv.drawContours(img, [approx], 0, (0, 0, 0), 2)
#     x = approx.ravel()[0]
#     y = approx.ravel()[1]
#     if len(approx) <= 12 and cv.arcLength(contour, True) > 50:
#         nazov = str(len(approx)) + "Uholnik"
#         cv.putText(img, nazov, (x, y), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0))
#     else:
#         cv.putText(img, 'Kruh', (x, y), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0))


# cv.drawContours(blank,contours, -1, (0,0,255), 2)
cv.imshow('contures', blank)
cv.imshow('shapes', img)
cv.waitKey(0)
cv.destroyAllWindows()