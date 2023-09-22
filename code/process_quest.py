#! usr/bin/env python3

#############################################################################################
#The “process_quest.py” script
#The script expects the output file from the previous rule (process_cycles.py) and the 
# questionnaire file (OvuSense_Cycle_Characteristics_Study-Survey-to_18NOV22_anon.xlsx) 
#as input and will output the specified selected data as a CSV. 
#The questionnaire data is read in and cleaned, partial duplicates are removed and the PCOS 
#values are re-coded. The cycles from the previous rule (cycles_temp_dates_duration) is also 
# read in.
# The 2 files are merged together and completed by coding users without PCOS 
# values as 2 (those without questionnaire data). This is then outputted as specified
# The essence of this part is to get a PCOS label for all cycles in the processed cycle data
#############################################################################################

import numpy as np
import pandas as pd
from classes.classes import Frames
import argparse

parser = argparse.ArgumentParser(description='A script for initial data cleaning')
parser.add_argument('-i','--input_file', type=str, required=True, help='The input dataset')
parser.add_argument('-j','--input_cycles', type=str, required=True, help='The input cycles dataset')
parser.add_argument('-o','--output_file', type=str, required=True, help='The output file')

def process_quest(INPUT, INPUT_CYCLES, OUTPUT):
    #read an excel dataframe
    df = Frames(INPUT).excel_df()

    #clean up the file
    df.rename({"Unnamed: 0":"User ID"}, inplace = True, axis = 1)
    df = df.iloc[2:,:]
    df.reset_index(inplace = True, drop = True)

    #drop partial duplicates
    df["count"] = df.isnull().sum(1)
    df_new = df.sort_values("count").drop_duplicates(subset = ["User ID"], keep='first').drop(columns = 'count')

    #rename the PCOS column
    df_new.rename({"What diagnoses were made? (tick all that apply)":"PCOS"}, axis = 1, inplace=True)

    #Select the relevant columns
    df_new = df_new[["User ID", "PCOS"]]

    #recode the PCOS column, gives a df of coded PCOS (0-negative, 1-positive) rows from the questinnaire
    the_df = Frames(df_new).recode_pcos()

    #get the cycles processed from process cycles
    cycles = Frames(INPUT_CYCLES).the_cycles_temp_dates_duration()

    #merge the questionnaire with the cycle 
    temp_dates_duration_pcos = pd.merge(
        cycles, df_new, left_on="User ID_y", right_on="User ID", how = "left"
        ).drop(
            "User ID", axis = 1
        )

    for i in range(len(temp_dates_duration_pcos)):
        if pd.isnull(temp_dates_duration_pcos['PCOS'][i]):
            temp_dates_duration_pcos.loc[i,'PCOS'] = 2
    
    temp_dates_duration_pcos.to_csv(OUTPUT)


if __name__ == "__main__":
    args = parser.parse_args()
    process_quest(args.input_file, args.input_cycles, args.output_file)
