# DLCutils

Various scripts to support [DeepLabCut](https://github.com/AlexEMG/DeepLabCut). Feel free to contribute your own analysis methods, and perhaps some short notebook of how to use it. 

Thanks! 

## DLC1 to DLC 2 conversion code

This code allows you to import the labeled data from DLC 1 to DLC 2 projects. Note, it is not streamlined and should be used with care.

https://github.com/AlexEMG/DLCutils/blob/master/convertDLC1TO2.py

Contributed by [Alexander Mathis](https://github.com/AlexEMG)

## Running project created on Windows on Colaboratory

This solves a path problem when creating a project and annotating data on Windows (see https://github.com/AlexEMG/DeepLabCut/issues/172). This functionality will be included in 
a later version of DLC 2.

https://github.com/AlexEMG/DLCutils/blob/master/convertWin2Unix.py

*Usage:* change the 

basepath='/content/drive/My Drive/DeepLabCut/examples/' 
projectname='Reaching-Mackenzie-2018-08-30'

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


Please direct inquires to the **contributors/code-maintainers of that code**. Note that the software(s) are provided "as is", without warranty of any kind, express or implied.
