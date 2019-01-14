#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to convert 


@author: alex
"""
#!/bin/bash
# make this a callable script.... and add the gpu number to the port!
# python3 runstuff.py 1 (2 or 3)
import subprocess, sys
import numpy as np
import itertools
import os
import pandas as pd
from pathlib import Path
os.environ['DLClight']="True"

import deeplabcut

def convertpaths2unixstyle(projectname,basepath):
    config=os.path.join(basepath,projectname,'config.yaml')
    #add appending to config path...
    config=os.path.join(basepath,config)
    cfg=deeplabcut.utils.read_config(config)
    
    cfg['project_path']=os.path.join(basepath,projectname) #config.split('config.yaml')[0]
    
    #videos = cfg['video_sets'].keys()
    #video_names = [Path(i).stem for i in videos]

    #folders = [Path(config).parent / 'labeled-data' /Path(i) for i in video_names]
    folders=[os.path.join(cfg['project_path'],'labeled-data',fn) for fn in os.listdir(os.path.join(cfg['project_path'],'labeled-data')) if "_labeled" not in fn]
    print("Creating images with labels by %s." %cfg['scorer'])
    print(folders)
    for folder in folders:
            #try:
            print(os.path.join(str(folder),'CollectedData_' + cfg['scorer'] + '.h5'))
            DataCombined = pd.read_hdf(os.path.join(str(folder),'CollectedData_' + cfg['scorer'] + '.h5'), 'df_with_missing')
            
            DataCombined.to_csv(os.path.join(str(folder),"CollectedData_" + "original" + ".csv"))
            DataCombined.to_hdf(os.path.join(os.path.join(str(folder),'CollectedData_' + "original" + '.h5')),'df_with_missing',format='table', mode='w')

            #frame = pd.DataFrame(a, columns = index, index = self.index)
            
            imindex=[]
            for fn in DataCombined.index:
                imindex.append(os.path.join('labeled-data',folder.split('/')[-1],'img'+fn.split('img')[1]))

            for j,bpt in enumerate(cfg['bodyparts']):
                index = pd.MultiIndex.from_product([[cfg['scorer']], [bpt], ['x', 'y']],names=['scorer', 'bodyparts', 'coords'])
                
                frame = pd.DataFrame(DataCombined[cfg['scorer']][bpt].values, columns = index, index = imindex)
                if j==0:
                    dataFrame=frame
                else:
                    dataFrame = pd.concat([dataFrame, frame],axis=1)
            
            dataFrame.to_csv(os.path.join(str(folder),"CollectedData_" + cfg['scorer'] + ".csv"))
            dataFrame.to_hdf(os.path.join(os.path.join(str(folder),'CollectedData_' + cfg['scorer'] + '.h5')),'df_with_missing',format='table', mode='w')

    deeplabcut.utils.write_config(config,cfg)
    
    return cfg,DataCombined

#path where your project sits (in colaboratory), e.g. see 
# for our example: https://github.com/AlexEMG/DeepLabCut/blob/master/examples/Colab_TrainNetwork_VideoAnalysis.ipynb

basepath='/content/drive/My Drive/DeepLabCut/examples/' 
projectname='Reaching-Mackenzie-2018-08-30'

cfg,DataCombined=convertpaths2unixstyle(projectname,basepath)