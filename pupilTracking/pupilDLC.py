# libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# data selection
path = input('path to csv files (eg. C:\\Users\\) :') #C:\Users\Windows\Desktop
path = os.path.normpath(path)
os.chdir(path)
files = [os.path.join(path, file) for file in os.listdir(path)
			if file.endswith('.csv')]
print(files)
i = input('which file to selecet (eg: 0 or 1) ?')
i = int(i)

# dataset
df = pd.read_csv(files[i])  # store the csv file in dataframe df
df = df.iloc[2:len(df.index), np.r_[0,1,2,4,5,7,8,10,11]]  # subselect dataframe
df.columns = ['frame','x1x','x1y','x2x','x2y','y1x','y1y','y2x','y2y']
df = df.convert_objects(convert_numeric=True)
df = df.assign(diamH = ((df.x2x-df.x1x)**2 + (df.x2y-df.x1y)**2)**0.5, diamV = ((df.y2x-df.y1x)**2 + (df.y2y-df.y1y)**2)**0.5) #obtain horizontal and vertucak pupil diameters respectively diamH and diamV 

# plot
figure = plt.figure()
plt.plot('frame','diamH', data=df, linestyle='none', marker='o', markersize=1, alpha=0.1)
plt.plot('frame','diamV', data=df, linestyle='none', marker='o', markersize=1, alpha=0.1)
plt.xlim(0,len(df.index))
plt.axis('off')
plt.box(False)
#plt.show()

figure.savefig(files[i]+'.png', bbox_inches='tight', transparent=True, dpi=300)