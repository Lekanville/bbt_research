import numpy as np
import pandas as pd

#Selecting the relevant data and renaming the columnns
def select_variables(df):
    df_selected = df.copy()
    columns = np.r_[0, 271:274, 275:280, 297:311, 596:604, 606:609, 678]
    df_process = df_selected.iloc[:, columns]
    
    x = {
        "Are you currently pregnant?":"Currently Pregnant (Yes)",
        "Unnamed: 272":"Currently Pregnant (No)",
        "Unnamed: 273":"Currently Pregnant (Prefer not to answer)",
        "How long were you trying before you got pregnant?":"Time before current preg (<6M)",
        "Unnamed: 276":"Time before current preg (6-11M)",
        "Unnamed: 277":"Time before current preg (>12M)",
        "Unnamed: 278":"Time before current preg (Unplanned Preg)",
        "Unnamed: 279":"Time before current preg (Dont Remember)",
    }
    
    df_renamed = df_process.rename(columns = x)
    df_sorted = df_renamed.sort_values("User ID").reset_index().drop(columns = "index")
    return df_sorted

#Combine the diabetes and HBD columns
def combining_currently_pregant_columns(df):
        df_combined = df.copy()
        df_combined["Currently Pregnant"] = ""
        df_combined["Time before current preg"] = ""
        
        for i in range(len(df_combined)):
            if (df_combined.loc[i, "Currently Pregnant (Yes)"] == "Yes") & \
            pd.isnull(df_combined.loc[i, "Currently Pregnant (No)"]) & \
            pd.isnull(df_combined.loc[i, "Currently Pregnant (Prefer not to answer)"]):
                df_combined.loc[i, "Currently Pregnant"] = "Yes"
                
            elif pd.isnull(df_combined.loc[i, "Currently Pregnant (Yes)"]) & \
            (df_combined.loc[i, "Currently Pregnant (No)"] == "No") & \
            pd.isnull(df_combined.loc[i, "Currently Pregnant (Prefer not to answer)"]):
                df_combined.loc[i, "Currently Pregnant"] = "No"
                
            elif pd.isnull(df_combined.loc[i, "Currently Pregnant (Yes)"]) & \
             pd.isnull(df_combined.loc[i, "Currently Pregnant (No)"]) & \
            (df_combined.loc[i, "Currently Pregnant (Prefer not to answer)"] == "Prefer not to answer"):
                df_combined.loc[i, "Currently Pregnant"] = "Prefer not to answer"
            
            else:
                df_combined.loc[i, "Currently Pregnant"] = "No response"
              
            
            if (df_combined.loc[i, "Time before current preg (<6M)"] == "Less than 6 months"):
                df_combined.loc[i, "Time before current preg"] = "Less than 6 months"
            elif (df_combined.loc[i, "Time before current preg (6-11M)"] == "6-11 months"):
                df_combined.loc[i, "Time before current preg"] = "6-11 months"
            elif (df_combined.loc[i, "Time before current preg (>12M)"] == "12 months or more"):
                df_combined.loc[i, "Time before current preg"] = "2 months or more"
            elif (df_combined.loc[i, "Time before current preg (Unplanned Preg)"] == "Pregnancy wasn't planned"):
                df_combined.loc[i, "Time before current preg"] = "Pregnancy wasn't planned"
            elif (df_combined.loc[i, "Time before current preg (Dont Remember)"] == "Don't remember"):
                df_combined.loc[i, "Time before current preg"] = "Don't remember"
            else:
                df_combined.loc[i, "Time before current preg"] = "No response"
        
        #return df_combined.iloc[:, np.r_[0, 9:12]]
        return df_combined
    
