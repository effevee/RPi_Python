import cv2
from imutils.video import VideoStream
import sys
import time
import PySimpleGUI as sg
import os

FULLPATH = '/home/pi/RPi_Python/projects/python/MachineLearning/FaceRecog/DataProjectFaces'

# naar de basismap gaan
os.chdir(FULLPATH)

# dictionary labels + namen
label_name = {}
for d in os.listdir():
    if '_' in d:
        name = d[:d.index('_')]
        label = int(d[d.index('_')+1:])
        label_name.update({label:name})
label_name.update({-1:'onbekend'})
print(label_name)

# maken van LBPH gezichtsherkennings object
recognizer = cv2.face.createLBPHFaceRecognizer()

# model opladen
recognizer.load(FULLPATH+'/FaceModel.yml')
recognizer.setThreshold(100)

# PySimpleGUI venster layout
layout = [  [sg.Text('Welkom:', key='-text-')],
            [sg.Image(filename='', key='-image-')] ]

# venster aanmaken
window = sg.Window('Herken persoon', layout)

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
face_cascade = cv2.CascadeClassifier('/home/pi/RPi_Python/projects/python/MachineLearning/FaceRecog/haarcascade_frontalface_default.xml')

# geen camera object
if webcam0 is None:
    print("Probleem met openen van USB-camera")
    sys.exit()

#oneidige lus
cnt = 0
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
        bx = 0; by = 0; bw = 0; bh = 0
        if faces is not None:
            print('Aantal gezichten {}'.format(len(faces)))
            for (x, y, w, h) in faces:
                # enkel het grootste gezicht 
                if w*h > bw*bh:
                    bx = x; by = y; bw = w; bh = h
                    print('gezicht {} {} {} {}'.format(bx, by, bw, bh))
                cv2.rectangle(frame, (bx, by), (bx+bw, by+bh), (0, 255, 0), 2)

                # gezicht opslaan
                # face = gray[y:y+h, x:x+w]
                # cv2.imwrite('face.png', face)
            
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

        # indien beeld, dan proberen te herkennen
        if bw*bh != 0:
            # voorspelling
            res = recognizer.predict(gray[by:by+bh, bx:bx+bw])
            # naam updaten in SimpleGUI window
            window["-text-"].update("Welkom: "+label_name[res[0]]+"("+str(res[1])+")")
            # sla het beeld tijdelijk op
            #fname = "face_"+ str(cnt) + ".png"
            #print(fname)
            #cv2.imwrite(fname, gray[by:by+bh, bx:bx+bw])
                
    except Exception as E:
        print("probleem met capteren beeld of afsluiten App")
        print(E)
