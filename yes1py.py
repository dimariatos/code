

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 10:47:14 2021
@author: Dimitrios
"""

import numpy as np
import pandas as pd 
import pickle
import math
import matplotlib.pyplot as plt


def read1(name1):
#k4 = k4 != 100
    pkl_file = open(name1, 'rb')
    dot = pickle.load(pkl_file)
    dot = pd.DataFrame(dot)
    return dot

def read2(name2):
    stimuli = np.load(name2, allow_pickle=True)
    stimuli = pd.DataFrame(stimuli)
    return stimuli

def sizefilter(df,length):
    newtotal3=pd.DataFrame()
    for i in range(df['trial'].max()):
       # print('trial',i)
        b=df.loc[df['trial']==i]
        c=len(b)
        #print('length',c)
        if c<length:
            #print('adding this one')
            newtotal3= pd.concat([newtotal3,b])
    return newtotal3

'''Begin by opening the stimulus data'''

k = read1('C:/Users/DIMITR~1/AppData/Local/Temp/Rar$DRa7704.41337/384952_4/thedata107.pkl') #open the pickle file with stimuli data

k.columns=['x','y','edges','opacity','radius','orientation','delete','x','y','edges','opacity','radius','orientation','laser','frame_time']
k = k.drop([0])
k.frame_time = k.frame_time.astype(float) #change the frame time into float 


k1=k.iloc[:,0:6] # first stimuli

k2=k.iloc[:,7:12] # second stimuli

k3 =k.iloc[:,13] # laser

k4 = k.iloc[:,14] # frame time


k = pd.concat([k1, k3, k4], axis=1) #stimulus we are analysing

stim2 = pd.concat([k2, k3], axis=1) #send stimuli to analyse

################################################################################

''' Open the Pose file'''

df = pd.read_hdf('C:/Users/DIMITR~1/AppData/Local/Temp/Rar$DRa7704.42970/384952_4/blackfly_384952_2021-07-22_4_DLC.hdf5') #open the hdf5 file from DLC live

df.columns=['snout_x','snout_y','snout_likelihood','left_ear_x','left_ear_y',
            'left_ear_likelihood','right_ear_x','right_ear_y','right_ear_likelihood',
            'tail_x','tail_y','tail_likelihood','frame_time','pose_time'] #rename the columns from the DLC live file 

df.frame_time = df.frame_time.astype(float)

k.frame_time = k.frame_time.round(1) #round the decimal points of the frame time to match the hdf5 file
 
df.frame_time = df.frame_time.round(1) #round the decimal points of the frame time to match the pickle file

'''merge the two files '''

merged = df.merge(k, how='outer', on='frame_time') # merge the hdf5 file with the pickle file dependent on the time frame


''' find the head body angle '''

[x1,y1] = [merged.snout_x,merged.snout_y]
[x2,y2] = [merged.left_ear_x,merged.left_ear_y]
[x3,y3] = [merged.right_ear_x,merged.right_ear_y]
[x4,y4] = [(x3+x2)/2,(y3+y2)/2]
angles = []
    
for i in range(merged.shape[0]):
    a = math.sqrt((x4[i]-x2[i])**2+(y4[i]-y2[i])**2)
    b = math.sqrt((x4[i]-x1[i])**2+(y4[i]-y1[i])**2)
    c = math.sqrt((x1[i]-x2[i])**2+(y1[i]-y2[i])**2)
    if (a**2+b**2-c**2)/(2*b*a) > 1:
        angle = math.acos(1)
    else:
        angle = math.acos((a**2+b**2-c**2)/(2*b*a))
    angle = math.degrees(angle)
    angles.append(angle)

right_head_angle = [180 - Value for Value in (angles)]  


[x1a,y1a] = [merged.tail_x,merged.tail_y]
[x2,y2] = [merged.left_ear_x,merged.left_ear_y]
[x3,y3] = [merged.right_ear_x,merged.right_ear_y]
[x4a,y4a] = [(x3+x2)/2,(y3+y2)/2]
angles1 = []
    
for i in range(merged.shape[0]):
    d = math.sqrt((x4a[i]-x2[i])**2+(y4a[i]-y2[i])**2)
    e = math.sqrt((x4a[i]-x1a[i])**2+(y4a[i]-y1a[i])**2)
    f = math.sqrt((x1a[i]-x2[i])**2+(y1a[i]-y2[i])**2)
    
    angle1 = math.acos((d**2+e**2-f**2)/(2*e*d))
    angle1 = math.degrees(angle1)
    angles1.append(angle1)
    
result = [Value + Value for Value, Value in zip(angles, angles1)]


data= df = pd.DataFrame(result) 

total = pd.concat([data, merged], axis=1).reindex(merged.index) #merge angles into the total dataframe


''' Change the name of the columns to fit the new dataframe'''

total.columns=['left_head_body_angle', 'snout_x','snout_y','snout_likelihood','left_ear_x','left_ear_y',
            'left_ear_likelihood','right_ear_x','right_ear_y','right_ear_likelihood',
            'tail_x','tail_y','tail_likelihood','frame_time','pose_time','x','y','edges'
            ,'opacity','radius','orientation','laser']


'''translate the frame time into real time'''

total.frame_time.astype(float)
first_frame = total.iloc[1,13]

translated_time=total.frame_time-first_frame

total = pd.concat([total, translated_time], axis=1).reindex(total.index)


total.left_head_body_angle.astype(float)


total.columns=['left_head_body_angle', 'snout_x','snout_y','snout_likelihood','left_ear_x','left_ear_y',
            'left_ear_likelihood','right_ear_x','right_ear_y','right_ear_likelihood',
            'tail_x','tail_y','tail_likelihood','frame_time','pose_time','x','y','edges'
            ,'opacity','radius','orientation','laser','time']

#Correct the data to only show the apperance of the stimuli

total = total.fillna(method='ffill')

total = total.dropna()



'''make laser true or false'''

laser = total['laser']

laser1 = laser%2==0


'''convert coordinates into psychopy'''

snout = ((total.iloc[0:total['snout_x'].shape[0]-1,1:3] - [45, 15]) / 380) * .93 + .035
snout['snout_y'] = 1-snout['snout_y']
snout = (snout-0.5)*2

total = pd.concat([total, snout], axis=1).reindex(total.index)

leftear = ((total.iloc[0:total['left_ear_x'].shape[0]-1,4:6] - [45, 15]) / 380) * .93 + .035
#snout = ((total.iloc[764,2] - [45, 15]) / 380) * .93 + .035
leftear['left_ear_y'] = 1-leftear['left_ear_y']
leftear = (leftear-0.5)*2

total = pd.concat([total, leftear], axis=1).reindex(total.index)

rightear = ((total.iloc[0:total['right_ear_x'].shape[0]-1,7:9] - [45, 15]) / 380) * .93 + .035
#snout = ((total.iloc[764,2] - [45, 15]) / 380) * .93 + .035
rightear['right_ear_y'] = 1-rightear['right_ear_y']
rightear = (rightear-0.5)*2

total = pd.concat([total, rightear], axis=1).reindex(total.index)

tail = ((total.iloc[0:total['tail_x'].shape[0]-1,10:12] - [45, 15]) / 380) * .93 + .035
#snout = ((total.iloc[764,2] - [45, 15]) / 380) * .93 + .035
tail['tail_y'] = 1-tail['tail_y']
tail = (tail-0.5)*2


total = pd.concat([total, tail], axis=1).reindex(total.index)


total.columns=['left_head_body_angle', 'snout_x_w','snout_y_w','snout_likelihood_w','left_ear_x_w','left_ear_y_w',
            'left_ear_likelihood','right_ear_x','right_ear_y','right_ear_likelihood',
            'tail_x','tail_y','tail_likelihood','frame_time','pose_time','x','y','edges'
            ,'opacity','radius','orientation','laser','time','x_snout','y_snout','left_ear_x_c','left_ear_y_c','right_ear_x_c','right_ear_y_c','tail_x_c','tail_y_c']

total = pd.concat([total, laser1], axis=1).reindex(total.index)


total = total.reset_index()
"find the angle of the dot from x axis and invert head angle in pose so the subtraction with dot angle is correct"""


