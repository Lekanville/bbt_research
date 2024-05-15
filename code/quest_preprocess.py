#! usr/bin/env python3

#############################################################################################
#The “quest_preprocess.py” script
#The script takes the cleaned questionnaire file (/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/df_questionnaire_final.csv) 
#as input and will output a preprocessed set of variables as a CSV. 
#############################################################################################

import numpy as np
import pandas as pd
import os

import argparse
import questionnaire_variables.preprocess_quest_tools as preprocess
import tools.tools as tools

parser = argparse.ArgumentParser(description='A script for preprocessing the questionnaire variables')
parser.add_argument('-i','--input_quest', type=str, required=True, help='The input questionnaire data')
parser.add_argument('-j','--model_cycle', type=str, required=True, help='The model cycle')
parser.add_argument('-k','--input_temps', type=str, required=True, help='The input temperatures data')
parser.add_argument('-o','--output_file', type=str, required=True, help='The output file')

def preprocess_cleaned(INPUT_QUEST, MODEL_CYCLE, INPUT_TEMPS, OUTPUT):
    #df_quest = pd.read_csv("/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/df_questionnaire_final.csv")
    
    #read the processed questionnaire
    df_quest = pd.read_csv(INPUT_QUEST)

    #get the model users  
    MODEL_LOC_SPLIT = MODEL_CYCLE.split("/")
    MODEL_LOC = "/".join(MODEL_LOC_SPLIT[0:-1])
    MODEL_CYCLES_FILE = os.path.join(MODEL_LOC,"individual_averages.json")
    MODEL_CYCLES = tools.load_model_cycle(MODEL_CYCLES_FILE)
    
    MODEL_USERS = []
    for i in range(len(MODEL_CYCLES)):
        MODEL_USERS.append(MODEL_CYCLES[i]["User"])

    #read temperature data "features_dtw_SS.csv"
    df_temps = pd.read_csv(INPUT_TEMPS)

    print(df_quest.head())
    print(MODEL_USERS)
    print(df_temps.head())

    #getting and defining row and columns missingness levels
    #df_missing = preprocess.get_missing(df_quest)
    df_missing = df_quest

    #preprocessing and defining categories
    df_preprocessed = preprocess.pre_processing(df_missing)

    dummies = pd.get_dummies(df_preprocessed[["Regular Smoker", "Night Sleep Troubles", "Unintentional Day Sleep", 
                       "When Active", "Endocrine_Problems", "Autoimmune_Problems", 
                       "Cardiometabolic_Problems", "Currently Pregnant", 
                       "Time before current preg", "Previous Pregancies", "Time before one preg",
                      "Live birth", "Baby weight (Kg)", "Age menstration started", "Period in last 3 months", 
                       "Acceptable?", "Regular periods", "Heavy periods", "Painful periods"]], drop_first=True)

    df_init = df_preprocessed[["User ID", "BMI", "Sleep Hours", "PCOS"]]

    df_ml = pd.concat([df_init, dummies], axis = 1)

    df_ml.rename({"User ID":"User"}, axis =1, inplace=True)
    



    df_ml.to_csv(OUTPUT, index=False)


if __name__ == "__main__":
    args = parser.parse_args()
    preprocess_cleaned(args.input_quest, args.model_cycle, args.input_temps, args.output_file)