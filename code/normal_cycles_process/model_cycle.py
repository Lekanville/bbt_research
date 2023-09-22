#!python
#!/usr/bin/env python3

#############################################################################################
#The “model_cycle.py” script
#The script expects the output file from the previous rule 5 (sel_cr_2.py) as input and will 
# output the and will output the averaged "normal" temperatures (using DBA). 
#The first aspect of the scripsobtains read the temeprature data and group them by the users
#and cycles. The temperature reading for each normal cycle is then extracted and stored in a
#list.  The average of this is then calculaed using DBA and saved in the data folder as
#model.json
#############################################################################################

import numpy as np
from scipy.signal import savgol_filter
from multiprocess import Pool
from tqdm import tqdm
import argparse

import normal_cycles_process.DBA as DBA
from normal_cycles_process.normal_cycles import normal
import normal_cycles_process.temp_and_day as temp_and_day

parser = argparse.ArgumentParser(description='A script for averaging the normal cycles')
parser.add_argument('-i','--input_temp', type=str, required=True, help='The input temperature dataset')

def get_normal(normal, temps):
    normal_smooths = []
    group_temp = temp_and_day.get_temps(temps)

    for i in normal:
        user = i[0]
        cycle = i[1]
        
        cycle_df = temp_and_day.actual_day(user, cycle, group_temp)
        cleaned_normal = (cycle_df["Mean_Temp"]).values
        smooth_normal  = savgol_filter(cleaned_normal, 10, 2)
        normal_smooths.append(smooth_normal)
    return normal_smooths

def main(normal_smooths):
    individual_series = [np.array(i) for i in normal_smooths]
    series = np.array(individual_series, dtype="object")
    
    #calculating average series with DBA
    average_series = DBA.performDBA(series)
    
    computed_avg_smoothed = savgol_filter(average_series, 10, 2)
    
    model_cycle = {"model":list(computed_avg_smoothed)}
    
    DBA.save_model_cycle(model_cycle)

    print (model_cycle)

if __name__ == "__main__":
    args = parser.parse_args()
    normal_smooths = get_normal(normal, args.input_temp)
    main(normal_smooths)