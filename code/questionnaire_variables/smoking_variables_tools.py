import numpy as np
import pandas as pd

def select_variables(df):
    df_selected = df.copy()
    df_process = df_selected.iloc[:, np.r_[0, 90:94, -1]]
    x = {"Have you ever been a regular smoker":"Regular Smoker: Yes", "Unnamed: 91":"Regular Smoker: No",
         "Unnamed: 92":"Regular Smoker: Prefer not to answer"}
    df_renamed = df_process.rename(columns = x)
    
    return df_renamed

def clean_smoking_age(df):
    df_to_clean = df.copy()
    
    for i in range(len(df_to_clean)):
        
        #Decision 1 - cleaning out wrong values in the "yes" column ("2-6 hours per week" - 4 and
        #("Less than one hour per week" - 2)
        if (df_to_clean.loc[i, "Regular Smoker: Yes"] != "Yes")& \
            (df_to_clean.loc[i, "Regular Smoker: Yes"] != np.NaN)& \
            (df_to_clean.loc[i, "Regular Smoker: Prefer not to answer"] == "Never"):
            
            df_to_clean.loc[i, "Regular Smoker: Yes"] = np.NaN
            df_to_clean.loc[i, "Regular Smoker: No"] = "No"
            df_to_clean.loc[i, "Regular Smoker: Prefer not to answer"] = np.NaN
            df_to_clean.loc[i, "At what age did you start smoking regularly?"] = np.NaN
        
        #Decision 2 - Take NaN in the 3 columns as prefer not to answer
        if pd.isnull(df_to_clean.loc[i, "Regular Smoker: Yes"])& \
            pd.isnull(df_to_clean.loc[i, "Regular Smoker: No"])& \
            pd.isnull(df_to_clean.loc[i, "Regular Smoker: Prefer not to answer"]):
            
            df_to_clean.loc[i, "Regular Smoker: Prefer not to answer"] = "Prefer not to answer"        

    return df_to_clean 

#Combine the smoking column
def combine_smoking_column(df):
        df_combined = df.copy()
        df_combined["Regular Smoker"] = ""
        
        for i in range(len(df)):
            #Combine all
            if df_combined.loc[i, "Regular Smoker: Yes"] == "Yes":
                df_combined.loc[i, "Regular Smoker"] = "Yes"
            elif df_combined.loc[i, "Regular Smoker: No"] == "No":
                df_combined.loc[i, "Regular Smoker"] = "No"
            else:
                df_combined.loc[i, "Regular Smoker"] = "Prefer not to answer"
                
        return df_combined[["PCOS", "Regular Smoker"]]