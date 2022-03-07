from buildData import BuildData
import cv2
import numpy as np

FULLPATH = '/home/pi/RPi_Python/projects/python/MachineLearning/FaceRecog/DataProjectFaces'

# training set maken en opbouwen
trainSet = BuildData(FULLPATH)
trainSet.build()  # lijst met labels en beelden

# maken van LBPH gezichtsherkennings object
recognizer = cv2.face.createLBPHFaceRecognizer()

# trainen van model
print('Start training ...')
recognizer.train(trainSet.images, np.array(trainSet.labels))
print('Training done')

# opslaan van het model
recognizer.save(FULLPATH+'/'+'/FaceModel.yml')