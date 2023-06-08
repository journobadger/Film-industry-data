import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

#%% Load data

data = np.loadtxt('Box-office-weekly-data.txt',dtype = str, delimiter = '\n') #Load weekly data

#%% Extract dates 

dates = []
for i in range(len(data)):
    date_index = data[i].find('$') - 1 #Date parameter in data is all characters until first '$' -1 for space.
    date = data[i][0:date_index]
    dates.append(date)

dates = dates[::-1] #Reverse the order so it goes from 3 Jan 2020 to 1 June 2023
 
#Remove rogue lines in data   
while bool('Re-relea' in dates) == True:
    dates.remove('Re-relea')   
while bool('' in dates) == True:
    dates.remove('')
    
#%% Convert dates to intergers that can be plotted

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
months_ints = ['01','02','03','04','05','06','07','08','09','10','11','12'] #Strings used first so preceding 0s can be used

date_ints = []

year = 2020
for i in range(len(dates)):
    dash_ind = dates[i].find('-')
    new_string = dates[i][dash_ind + 1:]
    if len(new_string) > 5: #If week goes across yeah:
        year += 1
    elif dates[i] == 'Jan 1-7': #Since first day is NYD, there is no year in raw data
        year += 1
    date_int = f'{year}' #Empty string which can be appended
    for j in range(len(months)):
        if len(new_string) < 3:
            if dates[i][:3] == months[j]: #Identify month of date
                date_int += months_ints[j]
                if len(new_string) == 1:
                    date_int += '0' + new_string #If date is 1-9, add preceding 0
                else:
                    date_int += new_string
                break
        elif len(new_string) > 3: #If week goes across a month
            if new_string[:3] == months[j]:
                date_int += months_ints[j] + '0' + new_string[4]
                break
    date_ints.append(date_int) #Convert date into integer

#Convert date integers into datetime objects
datetimes = []
for date in date_ints:
    datetimes.append(datetime(year = int(date[0:4]), month = int(date[4:6]), day = int(date[6:8])))

#%% Extract overall gross figures

def find_nth(haystack, needle, n):
    """

    Parameters
    ----------
    haystack : str
        String in which to search.
    needle : str
        Substring for which to search in haystack.
    n : int
        n-th occurence of needle.

    Returns
    -------
    start : index of n-th occurence of needle in haystack.

    """
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start

ogs = []
for line in data:
    og_index_start = find_nth(line, '$', 2) #Find the second occurence of the '$' symbol
    new_string = line[og_index_start + 1:] #Define new string to search
    for i in range(len(new_string)):
        try:
            int(new_string[i]) 
        except ValueError: #If we reach a string that is not a number, this is the end of the overall gross figure
            if new_string[i] == ',': #There are commas in the overall gross data, so ignore this result
                continue
            else:
                og_index_end = i
                og = new_string[:i] 
                break
    ogs.append(og)
    
ogs = ogs[::-1] #Reverse data so it goes forwards in time

#Remove rogue lines in data
while bool('R' in ogs) == True:
    ogs.remove('R')
while bool('' in ogs) == True:
    ogs.remove('')

#Convert gross data to integers
ogs_ints = []
for og in ogs:
    ogs_ints.append(int(og.replace(',','')))
    
#%% Calculate 2019 mean weekly gross

data_2019 = np.loadtxt('Box-office-weekly-data-2019.txt',dtype = str, delimiter = '\n') #Load weekly data

ogs_2019 = []
for line in data_2019:
    og_index_start = find_nth(line, '$', 2) #Find the second occurence of the '$' symbol
    new_string = line[og_index_start + 1:] #Define new string to search
    for i in range(len(new_string)):
        try:
            int(new_string[i]) 
        except ValueError: #If we reach a string that is not a number, this is the end of the overall gross figure
            if new_string[i] == ',': #There are commas in the overall gross data, so ignore this result
                continue
            else:
                og_index_end = i
                og = new_string[:i] 
                break
    ogs_2019.append(og)

#Remove rogue lines in data
while bool('R' in ogs_2019) == True:
    ogs.remove('R')
while bool('' in ogs_2019) == True:
    ogs.remove('')

