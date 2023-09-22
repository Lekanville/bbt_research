#!python
#!/usr/bin/env python3

#############################################################################################
#The “sel_cr_1.py” script
#The script expects the output file from the previous rule (merge_decrypted.py) as its input and will output the 
#specified selected data as a CSV. The script removes invalid data (NaN, 0.0 and 34500) from 
#the daily temperature records array. Afterwards, it computes the lengths of the data array 
#(the number of recordings in the data array) and selects only records that have more than 
#the specified minimum (defined in the variables file and imported into the snakefile). It 
#then selects the temperatures recorded from a specified point (defined in the variables 
#file and imported into the snakefile, it ensures device stabilization in taking measurements)
#and computes the average of the data values.
# Finally, the result is outputted as the specified file
#############################################################################################

import numpy as np
import pandas as pd
import argparse
import os

pd.options.mode.chained_assignment = None 

parser = argparse.ArgumentParser(description='A script to filters data')
parser.add_argument('-i','--input_data', type=str, required=True, help='The input dataset')
parser.add_argument('-o','--output_file', type=str, required=True, help='The output dataset')
parser.add_argument('-x','--min_data', type=int, required=True, help='Minimum number of true data')
parser.add_argument('-y','--init_data', type=int, required=True, help='Number of initial data to take out')

def remove_nan(temp):
#Removal of NaN, 34500.0 and 0.0
    j = []
    for i in temp:
        floated = float(i)
        if (str(floated) != "nan") & (str(floated) != "34500.0") & (str(floated) != "0.0"):
            j.append(floated)
    return j

def compute_mean(INPUT, OUTPUT, x, y):
    """
    This ensures each record have a minimum number of data (x), removes a specified
    number of initial data (y) and computes the average of the values
    """
    data = pd.read_csv(INPUT, index_col="prime")
    data["Data"] = data["Data"].apply(lambda x: x.replace('[', "").replace(']', "").replace("'", "").split(', '))
    
    data["Data_2"] = data["Data"].apply(remove_nan)

    
    #4a.Getting the length of each data field
    data["Data_len"] = data["Data_2"].apply(lambda x: len(x))
        
    #4a. Getting rows with more than x data
    data_new = data[data['Data_len'] >= x]
    #df_new.drop("Data_len", axis = 1, inplace = True)
    
    #4b. removing y initial data
    data_new['Data_to_Compute'] = data_new["Data_2"].apply(lambda j: j[y:])
    
     #4c. getting the average data values
    data_new["Mean_Temp"] = data_new['Data_to_Compute'].apply(lambda x: np.array(x).mean().round(0).astype(int))
    data_new.drop("Data_to_Compute", axis = 1, inplace = True)
    #data_new.to_csv("data/sel_crt_2.csv")
    data_new.to_csv(OUTPUT)
    
if __name__ == "__main__":
    args = parser.parse_args()
    compute_mean(args.input_data, args.output_file, args.min_data, args.init_data)