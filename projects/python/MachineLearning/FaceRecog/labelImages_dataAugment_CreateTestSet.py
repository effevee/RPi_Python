import os
import shutil
import DataAugment
import random

TEST_PERCENT = 15  # later als test voor gezichtsherkenning
FULLPATH = '/home/pi/RPi_Python/projects/python/MachineLearning/FaceRecog/DataProjectFaces'

# naar de basismap gaan
os.chdir(FULLPATH)

# hoogste label opzoeken voor het geval nieuwe personen achteraf toegevoegd worden
label = 1
labels = []
for d in os.listdir():
    if '_' in d:
        labels.append(int(d[d.index('_')+1:]))
if len(labels)>0:
    label = max(labels) + 1  # label voor nieuwe personen
    
# bestaat de map met test beelden ?
if 'testSet' in os.listdir():
    # verwijder ze
    shutil.rmtree(FULLPATH+'/testSet')

# door de lijst met mappen lopen om labels aan te hangen
for d in os.listdir():
    # sla yml bestand over (training)
    if 'yml' in d:
        continue
    # als de map nog niet hernoemd is
    if not '_' in d:
        # map hernoemen
        os.rename(d, d+'_'+str(label))
    # label ophogen
    label+=1
    
# door de lijst met mappen lopen voor data augmentie (extra bestanden met rotaties, intensiteit, ...)
for d in os.listdir():
    # sla yml bestand over (training)
    if 'yml' in d:
        continue
    # Data augmentatie
    DataAugment.rotate_ims(FULLPATH+'/'+d,2,3)  # 2 nieuwe beelden 3° gedraaid
    DataAugment.rotate_ims(FULLPATH+'/'+d,2,-3) # 2 nieuwe beelden -3° gedraaid
    DataAugment.denoise_ims(FULLPATH+'/'+d,3,12,24) # 3 nieuwe beelden die wat gesmooth worden
    DataAugment.change_intensity_ims(FULLPATH+'/'+d,3,0.5) # 3 nieuwe donkere beelden
    DataAugment.change_intensity_ims(FULLPATH+'/'+d,3,2) # 3 nieuwe lichtere beelden
    
# map voor testbeelden maken
os.chdir(FULLPATH)
os.mkdir('testSet')

# map met testbeelden opvullen
for d in os.listdir():
    # sla yml bestand over (training)
    if 'yml' in d:
        continue
    # map met testbeelden overslaan
    if d == 'testSet':
        continue
    # huidige inhoud van map ophalen
    faces = os.listdir(d)
    faces2id = []
    for i in range(len(faces)):
        faces2id.append(i)
    # bepalen aantal bestanden uit deze map om naar de testset map te kopieren
    num2test = TEST_PERCENT*len(faces)//100
    # ophalen label uit mapnaam vb frank_3 -> 3
    label = d[d.index('_')+1:]
    # lijst met unieke bestand indexen die naar de testSet moeten verplaatst worden
    retrieved = random.sample(faces2id, num2test)
    # bestanden verplaatsen naar testSet
    for r in retrieved:
        shutil.move(FULLPATH+'/'+d+'/'+faces[r],FULLPATH+'/testSet/'+str(label)+'__'+faces[r])
    