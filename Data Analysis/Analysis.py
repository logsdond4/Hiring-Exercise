# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:54:12 2020

@author: Dan Logsdon

#This code analyzes the cleaned data set for the Deloitte exercise
"""

#%% Import Packages
import pandas as pd
import os
import statistics as st
from collections import Counter
import statsmodels.stats.api as sms


#%% File Path
root = os.path.dirname(os.path.dirname(__file__)) #root folder
src = root + '\\Cleaned' #source folder
file = src + '\\clean_race_data.csv' #cleaned_file

#%% Import File
df = pd.read_csv(file)

#%% Functions
def q1_stats(df): #This function calculates the stats for question 2

    mean=st.mean(df['Net Tim_min']) #mean net time in minutes
    median=st.median(df['Net Tim_min']) #median net time in minutes
    minimum=min(df['Net Tim_min']) #min net time in minutes
    maximum=max(df['Net Tim_min']) #max net time in minutes
    metrics=[mean, median, minimum, maximum ]
    
    return metrics

def q2_3_stats(df): #This function calculates the mean and confidence interval for use in Q2 and Q3
    
    mean_net=st.mean(df['Net Tim_min']) #mean net time
    ci_net=sms.DescrStatsW(df['Net Tim_min']).tconfint_mean() # net 95 confidence interval (2-sided t-test)

    mean_gun=st.mean(df['Gun Tim_min']) #mean gun time
    ci_gun=sms.DescrStatsW(df['Gun Tim_min']).tconfint_mean() # gun 95 confidence interval (2-sided t-test)
    
    means=[mean_net, ci_net, mean_gun, ci_gun]
    return means
    

#%% Question 1: What are the mean, median, mode, and range of the race results for all racers by gender

#Male File
df_m=df[df['Sex']=='M']
mode_m=Counter(df_m['Net Tim_min']) #mode net time in minutes
metrics_m=q1_stats(df_m)

#Female File
df_f=df[df['Sex']=='F']
mode_f=Counter(df_f['Net Tim_min']) #mode net time in minutes
metrics_f=q1_stats(df_f)

#%% Question 2: Analyze the difference between gun and net time race results
# assumption, normal distribution 

#Male
means_m=q2_3_stats(df_m)

#Female
means_f=q2_3_stats(df_f)


#%% Question 3: How much time separates Chris Doe from the top 10 percentile of racers of the same division
df_chris=df_m[df_m["Name"]=='Chris Doe'] #get Chris Doe's Record
df_division=df_m[df_m["Division"]=='40-49'] # get Chris Doe's Division
top_10 = int(len(df_division)*0.1) # get number of runners in top 10
df_top_10= df_division.head(top_10) # get the top 10% in Chris' Division

chris_time=df_chris['Net Tim_min'] # get Chris' Time
means_div= q2_3_stats(df_top_10)  # get mean of top 10%
min_div=min(df_top_10['Net Tim_min']) # min time in top 10%
max_div=max(df_top_10['Net Tim_min']) # max time in top 10%


#%% Quesiton 4: Compare the race results of each division
#See Tableau output in powerpoint the data was analyzed in Tableau by Gender and Division

