import os
import cv2
from PIL import Image
import numpy

class BuildData:
    
    def __init__(self,location,test=""):
        self.labels = []
        self.images = []
        self.test_filename = []
        self.loc = location
        self.test = test
    
    def build(self):
        os.chdir(self.loc)
        if self.test != "": #build testset
            os.chdir(self.test)
            for f in os.listdir():
                label = f[:f.index("__")]
                file = f[f.index("__"):f.index(".")]
                self.labels.append(int(label))
                self.test_filename.append(file)
                im = Image.open(f)
                im=numpy.array(im) 
                self.images.append(im)
            return True
        
        for d in os.listdir():
            if "test" in d:
                continue
            if ".yml" in d:
                continue
            label = d[d.index("_")+1:]
            os.chdir(d)
            for f in os.listdir():
                im = Image.open(f)
                im=numpy.array(im)
                self.images.append(im)
                self.labels.append(int(label))
            os.chdir("..")
        return True
