#!python
#!/usr/bin/env python3

#############################################################################################
#The “learning_variables.py” script
#The script expects the output file from the previous rule (cycle_level_data) as input and will 
#output the features to a CSV file. After the the input is read the outliers on the peak day 
#are trimmed upto 3 times the std after mean. Outliers on the nadir temp are equally trimmed
#upto 3 times the standard deviation before abd after the mean. Records that have their nadir
#days to be greater than 50 were also trimmed out. Records with the difference between their
#nadirs and peaks days as zero, incomplete cycles (mostly last cycles) and cycles with data
#lengths more than 101 are also taken out
#############################################################################################

import numpy as np
import pandas as pd
import os
import argparse

import tools.tools as tools

parser = argparse.ArgumentParser(description= "A script to filter data")
parser.add_argument('-i', '--input_file', type=str, required=True, help= 'The input dataset')
parser.add_argument('-o', '--output_file', type=str, required=True, help= 'The output dataset')

def the_variables(INPUT, OUTPUT):
    temperatures = pd.read_csv(INPUT) #read the data
    temperatures_trimmed_out = tools.trimming_for_outliers(temperatures) #trim out outliers at the nadirs and peaks
    temperatures_pcos = temperatures_trimmed_out[temperatures_trimmed_out["PCOS"] != 2] #select users with known PCOS values

    dep_and_indep = temperatures_pcos[[
    "User", "Cycle", "Standard_smooth_temps", "Standard_distance", "Standard_nadir_day", "Standard_peak_day", 
    "Standard_nadir_temp_actual", "Standard_peak_temp_actual", "Standard_nadir_to_peak", "Standard_low_to_high_temp", 
    "nadir_valid", "peak_valid", "path_length", "warp_degree", "Curve_Length", "Data_Length", "Curve_by_Data", "PCOS"    
    ]] #select the independent and non-indepent variables

    #Maintain the "Minimum of 3 Cycles per User" rule
    less_3 = list(dep_and_indep.groupby("User").count()[dep_and_indep.groupby("User").count()["Cycle"] < 3].index)
    df_variables =  dep_and_indep[~(dep_and_indep["User"].isin(less_3))]

    #sample 3 cycles each from all users
    df_3_cycles = tools.select_3_cycles(df_variables)
    
    #save the final result
    df_3_cycles.to_csv(OUTPUT)

if __name__ == "__main__":
    args = parser.parse_args()
    the_variables(args.input_file, args.output_file)