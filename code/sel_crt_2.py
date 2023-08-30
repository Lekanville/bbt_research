#!python
#!/usr/bin/env python3

import numpy as np
import pandas as pd
import os
import argparse

OUT_FILE = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/"
parser = argparse.ArgumentParser(description= "A script to filter data")
parser.add_argument('-d', '--data', type=str, required=True, help= 'The dataset')
parser.add_argument('-r', '--min_records', type=int, required=True, help= 'Minimum number of record days')
parser.add_argument('-n', '--min_days', type=int, required=True, help= 'Minimum number of days in a cycle')
parser.add_argument('-c', '--min_cycles', type=int, required=True, help= 'Minimum number of cycles for a user')

def process_temp(file, x, y, z):
    temperatures = pd.read_csv(file, index_col="prime")

    temperatures['Start Time'] = pd.to_datetime(temperatures['Start Time']) #Convert date object to datetime
    temperatures['Date'] = temperatures['Start Time'].dt.date #Getting the date
    temperatures['Time'] = temperatures['Start Time'].dt.time #Getting the time

    df_user_group = temperatures.groupby('User ID').count() #Group data by user ID
    check_1 = list(df_user_group[df_user_group['Data'] < x].index) #Get list of IDs less than x
    check_1_records = list(temperatures[temperatures["User ID"].isin(check_1)].index) #Get list of records belonging to x
    clean_1 = temperatures[~temperatures["User ID"].isin(check_1)] #Taking out records belonging to x 

    check_2 = list(clean_1[clean_1["Cycle ID"] =="undefined"].index )#Taking out undefined records
    clean_2 = clean_1[clean_1["Cycle ID"] !="undefined"] #Taking out undefined records


    df_cycle_group = clean_2.groupby('Cycle ID').count() #Group by Cycle ID
    check_3 = list(df_cycle_group[df_cycle_group['Data'] < y].index) #Get list of Cycle IDs less than y
    check_3_records = list(clean_2[clean_2["Cycle ID"].isin(check_3)].index) #Get records belonging to y
    clean_3 = clean_2[~clean_2["Cycle ID"].isin(check_3)] #Taking out records belonging to x 

    df_cycle_less_days=clean_3.groupby('User ID')["Cycle ID"].nunique() #Get Users with Cycles less than z
    check_4 = list(df_cycle_less_days[df_cycle_less_days < z].index) #Get list of Users Cycles less than z
    check_4_records = list(clean_3[clean_3["User ID"].isin(check_4)].index) #Get records belonging to z
    clean_4 = clean_3[~clean_3["User ID"].isin(check_4)] #Taking out records belonging to z 


    #print("There are ", len(check_1), " User IDs with less than ", x, " Days of Data,", len(check_1_records), " records will be deleted")
    #print(len(check_2), " \"Undefined\" records will be deleted ")
    #print("There are ", len(check_3), " Cycle IDs with less than ", y, " Days,", len(check_3_records), " records will be deleted")
    #print("There are ", len(check_4), " User IDs with less than ", z, " Cycles,", len(check_4_records), " records will be deleted")

    #clean_4.to_csv("data/sel_crt_1.csv")
    
    clean_4[["User ID","Cycle ID","Raw Temp","Smooth Temp",\
    	"Start Time","Data","Data_2","Data_len","Mean_Temp","Date","Time"]]\
        .to_csv(os.path.join(OUT_FILE,"sel_crt_2.csv"))
    #return clean_4
if __name__ == "__main__":
    args = parser.parse_args()
    process_temp(args.data, args.min_records, args.min_days, args.min_cycles)