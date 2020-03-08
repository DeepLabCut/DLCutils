#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 18:08:31 2018

@author: alex
"""

from pathlib import Path
import os, yaml, distutils
import pandas as pd
import numpy as np
from skimage import io

def read_config(config):
    """
    Reads config file
    """
    with open(str(config), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return(cfg)

'''
Attention: this is not completely streamlined, please read carefully. It is assumed that this file 
is in the basepath (see below), where the new project was created.

Preparation steps:

    1. Create a new project (with DLC2 code)
    2. Copy all labeled data files (folders of images) into the labeled-data folder
    3. Copy the CollectedData_scorer.h5 file into the labeled data folder
    4. (Ideally) add the videos from which these folders were extractd to the videos folder (of the new project)
    
Then the following code will chop up the CollectedData_scorer.h5 file and put it in each folder individually. It will
update the body part list and the video_sets list. Note that it is assumed that the second image per folder is cropped just 
like the video itself. [The first image is extracted non-cropped in DLC 1].

The code does not carry over trained networks and other things, as this can be quickly recomputed (and is tricky)
'''


# Edit the variables of the new project:

scorer='Alex'
project='Trailing'
date='2018-10-05'

# edit the body parts according to the old DLC1 project:
bodyparts = ["snout","leftear","rightear","tailbase"]


# set path where the project is:
basepath='/home/alex/'

projectfolder=project+'-'+scorer+'-'+date

path_config_file = os.path.join(projectfolder,'config.yaml')
bflabeledata=os.path.join(basepath,projectfolder,'labeled-data')

videopath=os.path.join(basepath,projectfolder,'videos')

#Load config file and labeled data
cfg = read_config(path_config_file)
DataCombined = pd.read_hdf(os.path.join(bflabeledata,'CollectedData_' + scorer + '.h5'), 'df_with_missing')

# Load folders containing images:
folders = [f for f in os.listdir(bflabeledata) if 'Collected' not in f]
print(folders)

# The next step renames folders with labeled frames
# Thereby, the convection with 'Results' is based on some other DLC version that was not widely circulated
for fn in folders: 
    if 'Results' in fn:
        try:
            os.rename(os.path.join(bflabeledata,fn),os.path.join(bflabeledata,fn.split('Results')[1]))
        except OSError: #directory not empty!
            distutils.dir_util.copy_tree(os.path.join(bflabeledata,fn),os.path.join(bflabeledata,fn.split('Results')[1]))
            print("Merging", os.path.join(bflabeledata,fn))


folders = [f for f in os.listdir(bflabeledata) if 'Collected' not in f]
print("The following folders were found:")
print(folders)


scorer=list(set(DataCombined.columns.get_level_values(0)))[0]
bpts=list(set(DataCombined.columns.get_level_values(1)))

print("Labels and bpts in folder are:", scorer, bpts)
print("MAKE SURE THEY ARE IDENTICAL TO YOUR PROJECT OR EDIT!")



# Update the index to the relative path of the image
for j,fn in enumerate(DataCombined.index):
    if 'Results' in fn:
        DataCombined.index.values[j]=os.path.join('labeled-data',fn.split('Results')[1]) #FULL PATH!
    else:
        DataCombined.index.values[j]=os.path.join('labeled-data',fn) #FULL PATH!for j,fn in enumerate(DataCombined.index):
    
# Extracting data for each folder.
for folder in folders:
    frames2extract=[]
    for j,fn in enumerate(DataCombined.index):
        if folder in fn:
            frames2extract.append(j)
    print("Found", len(frames2extract), "images, saving...")
    
    DF=DataCombined.iloc[frames2extract]
    DF.to_csv(os.path.join(bflabeledata,folder, 'CollectedData_' + scorer + '.csv'))
    DF.to_hdf(os.path.join(bflabeledata,folder, 'CollectedData_' + scorer +".h5"),'df_with_missing',format='table',mode='w')
    
    #adding corresponding video...
    ny,nx,ncols=np.shape(io.imread(os.path.join(projectfolder,DF.index[1])))
    cfg['video_sets'].update({os.path.join(videopath,folder+'.mp4') : {'crop': ', '.join(map(str, [0, nx, 0, ny]))}})

   
#Now update list of bodyparts!
cfg['bodyparts']=bodyparts

with open(str(path_config_file), 'w') as ymlfile:
        yaml.dump(cfg, ymlfile,default_flow_style=False)



