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
from functools import reduce
import tools.tools as tools
from questionnaire_variables.get_quest_variables import Quest_data

parser = argparse.ArgumentParser(description='A script for initial data cleaning')
parser.add_argument('-i','--input_file', type=str, required=True, help='The input dataset')
parser.add_argument('-j','--input_cycles', type=str, required=True, help='The input cycles dataset')
parser.add_argument('-o','--output_file', type=str, required=True, help='The output file')
parser.add_argument('-q','--output_cleaned_quest', type=str, required=True, help='The output of the cleaned questionnaire')

def process_quest(INPUT, INPUT_CYCLES, OUTPUT, CLEANED_QUEST):
    #read an excel dataframe
    df_questionnaire = Frames(INPUT).excel_df()

    #clean up the file
    #df.rename({"Unnamed: 0":"User ID"}, inplace = True, axis = 1)
    #df = df.iloc[2:,:]
    #df.reset_index(inplace = True, drop = True)

    #drop partial duplicates
    #df["count"] = df.isnull().sum(1)
    #df_new = df.sort_values("count").drop_duplicates(subset = ["User ID"], keep='first').drop(columns = 'count')
    
    #clean up the file  
    df_cleaned_questionnaire = tools.clean_quest(df_questionnaire)

    #rename the PCOS column
    df_cleaned_questionnaire.rename({"What diagnoses were made? (tick all that apply)":"PCOS"}, axis = 1, inplace=True)

    #recode the PCOS column, gives a df of coded PCOS (0-negative, 1-positive) rows from the questionnaire
    the_quest_df = Frames(df_cleaned_questionnaire).recode_pcos()

    #processing the BMI variables
    df_bmi = Quest_data(the_quest_df).get_bmi()

    #processing the smoking variables    
    df_smoking = Quest_data(the_quest_df).get_smoking_variables()

    #processing the sleep and daily activity variables
    df_sleep_and_daily_activity = Quest_data(the_quest_df).get_sleep_and_daily_activity()

    #processing the ailments variables - I must use the PCOS values from here
    df_ailments = Quest_data(the_quest_df).get_ailments()

    #processing the pregnancy related variables
    df_pregnancy = Quest_data(the_quest_df).get_pregnants()

    #processing the menstrual period related variables
    df_menstrual = Quest_data(the_quest_df).get_menstruals()

    data_frames = [
        df_bmi[["User ID", "BMI"]], 
        df_smoking[["User ID", "Regular Smoker"]],
        df_sleep_and_daily_activity[["User ID", "Sleep Hours", "Night Sleep Troubles", "Unintentional Day Sleep", "When Active"]],
        df_ailments[["User ID", "Endocrine_Problems", "Autoimmune_Problems", "Cardiometabolic_Problems"]],
        df_pregnancy[["User ID", "Currently Pregnant", "Time before current preg", "Previous Pregancies", 
                        "Time before one preg", "Live birth", "Baby weight (Kg)"]],
        df_menstrual[["User ID", "Age menstration started", "Period in last 3 months",  "Acceptable?",
                        "Regular periods", "Heavy periods", "Painful periods"]],
        df_ailments[["User ID", "PCOS"]]
                        ]

    df_questionnaire_final = reduce(lambda left, right: pd.merge(left, right, on = "User ID", how = "outer"), data_frames)

    df_questionnaire_final.to_csv(CLEANED_QUEST, index=False)
    
    #get the cycles processed from process cycles
    cycles = Frames(INPUT_CYCLES).the_cycles_temp_dates_duration()

    #Select the relevant columns #I had to use df_ailments because the PCOS column here have included those
    #who indicated the disease in the right PCOS column
    df_new = df_ailments[["User ID", "PCOS"]]

    #merge the questionnaire (df_ailments) with the cycle 
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
    process_quest(args.input_file, args.input_cycles, args.output_file, args.output_cleaned_quest)
