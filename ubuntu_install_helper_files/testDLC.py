import deeplabcut
import os


configpath=os.path.join('/home/neudata/Desktop/DeepLabCut/examples/openfield-Pranav-2018-10-30/config.yaml')

deeplabcut.load_demo_data(configpath)

deeplabcut.train_network(configpath,maxiters=5) #trains for 5 iterations


#manually test GUI... 
deeplabcut.label_frames(configpath)