#Make snout psychopy coordinates fit with the stimulus psychopy coordinates
total['x_snout'] = total['x_snout'] * 0.4
total['y_snout'] = total['y_snout'] * 0.5

total['left_ear_x_c'] = total['left_ear_x_c'] * 0.4
total['left_ear_y_c'] = total['left_ear_y_c'] * 0.5

total['right_ear_x_c'] = total['right_ear_x_c'] * 0.4
total['right_ear_y_c'] = total['right_ear_y_c'] * 0.5

total['tail_x_c'] = total['tail_x_c'] * 0.4
total['tail_y_c'] = total['tail_y_c'] * 0.5


dangle = []
for i in total.index:
    dangle.append(math.atan2(total['y'][i], total['x'][i]))
total['dangle'] = dangle
total['dangle'] = np.rad2deg(total['dangle'])

total['dx'] = total['x_snout'] - total['x']
total['dy'] = total['y_snout'] - total['y']

total['dxsq'] = total['dx']**2
total['dysq'] = total['dy']**2
total['dis'] = total['dxsq'] + total['dysq']
total['dis'] = np.sqrt(total['dis'])


#calculate the line between the snout and midpoint between ears

[x1,y1] = [total.x_snout,total.y_snout]
[x2,y2] = [total.left_ear_x_c,total.left_ear_y_c]
[x3,y3] = [total.right_ear_x_c,total.right_ear_y_c]
[x4,y4] = [(x3+x2)/2,(y3+y2)/2]

