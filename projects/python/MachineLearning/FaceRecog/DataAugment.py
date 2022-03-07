import cv2
import os
import imutils
from PIL import Image
import numpy as np
import random
#gamma transform. Kleine gamma --> donker, grote gamma --> helder
def adjust_gamma(image, gamma=1.0):
   invGamma = 1.0 / gamma
   table = np.array([
      ((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)])
   return cv2.LUT(image.astype(np.uint8), table.astype(np.uint8))

#beeld draaien met een bepaalde hoek
def rotate_ims(path,num_new_ims,angle):
    os.chdir(path)
    ims = os.listdir()
    max_ims = len(ims)-1
    for _ in range(num_new_ims):
        i = random.randint(0,max_ims)
        f=ims[i]
        im=None
        im=cv2.imread(f,cv2.IMREAD_GRAYSCALE)
        if im is None:
            im=Image.open(f)
            im=np.array(im) 
        new_im=imutils.rotate(im,angle=angle)
        name = f[:f.index(".")]+"_rot"+str(angle)+".png"
        cv2.imwrite(name,new_im)

#verwijderen van ruis op een beeld --> hoge frequenties worden weggefilterd
def denoise_ims(path,num_new_ims,min_denoise,max_denoise):
    os.chdir(path)
    ims = os.listdir()
    max_ims = len(ims)-1
    for _ in range(num_new_ims):
        i = random.randint(0,max_ims)
        f=ims[i]
        im=None
        im=cv2.imread(f,cv2.IMREAD_GRAYSCALE)
        if im is None:
            im=Image.open(f)
            im=np.array(im) 
        h=random.randint(min_denoise,max_denoise)
        new_im=cv2.fastNlMeansDenoising(im,h)
        name = f[:f.index(".")]+"_denoise_"+str(h)+".png"
        cv2.imwrite(name,new_im)

#helder of minder helder maken beeld --> gamma<1 --> donker, gamma>1-->lichter
def change_intensity_ims(path,num_new_ims,gamma):
    os.chdir(path)
    ims = os.listdir()
    max_ims = len(ims)-1
    for _ in range(num_new_ims):
        i = random.randint(0,max_ims)
        f=ims[i]
        im=None
        im=cv2.imread(f,cv2.IMREAD_GRAYSCALE)
        if im is None:
            im=Image.open(f)
            im=np.array(im) 
        new_im=adjust_gamma(im, gamma=gamma)
        name=""
        if gamma>1:
            name = f[:f.index(".")]+"_bright.png"
        elif gamma<1:
            name = f[:f.index(".")]+"_dark.png"
        else:
            continue#geen wijziging, dus geen nieuw beeld
        cv2.imwrite(name,new_im)

