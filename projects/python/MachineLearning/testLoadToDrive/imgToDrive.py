from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

with open('frank_linkFaceRepo.txt', 'r') as f:
    line = f.readline()
    b = line.index('folders/')
    e = line.index('?usp=')
    driveFolderID = line[b+len('folders/'):e]
    print(driveFolderID)

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)
imgFile = drive.CreateFile({'parents': [{'id': driveFolderID}]})
imgFile.SetContentFile('TEST.jpg')
imgFile.Upload()