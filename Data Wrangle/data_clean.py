# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:54:12 2020

@author: Dan Logsdon

#This code cleans the two data sets provided by Deloitte for use in their 
excercises. This had been updated on 02/21/21 to test git functionality.
and again on 02/24 to retest
"""

#%% Import Packages
import pandas as pd
import os
import re
import numpy as np

#%% Functions
#this function converts a dataframe column into a single list in minutes
def convert_time(df_list):
   
    minutes=list() #empty list to store calculated minutes
    for time in df_list:
        
        if len(time) == 7: #condition where hours are included
            [h, m, s] = time.split(':')
        
            h=int(h)*60 #convert hours to minutes
            m=int(m)
            s=int(s)/60 #convert seconds to minutes
            total=h+m+s #total minutes
            minutes.append(total)
            
        else: #condition where hours are not included
            [m, s] = time.split(':')
        
            m=int(m)
            s=int(s)/60 #convert seconds to minutes
            total=m+s #total minutes
            minutes.append(total)
    
    return minutes

def character_strip(df_list):
    times=list()
    for time in df_list:
        stripped=re.sub(re.compile(r'^[^0-9]*'), '', time) #strips non-numeric characters from begining of string
        times.append(stripped)
        
    return times

#%% File Locations
root = os.path.dirname(os.path.dirname(__file__)) #root folder
src = root + '\\src' #source folder
m_file = src + '\\MA_Exer_PikesPeak_Males.csv' #male_file
f_file = src + '\\MA_Exer_PikesPeak_Females.csv' #female_file

#%% Import Files
df_m = pd.read_csv(m_file)
df_m['Sex']= 'M' #create sex flag for merge
df_f = pd.read_csv(f_file)
df_f['Sex']= 'F' #create sex flag for merge

#%% Merge Datasets
df=df_m.append(df_f)
df=df.reset_index()
df=df.drop(['index'], axis=1)

#%% Split Div/Tot Column
df[['Div', 'Tot']] =df['Div/Tot'].str.split("/", n=1, expand=True)
df=df.drop(['Div/Tot'], axis=1)

#%% Drop "." in Hometown
df['Hometown']=df['Hometown'].map(lambda x:x.rstrip(' .'))

#%% Drop Characters from Net Tim
df['Net Tim']=df['Net Tim'].map(lambda x:x.rstrip('#'))
df['Net Tim']=df['Net Tim'].map(lambda x:x.rstrip('*'))

#%% Drop Characters from Gun Tim
df['Gun Tim']=character_strip(df['Gun Tim']) #strips non-numeric characters from beginnging of strings

#%% Convert Time Columns Into Minutes
df['Net Tim_min']=convert_time(df['Net Tim'])
df['Gun Tim_min']=convert_time(df['Gun Tim'])
df['Pace_min']=convert_time(df['Pace'])

#%% Create Division Column to Check Given Division Values
#Remove negative age values
df = df[df['Ag']>=0]

conds = [df.Ag.between(0,14), df.Ag.between(15,19),
         df.Ag.between(20,29), df.Ag.between(30,39),
         df.Ag.between(40,49), df.Ag.between(50,59),
         df.Ag.between(60,69), df.Ag.between(70,79),
         df.Ag.between(80,89), df.Ag.between(90,99),
         df.Ag.between(100,109)] # age ranges

groups = ['0-14','15-19','20-29','30-39','40-49','50-59','60-69','70-79','80-89','90-99','100-109'] #value for the given ranges

df['Division'] = np.select(conds, groups, 12)

#%% Drop Division and Total Columns
#Note: significant errors were observed in division and total columns so they are dropped
df=df.drop(['Div'], axis=1)
df=df.drop(['Tot'], axis=1)

#%% Check for duplicates in the Num column before exporting
duplicateRows = df[df.duplicated(['Num'])] 
#none found

#%% Output Data
root = os.path.dirname(os.path.dirname(__file__)) #root folder
out = root + '\\Cleaned' #output folder
out_path = out + '\\clean_race_data.csv' #output file path
df.to_csv(out_path, index=False)





