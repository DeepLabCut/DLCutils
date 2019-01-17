########################################################################
# Create video with trace from DLC using python and Adobe Premiere Pro
# DLC analysis was done on Ubuntu 16.04 with Docker
# Data anlaysis and video montage on Windows due to easier access to Adobe products 
########################################################################

# DLC analysis
##############
training on 40 frames

# extract the data
##################
# in the command line cmd
C:\>ipython pupilDLC.py

# generate the video
#####################
# in the command line convert frames to video with ffmpeg
# go to the folder where DLC extracted the video frames # this is necessary as output labeled video may not read well in Adobe Premiere

C:\> cd C:\Users\Windows\Desktop\000-DLC\e3pupil\temp-e3v8114-20181221T1225-1235
C:\> ffmpeg -r 30 -f image2 -s 1280x720 -i file%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4

Open the pupilDLC.prproj to edit video


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# side notes for Adobe Premiere Pro
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

Adobe Premier Pro
* Import test.mp4
	* note the the video can be cropped later on if need be
* drag files to be edited in the Project
* drag files to work on in the sequence to the bottom 
* chose Clip>Speed/Duration (Ctl+R)
	* change the speed to 8000% for pupil
	* make sure it is link between time and speed %
* use the pen tool to create a line in Effec Controls:
	* Switch stroke
* go to effects
* Effects search for transform
* Drag Transform onto the Video/object layer of interest in the Sequence (purple/pink bar)
* Scale the trace for the amount of space you want to occupy
* go to Effects
* Effects search for Crop
* Drag Crop onto the Video/object layer of interest in the Sequence (purple/pink bar)
* Go to right
	* start video at 0 begining of the trace for cropping
	* push the clock on the right hand side
	* perform same operation for the end
* To add text select the text object on the side of the sequence
	* edit the object in the effect window
* To add timecode
	* go to effects 
	* Effects search for timecode 

## Notes 
* important if the PUT THE CROP Layer above TRANSFORM Layer
* Make sure the trace is going from edges to edge no margin