m = (y1 - y4) /(x1 - x4)
b = y1 - m * x1


ysnout = total['y_snout']
xsnout = total['x_snout']
xstimulus = total['x']
ystimulus = total['y']
y22 = m*(xstimulus) + b

mouseangles = []

for i in range(len(total)):
    a = y22[i]-ystimulus[i]  

    b = math.sqrt((xstimulus[i]-xsnout[i])**2 + (y22[i]-ysnout[i])**2)
    c = math.sqrt((xstimulus[i]-xsnout[i])**2 + (ystimulus[i]-ysnout[i])**2)
    angle = math.acos((b**2+c**2-a**2)/(2*b*c))
    #math.degrees(angle)
    mouseangles.append(angle)


df = pd.DataFrame(mouseangles)
total = pd.concat([total, df], axis=1).reindex(total.index)

total = total.drop(columns=['index'])


total.columns=['left_head_body_angle', 'snout_x','snout_y','snout_likelihood','left_ear_x','left_ear_y',
            'left_ear_likelihood','right_ear_x','right_ear_y','right_ear_likelihood',
            'tail_x','tail_y','tail_likelihood','frame_time','pose_time','x','y','edges'
            ,'opacity','radius','orientation','laser','time','x_snout','y_snout','left_ear_x_c','left_ear_y_c',
            'right_ear_x_c','right_ear_y_c','tail_x_c','tail_y_c','laser1','dangle','dx','dy','dxsq','dysq','distance','mouse_angle']


new_total = total.drop_duplicates(subset='time', keep='first', inplace=False, ignore_index=True)

# drop the nan values

new_total = new_total.dropna()
new_total = new_total[new_total['opacity'] != 100].reset_index()
new_total = new_total[new_total['y_snout'] > 0].reset_index()

#find the start, end and the number of trials

new_total.insert(40, 'trial', 0)
x = 0
idx = 0

