import cv2
from imutils.video import VideoStream
import sys
import time

webcam0 = None
piCamera = False

# maken camera object
if piCamera:
    webcam0 = VideoStream(src=0, UsePiCamera=True, resolution=(640,480))
    webcam0.start()
else:
    webcam0 = cv2.VideoCapture(0)
    webcam0.set(3,320)
    webcam0.set(4,240)
    
# HaarCascade object
fullBody_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

# geen camera object
if webcam0 is None:
    print("Probleem met openen van USB-camera")
    sys.exit()

#oneidige lus
while(True):
    try:
        # Capture frame-by-frame
        frame = None
        if piCamera :
            frame = webcam0.read()
        else:
            success, frame = webcam0.read()
        time.sleep(0.005)

        # frame omzetten naar grijswaarde
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # gezichtsdetectie algoritme
        bodies = None
        bodies = fullBody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        # er zijn gezichten gevonden
        if bodies is not None:
             for (x, y, w, h) in bodies:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        # toon frame met rechthoek rond gezicht
        cv2.imshow("Beeld", frame)
        
        # Waits for a user input to quit the application
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # When everything done, release the capture
            if piCamera:
                webcam0.stop()
            cv2.destroyAllWindows()
            sys.exit()
    
    except Exception as E:
        print("probleem met capteren beeld of afsluiten App")
        print(E)
