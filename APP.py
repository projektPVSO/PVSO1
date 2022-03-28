from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QDialog
from PyQt5 import uic
import sys
import cv2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui, QtWidgets

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import colorsys
from numpy.linalg import norm

buffer = 32

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
#greenUpper = (225, 100, 70)

pts = deque(maxlen=buffer)
counter = 0
(dX, dY) = (0, 0)
direction = ""

time.sleep(2.0)




class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        #Dialog.resize(815, 538)
        self.imgLabel_1 = QtWidgets.QLabel(Dialog)
        self.imgLabel_1.setGeometry(QtCore.QRect(150, 80, 471, 441))
        self.imgLabel_1.setAutoFillBackground(False)
        self.imgLabel_1.setFrameShape(QtWidgets.QFrame.Box)
        self.imgLabel_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgLabel_1.setLineWidth(2)
        self.imgLabel_1.setScaledContents(True)
        self.imgLabel_1.setObjectName("imgLabel_1")
        self.SHOW = QtWidgets.QPushButton(Dialog)
        self.SHOW.setGeometry(QtCore.QRect(10, 80, 71, 31))
        self.SHOW.setObjectName("SHOW")
        self.CAPTURE = QtWidgets.QPushButton(Dialog)
        self.CAPTURE.setGeometry(QtCore.QRect(10, 120, 131, 51))
        self.CAPTURE.setObjectName("CAPTURE")
        self.TEXT = QtWidgets.QTextBrowser(Dialog)
        self.TEXT.setGeometry(QtCore.QRect(10, 10, 256, 61))
        self.TEXT.setObjectName("TEXT")


        self.imgLabel_4 = QtWidgets.QLabel(Dialog)
        self.imgLabel_4.setGeometry(QtCore.QRect(630, 400, 151, 121))
        self.imgLabel_4.setFrameShape(QtWidgets.QFrame.Box)
        self.imgLabel_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgLabel_4.setLineWidth(2)
        self.imgLabel_4.setScaledContents(True)
        self.imgLabel_4.setObjectName("imgLabel_4")
        self.TEXT_2 = QtWidgets.QTextBrowser(Dialog)
        self.TEXT_2.setGeometry(QtCore.QRect(10, 210, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.TEXT_2.setFont(font)
        self.TEXT_2.setObjectName("TEXT_2")
        self.TEXT_3 = QtWidgets.QTextBrowser(Dialog)
        self.TEXT_3.setGeometry(QtCore.QRect(10, 270, 101, 31))
        self.TEXT_3.setObjectName("TEXT_3")
        self.TEXT_4 = QtWidgets.QTextBrowser(Dialog)
        self.TEXT_4.setGeometry(QtCore.QRect(10, 310, 101, 31))
        self.TEXT_4.setObjectName("TEXT_4")
        self.TEXT_5 = QtWidgets.QTextBrowser(Dialog)
        self.TEXT_5.setGeometry(QtCore.QRect(10, 350, 101, 31))
        self.TEXT_5.setObjectName("TEXT_5")
        self.TEXT_6 = QtWidgets.QTextBrowser(Dialog)
        self.TEXT_6.setGeometry(QtCore.QRect(90, 80, 51, 31))
        self.TEXT_6.setObjectName("TEXT_6")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 189, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.imgLabel_1.setText(_translate("Dialog", "TextLabel"))
        self.SHOW.setText(_translate("Dialog", "Show"))
        self.CAPTURE.setText(_translate("Dialog", "Capture Screen Shot"))
        #self.imgLabel_2.setText(_translate("Dialog", "TextLabel"))
        #self.imgLabel_3.setText(_translate("Dialog", "TextLabel"))
        self.imgLabel_4.setText(_translate("Dialog", "TextLabel"))
        self.label.setText(_translate("Dialog", "Center Coordinate"))


class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        
        self.ui.SHOW.clicked.connect(self.controlTimer)
        
        self.logic = 0
        self.value = 1
        self.ui.CAPTURE.clicked.connect(self.CaptureClicked)
        clicked = False
        #--------
        self.clicked = False
        self.first= False
        self.auto=False
        self.r = 0
        self.g = 0
        self.b = 0
        self.x_pos = 0
        self.y_pos = 0
        self.kernel = np.ones((5,5), np.uint8) 

        self.lower_blue = np.array([30, 30, 30])
        self.upper_blue = np.array([40, 40, 40])
        self.brightness


        global xs, ys
    
    def CaptureClicked(self):
        self.logic =2
    
    def mouseDoubleClickEvent(self, event):
        ret, image = self.cap.read()
        
        # convert image to RGB format
        imageFrame = imutils.resize(image, width=600)

        frameG = cv2.GaussianBlur(imageFrame, (7,7), 0)#cv2.medianBlur(frame, 21)#
        frameG = cv2.erode(frameG, self.kernel, iterations = 2)
        frameG = cv2.dilate(frameG, self.kernel, iterations = 1)
        global b,g,r
        y=event.x()-70
        x=event.y()-85
        b, g, r = frameG[x, y]
        # vector of chosen colors
        self.b=int(b)
        self.g=int(g)
        self.r=int(r) 
        
    def brightness(self,img):
        if len(img.shape) == 3:
            # Colored RGB or BGR (*Do Not* use HSV images with this function)
            # create brightness with euclidean norm
            return np.average(norm(img, axis=2)) / np.sqrt(3)
        else:
            # Grayscale
            return np.average(img)     
        
        
    def viewCam(self):
        self.ui.TEXT.setText('Kindle Press "Capture Image" to capture image')
        
        # read image in BGR format
        ret, imageFrame = self.cap.read()
        
        # convert image to RGB format
        imageFrame = imutils.resize(imageFrame, width=600)
        br=self.brightness(imageFrame)
        print(br)
        frameG = cv2.GaussianBlur(imageFrame, (7,7), 0)#cv2.medianBlur(frame, 21)#
        frameG = cv2.erode(frameG, self.kernel, iterations = 2)
        frameG = cv2.dilate(frameG, self.kernel, iterations = 1)
        
        #if clicked:

        hsv = cv2.cvtColor(frameG, cv2.COLOR_BGR2HSV)
        h,s,v=colorsys.rgb_to_hsv(self.r/255, self.g/255, self.b/255)
        h=h*360

        self.lower_blue = np.array([(h-11)/360*179, (s-0.3)*255, (v-0.2)*255])
        self.upper_blue = np.array([(h+11)/360*179, (s+0.3)*255, (v+0.2)*255])
        mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue) 


        clicked = False

        hsv = cv2.cvtColor(frameG, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue) 

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) > 1000:
                x, y, width, height = cv2.boundingRect(cnt)

                imageFrame=cv2.rectangle(imageFrame, (x , y), (x + width, y + height),(0, 0, 255), 2)

                xs=int(x+width/2)
                ys=int(y+height/2)

                cv2.rectangle(imageFrame,(xs,ys),(xs+2,ys+2),(255,0,255),3)

        
        # get image RGB
        height, width, channel = imageFrame.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(imageFrame.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.imgLabel_1.setPixmap(QPixmap.fromImage(qImg))
        

        # get image mask
        height_4, width_4= mask.shape
        step_4 = 3 * width_4                                                      # dont need step -> int bytesPerLine
        qImg_4 =  QImage(mask.data, width_4, height_4, QImage.Format_Grayscale8)  # link ref https://qt.developpez.com/doc/4.7/qimage/ ; https://doc.qt.io/qt-5/qimage.html
        self.ui.imgLabel_4.setPixmap(QPixmap.fromImage(qImg_4))
    
        if(self.logic==2):   
            self.value = self.value + 1
            self.ui.TEXT_3.setText("Capture")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imwrite('C:/Users/Hoang Image Win/Desktop/1_Image_Processing/1_Image_processing/1_GUI_pyQt5_webcam/hoang.png',image)
            self.logic=1       
    
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.TEXT_6.setText("Running")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.TEXT_6.setText("Stop")
        
        

                
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec_())
    
