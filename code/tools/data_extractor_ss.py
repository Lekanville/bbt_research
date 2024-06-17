#!python
#!/usr/bin/env python3

#############################################################################################
#The “data_extractor.py” script - this version use z-normalization (standard scaling)
#This script extracts the cycle level features of the data. To make it faster, horizontal scaling
#usimg multiprocessing is employed for the task. 
#The first part of the script tries to locate missing days that are not more than 10 at a
#single instance and then gets interpolated results for the missings days. 
#The second aspect of the script then compares each cycle for a user with the model cycles.
#This is done first by z-normalizing the cycles and then performaing dynamic time warping on the
#on bothe the model and the cycle. The nadirs, peaks and other related cycle level data are 
#then calculated from dtw results.
#The last part of the script calculates the length of the curve, the length of the data and 
#then calculates the dives the length of the curve by the length of the data.
# The last part is the entry point into the clas and handle the parallelization of the script
#############################################################################################

from multiprocess import Pool
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tqdm import tqdm

import tools.tools as tools

#Iniatial DTW method
from dtaidistance import dtw

#DTW with missing values
import dtw_missing.dtw_missing as dtw_m
import dtw_missing.dtw_missing_visualisation as dtw_m_vis

def actual_day(group_temp, user, cycle):
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
        missed = temperature_vals[temperature_vals["Missing_length"] > 10].head(1).index.values[0] #more than 10 missing days
        temperature_vals = temperature_vals.iloc[0:missed] #drop all recordings after 10-day miss
    except IndexError:
        temperature_vals = temperature_vals #otherwise keep all temperatures with the missing dates

    temperature_vals["Mean_Temp"] = temperature_vals["Mean_Temp"].interpolate(method = "linear", limit_direction = "forward")
    temperature_vals["Cycle ID"] = temperature_vals["Cycle ID"].fillna(method = "pad") #fill the missing cycle IDs
    temperature_vals["User ID"] = temperature_vals["User ID"].fillna(method = "pad") #fill the missing user IDs

    return temperature_vals


