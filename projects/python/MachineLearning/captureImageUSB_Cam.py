import cv2
from imutils.video import VideoStream
import sys
import time

webcam0 = None
piCamera = False

# maken camera object
if piCamera:
    webcam0 = VideoStream(src=0, UsePiCamera=True)
else:
    webcam0 = VideoStream(src=0)

# geen camera object
if webcam0 is None:
    print("Probleem met openen van USB-camera")
    sys.exit()

# videostream starten
webcam0.start()

#oneidige lus
while(True):
    try:
        # Capture frame-by-frame
        frame = webcam0.read()
        time.sleep(0.005)

        # er is een frame
        if frame is not None:
            cv2.imshow("preview", frame)
        
        # Waits for a user input to quit the application
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # When everything done, release the capture
            webcam0.stop()
            cv2.destroyAllWindows()
            sys.exit()
    
    except Exception as E:
        print("probleem met capteren beeld of afsluiten App")
        print(E)
