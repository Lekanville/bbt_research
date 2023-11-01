import numpy as np
import questionnaire_variables.bmi_tools as bmi_tools
import questionnaire_variables.smoking_variables_tools as smk_tools
import questionnaire_variables.sleep_and_activity_tools as slp_tools

class Quest_data():
    def __init__(self, df):
        self.df = df

    def get_bmi(self):
        df = self.df

        #selecting the relevant data
        df_process = df.iloc[:, np.r_[0, 61:90, -1]]

        #edit wrong entries
        df_process = bmi_tools.edit_wrong_inputs(df_process)

        #Geting the units of the values for each user
        df_units = bmi_tools.get_units(df_process)

        #getting the actual meaurement values for each user 
        df_values = bmi_tools.get_values(df_units)

        #sort by the user ID and reset the index
        df_units_values = df_values.sort_values("User ID").reset_index().drop(columns = "index")

        #the final unit values
        df_values_final = df_units_values.iloc[:, np.r_[0, 30:41]]

        #standarize the values
        df_unit_values = bmi_tools.get_standard_values(df_values_final)

        #getting the BMI
        df_bmi_with_missing_data = bmi_tools.get_bmi(df_unit_values)

        #imputation for missing BMIs
        df_bmi_final = bmi_tools.missing_bmi_imputation(df_bmi_with_missing_data)

        return df_bmi_final

    def get_smoking_variables(self):
        df = self.df

        #selecting the relevant data and renaming the columnns
        df_process = smk_tools.select_variables(df)

        #cleaning the smoking data
        df_cleaned = smk_tools.clean_smoking_age(df_process)
        
        #Combine the smoking column
        df_combined = smk_tools.combine_smoking_column(df_cleaned)

        return df_combined

    def get_sleep_and_daily_activity(self):
        df = self.df

        #selecting the relevant data and renaming the columnns
        df_process = slp_tools.select_variables(df)

        #Combine the sleeping 
        df_combined_1 = slp_tools.combining_sleep(df_process)

        #Combine the unintentional day sleep columns
        df_combined_2 = slp_tools.combining_unintentional_day_sleep(df_combined_1)

        #Convert hours to numeric
        df_combined_3 = slp_tools.combining_active_time_of_day(df_combined_2)

        #Imputaton for missing data and converting hours to numeric
        df_converted = slp_tools.convert_hours(df_combined_3)

        print (df_converted)

        return df_converted