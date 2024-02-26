import numpy as np
import pandas as pd
import re

#Selecting the relevant data and renaming the columnns
def select_variables(df):
    df_selected = df.copy()
    columns = np.r_[0, 628:642, 645:665, 678]
    df_process = df_selected.iloc[:, columns]
    
    return df_process

#Combining (collapsing) the menstrual columns
def combining_menstrual_columns(df):
    df_combined = df.copy()
    df_combined["Age menstration started"] = ""
    df_combined["Period in last 3 months"] = ""
    df_combined["Acceptable?"] = "" #if the reason for absence of period is due to acceptable reasons
    df_combined["Regular periods"] = ""
    #df_combined["How regular"] = ""
    #df_combined["Periods in a year"] = ""
    df_combined["Heavy periods"] = ""
    df_combined["Painful periods"] = ""

    accepted_reasons = [r".*contraceptive.*", r".*preg.*", r".*breast.*", r".*ivf.*", 
                        r".*baby.*", r".*misca.*", r".*postpartum.*", 
                        r".*bc.*", r".*stressed.*"]

    unaccepted_reasons = [r".*irregular.*", "don't know", r".*medicated.*", "pcos", r"haven't had periods.*",
                         r".*hormone.*"]

    reasons_groups = {"accepted_reasons":accepted_reasons, "unaccepted_reasons":unaccepted_reasons}

    reasons_columns = {"What is the reason you haven't had a period in the past 3 months?",
                       "Unnamed: 636",
                       "Unnamed: 637",
                       "Unnamed: 638",
                       "Unnamed: 639",
                       "Unnamed: 640",
                       "Unnamed: 641"}
        
    for i in range(len(df_combined)):

        #options for Age menstration started
        if (df_combined.loc[i, "How old were you when your periods (menstrual bleeds) first started?"] == "I have not had periods"):
            df_combined.loc[i, "Age menstration started"] = "I have not had periods"
        elif (df_combined.loc[i, "Unnamed: 629"] == "I don't remember"):
            df_combined.loc[i, "Age menstration started"] = "I don't remember"
        elif (df_combined.loc[i, "Unnamed: 630"] == "I don't remember"):
            df_combined.loc[i, "Age menstration started"] = "Prefer not to answer"
        elif str(df_combined.loc[i, "Unnamed: 631"]) != "nan":
            df_combined.loc[i, "Age menstration started"] = df_combined.loc[i, "Unnamed: 631"]
        else:
            df_combined.loc[i, "Age menstration started"] = "No response"

        #options for if there is a period in last 3 months           
        if (df_combined.loc[i, "Have you had a period in the last 3 months?"] == "Yes"):
            df_combined.loc[i, "Period in last 3 months"] = "Yes"                
        elif (df_combined.loc[i, "Unnamed: 633"] == "No"):
            df_combined.loc[i, "Period in last 3 months"] = "No"
        elif (df_combined.loc[i, "Unnamed: 634"] == "Prefer not to answer"):
            df_combined.loc[i, "Period in last 3 months"] = "Prefer not to answer"
        else:
            df_combined.loc[i, "Period in last 3 months"] = "No response"

    #options for Contraceptive or natal reason for no period within past 3 months
    for i in reasons_groups: #create a column for each group
        df_combined[i] = ""
        for j in reasons_columns:
            for k in range(len(df_combined)):
                for l in reasons_groups[i]:
                    if re.search(l, str(df_combined.loc[k, j]).lower()):
                        df_combined.loc[k, i] = "Yes"
                        
    for i in range(len(df_combined)):
        if (df_combined.loc[i, "accepted_reasons"] == "Yes"):
            df_combined.loc[i, "Acceptable?"] = "Yes"
        elif (df_combined.loc[i, "unaccepted_reasons"] == "Yes"):
            df_combined.loc[i, "Acceptable?"] = "No"
        else:
            df_combined.loc[i, "Acceptable?"] = "No response"
            

    #options for regular periods
    for i in range(len(df_combined)):
        if (df_combined.loc[i, "Are your periods regular?"] == "Yes"):
            df_combined.loc[i, "Regular periods"] = "Yes"
        elif (df_combined.loc[i, "Unnamed: 646"] == "No"):
            df_combined.loc[i, "Regular periods"] = "No" 
        else:
            df_combined.loc[i, "Regular periods"] = "No response"
            
    #options for heavy periods
    for i in range(len(df_combined)):
        if (df_combined.loc[i, "How would you describe your most recent (last six) periods?"] == "Very"):
            df_combined.loc[i, "Heavy periods"] = "Very"
        elif (df_combined.loc[i, "Unnamed: 658"] == "Moderately"):
            df_combined.loc[i, "Heavy periods"] = "Moderately"
        elif (df_combined.loc[i, "Unnamed: 659"] == "Mildly"):
            df_combined.loc[i, "Heavy periods"] = "Mildly"
        elif (df_combined.loc[i, "Unnamed: 660"] == "Not at all"):
            df_combined.loc[i, "Heavy periods"] = "Not at all"
        else:
            df_combined.loc[i, "Heavy periods"] = "No response"
    
    #options for painful periods
    for i in range(len(df_combined)):
        if (df_combined.loc[i, "Unnamed: 661"] == "Very"):
            df_combined.loc[i, "Painful periods"] = "Very"
        elif (df_combined.loc[i, "Unnamed: 662"] == "Moderately"):
            df_combined.loc[i, "Painful periods"] = "Moderately"
        elif (df_combined.loc[i, "Unnamed: 663"] == "Mildly"):
            df_combined.loc[i, "Painful periods"] = "Mildly"
        elif (df_combined.loc[i, "Unnamed: 664"] == "Not at all"):
            df_combined.loc[i, "Painful periods"] = "Not at all"
        else:
            df_combined.loc[i, "Painful periods"] = "No response"

    return df_combined.iloc[:, np.r_[0, 36:42]]