#Convert gross data to integers
ogs_ints_2019 = []
for og in ogs_2019:
    ogs_ints_2019.append(int(og.replace(',','')))

#Calculate 2019 mean
av_og_2019 = np.mean(ogs_ints_2019)

#%% Calculate 2022 mean weekly gross

av_og_2022 = np.mean(ogs_ints[-74:-22]) #Slice of 2022 figures

#%% Plot data

fig = plt.figure(dpi = 300)
ax = fig.add_subplot()

#Generate x-tick and y-tick locations and labels
X_ticks = [datetime(2020, 1, 9, 0, 0), 
 datetime(2021, 1, 7, 0, 0),
 datetime(2022, 1, 6, 0, 0),
 datetime(2023, 1, 5, 0, 0)]
X_labels = ['2020','2021','2022','2023']

Y_ticks = [0,100000000,200000000,300000000,400000000]
Y_labels = ['$0','$100m','$200m','$300m','$400m']

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(datetimes,ogs_ints,color = 'navy')

#Hide right and top axes
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#Plot horizontal lines for 2019 and 2022 averages
ax.axhline(av_og_2019,linestyle = '--',color = 'g',linewidth = 1,label = '2019 average')
ax.text(datetime(2023,8,1,0,0),av_og_2019,'2019 average',va = 'center',fontname = 'georgia')
ax.axhline(av_og_2022,linestyle = '--',color = 'c',linewidth = 1)
ax.text(datetime(2023,8,1,0,0),av_og_2022,'2022 average',va = 'center',fontname = 'georgia')

plt.xticks(X_ticks, labels = X_labels,fontname = 'Georgia', fontsize = 12)
plt.yticks(Y_ticks, labels = Y_labels,fontname = 'Georgia', fontsize = 12,rotation = 45)
plt.figtext(0.5,0.01,'Total weekly US box office revenue. Source: Box Office Mojo by IMDbPro.',
            horizontalalignment = 'center',fontname = 'georgia',weight = 'bold', fontsize = 9)

#Annotations
plt.text(datetime(2021,7,15,0,0),450887647,'Dec 17, 2021:',ha = 'center',fontname = 'georgia', weight = 'bold', fontsize = 7.5)
plt.text(datetime(2021,7,15,0,0),405500000, 'Spiderman: No Way \n Home is released', ha = 'center',fontname = 'georgia', style = 'italic',fontsize = 7.5)

plt.text(datetime(2020,12,10,0,0),125000000,'April 2021:',ha = 'center',fontname = 'georgia', weight = 'bold', fontsize = 7.5)
plt.text(datetime(2020,12,10,0,0),65000000, 'Regal movie theaters \n begins opening cinemas \n across the US', ha = 'center',fontname = 'georgia',style = 'italic', fontsize = 7.5)

plt.savefig('Box-office-weekly-data-chart.png')
plt.show()

#%% Load Netflix quarlterly earnings data

data = np.loadtxt('Netflix-quarterley-earnings.csv',dtype = str,delimiter = ',')

revenues = []
for line in data:
    revenues.append(int(line[2]))
    
date_range = pd.date_range(start = datetime(2019,3,1,0,0), end = datetime(2023,3,31,0,0), freq = 'Q')

date_range_list = []
for date in date_range:
    date_range_list.append(str(date))

#%% Plot netflix data

X_ticks = ['2019-03-31 00:00:00', '2020-03-31 00:00:00', '2021-03-31 00:00:00','2022-03-31 00:00:00','2023-03-31 00:00:00']
X_labels = ['2019 Q1','2020 Q1','2021 Q1','2022 Q1','2023 Q1']
Y_ticks = [0,2000000,4000000,6000000,8000000]
Y_labels = ['$0','$2m','$4m','$6m','$8m']

ax = plt.subplot(111)

ax.bar(date_range_list,revenues,color = 'navy')
plt.xticks(X_ticks, labels = X_labels, fontname = 'georgia',fontsize = 12)
plt.yticks(Y_ticks,labels = Y_labels,fontname = 'georgia',rotation = 45,fontsize = 12)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.figtext(0.5,0.01,'Netflix quarterly revenue',
            horizontalalignment = 'center',fontname = 'georgia',weight = 'bold', fontsize = 9)