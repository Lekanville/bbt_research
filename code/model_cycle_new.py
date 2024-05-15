#!python
#!/usr/bin/env python3

#############################################################################################
#The “sel_cr_1.py” script
#This script computes the model cycle
#############################################################################################

import numpy as np
import pandas as pd
import argparse
import os

from classes.classes import Frames
import normal_cycles_process.temp_and_day as process_temps
import tools.tools as tools

parser = argparse.ArgumentParser(description='A script to filters data')
parser.add_argument('-i','--input_questionnaire', type=str, required=True, help='The input questionnaire dataset')
parser.add_argument('-j','--input_temp_dates_duration', type=str, required=True, help='The input temps and duration dataset')
parser.add_argument('-k','--input_temps', type=str, required=True, help='The input daily temps dataset')
parser.add_argument('-o','--output_file', type=str, required=True, help='The output model cycle')

def get_model(QUEST, TEMPS_DUR, TEMPS, OUTPUT):
    #Read the Data
    def read_data(QUEST, TEMPS_DUR, TEMPS):
        quest_data = Frames(QUEST).excel_df_model()
        temps_dur_df = Frames(TEMPS_DUR).the_cycles_temp_dates_duration()
        temp_df = Frames(TEMPS).read_temp()

        return (quest_data, temps_dur_df, temp_df)


    OUTPUT_FOLDER = OUTPUT.split("/")
    OUTPUT_FOLDER = "/".join(OUTPUT_FOLDER[0:-1]) #create folder for the other preliminary outputs

    quest_data, temps_dur_df, temp_df = read_data(QUEST, TEMPS_DUR, TEMPS) #reading all dataframes
    selected_models_users = process_temps.select_models_questionnaire(quest_data, temp_df) #the users in which the models cycles were taken from
    model_temps, model_lenghts = process_temps.model_temps(selected_models_users, temp_df) #the model cycles with interpolated temperatures for missing days
    model_cycles = process_temps.filtering(temps_dur_df, model_lenghts) #the final model cycles
    all_model_temps, all_model_padded = process_temps.intepolate_offsets(model_temps, temps_dur_df, model_cycles,  OUTPUT_FOLDER) #Temperature data of the model cycles
    #averaged_ref = process_temps.ref_DBA_averaging(all_model_temps,  OUTPUT_FOLDER)
    averaged_ref = process_temps.ref_DBA_averaging(all_model_padded,  OUTPUT_FOLDER)

    
    #final_out_file = os.path.join(OUTPUT, "model_cycle.json")
    tools.save_model_cycle(averaged_ref, OUTPUT)
    

if __name__ == "__main__":
    args = parser.parse_args()
    #quest_data, temps_dur_df, temp_df = read_data(args.input_questionnaire, args.input_temp_dates_duration, args.input_temps, args.output_file)
    get_model(args.input_questionnaire, args.input_temp_dates_duration, args.input_temps, args.output_file)