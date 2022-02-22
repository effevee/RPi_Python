import cv2
from imutils.video import VideoStream
import sys
import time
import PySimpleGUI as sg

# PySimpleGUI venster layout
layout = [  [sg.Text('Is deze foto OK?')],
            [sg.Image(filename='', key='-image-')],
            [sg.Button('Save'), sg.Button('Exit')] ]

# venster aanmaken
window = sg.Window('Valideer persoon', layout)

# maken camera object
webcam0 = None
piCamera = False
if piCamera:
    webcam0 = VideoStream(src=0, UsePiCamera=True, resolution=(640,480))
    webcam0.start()
else:
    webcam0 = cv2.VideoCapture(0)
    webcam0.set(3,320)
    webcam0.set(4,240)
    
# HaarCascade object
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

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
        faces = None
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        # er zijn gezichten gevonden
        x = 0; y = 0; w = 0; h = 0
        if faces is not None:
            print('Aantal gezichten {}'.format(len(faces)))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # gezicht opslaan
                #face = gray[y:y+h, x:x+w]
                #cv2.imwrite('face.png', face)
            
        # toon frame met rechthoek rond gezicht
        # cv2.imshow("Gezicht gevonden", frame)
        
        # wachten op event sg window
        event, values = window.read(timeout=1)

        # Waits for a user input to quit the application
        if event in (None, 'Exit'):
            # When everything done, release the capture
            if piCamera:
                webcam0.stop()
            #cv2.destroyAllWindows()
            window.close()
            sys.exit()

        # toon frame met rechthoek rond gezicht in sg window
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window['-image-'].update(data=imgbytes)

        # als op Save knop is gedrukt
        if event == 'Save' and w*h != 0:
            # sla het beeld op
            cv2.imwrite('test.jpg', gray[y:y+h, x:x+w])
   
    except Exception as E:
        print("probleem met capteren beeld of afsluiten App")
        print(E)
