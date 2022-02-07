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

        # er is een frame
        if frame is not None:
            cv2.imshow("preview", frame)
        
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
