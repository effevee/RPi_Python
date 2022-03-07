import cv2
import numpy as np

FULLPATH = '/home/pi/RPi_Python/projects/python/MachineLearning/FaceRecog/DataProjectFaces'

# maken van LBPH gezichtsherkennings object
recognizer = cv2.face.createLBPHFaceRecognizer()

# model opladen
recognizer.load(FULLPATH+'/FaceModel.yml')

# histogrammen
#print('histrogrammen:')
#print(recognizer.getHistograms())

# labels
#print('labels:')
#print(recognizer.getLabels())

# eerste histogram
print('1ste histrogram:')
print(recognizer.getHistograms()[0][0])

print('bijhorend label:')
print(recognizer.getLabels()[0][0])