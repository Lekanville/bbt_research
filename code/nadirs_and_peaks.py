#! usr/bin/env python3
#############################################################################################
#The “nadirs_and_peaks.py” script
#This scripts (along with the helper scripts) gets the nadirs and peaks of the individual cycles
#by comparing the cycles with the model cycle. Firstly, the temperature data is read in followed
#by the cycle data. Both data frames are grouped by the user and cycle IDs and the user list is
#obtained. The data is then inputted as arguments into the extract class.
#############################################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from fastdtw import fastdtw
import seaborn as sns
from dtaidistance import dtw_visualisation as dtwvis
import random
import argparse

from classes.classes import Frames
from tools.data_extractor_ss import Extract
import tools.tools as tools


parser = argparse.ArgumentParser(description='A script for getting nairs and peaks using DTW')
parser.add_argument('-i','--input_temps', type=str, required=True, help='The input temperatures dataset')
parser.add_argument('-j','--input_cycles', type=str, required=True, help='The input cycles dataset')
parser.add_argument('-o','--output_file', type=str, required=True, help='The output file')

def nadir_peaks_ss(INPUT_TEMPS, INPUT_CYCLES, OUTPUT):

    #read the temperatures dataset (from sel_crt_2)
    temp_sort = Frames(INPUT_TEMPS).read_temp() #read the temperatures
    temp_sort["Mean_Temp"] = temp_sort["Mean_Temp"].apply(lambda x: int(x)) #convert data to integer type
    temp_final = temp_sort[(temp_sort["Mean_Temp"] > 35000) & (temp_sort["Mean_Temp"] < 40000)] #ensures that true values are selected

    #read the cycles and questionnaire  dataset (from process_quest)
    cycles = Frames(INPUT_CYCLES).read_cycles_and_pcos()

    #Group the temperatures by the user IDs and cycle IDs
    group_temp = temp_final.groupby(["User ID", "Cycle ID"])

    #Group the cycles by user IDs and cycle IDs
    grouped = cycles.groupby(["User ID_y","Cycle ID"]).first()

    #Get all the users
    users = tools.get_users(grouped)

    #Get users with cycles between 3 and 10
    #users_10_cycles = tools.users_btw_3_and_10(cycles) #now get the the users
    extracted = Extract(users=users, group_temp=group_temp, grouped=grouped).compute_mv()

    print (extracted)

if __name__ == "__main__":
    args = parser.parse_args()
    nadir_peaks_ss(args.input_temps, args.input_cycles, args.output_file)






