#! usr/bin/env python3

#############################################################################################
#The “quest_variables.py” script
#The script takes the questionnaire file (OvuSense_Cycle_Characteristics_Study-Survey-to_18NOV22_anon.xlsx) 
#as input and will output the selected questionnaire variables into the specified selected data as a CSV. 
#The user level data is also read in to obtain the recoded PCOS values.
#############################################################################################

import numpy as np
import pandas as pd
from classes.classes import Frames
import argparse
import tools.tools as tools
from questionnaire_variables.process_quest import Quest_data

parser = argparse.ArgumentParser(description='A script for initial data cleaning')
parser.add_argument('-i','--input_file', type=str, required=True, help='The input dataset')
parser.add_argument('-j','--input_user_level', type=str, required=True, help='The input cycles dataset')
parser.add_argument('-o','--output_file', type=str, required=True, help='The output file')

def process_quest(INPUT, INPUT_USERS, OUTPUT):
    #read an excel dataframe
    df = Frames(INPUT).excel_df()

    #get the user level data
    user_data = Frames(INPUT_USERS).read_user_level_data()

    #clean up the file  
    df_cleaned = tools.clean_quest(df)

    #merge the user level data and the unit values
    df_values_and_pcos = pd.merge(
        df_cleaned, user_data, left_on="User ID", right_on="User", how="inner"
        ).drop(columns = "User")

    #getting the BMI
    df_bmi = Quest_data(df_values_and_pcos).get_bmi()

    #getting the Smoking variable    
    df_smoking = Quest_data(df_values_and_pcos).get_smoking_variables()

if __name__ == "__main__":
    args = parser.parse_args()
    process_quest(args.input_file, args.input_user_level, args.output_file)