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
from loguru import logger

from classes.classes import Frames
import tools.tools as tools
import questionnaire_variables.preprocess_quest_tools as preprocess

parser = argparse.ArgumentParser(description= "A script to filter data")
parser.add_argument('-i', '--input_temps', type=str, required=True, help= 'The input temperatures dataset')
parser.add_argument('-j','--input_quest', type=str, required=True, help='The input questionnaire data')
parser.add_argument('-k','--model_cycle', type=str, required=True, help='The model cycle')
parser.add_argument('-o', '--output_temps', type=str, required=True, help= 'The output temperatures dataset')
parser.add_argument('-p', '--output_quest', type=str, required=True, help= 'The output questionnaire dataset')

def the_variables(INPUT_TEMPS, INPUT_QUEST, MODEL_CYCLE, OUTPUT_TEMPS, OUTPUT_QUEST):
    temperatures = pd.read_csv(INPUT_TEMPS) #read the data
    #temperatures_trimmed_out = tools.trimming_for_outliers(temperatures) #trim out outliers at the nadirs and peaks
    #temperatures_pcos = temperatures_trimmed_out[temperatures_trimmed_out["PCOS"] != 2] #select users with known PCOS values

    quest = pd.read_csv(INPUT_QUEST)

    logger.info("================User Selection Started==================")

    #1. Users with known PCOS values and temperature data
    temperatures_pcos = temperatures[temperatures["PCOS"] != 2] 
    counts = temperatures_pcos["User"].nunique()
    logger.info(f"Total Users with Questionnaire and Temperature Data: {counts}")
    

    #2. Users in model cycle
    model_users = Frames(MODEL_CYCLE).model_users()
    non_model = temperatures_pcos[~(temperatures_pcos["User"].isin(model_users))]
    counts = non_model["User"].nunique()
    logger.info(f"Non-model Users: {counts}")
    
    #3. Users with more than 3 Cycles
    more_than_3 = non_model.groupby("User").count()[non_model.groupby("User").count()["Cycle"] > 2]
    more_than_3_list = more_than_3.index.to_list()
    more_than_3_df = non_model[non_model["User"].isin(more_than_3_list)]
    counts = more_than_3_df["User"].nunique()
    logger.info(f"Users with 3 and more cycles: {counts}")
    counts = more_than_3_df["PCOS"].value_counts()
    logger.info(f"Cycles Distribution: {counts}")

    # dep_and_indep = final_df[[
    # "User", "Cycle", "Standard_smooth_temps", "Standard_distance", "Standard_nadir_day", "Standard_peak_day", 
    # "Standard_nadir_temp_actual", "Standard_peak_temp_actual", "Standard_nadir_to_peak", "Standard_low_to_high_temp", 
    # "nadir_valid", "peak_valid", "path_length", "warp_degree", "Curve_Length", "Data_Length", "Curve_by_Data", "PCOS"    
    # ]]

    #4. Questionnaire Missingness (first get users with more thna 3 cycles from temps, then get users with less than 3 missing questionnaire varibles 
    # from "BMI", "Regular Smoker", "Age menstration started", "Period in last 3 months", "Regular periods", "Heavy periods", "Painful periods) and preprocessing

    df_quest = quest[quest["User ID"].isin(more_than_3_list)][["User ID", "BMI", "Regular Smoker", "Age menstration started", "Period in last 3 months", "Regular periods", \
                                                       "Heavy periods", "Painful periods", "PCOS"]].reset_index(drop = True)
    #missingness in the questionnaire variables
    df_missingness = preprocess.get_missing(df_quest)
    
    #preprocessing and defining categories
    df_preprocessed = preprocess.pre_processing_redone(df_missingness)

    #Get dummy variables
    dummies = pd.get_dummies(df_preprocessed[["Regular Smoker", "Period in last 3 months", "Regular periods", "Heavy periods", "Painful periods"]], drop_first=True)
    df_init = df_preprocessed[["User ID", "BMI", "Age menstration started", "PCOS"]]
    final_quest_ml = pd.concat([df_init, dummies], axis = 1)
    final_quest_ml.rename({"User ID":"User"}, axis =1, inplace=True)
    counts = quest["User"].nunique()
    logger.info(f"Final users in questionnaire data: {counts}")

    #list cleaned from questionnaire
    quest_list = final_quest_ml["User"].to_list()

    # Obtain the questionnare list from the temperature df
    final_temp_df = more_than_3_df[more_than_3_df["User"].isin(quest_list)]
    counts = final_temp_df["User"].nunique()
    logger.info(f"Final users in temperatures data: {counts}")
    counts = final_temp_df["PCOS"].value_counts()
    logger.info(f"Final Cycles Distribution: {counts}")

    dep_and_indep = final_temp_df[[
    "Data_Length", "Next Cycle Difference", "Cycle Completeness", "max_of_2_periods", "max_pos_of_2_periods", 
    "max_of_3_periods", "max_pos_of_3_periods", "Change Point Day", "Change Point Mean Diff", "Standard_distance",
    "path_length_with_diff", "Standard_nadir_day", "Standard_peak_temp", "Standard_nadir_temp_actual",
    "Standard_peak_temp_actual", "Standard_nadir_to_peak", "Standard_low_to_high_temp", "cost_with_diff", "PCOS"
    ]] #select the independent and non-indepent variables

    #Maintain the "Minimum of 3 Cycles per User" rule
    # less_3 = list(dep_and_indep.groupby("User").count()[dep_and_indep.groupby("User").count()["Cycle"] < 3].index)
    # df_variables =  dep_and_indep[~(dep_and_indep["User"].isin(less_3))]

    #sample 3 cycles each from all users
    #df_3_cycles = tools.select_3_cycles(df_variables)

    df_3_cycles = tools.select_3_cycles(dep_and_indep)

    #save the final result
    df_3_cycles.to_csv(OUTPUT_TEMPS, index=False)
    final_quest_mlto_csv(OUTPUT_QUEST, index=False)

if __name__ == "__main__":
    args = parser.parse_args()
    the_variables(args.input_temps, args.input_quest, args.model_cycle, args.output_file, args.output_quest)