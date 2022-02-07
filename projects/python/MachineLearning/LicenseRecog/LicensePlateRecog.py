import os
import cv2
import sys
import numpy as np
import pytesseract # wrapper rond tesseract OCR
import time

# beelden in lijst steken
content = os.listdir("/home/pi/RPi_Python/projects/python/MachineLearning/LicenseRecog/images")
#print(content)

# doorlopen van map met beelden
for fl in content:
    if ".jpg" in fl:
        # beeld inlezen
        im = cv2.imread('images/'+fl)
        # beeld omzetten naar grijswaarden
        imGray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("gray car:"+fl, imGray)
        # neem threshold van het beeld
        ret, imTh = cv2.threshold(imGray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        cv2.imshow("threshold car:"+fl, imTh)
        # nummerplaat contouren zoeken
        contours, hierarchy, _ = cv2.findContours(image=imTh, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)
        print(contours)
        #cv2.imshow("preview", im)
        # wachten op key
        while True:
            key = cv2.waitKey(1) & 0xFF
            # volgend beeld
            if key == ord('n'):
                time.sleep(2)
                break
            # stoppen
            elif key == ord('q'):
                cv2.destroyAllWindows()
                sys.exit()

# programma stoppen
time.sleep(5)
cv2.destroyAllWindows()