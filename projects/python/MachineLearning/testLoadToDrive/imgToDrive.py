from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

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

# object maken voor image file
imgFile = drive.CreateFile({'parents': [{'id': driveFolderID}]})

# object opvullen met test image
imgFile.SetContentFile('TEST.jpg')

# uploaden van image naar Google Drive
imgFile.Upload()