#Getting the previous pregancies
def number_of_previous_pregs(df):
    df_pregs = df.copy()
    df_pregs["Previous Pregancies"] = ""
    
    for i in range(len(df_pregs)):
        if str(df_pregs.loc[i, "How many times have you been pregnant in the past"]) != "nan":
            df_pregs.loc[i, "Previous Pregancies"] = df_pregs.loc[i, "How many times have you been pregnant in the past"]
        elif str(df_pregs.loc[i, "Unnamed: 301"]) != "nan":
            df_pregs.loc[i, "Previous Pregancies"] = df_pregs.loc[i, "Unnamed: 301"]
        elif str(df_pregs.loc[i, "Unnamed: 302"]) != "nan":
            df_pregs.loc[i, "Previous Pregancies"] = df_pregs.loc[i, "Unnamed: 302"]
        elif str(df_pregs.loc[i, "Unnamed: 303"]) != "nan":
            df_pregs.loc[i, "Previous Pregancies"] = df_pregs.loc[i, "Unnamed: 303"]
        elif str(df_pregs.loc[i, "Unnamed: 304"]) != "nan":
            df_pregs.loc[i, "Previous Pregancies"] = df_pregs.loc[i, "Unnamed: 304"]
        elif str(df_pregs.loc[i, "Unnamed: 305"]) != "nan":
            df_pregs.loc[i, "Previous Pregancies"] = df_pregs.loc[i, "Unnamed: 305"]
        elif str(df_pregs.loc[i, "Unnamed: 306"]) != "nan":
            df_pregs.loc[i, "Previous Pregancies"] = df_pregs.loc[i, "Unnamed: 306"]
        elif str(df_pregs.loc[i, "Unnamed: 307"]) != "nan":
            df_pregs.loc[i, "Previous Pregancies"] = df_pregs.loc[i, "Unnamed: 307"]
        elif str(df_pregs.loc[i, "Unnamed: 308"]) != "nan":
            df_pregs.loc[i, "Previous Pregancies"] = df_pregs.loc[i, "Unnamed: 308"]
        elif str(df_pregs.loc[i, "Unnamed: 309"]) != "nan":
            df_pregs.loc[i, "Previous Pregancies"] = df_pregs.loc[i, "Unnamed: 309"]
        elif str(df_pregs.loc[i, "Unnamed: 308"]) != "nan":
            df_pregs.loc[i, "Previous Pregancies"] = df_pregs.loc[i, "Unnamed: 308"]
        else:
            df_pregs.loc[i, "Previous Pregancies"] = "No response"
    #return df_pregs.iloc[:, np.r_[0, 23:27]]
    return df_pregs

#Getting the previous pregancies
def one_pregnancy(df):
    df_one_preg = df.copy()
    
    df_one_preg["Time before one preg"] = ""
    df_one_preg["Live birth"] = ""
    df_one_preg["Baby weight (Kg)"] = ""
    
    for i in range(len(df_one_preg)):
        #trying length
        if (df_one_preg.loc[i, "How long were you trying before you got pregnant?.10"] == "Less than 6 months"):
            df_one_preg.loc[i, "Time before one preg"] = "Less than 6 months"
        elif (df_one_preg.loc[i, "Unnamed: 597"] == "6-11 months"):
            df_one_preg.loc[i, "Time before one preg"] = "6-11 months"
        elif (df_one_preg.loc[i, "Unnamed: 598"] == "12 months or more"):
            df_one_preg.loc[i, "Time before one preg"] = "2 months or more"
        elif (df_one_preg.loc[i, "Unnamed: 599"] == "Pregnancy wasn't planned"):
            df_one_preg.loc[i, "Time before one preg"] = "Pregnancy wasn't planned"
        elif (df_one_preg.loc[i, "Unnamed: 600"] == "Don't remember"):
            df_one_preg.loc[i, "Time before one preg"] = "Don't remember"
        else:
            df_one_preg.loc[i, "Time before one preg"] = "No response"

        #live birth
        if  df_one_preg.loc[i, "Did this result in a live birth?.9"] == "Yes":
            df_one_preg.loc[i, "Live birth"] = "Yes"
        elif df_one_preg.loc[i, "Unnamed: 602"] == "No":
            df_one_preg.loc[i, "Live birth"] = "No"
        elif df_one_preg.loc[i, "Unnamed: 603"] == "Prefer not to answer":
            df_one_preg.loc[i, "Live birth"] = "Prefer not to answer"
        else:
            df_one_preg.loc[i, "Live birth"] = "No response"
            
        #birth weight
        if  (df_one_preg.loc[i, "Please let us know the units of weight for your baby.8"] == "Pounds Ounces") & \
        ~pd.isnull(df_one_preg.loc[i, "What was the birth weight of your baby.2"]):
            df_one_preg.loc[i, "Baby weight (Kg)"] = "{0:.1f}".format(df_one_preg.loc[i, "What was the birth weight of your baby.2"] * 0.453592)
        elif (df_one_preg.loc[i, "Unnamed: 607"] == "Kilograms") & \
        ~pd.isnull(df_one_preg.loc[i, "What was the birth weight of your baby.2"]):
            df_one_preg.loc[i, "Baby weight (Kg)"] = "{0:.1f}".format(df_one_preg.loc[i, "What was the birth weight of your baby.2"])
        else:
            df_one_preg.loc[i, "Baby weight (Kg)"] = "No response"
    return df_one_preg.iloc[:, np.r_[0, 34:41]]

