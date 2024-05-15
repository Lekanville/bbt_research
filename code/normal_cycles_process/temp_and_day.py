#The first aspect of the script reads the temperature data, ensures the values are 
#within the acceptable range and the groups the values by the uses and cycles.
#The secomd aspect of the script tried to locate missing days, esures that the missing
# days are not more than 10 and then interpolate for the missing days if they exist

import numpy as np
import pandas as pd
import os
from datetime import datetime, date, timedelta, timezone
from loguru import logger
from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import normal_cycles_process.DBA as DBA
import tools.tools as tools

from classes.classes import Frames

def get_temps(temps):
    #read the temperatures dataset (from sel_crt_2)
    temp_sort = Frames(temps).read_temp() #read the temperatures
    temp_sort["Mean_Temp"] = temp_sort["Mean_Temp"].apply(lambda x: int(x)) #convert data to integer type
    temp_final = temp_sort[(temp_sort["Mean_Temp"] > 35000) & (temp_sort["Mean_Temp"] < 40000)] #ensures that true values are selected
    
    #Group the temperatures by the user IDs and cycle IDs
    group_temp = temp_final.groupby(["User ID", "Cycle ID"])

    return group_temp

def actual_day(user, cycle, group_temp):
    #Computing the actual recording day while considering missing temperature days

    cycle_temp = group_temp.get_group((user, cycle)).sort_values("Date").reset_index(drop=True)#the temperature values of the cycle
    cycle_temp["Date"] = pd.to_datetime(cycle_temp["Date"])
    cycle_temp = cycle_temp.drop_duplicates(subset="Date", keep = "first").set_index("Date")#this deals with cycles with duplicate dates
    start = str(cycle_temp.index.min()).split(" ")[0]
    end = str(cycle_temp.index.max()).split(" ")[0]

    df_reindexed = pd.DataFrame(cycle_temp.reindex(pd.date_range(start, end)).isnull().all(1), columns=["Missing_Day"])
    temperature_vals = pd.merge(cycle_temp,  df_reindexed, left_on=cycle_temp.index, right_on= df_reindexed.index, how = "outer", sort = True)
    
    temperature_vals["Missing_length"] = 0

    for i in (temperature_vals[temperature_vals["Missing_Day"] == True].index):
        last_day_before_miss = temperature_vals.iloc[0:i][temperature_vals.iloc[0:i]["Missing_Day"] == False].tail(1).index
        first_day_after_miss = temperature_vals.iloc[i:][temperature_vals.iloc[i:]["Missing_Day"] == False].head(1).index
        
        temperature_vals.loc[i, "Missing_length"] = first_day_after_miss - last_day_before_miss - 1
        
    try:    
        missed = temperature_vals[temperature_vals["Missing_length"] > 10].head(1).index.values[0] #if there are more than 10 missing days
        temperature_vals = temperature_vals.iloc[0:missed] #drop all recordings after 10 missing days
    except IndexError:
        temperature_vals = temperature_vals #otherwise keep all temperatures with the missing dates
    
    temperature_vals["Mean_Temp"] = temperature_vals["Mean_Temp"].interpolate(method = "linear", limit_direction = "forward")
    temperature_vals["Cycle ID"] = temperature_vals["Cycle ID"].fillna(method = "pad") #fill the missing cycle IDs
    temperature_vals["User ID"] = temperature_vals["User ID"].fillna(method = "pad") #fill the missing user IDs
        
    return temperature_vals

