import cv2
import numpy as np

# Ak problem tak skonci
def nothing(x):
    pass
# Nastavenie kamery
cap = cv2.VideoCapture(0)

# Nastavenie kernel
kernel = np.ones((5,5), np.uint8) 
kernel2 = np.ones((10,10), np.uint8) 
a=1
b=1

# Progam
while True:
    _, imageFrame = cap.read() # citanie obrazu
    
    # filtracia
    frameG = cv2.GaussianBlur(imageFrame, (7,7), 0)#cv2.medianBlur(frame, 21)#
    frameG = cv2.erode(frameG, kernel, iterations = 2)
    frameG = cv2.dilate(frameG, kernel, iterations = 1)
    hsv = cv2.cvtColor(frameG, cv2.COLOR_BGR2HSV)
    
    a = cv2.getTrackbarPos("0 - 10", "Trackbars")
    b = cv2.getTrackbarPos("0 - 10", "Trackbars")
    
    # Rozsah
    red_lower = np.array([145, 0, 195], np.uint8) 
    red_upper = np.array([179, 255, 255], np.uint8) 
    red_mask = cv2.inRange(hsv, red_lower, red_upper) 

    # Rozsah
    green_lower = np.array([45, 64, 142], np.uint8) 
    green_upper = np.array([75, 255, 255], np.uint8) 
    green_mask = cv2.inRange(hsv, green_lower, green_upper) 

    # Rozsah
    blue_lower = np.array([90, 180, 169], np.uint8) 
    blue_upper = np.array([179, 255, 255], np.uint8) 
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper) 
    
    #lower_blue = np.array([l_h, l_s, l_v])
    #upper_blue = np.array([u_h, u_s, u_v])
    
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    #fgmask = cv2.erode(mask, kernel, iterations = 3)
    #fgmask = cv2.dilate(fgmask, kernel, iterations = 2)
    
    
    #Blue--------------------------------------
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:

        # Urcenie obsahu utvaru
        if cv2.contourArea(cnt) > 2000:

            # Urcenie rozmerou stvorca
            x, y, width, height = cv2.boundingRect(cnt)

            # Kreslenie stvorca
            imageFrame=cv2.rectangle(imageFrame, (x , y), (x + width, y + height),(0, 0, 255), 2)
            
            # Text
            cv2.putText(imageFrame, 'Blue', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            
    #Red------------------------------------
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        # Urcenie obsahu utvaru
        if cv2.contourArea(cnt) > 2000:

            # Urcenie rozmerou stvorca
            x, y, width, height = cv2.boundingRect(cnt)

            # Kreslenie stvorca
            imageFrame=cv2.rectangle(imageFrame, (x , y), (x + width, y + height),(0, 0, 255), 2)
            
            # Text
            cv2.putText(imageFrame, 'Red', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            
    #Green----------------------------------        
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        # Urcenie obsahu utvaru
        if cv2.contourArea(cnt) > 2000:

            # Urcenie rozmerou stvorca
            x, y, width, height = cv2.boundingRect(cnt)

            # Kreslenie stvorca
            imageFrame=cv2.rectangle(imageFrame, (x , y), (x + width, y + height),(0, 0, 255), 2)
            
            # Text
            cv2.putText(imageFrame, 'Green', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    
    
    result = cv2.bitwise_and(imageFrame, imageFrame, mask=fgmask)
    cv2.imshow("frame", imageFrame)

    
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
