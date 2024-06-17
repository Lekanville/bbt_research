import numpy as np
import pandas as pd
import os
from loguru import logger
import glob

class Frames:
    def __init__(self, df):
        self.df = df
        
    def recode_pcos(self):
        the_df = self.df
        for i in range(len(the_df)):
            if the_df.iloc[i, 678] == "Polycystic Ovarian Syndrome (PCOS)":
                the_df.iloc[i, 678] = 1

            else:
                the_df.iloc[i, 678] = 0
        return the_df

    def the_cycles_temp_dates_duration(self):
        temp_dates_duration = self.df
        cycles = pd.read_csv(
            temp_dates_duration, usecols = ["Cycle ID", "Data_Dur", "Date_x", "User ID_y", "Offset", "Date_Diff", "Ovulation Day"]
            )
        cycles = cycles.sort_values("Date_x")
        return cycles

    def excel_df(self):
        excel_file = self.df
        df = pd.read_excel(excel_file)
        return df

    def excel_df_model(self):
        excel_file = self.df
        df = pd.read_excel(excel_file,  skiprows=2)
        return df

    def read_temp(self):
        INPUT_TEMPS = self.df
        chunk_temperatures = pd.read_csv(
            INPUT_TEMPS, 
            usecols=["prime","Cycle ID","Start Time","Mean_Temp","Date","Time"],
            chunksize=50000
            )
        temperatures = pd.concat(chunk_temperatures)
        temperatures["User ID"] = temperatures["prime"].apply(lambda x: x.split("_")[0])
        temp_sort = temperatures.sort_values(["Date", "Time"]).reset_index(drop = True)
        #temp_sort["Cycle ID"] = temp_sort["Cycle ID"].apply(lambda x: x.lower())
        temp_sort["Cycle ID"] = temp_sort["Cycle ID"]
        
        temp_sort["Mean_Temp"] = temp_sort["Mean_Temp"].apply(lambda x: int(x)) #convert data to integer type
        temp_sort_final = temp_sort[(temp_sort["Mean_Temp"] > 35000) & (temp_sort["Mean_Temp"] < 40000)] #ensures that true values are selected

        return temp_sort_final

    def read_cycles_and_pcos(self):
        INPUT_CYCLES_PCOS = self.df
        cycles = pd.read_csv(
            INPUT_CYCLES_PCOS, usecols = ["Cycle ID", "Data_Dur", "Date_x", "User ID_y", "Offset", "Date_Diff", "Ovulation Day", "PCOS"]
            )
        cycles = cycles.sort_values("Date_x")
        return cycles

    def read_user_level_data(self):
        INPUT_USER_LEVEL = self.df
        user_data = pd.read_csv(
            INPUT_USER_LEVEL, usecols = ["User", "PCOS"]
            )
        return user_data

    def read_events(self):
        ALL_EVENTS_FOLDER = self.df
        ALL_EVENTS_PATH = os.path.join(ALL_EVENTS_FOLDER, "alluserevents*")
        ALL_EVENTS_FILE = glob.glob(ALL_EVENTS_PATH)

        #combine the allusercycles files
        events_df = pd.DataFrame()
        for file in  ALL_EVENTS_FILE:
            event_data = pd.read_csv(file)
            events_df = pd.concat([events_df, event_data], axis=0)
            dataset_name = file.split("/")[-1]
            logger.info(dataset_name+" loaded")

        events_df["Date"] = pd.to_datetime(events_df["Date"])
        events_df = events_df.sort_values("Date").reset_index(drop = True)
        period_events = events_df[events_df["Event Type"] == "period"]
        return (period_events)