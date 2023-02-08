#!python
#!/usr/bin/env python3

import numpy as np
import pandas as pd
import argparse
import os

pd.options.mode.chained_assignment = None 

OUT_FILE = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/"
parser = argparse.ArgumentParser(description='A script to filters data')
parser.add_argument('-d','--data', type=str, required=True, help='The Dataset')
parser.add_argument('-x','--min_data', type=int, required=True, help='Minimun number of true data')
parser.add_argument('-y','--init_data', type=int, required=True, help='Number of initial data to take out')

def remove_nan(temp):
#Removal of NaN, 34500.0 and 0.0
    j = []
    for i in temp:
        floated = float(i)
        if (str(floated) != "nan") & (str(floated) != "34500.0") & (str(floated) != "0.0"):
            j.append(floated)
    return j

def compute_mean(clean, x, y):
    """
    This ensures each record have a minimum number of data (x), removes a specified
    number of initial data (y) and computes the average of the values
    """
    data = pd.read_csv(clean, index_col="prime")
    data["Data"] = data["Data"].apply(lambda x: x.replace('[', "").replace(']', "").replace("'", "").split(', '))
    
    data["Data_2"] = data["Data"].apply(remove_nan)

    
    #4a.Getting the lenght of each data field
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
    data_new.to_csv(os.path.join(OUT_FILE,"sel_crt_1.csv"))
if __name__ == "__main__":
    args = parser.parse_args()
    compute_mean(args.data, args.min_data, args.init_data)