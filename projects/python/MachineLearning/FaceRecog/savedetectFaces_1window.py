import cv2
from imutils.video import VideoStream
import sys
import time
import PySimpleGUI as sg
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# PySimpleGUI venster layout
layout = [  [sg.Text('Is deze foto OK?')],
            [sg.Image(filename='', key='-image-')],
            [sg.Button('Save'), sg.Button('Exit')] ]

# venster aanmaken
window = sg.Window('Valideer persoon', layout)

# ophalen van driveFolderID
with open('frank_linkFaceRepo.txt', 'r') as f:
    line = f.readline()
    b = line.index('folders/')
    e = line.index('?usp=')
    driveFolderID = line[b+len('folders/'):e]
    print(driveFolderID)

# ophalen van authentication gegevens uit json
gauth = GoogleAuth()

# uitvoeren van authentication
gauth.LocalWebserverAuth()  

# connectie maken met Google Drive
drive = GoogleDrive(gauth)

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

        # als op Save knop is gedrukt
        if event == 'Save' and bw*bh != 0:
            # sla het beeld tijdelijk op
            fname = "face_"+ str(cnt) + ".png"
            print(fname)
            cv2.imwrite(fname, gray[by:by+bh, bx:bx+bw])
            # bestand uploaden naar Google Drive
            imgFile = drive.CreateFile({'parents': [{'id': driveFolderID}]})
            imgFile.SetContentFile(fname)
            imgFile.Upload()
            # lokaal bestand verwijderen
            #os.remove(fname)
            # teller ophogen
            cnt += 1
            if cnt > 1000:
                cnt = 0
                
    except Exception as E:
        print("probleem met capteren beeld of afsluiten App")
        print(E)
