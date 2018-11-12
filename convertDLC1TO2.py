#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 18:08:31 2018

@author: alex
"""

'''
Steps:
    1. copy all labeled data files (folders of images) + CollectedData_user.h5 files to labeled-data
    
'''



from pathlib import Path
import os, yaml, distutils
import pandas as pd
import numpy as np
from skimage import io

'''
#First create the project:
scorer='Mackenzie'
project='openfield
pcf=deeplabcut.create_new_project(project,scorer,['/home/alex/Hacking/DLCutils/m3v1mp4.mp4'],copy_videos=True)

'''
    
def read_config(config):
    """
    Reads config file
    """
    with open(str(config), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return(cfg)

scorer='Mackenzie'
project='openfield'
date='2018-10-30'

#path_config_file=deeplabcut.create_new_project(project,scorer,['/home/alex/Hacking/Social_Behavior/1802202_Day6 Dummy_DeepLabCutlabeled.mp4'],copy_videos=False)

basepath='/home/alex/Hacking/DLCutils'
projectfolder=project+'-'+scorer+'-'+date
path_config_file = os.path.join(projectfolder,'config.yaml')
bflabeledata=os.path.join(basepath,projectfolder,'labeled-data')


#Load config file and labeled data
cfg = read_config(path_config_file)
DataCombined = pd.read_hdf(os.path.join(bflabeledata,'CollectedData_' + scorer + '.h5'), 'df_with_missing')

# load folders containing images:
folders = [f for f in os.listdir(bflabeledata) if 'Collected' not in f]
print(folders)

for fn in folders: #rename folders (old DLC1.2 convention)
    if 'Results' in fn:
        try:
            os.rename(os.path.join(bflabeledata,fn),os.path.join(bflabeledata,fn.split('Results')[1]))
        except OSError: #directory not empty!
            distutils.dir_util.copy_tree(os.path.join(bflabeledata,fn),os.path.join(bflabeledata,fn.split('Results')[1]))
            print("Merging", os.path.join(bflabeledata,fn))
            #NOW DELETE!!!

#%%

folders = [f for f in os.listdir(bflabeledata) if 'Collected' not in f]
print(folders)


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
    #ny,nx,ncols=np.shape(io.imread(os.path.join(projectfolder,DF.index[0])))
    #cfg['video_sets'].update({os.path.join(videopath,folder+'.mp4') : {'crop': ', '.join(map(str, [0, nx, 0, ny]))}})

#%%
    
#Now update list of bodyparts!
bodyparts = ["snout","leftear","rightear","shoulder"]

cfg['bodyparts']=bodyparts

with open(str(path_config_file), 'w') as ymlfile:
        yaml.dump(cfg, ymlfile,default_flow_style=False)



