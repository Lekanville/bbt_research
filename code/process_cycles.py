import numpy as np
import pandas as pd
from loguru import logger
import os
import glob
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

#get cycles from the allusercycles files
ABSOLUTE = "/projects/MRC-IEU/research/data/fertility_focus/ovusense/released/2022-11-30/data/temperature/"
OUT_FILE = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/"
PATH = os.path.join(ABSOLUTE, "allusercycles*")
FOLDER = glob.glob(PATH)

def process_cycles():
    #combine the allusercycles files
    df = pd.DataFrame()
    for file in FOLDER:
        data = pd.read_csv(file)
        df = pd.concat([df,data], axis = 0)
        dataset_name = file.split("/")[-1]
        logger.info(dataset_name+" loaded")

    logger.info("Datasets merged")
    cycles_sort = df.sort_values("Date").reset_index(drop = True)
    cycles_sort["Cycle ID"] = cycles_sort["Cycle ID"].apply(lambda x: x.lower())
    logger.info("Cycles dataset loaded and sorted by date")

    #get cleaned temperatures from the workflow
    INPUT = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/"
    file = "sel_crt_2.csv"
    temperatures = pd.read_csv(os.path.join(INPUT, file), usecols=["prime","Cycle ID","Start Time","Mean_Temp","Date","Time"])
    temperatures["User ID"] = temperatures["prime"].apply(lambda x: x.split("_")[0])
    temp_sort = temperatures.sort_values("Date").reset_index(drop = True)
    temp_sort["Cycle ID"] = temp_sort["Cycle ID"].apply(lambda x: x.lower())
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
            temp_dates.loc[i, "Data_Dur"] = (str(temp_dates.loc[i, "Max_date"] - temp_dates.loc[i, "Min_date"]))
            #temp_dates["Data_Dur"] = temp_dates["Data_Dur"].apply(lambda x: int(x.split(" ")[0]))
            temp_dates["Data_Dur"] = temp_dates["Data_Dur"].apply(lambda x: str(x).split(" ")[0])

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

    temp_dates_duration.to_csv(os.path.join(OUT_FILE, "temp_dates_duration.csv"))
    logger.info("Completed: Dataset ready and saved")

if __name__ == "__main__":
    process_cycles()