for i in range(len(new_total)):
    if x == new_total['x'][i]:
        new_total.iloc[i,40] = idx

    else:
        x = new_total['x'][i]
        idx = idx + 1
        new_total.iloc[i,40] = idx

headangle = new_total['left_head_body_angle']
trials = new_total['trial']                 
                       
headangletrials = pd.concat([trials, headangle], axis=1).reindex(new_total.index)

headangletrials = headangletrials.pivot(columns='trial', values='left_head_body_angle')

difference_angle = headangletrials.diff();
difference_angle = difference_angle.max()
mean = difference_angle.mean()+difference_angle.std()

new_total = new_total.dropna()

plt.figure(1)
plt.plot(difference_angle)
plt.ylabel('Angle')
plt.xlabel('Stimuli')
plt.title('Head Angle all trials')
# Create two new dataframe one with stimuli and one without

new_total1 = new_total[new_total['opacity'] == 0]

new_total2 = new_total[new_total['opacity'] != 0]

#######################################################################
#%%
'''WITH STIMULI '''

#find the start, end and the number of trials


######################################
# Get trials with laser and without laser WITH stimuli

new_total3 = new_total2[new_total2['laser1'] == True]

new_total4 = new_total2[new_total2['laser1'] == False]
        
# calculate the difference in head body angle over each trial

#%%
'''Plot the head angle for stimuli with laser'''
  
# head turns 
         
headangle = new_total3['left_head_body_angle']
trials = new_total3['trial']               

headangletrials = pd.concat([trials, headangle], axis=1).reindex(new_total3.index)
headangletrials = headangletrials.pivot(columns='trial', values='left_head_body_angle')
difference_angle = headangletrials.diff();
difference_angle = difference_angle.max()

#mousestim

mouse_angle = new_total3['mouse_angle']
trials = new_total3['trial']
                                        
mouse_stim1 = pd.concat([trials, mouse_angle], axis=1).reindex(new_total3.index)
mouse_stim1 = mouse_stim1.pivot(columns='trial', values='mouse_angle')
mouse_stim1 = mouse_stim1.min()

# average 
mouse_stim_min = mouse_stim1
difference_ang_max = difference_angle


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

normmouse = normalize(mouse_stim_min)
normang = normalize(difference_ang_max)

plt.figure(2)
plt.title('Normalized')
plt.xlabel('Stimuli')
plt.ylabel('1-0')
plt.plot(normmouse)
plt.plot(normang)
plt.legend(['mouse stimulus angle','head turn'])
score = []
highval = 0
index = 0   

normmouse = normmouse.tolist()
normang = normang*1
normang = normang.tolist()

# Calculating score of both angle and velocity for all stimuli and finding
# best stimuli for mouse distraction
# Weights need to be determined for optimal score
w_turn = 1/2
w_mouse = 1/2
for i in range(len(normmouse)):
    temp = (w_mouse*normmouse[i]+w_turn*normang[i])
    score.append(temp)
    if temp > highval:
        highval = temp
        index = i

# Plotting score for all the stimuli
plt.figure(3)
plt.title('Stimuli Score')
plt.xlabel('Stimuli')
plt.ylabel('Score')
plt.plot(score)

#the distracting stimuli with laser
df1 = pd.DataFrame(list(score))
value = df1.value_counts()
value = value.sum()
value1 = df1 > 0.07
value1 = value1.sum()

percentage_with_laser = value1/value

#%%


'''Plot the head angle for stimuli without laser'''
  
# head turns 
         
headangle = new_total4['left_head_body_angle']
trials = new_total4['trial']               

headangletrials = pd.concat([trials, headangle], axis=1).reindex(new_total4.index)
headangletrials = headangletrials.pivot(columns='trial', values='left_head_body_angle')
difference_angle = headangletrials.diff();
difference_angle = difference_angle.max()

#mousestim

mouse_angle = new_total4['mouse_angle']
trials = new_total4['trial']
                                        
