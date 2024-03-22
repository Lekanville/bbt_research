#! usr/bin/env python3

#############################################################################################
#The “quest_preprocess.py” script
#The script takes the cleaned questionnaire file (/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/df_questionnaire_final.csv) 
#as input and will output a preprocessed set of variables as a CSV. 
#############################################################################################

import numpy as np
import pandas as pd

import argparse
import questionnaire_variables.preprocess_quest_tools as preprocess

parser = argparse.ArgumentParser(description='A script for preprocessing the questionnaire variables')
parser.add_argument('-i','--input_file', type=str, required=True, help='The input dataset')
parser.add_argument('-o','--output_file', type=str, required=True, help='The output file')

def preprocess_cleaned(INPUT, OUTPUT):
    #df_quest = pd.read_csv("/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/df_questionnaire_final.csv")
    df_quest = pd.read_csv(INPUT)

    #getting and defining row and columns missingness levels
    df_missing = preprocess.get_missing(df_quest)

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
    preprocess_cleaned(args.input_file, args.output_file)