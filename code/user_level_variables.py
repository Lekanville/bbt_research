#!python
#!/usr/bin/env python3

#############################################################################################
#The “learning_variables.py” script 
#The script expects the output file from the previous rule (cycle_level_data) as input and will 
#output the features to a CSV file. After the the input is read the user level data is computed
#from the cycle level data.
#############################################################################################

import numpy as np
import pandas as pd
import os
import argparse
from dtaidistance import dtw
from sklearn.preprocessing import StandardScaler
import argparse
from loguru import logger

import itertools
import tools.tools as tools

parser = argparse.ArgumentParser(description= "A script to filter data")
parser.add_argument('-i', '--input_file', type=str, required=True, help= 'The input dataset')
parser.add_argument('-o', '--output_file', type=str, required=True, help= 'The output dataset')

def the_user_level_variables(INPUT, OUTPUT):
    df = pd.read_csv(INPUT)
    users = (set(df["User"]))
    user_lvl_ftrs = []
    
    scalerStandard = StandardScaler()
    
    for i in users:
        test_df = df[df["User"] == i]
        cycles = list(test_df["Cycle"])
        combinations = list(itertools.combinations(cycles, 2)) #mathematical combination

        #Calculating Pairwise distances and path lengths
        distances = []
        path_lengths = []
        for sub_set in combinations:
            cycle_1 = sub_set[0]
            cycle_2 = sub_set[1]

            data_1 = test_df[test_df["Cycle"] == cycle_1]["Smooth_Temp"].values[0]
            data_2 = test_df[test_df["Cycle"] == cycle_2]["Smooth_Temp"].values[0]

            data_1 = data_1.replace("[", "").replace("]", "").replace(",", "").split(" ")
            data_2 = data_2.replace("[", "").replace("]", "").replace(",", "").split(" ")

            #data_1 = [i for i in data_1 if i != ""]
            data_1 = list(map(float, data_1))
            data_1 = scalerStandard.fit_transform(np.array(data_1).reshape(-1, 1)).reshape(-1)
            
            #data_2 = [i for i in data_2 if i != ""]
            data_2 = list(map(float, data_2))
            data_2 = scalerStandard.fit_transform(np.array(data_2).reshape(-1, 1)).reshape(-1)

            #d, paths, best_path = dtw_m.warping_paths(np.array(data_1), np.array(data_2), return_optimal_warping_path=True)

            d, paths = dtw.warping_paths(np.array(data_1), np.array(data_2))
            best_path = dtw.warping_path(np.array(data_1), np.array(data_2))

            #Getting the length of warping line and warping amount - obtained by getting the points were the 
            #2 positions are not the same)    
            #min_warp = min([j for i, j in enumerate(best_path) if j[0] != j[1]]) #minimun warped point 
            #max_warp = max([j for i, j in enumerate(best_path) if j[0] != j[1]]) #maximum warped point

            #min_ind = best_path.index(min_warp)
            #max_ind = best_path.index(max_warp)
            #warped_points = best_path[min_ind:max_ind+1]

            #Getting the length of warping line and warping amount
            path_x_axis = [x[0] for x in best_path]
            path_y_axis = [x[1] for x in best_path]
            path_length = tools.length_of_line(path_y_axis, path_x_axis)

            distances.append(d)
            path_lengths.append(path_length)

        #Average Pairwise distances and path lengths
        med_pair_distances = np.median(distances)
        med_pair_lengths = np.median(path_lengths)


        #Other cycle level features
        Data_Length = list(test_df["Data_Length"])
        Cycle_Length = list(test_df["Next Cycle Difference"])
        Cycle_Completeness = list(test_df["Cycle Completeness"])
        Curve_by_Data = list(test_df["Curve_by_Data" ])
        Max_of_2_Periods = list(test_df["max_of_2_periods"])
        Max_Pos_of_2_Periods = list(test_df["max_pos_of_2_periods"])
        Max_of_3_Periods = list(test_df["max_of_3_periods"])
        Max_Pos_of_3_Periods = list(test_df["max_pos_of_3_periods"])
        Change_Point_Day = list(test_df["Change Point Day"])
        Change_Point_Mean_Diff = list(test_df["Change Point Mean Diff"])
        Path_Length_with_Diff = list(test_df["path_length_with_diff"])
        Standard_Nadir_Temp_Actual = list(test_df["Standard_nadir_temp_actual"])
        Standard_Peak_Temp_Actual = list(test_df["Standard_peak_temp_actual"])
        Low_to_High_Temp = list(test_df["Standard_low_to_high_temp"])
        Cost_with_Diff = list(test_df["cost_with_diff"])
        Standard_Nadir_Day = list(test_df["Standard_nadir_day"])
        Standard_Peak_Day = list(test_df["Standard_peak_day"])
        Nadir_to_Peak = list(test_df["Standard_nadir_to_peak"])
        Expanded_Nadir_Day = list(test_df["Expanded_nadir_day"])
        Expanded_Peak_Day = list(test_df["Expanded_peak_day"])
        Expanded_Nadir_to_Peak = list(test_df["Expanded_nadir_to_peak"])

        #minimum cycle level features
        min_Data_Length = np.min(Data_Length)
        min_Cycle_Length = np.min(Cycle_Length)
        min_Cycle_Completeness = np.min(Cycle_Completeness)
        min_Curve_by_Data = np.min(Curve_by_Data)
        min_Max_of_2_Periods = np.min(Max_of_2_Periods)
        min_Max_Pos_of_2_Periods = np.min(Max_Pos_of_2_Periods)
        min_Max_of_3_Periods = np.min(Max_of_3_Periods)
        min_Max_Pos_of_3_Periods = np.min(Max_Pos_of_3_Periods)
        min_Change_Point_Day = np.min(Change_Point_Day)
        min_Change_Point_Mean_Diff = np.min(Change_Point_Mean_Diff)
        min_Path_Length_with_Diff = np.min(Path_Length_with_Diff)
        min_Standard_Nadir_Temp_Actual = np.min(Standard_Nadir_Temp_Actual)
        min_Standard_Peak_Temp_Actual = np.min(Standard_Peak_Temp_Actual)
        min_Low_to_High_Temp = np.min(Low_to_High_Temp)
        min_Cost_with_Diff = np.min(Cost_with_Diff)
        min_Standard_Nadir_Day = np.min(Standard_Nadir_Day)
        min_Standard_Peak_Day = np.min(Standard_Peak_Day)
        min_Nadir_to_Peak = np.min(Nadir_to_Peak)
        min_Expanded_Nadir_Day = np.min(Expanded_Nadir_Day)
        min_Expanded_Peak_Day = np.min(Expanded_Peak_Day)
        min_Expanded_Nadir_to_Peak = np.min(Expanded_Nadir_to_Peak)

        #maximum cycle level features
        max_Data_Length = np.max(Data_Length)
        max_Cycle_Length = np.max(Cycle_Length)
        max_Cycle_Completeness = np.max(Cycle_Completeness)
        max_Curve_by_Data = np.max(Curve_by_Data)
        max_Max_of_2_Periods = np.max(Max_of_2_Periods)
        max_Max_Pos_of_2_Periods = np.max(Max_Pos_of_2_Periods)
        max_Max_of_3_Periods = np.max(Max_of_3_Periods)
        max_Max_Pos_of_3_Periods = np.max(Max_Pos_of_3_Periods)
        max_Change_Point_Day = np.max(Change_Point_Day)
        max_Change_Point_Mean_Diff = np.max(Change_Point_Mean_Diff)
        max_Path_Length_with_Diff = np.max(Path_Length_with_Diff)
        max_Standard_Nadir_Temp_Actual = np.max(Standard_Nadir_Temp_Actual)
        max_Standard_Peak_Temp_Actual = np.max(Standard_Peak_Temp_Actual)
        max_Low_to_High_Temp = np.max(Low_to_High_Temp)
        max_Cost_with_Diff = np.max(Cost_with_Diff)
        max_Standard_Nadir_Day = np.max(Standard_Nadir_Day)
        max_Standard_Peak_Day = np.max(Standard_Peak_Day)
        max_Nadir_to_Peak = np.max(Nadir_to_Peak)
        max_Expanded_Nadir_Day = np.max(Expanded_Nadir_Day)
        max_Expanded_Peak_Day = np.max(Expanded_Peak_Day)
        max_Expanded_Nadir_to_Peak = np.max(Expanded_Nadir_to_Peak)

        #median cycle level features
        med_Data_Length = np.median(Data_Length)
        med_Cycle_Length = np.median(Cycle_Length)
        med_Cycle_Completeness = np.median(Cycle_Completeness)
        med_Curve_by_Data = np.median(Curve_by_Data)
        med_Max_of_2_Periods = np.median(Max_of_2_Periods)
        med_Max_Pos_of_2_Periods = np.median(Max_Pos_of_2_Periods)
        med_Max_of_3_Periods = np.median(Max_of_3_Periods)
        med_Max_Pos_of_3_Periods = np.median(Max_Pos_of_3_Periods)
        med_Change_Point_Day = np.median(Change_Point_Day)
        med_Change_Point_Mean_Diff = np.median(Change_Point_Mean_Diff)
        med_Path_Length_with_Diff = np.median(Path_Length_with_Diff)
        med_Standard_Nadir_Temp_Actual = np.median(Standard_Nadir_Temp_Actual)
        med_Standard_Peak_Temp_Actual = np.median(Standard_Peak_Temp_Actual)
        med_Low_to_High_Temp = np.median(Low_to_High_Temp)
        med_Cost_with_Diff = np.median(Cost_with_Diff)
        med_Standard_Nadir_Day = np.median(Standard_Nadir_Day)
        med_Standard_Peak_Day = np.median(Standard_Peak_Day)
        med_Nadir_to_Peak = np.median(Nadir_to_Peak)
        med_Expanded_Nadir_Day = np.median(Expanded_Nadir_Day)
        med_Expanded_Peak_Day = np.median(Expanded_Peak_Day)
        med_Expanded_Nadir_to_Peak = np.median(Expanded_Nadir_to_Peak)
        

        #range of cycle level features
        rge_Data_Length = np.ptp(Data_Length)
        rge_Cycle_Length = np.ptp(Cycle_Length)
        rge_Cycle_Completeness = np.ptp(Cycle_Completeness)
        rge_Curve_by_Data = np.ptp(Curve_by_Data)
        rge_Max_of_2_Periods = np.ptp(Max_of_2_Periods)
        rge_Max_Pos_of_2_Periods = np.ptp(Max_Pos_of_2_Periods)
        rge_Max_of_3_Periods = np.ptp(Max_of_3_Periods)
        rge_Max_Pos_of_3_Periods = np.ptp(Max_Pos_of_3_Periods)
        rge_Change_Point_Day = np.ptp(Change_Point_Day)
        rge_Change_Point_Mean_Diff = np.ptp(Change_Point_Mean_Diff)
        rge_Path_Length_with_Diff = np.ptp(Path_Length_with_Diff)
        rge_Standard_Nadir_Temp_Actual = np.ptp(Standard_Nadir_Temp_Actual)
        rge_Standard_Peak_Temp_Actual = np.ptp(Standard_Peak_Temp_Actual)
        rge_Low_to_High_Temp = np.ptp(Low_to_High_Temp)
        rge_Cost_with_Diff = np.ptp(Cost_with_Diff)
        rge_Standard_Nadir_Day = np.ptp(Standard_Nadir_Day)
        rge_Standard_Peak_Day = np.ptp(Standard_Peak_Day)
        rge_Nadir_to_Peak = np.ptp(Nadir_to_Peak)
        rge_Expanded_Nadir_Day = np.ptp(Expanded_Nadir_Day)
        rge_Expanded_Peak_Day = np.ptp(Expanded_Peak_Day)
        rge_Expanded_Nadir_to_Peak = np.ptp(Expanded_Nadir_to_Peak)

        #The dependent variable
        PCOS = list(test_df["PCOS"])[0]

        user = {
            "User":i,

            "med_pair_distances":med_pair_distances, "med_pair_lengths":med_pair_lengths,

            "min_Data_Length":min_Data_Length,
            "min_Cycle_Length":min_Cycle_Length,
            "min_Cycle_Completeness":min_Cycle_Completeness,
            "min_Curve_by_Data":min_Curve_by_Data,
            "min_Max_of_2_Periods":min_Max_of_2_Periods,
            "min_Max_Pos_of_2_Periods":min_Max_Pos_of_2_Periods,
            "min_Max_of_3_Periods":min_Max_of_3_Periods,
            "min_Max_Pos_of_3_Periods":min_Max_Pos_of_3_Periods,
            "min_Change_Point_Day":min_Change_Point_Day,
            "min_Change_Point_Mean_Diff":min_Change_Point_Mean_Diff,
            "min_Path_Length_with_Diff":min_Path_Length_with_Diff,
            "min_Standard_Nadir_Temp_Actual":min_Standard_Nadir_Temp_Actual,
            "min_Standard_Peak_Temp_Actual":min_Standard_Peak_Temp_Actual,
            "min_Low_to_High_Temp":min_Low_to_High_Temp,
            "min_Cost_with_Diff":min_Cost_with_Diff,
            "min_Standard_Nadir_Day":min_Standard_Nadir_Day,
            "min_Standard_Peak_Day":min_Standard_Peak_Day,
            "min_Nadir_to_Peak":min_Nadir_to_Peak,
            "min_Expanded_Nadir_Day":min_Expanded_Nadir_Day,
            "min_Expanded_Peak_Day":min_Expanded_Peak_Day,
            "min_Expanded_Nadir_to_Peak":min_Expanded_Nadir_to_Peak,

            "max_Data_Length":max_Data_Length,
            "max_Cycle_Length":max_Cycle_Length,
            "max_Cycle_Completeness":max_Cycle_Completeness,
            "max_Curve_by_Data":max_Curve_by_Data,
            "max_Max_of_2_Periods":max_Max_of_2_Periods, 
            "max_Max_Pos_of_2_Periods":max_Max_Pos_of_2_Periods,
            "max_Max_of_3_Periods":max_Max_of_3_Periods,
            "max_Max_Pos_of_3_Periods":max_Max_Pos_of_3_Periods,
            "max_Change_Point_Day":max_Change_Point_Day,
            "max_Change_Point_Mean_Diff":max_Change_Point_Mean_Diff,
            "max_Path_Length_with_Diff":max_Path_Length_with_Diff,
            "max_Standard_Nadir_Temp_Actual":max_Standard_Nadir_Temp_Actual,
            "max_Standard_Peak_Temp_Actual":max_Standard_Peak_Temp_Actual,
            "max_Low_to_High_Temp":max_Low_to_High_Temp,
            "max_Cost_with_Diff":max_Cost_with_Diff,
            "max_Standard_Nadir_Day":max_Standard_Nadir_Day,
            "max_Standard_Peak_Day":max_Standard_Peak_Day,
            "max_Nadir_to_Peak":max_Nadir_to_Peak,
            "max_Expanded_Nadir_Day":max_Expanded_Nadir_Day,
            "max_Expanded_Peak_Day":max_Expanded_Peak_Day,
            "max_Expanded_Nadir_to_Peak":max_Expanded_Nadir_to_Peak,

            "med_Data_Length":med_Data_Length,
            "med_Cycle_Length":med_Cycle_Length,
            "med_Cycle_Completeness":med_Cycle_Completeness,
            "med_Curve_by_Data":med_Curve_by_Data,
            "med_Max_of_2_Periods":med_Max_of_2_Periods,
            "med_Max_Pos_of_2_Periods":med_Max_Pos_of_2_Periods,
            "med_Max_of_3_Periods":med_Max_of_3_Periods,
            "med_Max_Pos_of_3_Periods":med_Max_Pos_of_3_Periods,
            "med_Change_Point_Day":med_Change_Point_Day,
            "med_Change_Point_Mean_Diff":med_Change_Point_Mean_Diff,
            "med_Path_Length_with_Diff":med_Path_Length_with_Diff,
            "med_Standard_Nadir_Temp_Actual":med_Standard_Nadir_Temp_Actual,
            "med_Standard_Peak_Temp_Actual":med_Standard_Peak_Temp_Actual,
            "med_Low_to_High_Temp":med_Low_to_High_Temp,
            "med_Cost_with_Diff":med_Cost_with_Diff,
            "med_Standard_Nadir_Day":med_Standard_Nadir_Day,
            "med_Standard_Peak_Day":med_Standard_Peak_Day,
            "med_Nadir_to_Peak":med_Nadir_to_Peak,
            "med_Expanded_Nadir_Day":med_Expanded_Nadir_Day,
            "med_Expanded_Peak_Day":med_Expanded_Peak_Day,
            "med_Expanded_Nadir_to_Peak":med_Expanded_Nadir_to_Peak,

            "rge_Data_Length":rge_Data_Length,
            "rge_Cycle_Length":rge_Cycle_Length,
            "rge_Cycle_Completeness":rge_Cycle_Completeness,
            "rge_Curve_by_Data":rge_Curve_by_Data,
            "rge_Max_of_2_Periods":rge_Max_of_2_Periods,
            "rge_Max_Pos_of_2_Periods":rge_Max_Pos_of_2_Periods,
            "rge_Max_of_3_Periods":rge_Max_of_3_Periods,
            "rge_Max_Pos_of_3_Periods":rge_Max_Pos_of_3_Periods,
            "rge_Change_Point_Day":rge_Change_Point_Day,
            "rge_Change_Point_Mean_Diff":rge_Change_Point_Mean_Diff,
            "rge_Path_Length_with_Diff":rge_Path_Length_with_Diff,
            "rge_Standard_Nadir_Temp_Actual":rge_Standard_Nadir_Temp_Actual,
            "rge_Standard_Peak_Temp_Actual":rge_Standard_Peak_Temp_Actual,
            "rge_Low_to_High_Temp":rge_Low_to_High_Temp,
            "rge_Cost_with_Diff":rge_Cost_with_Diff,
            "rge_Standard_Nadir_Day":rge_Standard_Nadir_Day,
            "rge_Standard_Peak_Day":rge_Standard_Peak_Day,
            "rge_Nadir_to_Peak":rge_Nadir_to_Peak,
            "rge_Expanded_Nadir_Day":rge_Expanded_Nadir_Day,
            "rge_Expanded_Peak_Day":rge_Expanded_Peak_Day,
            "rge_Expanded_Nadir_to_Peak":rge_Expanded_Nadir_to_Peak,

            "PCOS":PCOS
            }
        
        user_lvl_ftrs.append(user)
        
    df_user_lvl_ftrs = pd.DataFrame(user_lvl_ftrs)
    df_user_lvl_ftrs.to_csv(OUTPUT, index=False)
    logger.info(f"User Level Variables: {OUTPUT}")

if __name__ == "__main__":
    args = parser.parse_args()
    the_user_level_variables(args.input_file, args.output_file)