def model_temps_process(cycle, grouped_temps):
    cycle_temp = grouped_temps.get_group(cycle).sort_values("Date")
    
    #Convert date to datetime format
    cycle_temp["Date"] = pd.to_datetime(cycle_temp["Date"])
    
    #Set date as index. There cannot be duplicates on the index so duplicate values must be dealth with
    cycle_temp = cycle_temp.drop_duplicates(subset="Date", keep = "first").set_index("Date")
    
    #get the start and end dates
    start = str(cycle_temp.index.min()).split(" ")[0]
    end = str(cycle_temp.index.max()).split(" ")[0]
    
    #get the dates in the range of the cycle and put in a dataframe
    df_reindexed = pd.DataFrame(cycle_temp.reindex(pd.date_range(start, end)).isnull().all(1), columns=["Missing_Day"])
    
    #Combine the temperature data with the data range to view missing days
    temperature_vals = pd.merge(cycle_temp,  df_reindexed, left_on=cycle_temp.index, right_on= df_reindexed.index, how = "outer", sort = True)
    
    #This set of code lines drops records after 10 consequtive days of missing values
    temperature_vals["Missing_length"] = 0

    for i in (temperature_vals[temperature_vals["Missing_Day"] == True].index):
        last_day_before_miss = temperature_vals.iloc[0:i][temperature_vals.iloc[0:i]["Missing_Day"] == False].tail(1).index
        first_day_after_miss = temperature_vals.iloc[i:][temperature_vals.iloc[i:]["Missing_Day"] == False].head(1).index
        
        temperature_vals.loc[i, "Missing_length"] = first_day_after_miss - last_day_before_miss - 1
        
    try:    
        missed = temperature_vals[temperature_vals["Missing_length"] > 10].head(1).index.values[0] #if there are more than 10 missing days
        temperature_vals = temperature_vals.iloc[0:missed] #drop all recordings after 10 missing days
    except IndexError:
        temperature_vals = temperature_vals #otherwise keep all temperatures with the missing dates
    
    temperature_vals["Mean_Temp"] = temperature_vals["Mean_Temp"].interpolate(method = "linear", limit_direction = "forward")
    temperature_vals["Cycle ID"] = temperature_vals["Cycle ID"].fillna(method = "pad") #fill the missing cycle IDs
    temperature_vals["User ID"] = temperature_vals["User ID"].fillna(method = "pad") #fill the missing user IDs

    return (temperature_vals)


#Selecting those who indicated "I am just interested in monitoring my cycles
def select_models_questionnaire(data_quest, temps_data):
    model_users = []
    quest_models = data_quest[~(pd.isnull(data_quest[727])) &
                (data_quest[219] != "Poly cystic ovarian syndrom ") &
            (data_quest[688] != "amenohrea ") &
            (pd.isnull(data_quest[679]))][1].to_list()
    models_unique = list(np.unique(quest_models))

    for i in models_unique:
        user_temps = temps_data[temps_data["User ID"] == i]
        if len(user_temps) > 0:
            model_users.append(i)

    return (model_users)

#Selecting the cycles to average as the model cycle
def model_temps(the_model_users, temps_data):
    all_model_temps = pd.DataFrame()
    data_lengths = []
    for i in the_model_users:
        user_temps = temps_data[temps_data["User ID"] == i]
        user_cycles = list(user_temps["Cycle ID"].unique())
        user_temp_grouped = user_temps.groupby("Cycle ID")

        for j in user_cycles:
            processed_temps = model_temps_process(j, user_temp_grouped)

            length = len(processed_temps)
            cycle_length = {"Cycle": j, "Data_Length":length}
            data_lengths.append(cycle_length)

            all_model_temps = pd.concat([all_model_temps, processed_temps], axis = 0, ignore_index=True)
    
    lengths_df = pd.DataFrame(data_lengths)

    return (all_model_temps, lengths_df)


