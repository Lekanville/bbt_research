#!python
#!/usr/bin/env python3

#############################################################################################
#The “process_cycles.py” script
#The script expects the output file from the previous rule (sel_cr_2.py) and the folder 
#containing the cycles files (allusercycles.csv) as input and will output the specified 
#selected data as a CSV. The script reads all user cycle files and concatenates them into a 
#single data frame. The temperature records outputted from the previous rule (sel_cr_2.py) 
#are equally read in.  The temperatures table is merged with the cycles table and grouped by 
#the user IDs and cycle IDs. The dates are converted into datetime formats. Records that have 
#indicated cycle start dates were selected.
#The length of each cycle is computed by subtracting succeeding start dates (as indicated by 
#the user) and the last cycle is given the value “indeterminate last cycle”.
#Cycle offsets (number of days between the cycle start and the first day of temperature 
#recording) are computed by subtracting the first date of temperature recording from the cycle 
#start date (as indicated by the user).
#Again, cycle durations were computed by subtracting the last day of temperature recording 
#from the first day of temperature recording. The cycle offsets and durations are then merged 
#and saved as “dates_duration”.
#Finally, the result is outputted as the specified file
#############################################################################################


import numpy as np
import pandas as pd
from loguru import logger
import os
import glob
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import argparse
from classes.classes import Frames

parser = argparse.ArgumentParser(description= "A script to process the cycles")
parser.add_argument('-i', '--input_cycles', type=str, required=True, help= 'The folder of the input cycles datasets')
parser.add_argument('-j', '--input_temps', type=str, required=True, help= 'The output file from select_criteria_2')
parser.add_argument('-o', '--output_file', type=str, required=True, help= 'The output dataset')

def process_cycles(INPUT_CYCLES, INPUT_TEMPS, OUTPUT):
    #get cycles from the allusercycles files
    PATH = os.path.join(INPUT_CYCLES, "allusercycles*")
    FOLDER = glob.glob(PATH)

    #combine the allusercycles files
    df = pd.DataFrame()
    for file in FOLDER:
        data = pd.read_csv(file)
        df = pd.concat([df,data], axis = 0)
        dataset_name = file.split("/")[-1]
        logger.info(dataset_name+" loaded")

    logger.info("Datasets merged")
    cycles_sort = df.sort_values("Date").reset_index(drop = True)
    #cycles_sort["Cycle ID"] = cycles_sort["Cycle ID"].apply(lambda x: x.())
    cycles_sort["Cycle ID"] = cycles_sort["Cycle ID"]
    logger.info("Cycles dataset loaded and sorted by date")

    #get cleaned temperatures from the workflow
    temp_sort = Frames(INPUT_TEMPS).read_temp()
    logger.info("Temperatures dataset loaded and sorted by date")

    #merge the temperatures table with the cycles table
    temp_and_cycles = pd.merge(temp_sort, cycles_sort, left_on= "Cycle ID", right_on="Cycle ID", how = "left")
    logger.info("Temperatures and Cycles merged")

    #group the merged tables by the users and cycles
    grouped = temp_and_cycles.groupby(["User ID_x","Cycle ID"]).first()
    logger.info("Dataset grouped by users and cycles")

    #convert the dates
    #note: [j, 6] or date_y is the date indicated by a user as the start of the cycle
    #note: [j, 3] or date_x is first date of temperature recording
    grouped["Date_x"], grouped["Date_y"] = pd.to_datetime(grouped["Date_x"]), pd.to_datetime(grouped["Date_y"])
    logger.info("Dates converted")

    #get records without null on the cycle start column
    grouped = grouped[~(grouped["Date_y"].isnull())]
    logger.info("Null cycle start dates removed")

    #routine to get the users
    def get_users(grouped_data):
        usershat = []
        for key, group in grouped_data.index:
            if key not in usershat:
                usershat.append(key)
        return usershat

    #routine to compute the cycle lengths
    def cycle_lengths(usershat, groupedhat):
        grouped_date_diff = pd.DataFrame()
        #get the cycles for each user
        for i in usershat:
            user_cycles = groupedhat.xs(i, level= 0).sort_values("Date_x")
            user_cycles["Date_Diff"] = ""

        #get the difference between each cycles using the recorded dates on the cycles table
        #note: [j, 6] or date_y is the date indicated by a user as the start of the cycle
        #note: [j, 3] or date_x is first date of temperature recording
        
            for j in range(len(user_cycles)-1):
                #get the start date of the current record
                y = user_cycles.iloc[j,6]

                #get the start date of the succeeding record
                x = user_cycles.iloc[j+1,6]
                
                #now initiate the action
                try:
                    z = int(float(str((x) - (y)).split(" ")[0]))
                    #if z > 0:
                    user_cycles.iloc[j,13] = z
                except (ValueError) as e:
                    user_cycles.iloc[j,13] = "Indeterminate Cycle Length"

            #this is for the last cycles
            user_cycles.iloc[len(user_cycles)-1,13] = "Indeterminate Last Cycle"
            grouped_date_diff = pd.concat([grouped_date_diff, user_cycles], axis = 0)
        return grouped_date_diff

    #routine to compute the temperature date offsets
    def date_offsets(df):
        df["Offset"] = ""
        #note: [j, 6] or date_y is the date indicated by a user as the start of the cycle
        #note: [j, 3] or date_x is first date of temperature recording
        for i in range(len(df)):
            x = df.loc[i, "Date_x"]
            y = df.loc[i, "Date_y"]
            df.loc[i, "Offset"] =  int(str(x - y).split(" ")[0])
        return df

    #routine to compute the duration of the temperature recordings
    def data_duration(df_temp, df_offsets):
        temp_dates = df_temp.groupby("Cycle ID").agg(Min_date = ("Date", "min"), Max_date = ("Date", "max")).reset_index()
        temp_dates["Min_date"], temp_dates["Max_date"] = pd.to_datetime(temp_dates["Min_date"]), pd.to_datetime(temp_dates["Max_date"])
        
        for i in range(len(temp_dates)):
            temp_dates.loc[i, "Data_Dur"] = int(str(temp_dates.loc[i, "Max_date"] - temp_dates.loc[i, "Min_date"]).split(" ")[0]) + 1
            #temp_dates["Data_Dur"] = temp_dates["Data_Dur"].apply(lambda x: int(x.split(" ")[0]))
            #temp_dates["Data_Dur"] = temp_dates["Data_Dur"].apply(lambda x: str(x).split(" ")[0])

        dates_duration = pd.merge(temp_dates, df_offsets, left_on= "Cycle ID", right_on="Cycle ID", how = "inner")

        return dates_duration

    #get the users
    users = get_users(grouped)
    logger.info("users' list created")

    #compute the cycle lengths
    lengths =  cycle_lengths(users, grouped)
    lengths.reset_index(inplace = True)
    logger.info("Cycle lengths computed")

    #compute the date offsets
    offsets = date_offsets(lengths)
    logger.info("Date offsets computed")

    #compute the duration of the temperature recordings
    temp_dates_duration = data_duration(temp_sort, offsets)
    logger.info("temperatures duration computed")

    temp_dates_duration.to_csv(OUTPUT)
    logger.info("Completed: Dataset ready and saved")

if __name__ == "__main__":
    args = parser.parse_args()
    process_cycles(args.input_cycles, args.input_temps, args.output_file)