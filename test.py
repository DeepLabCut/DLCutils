import pandas as pd
import os 

from time_in_each_roi import *

# Get data
datafile = "/Users/federicoclaudi/Downloads/c190m615 b vs aDeepCut_resnet50_Network_Training_11Sep11shuffle1_1030000.h5"

data = pd.read_hdf(datafile)
scorer = data.columns.get_level_values(0)[0] #you can read out the header to get the scorer name!
bps = sorted(list(set(data[scorer].columns.get_level_values(0)))) # get the bodyparts names

# Get nose tracking data
pcutoff = 0.5
x, y = data[scorer][bps[1]]['x'].values.flatten(), data[scorer][bps[1]]['x'].values.flatten()

# define rois
from collections import namedtuple
position = namedtuple('position', ['topleft', 'bottomright'])
bp_tracking = np.array((x, y)).T

#two points defining each roi: topleft(X,Y) and bottomright(X,Y).
rois = {'Familiar': position((0, 0), (213.4, 126.76)),'Novel': position((273.5, 339), (480, 480))} 
print(rois)

# get results
print(get_timeinrois_stats(bp_tracking, rois, fps=16, returndf=True))