#Filtering the cycles to use as reference
def filtering(temps_dur, lenghts):
    all_refs = []
    notlast = []
    initial_offset = []
    complete_cycles = []
    length_of_data = []

    the_cycles = lenghts["Cycle"].to_list()
    for i in the_cycles: #get cycles that are not the last cycles
        try:
            end = temps_dur[temps_dur["Cycle ID"] == i]["Date_Diff"].values[0]
        except IndexError:
            end = "none"

        if (str(end) != "none") & (str(end) != "Indeterminate Last Cycle"):
            notlast.append(i)
    print("Non last cycles-", len(notlast))
    #logger.info("Non last cycles-", len(notlast))

    for c in notlast: #get cycles that has less that 7 missing days at the beginning
        offset = temps_dur[temps_dur["Cycle ID"] == c]["Offset"].values[0]

        if (offset <= 7):
            initial_offset.append(c) 
    print("Cycles with early starts-", len(initial_offset))
    #logger.info("Cycles with early starts-", len(initial_offset))  

    for c in initial_offset: #get cycles with data close to the end of the cycle
        offset = int(temps_dur[temps_dur["Cycle ID"] == c]["Offset"].values[0])
        end = int(temps_dur[temps_dur["Cycle ID"] == c]["Date_Diff"].values[0])
        Data_Length = int(lenghts[lenghts["Cycle"] == c]["Data_Length"].values[0])
        completeness = end - (offset+Data_Length)
        
        if (completeness < 1):
            complete_cycles.append(c) 

    print("Cycles with less than 1 end missingness-", len(complete_cycles))
    #logger.info("Cycles with less than 1 end missingness-", len(complete_cycles))  

    for c in complete_cycles: #the cycle lengths
        Data_Length = int(temps_dur[temps_dur["Cycle ID"] == c]["Date_Diff"].values[0])

        if (Data_Length >= 25) & (Data_Length <= 31):
            length_of_data.append(c) 
            
    print("Cycles with lengths between 25 and 32-", len(length_of_data))
    #logger.info("Cycles with lengths between 25 and 32-", len(length_of_data))  

    return length_of_data        


