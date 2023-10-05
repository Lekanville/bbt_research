#!python
#!/usr/bin/env python3

#############################################################################################
#The “learning_variables.py” script - this is for standardization
#The script expects the output file from the previous rule (cycle_level_data) as input and will 
#output the features to a CSV file. After the the input is read the user level data is computed
#from the cycle level data.
#############################################################################################

import numpy as np
import pandas as pd
import os
import argparse
from dtaidistance import dtw

import itertools
import tools.tools as tools

parser = argparse.ArgumentParser(description= "A script to filter data")
parser.add_argument('-i', '--input_file', type=str, required=True, help= 'The input dataset')
parser.add_argument('-o', '--output_file', type=str, required=True, help= 'The output dataset')

def the_user_level_variables(INPUT, OUTPUT):
    df = pd.read_csv(INPUT)
    users = (set(df["User"]))
    user_lvl_ftrs = []
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

            data_1 = test_df[test_df["Cycle"] == cycle_1]["Standard_smooth_temps"].values[0]
            data_2 = test_df[test_df["Cycle"] == cycle_2]["Standard_smooth_temps"].values[0]

            data_1 = data_1.replace("[[", "").replace("]", "").replace("\n", "").replace("[", "").replace("]]", "").split(" ")
            data_2 = data_2.replace("[[", "").replace("]", "").replace("\n", "").replace("[", "").replace("]]", "").split(" ")

            data_1 = [i for i in data_1 if i != ""]
            data_1 = list(map(float, data_1))
            data_2 = [i for i in data_2 if i != ""]
            data_2 = list(map(float, data_2))

            d, paths = dtw.warping_paths(np.array(data_1), np.array(data_2), window=None)
            best_path = dtw.best_path(paths)

            #Getting the length of warping line and warping amount
            path_x_axis = [x[0] for x in best_path]
            path_y_axis = [x[1] for x in best_path]
            path_length = tools.length_of_line(path_y_axis, path_x_axis)

            distances.append(d)
            path_lengths.append(path_length)

        #Pairwise distances and path lengths
        #c1_c2_dist = distances[0]
        #c1_c3_dist = distances[1]
        #c2_c3_dist = distances[2]

        #Pairwise path lengths
        #c1_c2_path_len = path_lengths[0]
        #c1_c3_path_len = path_lengths[1]
        #c2_c3_path_len = path_lengths[2]

        #Average Pairwisedistances and path lengths
        med_pair_distances = np.median(distances)
        med_pair_lengths = np.median(path_lengths)

        #Other cycle level features
        dist_to_model = list(test_df["Standard_distance"])
        nadir_days = list(test_df["Standard_nadir_day"])
        peak_days = list(test_df["Standard_peak_day"])
        nadir_temps = list(test_df["Standard_nadir_temp_actual"])
        peak_temps = list(test_df["Standard_peak_temp_actual"])
        nadirs_to_peaks = list(test_df["Standard_nadir_to_peak"])
        low_to_high_temps = list(test_df["Standard_low_to_high_temp"])
        path_length_to_model = list(test_df["path_length"])
        warp_degree_with_model = list(test_df["warp_degree"])
        Curve_Lengths = list(test_df["Curve_Length"])
        Data_Lengths = list(test_df["Data_Length"])
        Curves_by_Data = list(test_df["Curve_by_Data"])

        #minimum cycle level features
        min_dist_to_model = np.min(list(test_df["Standard_distance"]))
        min_nadir_days = np.min(list(test_df["Standard_nadir_day"]))
        min_peak_days = np.min(list(test_df["Standard_peak_day"]))
        min_nadir_temps = np.min(list(test_df["Standard_nadir_temp_actual"]))
        min_peak_temps = np.min(list(test_df["Standard_peak_temp_actual"]))
        min_nadirs_to_peaks = np.min(list(test_df["Standard_nadir_to_peak"]))
        min_low_to_high_temps = np.min(list(test_df["Standard_low_to_high_temp"]))
        min_path_length_to_model = np.min(list(test_df["path_length"]))
        min_warp_degree_with_model = np.min(list(test_df["warp_degree"]))
        min_Curve_Lengths = np.min(list(test_df["Curve_Length"]))
        min_Data_Lengths = np.min(list(test_df["Data_Length"]))
        min_Curves_by_Data = np.min(list(test_df["Curve_by_Data"]))
        
        #minimum cycle level features
        max_dist_to_model = np.max(list(test_df["Standard_distance"]))
        max_nadir_days = np.max(list(test_df["Standard_nadir_day"]))
        max_peak_days = np.max(list(test_df["Standard_peak_day"]))
        max_nadir_temps = np.max(list(test_df["Standard_nadir_temp_actual"]))
        max_peak_temps = np.max(list(test_df["Standard_peak_temp_actual"]))
        max_nadirs_to_peaks = np.max(list(test_df["Standard_nadir_to_peak"]))
        max_low_to_high_temps = np.max(list(test_df["Standard_low_to_high_temp"]))
        max_path_length_to_model = np.max(list(test_df["path_length"]))
        max_warp_degree_with_model = np.max(list(test_df["warp_degree"]))
        max_Curve_Lengths = np.max(list(test_df["Curve_Length"]))
        max_Data_Lengths = np.max(list(test_df["Data_Length"]))
        max_Curves_by_Data = np.max(list(test_df["Curve_by_Data"]))
        
        #median cycle level features
        med_dist_to_model = np.median(list(test_df["Standard_distance"]))
        med_nadir_days = np.median(list(test_df["Standard_nadir_day"]))
        med_peak_days = np.median(list(test_df["Standard_peak_day"]))
        med_nadir_temps = np.median(list(test_df["Standard_nadir_temp_actual"]))
        med_peak_temps = np.median(list(test_df["Standard_peak_temp_actual"]))
        med_nadirs_to_peaks = np.median(list(test_df["Standard_nadir_to_peak"]))
        med_low_to_high_temps = np.median(list(test_df["Standard_low_to_high_temp"]))
        med_path_length_to_model = np.median(list(test_df["path_length"]))
        med_warp_degree_with_model = np.median(list(test_df["warp_degree"]))
        med_Curve_Lengths = np.median(list(test_df["Curve_Length"]))
        med_Data_Lengths = np.median(list(test_df["Data_Length"]))
        med_Curves_by_Data = np.median(list(test_df["Curve_by_Data"]))

        #range of cycle level features
        rge_dist_to_model = np.ptp(list(test_df["Standard_distance"]))
        rge_nadir_days = np.ptp(list(test_df["Standard_nadir_day"]))
        rge_peak_days = np.ptp(list(test_df["Standard_peak_day"]))
        rge_nadir_temps = np.ptp(list(test_df["Standard_nadir_temp_actual"]))
        rge_peak_temps = np.ptp(list(test_df["Standard_peak_temp_actual"]))
        rge_nadirs_to_peaks = np.ptp(list(test_df["Standard_nadir_to_peak"]))
        rge_low_to_high_temps = np.ptp(list(test_df["Standard_low_to_high_temp"]))
        rge_path_length_to_model = np.ptp(list(test_df["path_length"]))
        rge_warp_degree_with_model = np.ptp(list(test_df["warp_degree"]))
        rge_Curve_Lengths = np.ptp(list(test_df["Curve_Length"]))
        rge_Data_Lengths = np.ptp(list(test_df["Data_Length"]))
        rge_Curves_by_Data = np.ptp(list(test_df["Curve_by_Data"]))

        #The dependent variable

        PCOS = list(test_df["PCOS"])[0]

        user = {
        "User":i,

        "med_pair_distances":med_pair_distances, "med_pair_lengths":med_pair_lengths,
            
        "min_dist_to_model":min_dist_to_model,
        "min_nadir_days":min_nadir_days,
        "min_peak_days":min_peak_days,
        "min_nadir_temps":min_nadir_temps,
        "min_peak_temps":min_peak_temps,
        "min_nadirs_to_peaks":min_nadirs_to_peaks,
        "min_low_to_high_temps":min_low_to_high_temps,
        "min_path_length_to_model":min_path_length_to_model,
        "min_warp_degree_with_model":min_warp_degree_with_model,
        "min_Curve_Lengths":min_Curve_Lengths,
        "min_Data_Lengths":min_Data_Lengths,
        "min_Curves_by_Data":min_Curves_by_Data,
            
        "max_dist_to_model":max_dist_to_model,
        "max_nadir_days":max_nadir_days,
        "max_peak_days":max_peak_days,
        "max_nadir_temps":max_nadir_temps,
        "max_peak_temps":max_peak_temps,
        "max_nadirs_to_peaks":max_nadirs_to_peaks,
        "max_low_to_high_temps":max_low_to_high_temps,
        "max_path_length_to_model":max_path_length_to_model,
        "max_warp_degree_with_model":max_warp_degree_with_model,
        "max_Curve_Lengths":max_Curve_Lengths,
        "max_Data_Lengths":max_Data_Lengths,
        "max_Curves_by_Data":max_Curves_by_Data,

        "med_dist_to_model":med_dist_to_model,
        "med_nadir_days":med_nadir_days,
        "med_peak_days":med_peak_days,
        "med_nadir_temps":med_nadir_temps,
        "med_peak_temps":med_peak_temps,
        "med_nadirs_to_peaks":med_nadirs_to_peaks,
        "med_low_to_high_temps":med_low_to_high_temps,
        "med_path_length_to_model":med_path_length_to_model,
        "med_warp_degree_with_model":med_warp_degree_with_model,
        "med_Curve_Lengths":med_Curve_Lengths,
        "med_Data_Lengths":med_Data_Lengths,
        "med_Curves_by_Data":med_Curves_by_Data,

        "rge_dist_to_model":rge_dist_to_model,
        "rge_nadir_days":rge_nadir_days,
        "rge_peak_days":rge_peak_days,
        "rge_nadir_temps":rge_nadir_temps,
        "rge_peak_temps":rge_peak_temps,
        "rge_nadirs_to_peaks":rge_nadirs_to_peaks,
        "rge_low_to_high_temps":rge_low_to_high_temps,
        "rge_path_length_to_model":rge_path_length_to_model,
        "rge_warp_degree_with_model":rge_warp_degree_with_model,
        "rge_Curve_Lengths":rge_Curve_Lengths,
        "rge_Data_Lengths":rge_Data_Lengths,
        "rge_Curves_by_Data":rge_Curves_by_Data,
            
        "PCOS":PCOS
        }

        user_lvl_ftrs.append(user)
        
    df_user_lvl_ftrs = pd.DataFrame(user_lvl_ftrs)
    df_user_lvl_ftrs.to_csv(OUTPUT)

if __name__ == "__main__":
    args = parser.parse_args()
    the_user_level_variables(args.input_file, args.output_file)