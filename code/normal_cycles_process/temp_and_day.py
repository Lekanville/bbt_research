#The first aspect of the script reads the temperature data, ensures the values are 
#within the acceptable range and the groups the values by the uses and cycles.
#The secomd aspect of the script tried to locate missing days, esures that the missing
# days are not more than 10 and then interpolate for the missing days if they exist

import pandas as pd

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