def intepolate_offsets(temps_model, temps_dur, cycles_models, output):
    temps_model.rename({"key_0":"Date"}, axis = 1, inplace=True)
    temps_model["Date"] = pd.to_datetime(temps_model["Date"])
    all_model_temps = pd.DataFrame()

    #for each cycle
    for c in cycles_models:
        cycle_temps = temps_model[temps_model["Cycle ID"] == c]
        user = cycle_temps["User ID"].unique()[0]
        offset = int(temps_dur[temps_dur["Cycle ID"] == c]["Offset"].values[0])
        date_diff = int(temps_dur[temps_dur["Cycle ID"] == c]["Date_Diff"].values[0])
        #first_date = datetime.strptime(str(cycle_temps.head(1)["Date"].values[0]).split("T")[0], '%Y-%m-%d')
        first_date = datetime.fromisoformat(str(cycle_temps.head(1)["Date"].values[0])).astimezone(timezone.utc)

        #get the offset and the first date of recording 
        j = offset
        offset_date = first_date
        dates_to_interpolate = []

        #computes dates in the offset
        while j > 0:
            date_offset = (first_date - timedelta(days=j)).date()
            formated_date = date_offset.strftime('%Y-%m-%d')
            dates_to_interpolate.append(formated_date)
            j = j-1

        #get the last date on the cycle
        last_temp = cycle_temps.tail(1)["Mean_Temp"].values[0]

        #create df of the offset dates and merge with the cycle dates
        if len(dates_to_interpolate) > 0 :
            offset_df = pd.DataFrame(dates_to_interpolate, columns=["Date"])
            offset_df["User ID"] = user
            offset_df["Cycle ID"] = c
            offset_df.loc[0, "Mean_Temp"] = last_temp
            offset_df["Missing_length"] = offset
            offset_df["Missing_Day"] = True
            cycle_df = pd.concat([offset_df, cycle_temps], axis=0, ignore_index=True)

            #interpolate missing dates
            cycle_df["Mean_Temp"] = cycle_df["Mean_Temp"].interpolate(method = "linear", limit_direction = "forward")
        else: #for cycles with no offset
            cycle_df = cycle_temps.copy().reset_index(drop = True)

        cycle_df["Date"] = pd.to_datetime(cycle_df["Date"])
        #cycle_df["Cycle ID"] = cycle_df["Cycle ID"].fillna(method = "backfill") #fill the missing cycle IDs
        #cycle_df["User ID"] = cycle_df["User ID"].fillna(method = "backfill") #fill the missing user IDs

        cycle_df["Smooth_Temp"] = savgol_filter(cycle_df["Mean_Temp"], 10, 2)
        cycle_df["Date_Diff"] = date_diff

        #standardizing the smooth values    
        scalerStandard = StandardScaler()
        mean_temps = cycle_df["Mean_Temp"].to_list()
        smooth_temps = cycle_df["Smooth_Temp"].to_list()

        Standard_mean_temps = scalerStandard.fit_transform(np.array(mean_temps).reshape(-1, 1))
        Standard_smooth_temps = scalerStandard.fit_transform(np.array(smooth_temps).reshape(-1, 1))

        Standard_mean_temps = [i for j in Standard_mean_temps for i in j]
        Standard_smooth_temps = [i for j in Standard_smooth_temps for i in j]

        standardized_mean_df = pd.DataFrame(Standard_mean_temps, columns=["Standard_mean_temps"])
        standardized_smooth_df = pd.DataFrame(Standard_smooth_temps, columns=["Standard_smooth_temps"])
        #standardized_mean_df["Standard_smooth_temps"] = savgol_filter(standardized_mean_df["Standard_mean_temps"], 10, 2)

        #add the standardized temperatures to the cycle dataframe
        cycle_df = pd.concat([cycle_df, standardized_mean_df, standardized_smooth_df], axis = 1)
        #cycle_df = pd.concat([cycle_df, standardized_mean_df], axis = 1)

        #standardizing the x-axis
        cycle_pos = cycle_df.index.to_list()
        scalerMinMax = MinMaxScaler()
        Normal_Positions = scalerMinMax.fit_transform(np.array(cycle_pos).reshape(-1, 1))
        Normal_Positions = [i for j in Normal_Positions for i in j]
        Normal_Positions_df = pd.DataFrame(Normal_Positions, columns=["Normal_Positions"])
        cycle_df = pd.concat([cycle_df, Normal_Positions_df], axis = 1)
        
        #concatenate with the rest of the references
        all_model_temps = pd.concat([all_model_temps, cycle_df], axis = 0)

    save_file = os.path.join(output, "all_model_temps.csv")
    all_model_temps.to_csv(save_file)
    return (all_model_temps)


def ref_DBA_averaging(all_model_temps, output):
    users = list(all_model_temps["User ID"].unique())
    individual_avarages = []
    for user in users:
        user_cycles_temps = []

        user_df = all_model_temps[all_model_temps["User ID"] == user]
        user_cycles = list(user_df["Cycle ID"].unique())

        for cycle in user_cycles:
            cycle_temps = user_df[user_df["Cycle ID"] == cycle]["Standard_smooth_temps"].to_list()
            cycle_temps = np.array(cycle_temps)
            user_cycles_temps.append(cycle_temps)

        user_temps = np.array(user_cycles_temps, dtype=object)

        if len(user_temps) > 1:
            user_averaged = DBA.performDBA(user_temps)
            user_averaged = list(user_averaged)
        else:
            user_averaged = [i for j in user_temps for i in j]

        user_avg = {"User":user, "user_averaged":user_averaged}
        individual_avarages.append(user_avg)

    out_file = os.path.join(output, "individual_averages.json")
    tools.save_model_cycle(individual_avarages, out_file)

    to_average = []
    for avg in individual_avarages:
        avg_temps = avg["user_averaged"]
        to_average.append(np.array(avg_temps))
    
    to_average_final =  np.array(to_average,  dtype=object)
    model_cycle = DBA.performDBA(to_average_final)
    #print(model_cycle)
    model_cycle = {"model_cycle":list(model_cycle)}

    return (model_cycle)

