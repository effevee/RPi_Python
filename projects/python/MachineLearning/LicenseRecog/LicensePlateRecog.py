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
        #cv2.imshow("gray car: "+fl, imGray)
        
        # neem threshold van het beeld
        # param 1 : beeld
        # param 2 : threshold 0 = eenvoudige threshold
        # param 3 : waarde wanneer threshold overschreden wordt (255 = wit)
        # param 4 : threshold methode : zwart/wit met methode van Otsu
        ret, imTh = cv2.threshold(imGray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        cv2.imshow("threshold car: "+fl, imTh)
        
        # blobs analyse (witte vlakken)
        # param 1 : blob
        # param 2 : mode
        # param 3 : methode 
        contours, hierarchy, _ = cv2.findContours(image=imTh, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)
        print(contours)
        for c in contours:
            # rechthoek rond de blob
            x, y, w, h = cv2.boundingRect(c)
            print(x,y,w,h)
            ratio = w/h
            aRect = w*h
            aC = cv2.contourArea(c)
            extent = aC/aRect
            # filteren op blobs die rechthoekig en langwerpig zijn
            if ratio>2 and ratio<10 and aRect>1200 and aRect<800000and extent>=0.8:
                # informatie blob
                print("OK: ratio {} - opp rechthoek {} - extent {}".format(ratio, aRect, extent))
                # teken contouren
                cv2.drawContours(image=im, contours=[c], contourIdx=-1, color=(0, 255, 0),thickness=2, lineType=LINE_8)
                # toon beeld met contouren
                cv2.imshow("Contours: "+fl, im)
                # nummerplaat detectie
                aPlate = im[y:y+h, x:x+w]
                cv2.imshow("Nummerplaat: "+fl, aPlate)
                print("Nummerplaat:"+fl, pytesseract.image_to_string(aPlate, config='--psm 13'))
        
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