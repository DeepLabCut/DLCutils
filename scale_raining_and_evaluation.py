#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 14:12:43 2018

An example script to automate analysis on 3 different GPUs for different projects. Feel free to adapt this to your needs!

@author: alex

First start container:
python3 scale_raining_and_evaluation.py 1 (2 or 3)

"""

import subprocess, sys
import numpy as np
import itertools
import os

import deeplabcut

Maxiter=int(1.5*10**5) 

model=int(sys.argv[1])

Projects=[['project1-phoenix-2019-01-28'],['ComplexWheelD3-12-Fumi-2019-01-28', 'maze-ariel-2019-01-28'], ['TBI-BvA-2019-01-28','group-eli-2019-01-28']]

shuffle=1

prefix='/home/alex/DLC-workshopRowland'

for project in Projects[model]:
    projectpath=os.path.join(prefix,project)
    config=os.path.join(projectpath,'config.yaml')
    
    cfg=deeplabcut.auxiliaryfunctions.read_config(config)
    previous_path=cfg['project_path']
    
    cfg['project_path']=projectpath
    deeplabcut.auxiliaryfunctions.write_config(config,cfg)
    
    print("This is the name of the script: ", sys.argv[0])
    print("Shuffle: ", shuffle)
    print("config: ", config)
    
    deeplabcut.create_training_dataset(config, Shuffles=[shuffle],windows2linux=True)
    
    deeplabcut.train_network(config, shuffle=shuffle, max_snapshots_to_keep=5, maxiters=Maxiter)
    print("Evaluating...")
    deeplabcut.evaluate_network(config, Shuffles=[shuffle],plotting=True)

    print("Analyzing videos..., switching to last snapshot...")
    #cfg=deeplabcut.auxiliaryfunctions.read_config(config)
    #cfg['snapshotindex']=-1
    #deeplabcut.auxiliaryfunctions.write_config(config,cfg)
    
    for vtype in ['.mp4','.m4v','.mpg']:
        try:
            deeplabcut.analyze_videos(config,[str(os.path.join(projectpath,'videos'))],shuffle=shuffle,videotype=vtype,save_as_csv=True)
        except:
            pass
    
    print("DONE WITH ", project," resetting to original path")
    cfg['project_path']=previous_path
    deeplabcut.auxiliaryfunctions.write_config(config,cfg)