mouse_stim1 = pd.concat([trials, mouse_angle], axis=1).reindex(new_total4.index)
mouse_stim1 = mouse_stim1.pivot(columns='trial', values='mouse_angle')
mouse_stim1 = mouse_stim1.min()

# average 
mouse_stim_min = mouse_stim1
difference_ang_max = difference_angle


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

normmouse = normalize(mouse_stim_min)
normang = normalize(difference_ang_max)

plt.figure(4)
plt.title('Normalized')
plt.xlabel('Stimuli')
plt.ylabel('1-0')
plt.plot(normmouse)
plt.plot(normang)
plt.legend(['mouse stimulus angle','head turn'])
score = []
highval = 0
index = 0   

normmouse = normmouse.tolist()
normang = normang*1
normang = normang.tolist()

# Calculating score of both angle and velocity for all stimuli and finding
# best stimuli for mouse distraction
# Weights need to be determined for optimal score
w_turn = 1/2
w_mouse = 1/2
for i in range(len(normmouse)):
    temp = (w_mouse*normmouse[i]+w_turn*normang[i])
    score.append(temp)
    if temp > highval:
        highval = temp
        index = i

# Plotting score for all the stimuli
plt.figure(5)
plt.title('Stimuli Score')
plt.xlabel('Stimuli')
plt.ylabel('Score')
plt.plot(score)

#the distracting stimuli with laser
df = pd.DataFrame(list(score))
value = df.value_counts()
value = value.sum()
value1 = df > 0.07
value1 = value1.sum()

percentage_without_laser = value1/value

'''Bar graph of distraction percentage with stimuli and laser status'''

plt.figure(6)
Values = [percentage_without_laser[0], percentage_with_laser[0]]        
Label = ['Without_Laser_Stim','With_Laser_Stim']
plt.bar(Label, Values, color = 'maroon', width = 0.6)
plt.xlabel('Laser Status')
plt.ylabel('Distraction Percentage')
plt.title('Distraction Percentage of Stimulus VS Laser Status')
plt.show()

plt.bar(['with','without'],[df.mean()[0],df1.mean()[0]],yerr=[df.std()[0],df1.std()[0]])

#%%
'''WITHOUT STIMULI '''

#find the start, end and the number of trials


######################################
# Get trials with laser and without laser WITH stimuli

new_total5 = new_total1[new_total1['laser1'] == True]

new_total6 = new_total1[new_total1['laser1'] == False]
        
# calculate the difference in head body angle over each trial

'''Plot the head angle no stimuli with laser'''
  
# head turns 
         
headangle = new_total5['left_head_body_angle']
trials = new_total5['trial']               

headangletrials = pd.concat([trials, headangle], axis=1).reindex(new_total5.index)
headangletrials = headangletrials.pivot(columns='trial', values='left_head_body_angle')
difference_angle = headangletrials.diff();
difference_angle = difference_angle.max()

#mousestim

mouse_angle = new_total5['mouse_angle']
trials = new_total5['trial']
                                        
mouse_stim1 = pd.concat([trials, mouse_angle], axis=1).reindex(new_total5.index)
mouse_stim1 = mouse_stim1.pivot(columns='trial', values='mouse_angle')
mouse_stim1 = mouse_stim1.min()

# average 
mouse_stim_min = mouse_stim1
difference_ang_max = difference_angle

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

normmouse = normalize(mouse_stim_min)
normang = normalize(difference_ang_max)

plt.figure(7)
plt.title('Normalized')
plt.xlabel('Stimuli')
plt.ylabel('1-0')
plt.plot(normmouse)
plt.plot(normang)
plt.legend(['mouse stimulus angle','head turn'])
score = []
highval = 0
index = 0   

normmouse = normmouse.tolist()
normang = normang*1
normang = normang.tolist()

