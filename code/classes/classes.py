import numpy as np
import pandas as pd
import os
from loguru import logger
import glob
import tools.tools as tools

class Frames:
    def __init__(self, df):
        self.df = df
        
    def recode_pcos(self):
        the_df = self.df

        for i in range(len(the_df)):
            if (the_df.loc[i, "PCOS"] == "Polycystic Ovarian Syndrome (PCOS)"): # One person indicated PCOS but didnt answer
                the_df.loc[i, "PCOS"] = 1                                     # "Yes" to infertility

            elif (the_df.loc[i, "Have you ever gone to a doctor because you thought you were infertile?"] == "Yes") \
            & (the_df.loc[i, "PCOS"] != "Polycystic Ovarian Syndrome (PCOS)"):
                the_df.loc[i, "PCOS"] = 0 # Those that answered yes to infertility but do not have PCOS
            
            elif (the_df.loc[i, "Have you ever gone to a doctor because you thought you were infertile?"] == "No"):
                the_df.loc[i, "PCOS"] = 0 # Some answered "No" to infertility in the "Yes" column
                
            elif (the_df.loc[i, "Unnamed: 676"] == "No"):
                the_df.loc[i, "PCOS"] = 0 # Those that indicated "No to infertility"
                
            else:
                the_df.loc[i, "PCOS"] = 2 # Those with no response to infertility question
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
            INPUT_CYCLES_PCOS, usecols = ["Cycle ID", "Data_Dur", "Date_x", "User ID_y", "Offset", "Date_Diff", "Ovulation Day", "PCOS", "cycle_compl"]
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
    
    def model_users(self):
        MODEL_CYCLE = self.df
        MODEL_LOC_SPLIT = MODEL_CYCLE.split("/")
        MODEL_LOC = "/".join(MODEL_LOC_SPLIT[0:-1])
        MODEL_CYCLES_FILE = os.path.join(MODEL_LOC,"individual_averages.json")
        THE_MODEL_CYCLES = tools.load_model_cycle(MODEL_CYCLES_FILE)
        MODEL_USERS = [ THE_MODEL_CYCLES[i]["User"] for i, j in enumerate(THE_MODEL_CYCLES)]
        return (MODEL_USERS)