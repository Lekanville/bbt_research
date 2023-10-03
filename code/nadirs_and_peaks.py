#! usr/bin/env python3
#############################################################################################
#The “nadirs_and_peaks.py” script
#This scripts (along with the helper scripts) gets the nadirs and peaks of the individual cycles
#by comparing the cycles with the model cycle. Firstly, the temperature data is read in followed
#by the cycle data. Both data frames are grouped by the user and cycle IDs and the user list is
#obtained. 
#The actual days (with interpolation for missing days), the nadirs and peaks (and related data)
#and the cycle lengths (and related data) are then comupted
#############################################################################################

import numpy as np
import pandas as pd
from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns
from dtaidistance import dtw_visualisation as dtwvis
import random
import argparse
from multiprocess import Pool
from tqdm import tqdm

from classes.classes import Frames
import tools.data_extractor_ss as extract
import tools.tools as tools

parser = argparse.ArgumentParser(description='A script for getting nairs and peaks using DTW')
parser.add_argument('-i','--input_temps', type=str, required=True, help='The input temperatures dataset')
parser.add_argument('-j','--input_cycles', type=str, required=True, help='The input cycles dataset')
parser.add_argument('-m','--model_cycle', type=str, required=True, help='The location of the model cycle')
parser.add_argument('-o','--output_file', type=str, required=True, help='The output file')

def users_cycles_and_temps(INPUT_TEMPS, INPUT_CYCLES, MODEL_CYCLE):
    #read the temperatures dataset (from sel_crt_2)
    logger.info("loading the temperatures dataset")
    temp_sort = Frames(INPUT_TEMPS).read_temp() #read the temperatures
    temp_sort["Mean_Temp"] = temp_sort["Mean_Temp"].apply(lambda x: int(x)) #convert data to integer type
    temp_final = temp_sort[(temp_sort["Mean_Temp"] > 35000) & (temp_sort["Mean_Temp"] < 40000)] #ensures that true values are selected
    logger.info("temperatures dataset loaded")

    #read the cycles and questionnaire  dataset (from process_quest)
    logger.info("loading the cycles dataset")    
    cycles = Frames(INPUT_CYCLES).read_cycles_and_pcos()
    logger.info("cycles dataset loaded")

    #Group the temperatures by the user IDs and cycle IDs
    logger.info("grouping the temperatures dataset by User and Cycle IDs")   
    group_temp = temp_final.groupby(["User ID", "Cycle ID"])
    logger.info("temperatures dataset grouped by User and Cycle IDs")   

    #Group the cycles by user IDs and cycle IDs
    logger.info("grouping the cycles dataset by User and Cycle IDs")   
    grouped = cycles.groupby(["User ID_y","Cycle ID"]).first()
    logger.info("cycles dataset grouped by User and Cycle IDs")   

    #Get all the users
    logger.info("getting all users")      
    users = tools.get_users(grouped)
    logger.info("all users ready")  
    
    #location of the model cycle
    model_cycle = MODEL_CYCLE

    return (users, grouped, group_temp, model_cycle)

def independent_variables(user):
    user_cycles = grouped.xs(user, level = 0).sort_values("Date_x")#get all users cycles and sort them by date
    user_cycles_list = list(user_cycles.index) #wrap the cycles into a list

    results = []

    for cycle in user_cycles_list: #for each cycle

        ################Actual Cycle Days##################
        actual_temp_vals = extract.actual_day(group_temp, user, cycle)
        days = {"Days":list(actual_temp_vals.index)}

        ##
        if len(days["Days"]) > 9: #This has to be done because removing missing days will reduce some cycle lengths
            missing_days = list(actual_temp_vals[actual_temp_vals["Missing_Day"] == True]["Mean_Temp"].index)
            missing_days_temps = list(actual_temp_vals[actual_temp_vals["Missing_Day"] == True]["Mean_Temp"])

            missing = {"Missing_Days":missing_days, "Missing_Days_Temp":missing_days_temps}

            ################Nadir and Peak####################
            nad_and_peak = extract.slope_nadir_peak(user, user_cycles, cycle, actual_temp_vals, model_cycle)

            ################Length of the Curve###############
            curve_distance = extract.curve_by_length(nad_and_peak)

            cycle_est = dict(nad_and_peak, **curve_distance, **days, **missing)
            #cycle_est = dict(nad_and_peak, **days, **missing)

            results.append(cycle_est)
            #print(days)
    return results

    #return(independent_variables('1NnOjBOgQQ'))
def compute_features(users):
    max_pool = 50
    with Pool(max_pool) as p:
        pool_outputs = list(tqdm(p.imap(independent_variables, users), total=len(users)))
    return pool_outputs

def save_data(extracted, OUTPUT):
    data = [i for ls in extracted for i in ls]
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT)

if __name__ == "__main__":
    args = parser.parse_args() #get the args variables
    users, grouped, group_temp, model_cycle = users_cycles_and_temps(args.input_temps, args.input_cycles, args.model_cycle) #get the users, cycles and temperatures
    
    logger.info("computing the cycle level data")  
    extracted = compute_features(users=users) #get the cycle level data
    logger.info("cycle level data computed")  

    logger.info("saving the cycle level data")  
    save_data(extracted, args.output_file) #save the data
    logger.info("process complete")  