# Calculating score of both angle and velocity for all stimuli and finding
# best stimuli for mouse distraction
# Weights need to be determined for optimal score
w_turn = 1/2
w_mouse = 1/2
for i in range(len(normmouse)):
    temp = (w_mouse*normmouse[i])
    score.append(temp)
    if temp > highval:
        highval = temp
        index = i

# Plotting score for all the stimuli
plt.figure(8)
plt.title('Stimuli Score')
plt.xlabel('Stimuli')
plt.ylabel('Score')
plt.plot(score)

#the distracting stimuli with laser
df2 = pd.DataFrame(list(score))
value = df2.value_counts()
value = value.sum()
value1 = df2 > 0.07
value1 = value1.sum()

No_Stim_percentage_with_laser = value1/value



'''Plot the head angle for stimuli without laser'''
  
# head turns 
         
headangle = new_total6['left_head_body_angle']
trials = new_total6['trial']               

headangletrials = pd.concat([trials, headangle], axis=1).reindex(new_total6.index)
headangletrials = headangletrials.pivot(columns='trial', values='left_head_body_angle')
difference_angle = headangletrials.diff();
difference_angle = difference_angle.max()

#mousestim

mouse_angle = new_total6['mouse_angle']
trials = new_total6['trial']
                                        
mouse_stim1 = pd.concat([trials, mouse_angle], axis=1).reindex(new_total6.index)
mouse_stim1 = mouse_stim1.pivot(columns='trial', values='mouse_angle')
mouse_stim1 = mouse_stim1.min()

# average 
mouse_stim_min = mouse_stim1
difference_ang_max = difference_angle


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

normmouse = normalize(mouse_stim_min)
normang = normalize(difference_ang_max)

plt.figure(9)
plt.title('Normalized')
plt.xlabel('Stimuli')
plt.ylabel('1-0')
plt.plot(normmouse)
plt.plot(normang)
plt.legend(['mouse stimulus angle','head turn'])
score = []
highval = 0
index = 0   

normmouse = normmouse.tolist()
normang = normang*1
normang = normang.tolist()

# Calculating score of both angle and velocity for all stimuli and finding
# best stimuli for mouse distraction
# Weights need to be determined for optimal score
w_turn = 1/2
w_mouse = 1/2
for i in range(len(normmouse)):
    temp = (w_mouse*normmouse[i])
    score.append(temp)
    if temp > highval:
        highval = temp
        index = i

# Plotting score for all the stimuli
plt.figure(10)
plt.title('Stimuli Score')
plt.xlabel('Stimuli')
plt.ylabel('Score')
plt.plot(score)

#the distracting stimuli with laser
df3 = pd.DataFrame(list(score))
value = df3.value_counts()
value = value.sum()
value1 = df3 > 0.07
value1 = value1.sum()

No_Stim_percentage_without_laser = value1/value

'''Bar graph of distraction percentage with stimuli and laser status'''

plt.figure(11)
Values = [percentage_without_laser[0], percentage_with_laser[0]]        
Label = ['Without_Laser_Stim','With_Laser_Stim']
plt.bar(Label, Values, color = 'maroon', width = 0.6)
plt.xlabel('Laser Status')
plt.ylabel('Distraction Percentage')
plt.title('Distraction Percentage of Stimulus VS Laser Status')
plt.show()


#################

plt.figure(12)
plt.bar(['with laser','without laser'],[df1.mean()[0],df.mean()[0]],yerr=[df1.std()[0],df.std()[0]])

plt.figure(13)
plt.bar(['with laser','without laser'],[df2.mean()[0],df3.mean()[0]],yerr=[df2.std()[0],df3.std()[0]])

plt.figure(14)
fig = plt.figure(figsize = (10,5))
plt.title('Mean & Standard Deviation')
plt.bar(['stim_with_laser','stim_without_laser','no_stim_with_laser','no_stim_without_laser'],[df.mean()[0],df1.mean()[0],df2.mean()[0],df3.mean()[0]],yerr=[df.std()[0],df1.std()[0],df2.std()[0],df3.std()[0]])