def slope_nadir_peak(user, user_cycles, cycle, temp_vals, model_cycle):
    model_cycle = tools.load_model_cycle(model_cycle)['model_cycle']#the model cycle 
    keep = user_cycles[user_cycles.index == cycle]
    date_dur = keep["Data_Dur"].values[0]#get the data duration of the cycle
    offset = int(keep["Offset"])#get the offset of the cycle
    #Date_D = keep["Date_Diff"].values#get the cycle length of the cycle
    Date_Diff = keep["Date_Diff"].values[0]
    #ovul = user_cycles[user_cycles.index == cycle.lower()]["Ovulation Day"]#get the ovulation date of the cycle
    ovul = user_cycles[user_cycles.index == cycle]["Ovulation Day"]#get the ovulation date of the cycle
    PCOS = keep["PCOS"].values[0]

    # if Date_D == "Indeterminate Last Cycle":
    #     Date_Diff = ""#the last cycle
    # else:
    #     Date_Diff = int(Date_D) #all cycles asides the last cycle    

    if str(ovul.values) == "[nan]":
        ovulation = ""#ovulation dates not found
    else:
        ovulation = int(ovul) #ovulation dates found

    cycle_temp = temp_vals#the temperature data frame of the cycle

    #Smoothing the temperatures    
    try:
        cycle_temp["Smooth_Temp"] = savgol_filter(cycle_temp["Mean_Temp"], 10, 2)#smoothing the temperature values across 10 days and polynomial order 2
    except ValueError:
        cycle_temp["Smooth_Temp"] = savgol_filter(cycle_temp["Mean_Temp"], len(cycle_temp), 2)#if the number of days is not up to 10, we smooth across the entire data


    #Computing Nadirs and Peaks with "Dynamic Time Warping" 
    temps = list(cycle_temp["Mean_Temp"])#wrapping the cycle temperatures into a list
    #model_cycle = load_model_cyle()['model']#the model cycle    
    smooth_temps = list(cycle_temp["Smooth_Temp"])#the smooth cycle temperatures

    #if  (Date_Diff != ""):

    # if (offset < 0) & ((offset + len(smooth_temps)) < 0):
    #     head = 0
    #     tail = 0
    #     smooth_temps_before = []

    # elif (offset < 0) & ((offset + len(smooth_temps)) > 0):
    #     #tail = Date_Diff - (offset + len(smooth_temps))
    #     smooth_temps_before = smooth_temps[abs(offset):]
    #     head = 0
    #     tail = Date_Diff - len(smooth_temps_before)

    # elif (offset >= 0):
    head = offset
    tail = Date_Diff - (offset + len(smooth_temps))
    smooth_temps_before = smooth_temps
    print(smooth_temps_before)

    head_data = [np.nan]*head
    tail_data = [np.nan]*tail
    print ("head: ", head)
    print("head_data", head_data)
    print ("tail: ", tail)
    print("tail_data", tail_data)

    smooth_temps_after = head_data + smooth_temps_before + tail_data #add head and tail missing records to the data
    print(smooth_temps_after)

        # if (offset >= 0) & (smooth_temps_after != Date_Diff):
        #     if len(smooth_temps_after) != Date_Diff :
        #         print("There is a problem here: ", cycle)
        #         print ("The Offset is: ", offset)
        #         print ("The Length Before is: ", len(smooth_temps_before))
        #         print ("The Summed Length is: ", Date_Diff)
        #         print ("The Final Length is: ", len(smooth_temps_after))

        #         print ("Tail is: ", tail)
        #         print ((head_data))
        #         print ((tail_data))
        #         print("The actual smooth temps", smooth_temps)
        #         print ("Smooth Temps before:", smooth_temps_before)

        
    # else:
    #      smooth_temps_after =  smooth_temps
    
    Expanded_smooth_temps = tools.get_expanded_values(smooth_temps_after)

    #standardizing the smooth values    
    scalerStandard = StandardScaler()
    #Since the model cycle was computed as an average of standardized normal cycles, i do not think there is a need to standardize anymore
    #Standard_model_cycle = scalerStandard.fit_transform(np.array(model_cycle).reshape(-1, 1))
    Standard_model_cycle = model_cycle

    Standard_smooth_temps_initial = scalerStandard.fit_transform(np.array(Expanded_smooth_temps).reshape(-1, 1))
    Standard_smooth_temps = Standard_smooth_temps_initial.reshape(-1)
    #interpolate standardized cycle temperatures to obtain 51 points inclusive of missing head and tail values
    #1. First get the missing head and tail values

    #print (Standard_smooth_temps)
    #2. Then interpolate the 51 points
    #Standard_smooth_temps = tools.get_expanded_values(Standard_smooth_temps)


    #Initial dtw method    
    # Standard_path = dtw.warping_path(Standard_model_cycle, Standard_smooth_temps)
    # Standard_distance = "{0:.2f}".format(dtw.distance(Standard_model_cycle, Standard_smooth_temps))
    # d, Standard_path_values = dtw.warping_paths(Standard_model_cycle, Standard_smooth_temps)

    #for those with zero or positive offsets, the DTW with missigness algorithm is used
    if (offset >= 0):
        d, Standard_path_values, Standard_path = dtw_m.warping_paths(np.array(Standard_model_cycle), np.array(Standard_smooth_temps), return_optimal_warping_path=True)
        Standard_distance = "{0:.2f}".format(d)
    
    #for those with negative offsets, the regular DTW was used just to avoid errors with the data return. We will not use them in the analysis
    else:
        # Standard_path = dtw.warping_path(Standard_model_cycle, Standard_smooth_temps)
        # Standard_distance = "{0:.2f}".format(dtw.distance(Standard_model_cycle, Standard_smooth_temps))
        # d, Standard_path_values = dtw.warping_paths(Standard_model_cycle, Standard_smooth_temps)
        d, Standard_path_values, Standard_path = dtw_m.warping_paths(np.array(Standard_model_cycle), np.array(Standard_smooth_temps), return_optimal_warping_path=True)
        Standard_distance = "{0:.2f}".format(d)

    cycle_max_pos = len(Standard_smooth_temps) - 1

    #Getting the length of warping line and warping amount
    path_x_axis = [x[0] for x in Standard_path]
    path_y_axis = [x[1] for x in Standard_path]
    initial_path_length = tools.length_of_line(path_y_axis, path_x_axis)
    pos_count_with_diff, path_length_with_diff, cost_with_diff = tools.other_dtw_values(Standard_path, Standard_path_values, cycle_max_pos)
    #warp_deg = tools.warp_degree(path_y_axis, path_x_axis) Louise said we should remove this


    # print("Cycle ID", cycle)
    # print("Smooth Temps", smooth_temps)
    # print("Smooth Temps with NAs", smooth_temps_after)
    # print("Length of the expanded smooths", len(expanded_smooth_temps))
    # print("The expanded smooths", expanded_smooth_temps)
    # print("The length of the standardized values", len(Standard_smooth_temps))
    # print("The standardized values", Standard_smooth_temps)
    # print(Standard_path)

    # print("*******************************")

    #Computing nadir and peak using DTW and standardized temperature values
    #Standard_nadir_day, Standard_nadir_temp, Standard_nadir_temp_actual, Standard_peak_day, Standard_peak_temp, Standard_peak_temp_actual = tools.get_nadirs_and_peaks(Standard_smooth_temps, Standard_path, smooth_temps, model_cycle)
    Standard_nadir_day, Standard_nadir_temp, Standard_nadir_temp_actual, Standard_peak_day, Standard_peak_temp, Standard_peak_temp_actual = tools.get_nadirs_and_peaks(
        Standard_smooth_temps, Standard_path, Expanded_smooth_temps, model_cycle, cycle
        )

    #Nadir and Peak Validity Check
    temp_diffs = [smooth_temps[i+1] - smooth_temps[i] for i in range(len(smooth_temps)-1)]
    lower_curve_list = temp_diffs[:Standard_nadir_day]
    top_curve_list = temp_diffs[Standard_peak_day:]

    nadir_valid = any(i < 0 for i in lower_curve_list)
    peak_valid = any(i < 0 for i in top_curve_list)

    #Time from nadir to peak using Standard Scaling
    Standard_nadir_to_peak = Standard_peak_day - Standard_nadir_day

    #Difference between lowest and highest temperature using Standard Scaling
    Standard_low_to_high_temp = Standard_peak_temp_actual - Standard_nadir_temp_actual

    #we create a dictionary of the results for each cycle
    data = {"User":user, "Cycle":cycle, "Temps":temps, "Smooth_Temp":smooth_temps, "Smooth_Temp_with_NAs": smooth_temps_after,
            "Ovulation Day":ovulation, "Next Cycle Difference":Date_Diff, "Offset":offset, "PCOS":PCOS,

            "Standard_model_cycle":Standard_model_cycle, "Standard_smooth_temps":Standard_smooth_temps, "Expanded_smooth_temps": Expanded_smooth_temps,
            "Standard_distance":Standard_distance, "Standard_path":Standard_path, 
            "Standard_nadir_day":Standard_nadir_day, "Standard_peak_day":Standard_peak_day, 
            "Standard_nadir_temp":Standard_nadir_temp, "Standard_peak_temp":Standard_peak_temp,
            "Standard_nadir_temp_actual":Standard_nadir_temp_actual, "Standard_peak_temp_actual":Standard_peak_temp_actual,
            "Standard_nadir_to_peak":Standard_nadir_to_peak, "Standard_low_to_high_temp":Standard_low_to_high_temp,
            "nadir_valid":nadir_valid, "peak_valid":peak_valid,
            "initial_path_length":initial_path_length, "pos_count_with_diff":pos_count_with_diff, "path_length_with_diff":path_length_with_diff, 
            "cost_with_diff":cost_with_diff
        }

    return data


def curve_by_length(nad_and_peak):
    offset = nad_and_peak["Offset"]
    yaxis = nad_and_peak["Smooth_Temp"]
    xaxis = [k + offset for k in range(len(yaxis))]

    curve_length = tools.length_of_line(yaxis, xaxis)
    data_length = len(yaxis)
    curve_by_data = curve_length/(data_length - 1)

    distance = {"Curve_Length":curve_length, "Data_Length":data_length, "Curve_by_Data":curve_by_data}

    return distance

