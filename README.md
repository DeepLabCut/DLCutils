
[![Image.sc forum](https://img.shields.io/badge/dynamic/json.svg?label=forum&amp;url=https%3A%2F%2Fforum.image.sc%2Ftags%2Fdeeplabcut.json&amp;query=%24.topic_list.tags.0.topic_count&amp;colorB=brightgreen&amp;&amp;suffix=%20topics&amp;logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAABPklEQVR42m3SyyqFURTA8Y2BER0TDyExZ+aSPIKUlPIITFzKeQWXwhBlQrmFgUzMMFLKZeguBu5y+//17dP3nc5vuPdee6299gohUYYaDGOyyACq4JmQVoFujOMR77hNfOAGM+hBOQqB9TjHD36xhAa04RCuuXeKOvwHVWIKL9jCK2bRiV284QgL8MwEjAneeo9VNOEaBhzALGtoRy02cIcWhE34jj5YxgW+E5Z4iTPkMYpPLCNY3hdOYEfNbKYdmNngZ1jyEzw7h7AIb3fRTQ95OAZ6yQpGYHMMtOTgouktYwxuXsHgWLLl+4x++Kx1FJrjLTagA77bTPvYgw1rRqY56e+w7GNYsqX6JfPwi7aR+Y5SA+BXtKIRfkfJAYgj14tpOF6+I46c4/cAM3UhM3JxyKsxiOIhH0IO6SH/A1Kb1WBeUjbkAAAAAElFTkSuQmCC)](https://forum.image.sc/tags/deeplabcut) 
# DLCutils 
Various scripts to support [DeepLabCut](https://github.com/AlexEMG/DeepLabCut). Feel free to contribute your own analysis methods, and perhaps some short notebook of how to use it. Thanks! 


## Example scripts for automation of anlysis & training

These two scripts illustrate how to train, test and analyze videos for multiple projects automatically (scale_raining_and_evaluation.py) and
how to analyze videos that are organized in subfolders automatically (scale_analysis_oversubfolders.py). Feel free to adjust them for your needs!

https://github.com/AlexEMG/DLCutils/blob/master/scale_analysis_oversubfolders.py
https://github.com/AlexEMG/DLCutils/blob/master/scale_raining_and_evaluation.py

Contributed by [Alexander Mathis](https://github.com/AlexEMG)



## DLC1 to DLC 2 conversion code

This code allows you to import the labeled data from DLC 1 to DLC 2 projects. Note, it is not streamlined and should be used with care.

https://github.com/AlexEMG/DLCutils/blob/master/convertDLC1TO2.py

Contributed by [Alexander Mathis](https://github.com/AlexEMG)

## Running project created on Windows on Colaboratory
#UPDATE: as of Deeplabcut 2.0.4 you no longer need to use this code! You can simply create the training set on the cloud and it will automatically convert your project for you. 

   - This solves a path problem when creating a project and annotating data on Windows (see https://github.com/AlexEMG/DeepLabCut/issues/172). This functionality will be included in 
a later version of DLC 2 (DONE!)
https://github.com/AlexEMG/DLCutils/blob/master/convertWin2Unix.py

*Usage:* change in lines 70 and 71 of https://github.com/AlexEMG/DLCutils/blob/master/convertWin2Unix.py

```basepath='/content/drive/My Drive/DeepLabCut/examples/'``` 

```projectname='Reaching-Mackenzie-2018-08-30'```

then run this script on colaboratory after uploading your labeled data to the drive. Thereby it will be converted
to unix format, then create a training set (with deeplabcut) and proceed as usual...

Contributed by [Alexander Mathis](https://github.com/AlexEMG)

## Time spent of a body part in a particular region of interest (ROI)

https://github.com/AlexEMG/DLCutils/blob/master/time_in_each_roi.py

Contributed by [Federico Claudi](https://github.com/FedeClaudi)

## Behavior clustering with MotionMapper 
- (adpated from https://github.com/gordonberman/MotionMapper)

https://github.com/AlexEMG/DLCutils/tree/master/DLC_2_MotionMapper

Contributed by [Mackenzie Mathis](https://github.com/MMathisLab)


## Using DeepLabCut for USB-CGPIO feedback 
paper: https://www.biorxiv.org/content/early/2018/11/28/482349
code: https://github.com/bf777/DeepCutRealTime

maintainer: [Brandon Forys](https://github.com/bf777)

## Pupil Tracking 
- From Tom Vaissie - tvaissie@scripps.edu
- Please see the README.txt file https://github.com/AlexEMG/DLCutils/tree/master/pupilTracking for details; this code makes the video in case study 7 http://www.mousemotorlab.org/deeplabcut/. 


Please direct inquires to the **contributors/code-maintainers of that code**. Note that the software(s) are provided "as is", without warranty of any kind, express or implied.

