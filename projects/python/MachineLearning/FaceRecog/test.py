from buildData import BuildData
import cv2
import numpy as np

FULLPATH = '/home/pi/RPi_Python/projects/python/MachineLearning/FaceRecog/DataProjectFaces'

# test set maken en opbouwen
testSet = BuildData(FULLPATH, test='testSet')
testSet.build()  # lijst met labels en beelden

# maken van LBPH gezichtsherkennings object
recognizer = cv2.face.createLBPHFaceRecognizer()

# model opladen
recognizer.load(FULLPATH+'/FaceModel.yml')
recognizer.setThreshold(35)

# door de test set lopen
i = 0
for im in testSet.images:
    res = recognizer.predict(im)
    print('echt label:', testSet.labels[i], 'voorspelling:', res, 'bestand:', testSet.test_filename[i])
    i+=1

print(recognizer.getThreshold())