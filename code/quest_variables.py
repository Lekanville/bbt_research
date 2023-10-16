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

parser = argparse.ArgumentParser(description='A script for initial data cleaning')
parser.add_argument('-i','--input_file', type=str, required=True, help='The input dataset')
parser.add_argument('-j','--input_user_level', type=str, required=True, help='The input cycles dataset')
parser.add_argument('-o','--output_file', type=str, required=True, help='The output file')

def process_quest(INPUT, INPUT_CYCLES, OUTPUT):
    #read an excel dataframe
    df = Frames(INPUT).excel_df()

    #clean up the file  
    df_cleaned = tools.clean_quest(df)

    #selecting the relevant data
    df_process = df_cleaned.iloc[:, np.r_[0, 61:90]]

    #edit wrong entries
    df_process = tools.edit_wrong_inputs(df_process)

    #Geting the units of the values for each user
    df_units = tools.get_units(df_process)

    #getting the actual meaurement values for each user 
    df_values = tools.get_values(df_units)

    #sort by the user ID and reset the index
    df_units_values = df_values.sort_values("User ID").reset_index().drop(columns = "index")

    #the final unit values
    df_values_final = df_units_values.iloc[:, np.r_[0, 30:40]]

    #get the user level data
    user_data = Frames(INPUT_CYCLES).read_user_level_data()

    #merge the user level data and the unit values
    users_and_units = pd.merge(
        df_values_final, user_data, left_on="User ID", right_on="User", how="inner"
        ).drop(columns = "User")

    #standarize the values
    df_unit_values = tools.get_standard_values(users_and_units)

    #getting the BMI
    df_bmi = tools.get_bmi(df_unit_values)

    #imputation for missing BMIs
    df_bmi_final = tools.missing_bmi_imputation(df_bmi)

    print(df_bmi_final.head(3))
    print(df_bmi_final.info())

if __name__ == "__main__":
    args = parser.parse_args()
    process_quest(args.input_file, args.input_user_level, args.output_file)