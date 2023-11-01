import numpy as np
import pandas as pd

#selecting the relevant data and renaming the columnns
def select_variables(df):
    df_selected = df.copy()
    df_process = df_selected.iloc[:, np.r_[0, 171:188, -1]]
    x = {"About how many hours sleep do you get in every 24 hours? (please include naps)":"Sleep Hours", 
         "Do you have trouble falling asleep at night or do you wake up in the middle of the night?": "Night Sleep Troubles (Never/ rarely)",
         "Unnamed: 173":"Night Sleep Troubles (Sometimes)",
         "Unnamed: 174":"Night Sleep Troubles (Usually)",
         "Unnamed: 175":"Night Sleep Troubles (Prefer not to answer)",
         "How likely are you to doze off or fall asleep during the daytime when you don't mean to?": "Unintentional Day Sleep (Never/ rarely)",
         "Unnamed: 177":"Unintentional Day Sleep (Sometimes)",
         "Unnamed: 178":"Unintentional Day Sleep (Often)",
         "Unnamed: 179":"Unintentional Day Sleep (All of the time)",
         "Unnamed: 180":"Unintentional Day Sleep (Do not know)",
         "Unnamed: 181":"Unintentional Day Sleep (Prefer not to answer)",
         "Do you consider yourself to be?": "When Active (Very Morning)",
         "Unnamed: 183":"When Active (More Morning)",
         "Unnamed: 184":"When Active (More Evening)",
         "Unnamed: 185":"When Active (Very Evening)",
         "Unnamed: 186":"When Active (Do not know)",
         "Unnamed: 187":"When Active (Prefer not to answer)"
        }
        
    df_renamed = df_process.rename(columns = x)
    df_sorted = df_renamed.sort_values("User ID").reset_index().drop(columns = "index")
    
    return df_sorted

#Combine the sleeping 
def combining_sleep(df):
        df_combined = df.copy()
        df_combined["Night Sleep Troubles"] = ""    
        
        for i in range(len(df_combined)):

            if (df_combined.loc[i, "Night Sleep Troubles (Never/ rarely)"] == "Never/ rarely")& \
            pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Sometimes)"]) & \
            pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Usually)"]) & \
            pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Prefer not to answer)"]):
                df_combined.loc[i, "Night Sleep Troubles"] = "Never/ rarely"
                
            elif pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Never/ rarely)"])& \
            (df_combined.loc[i, "Night Sleep Troubles (Sometimes)"] == "Sometimes") & \
            pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Usually)"]) & \
            pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Prefer not to answer)"]):
                df_combined.loc[i, "Night Sleep Troubles"] = "Sometimes"

            elif pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Never/ rarely)"])& \
            pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Sometimes)"]) & \
            (df_combined.loc[i, "Night Sleep Troubles (Usually)"] == "Usually") & \
            pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Prefer not to answer)"]):
                df_combined.loc[i, "Night Sleep Troubles"] = "Usually"
                
            elif pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Never/ rarely)"])& \
            pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Sometimes)"]) & \
            pd.isnull(df_combined.loc[i, "Night Sleep Troubles (Usually)"]) & \
            (df_combined.loc[i, "Night Sleep Troubles (Prefer not to answer)"] == "Prefer not to answer"):
                df_combined.loc[i, "Night Sleep Troubles"] = "Prefer not to answer"
                
            else:
                df_combined.loc[i, "Night Sleep Troubles"] = "Prefer not to answer"
                
        
        return df_combined.iloc[:, np.r_[0:2, 6:20]]

#Combine the unintentional day sleep columns
def combining_unintentional_day_sleep(df):
        df_combined = df.copy()
        df_combined["Unintentional Day Sleep"] = ""        
        
        for i in range(len(df_combined)):
            if (df_combined.loc[i, "Unintentional Day Sleep (Never/ rarely)"] == "Never/ rarely")& \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Sometimes)"]) & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Often)"]) & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (All of the time)"]) & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Do not know)"]) & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Prefer not to answer)"]):
                df_combined.loc[i, "Unintentional Day Sleep"] = "Never/ rarely"            
            
            elif pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Never/ rarely)"])& \
            (df_combined.loc[i, "Unintentional Day Sleep (Sometimes)"] == "Sometimes") & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Often)"]) & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (All of the time)"]) & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Do not know)"]) & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Prefer not to answer)"]):
                df_combined.loc[i, "Unintentional Day Sleep"] = "Sometimes"    
            
            elif pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Never/ rarely)"])& \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Sometimes)"]) & \
            (df_combined.loc[i, "Unintentional Day Sleep (Often)"] == "Often") & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (All of the time)"]) & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Do not know)"]) & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Prefer not to answer)"]):
                df_combined.loc[i, "Unintentional Day Sleep"] = "Often"  

            elif pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Never/ rarely)"])& \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Sometimes)"]) & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Often)"]) & \
            (df_combined.loc[i, "Unintentional Day Sleep (All of the time)"] == "All of the time") & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Do not know)"]) & \
            pd.isnull(df_combined.loc[i, "Unintentional Day Sleep (Prefer not to answer)"]):
                df_combined.loc[i, "Unintentional Day Sleep"] = "All of the time"  
                
            else:
                df_combined.loc[i, "Unintentional Day Sleep"] = "Prefer not to answer"
                
        return df_combined.iloc[:, np.r_[0:2, 8:17]]

#Combine the active time of day
def combining_active_time_of_day(df):
        df_combined = df.copy()
        df_combined["When Active"] = ""        
        
        for i in range(len(df_combined)):
            if (df_combined.loc[i, "When Active (Very Morning)"] == "Definitely a 'morning' person")& \
            pd.isnull(df_combined.loc[i, "When Active (More Morning)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (More Evening)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (Very Evening)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (Do not know)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (Prefer not to answer)"]):
                df_combined.loc[i, "When Active"] = "Definitely a 'morning' person"            
            
            elif pd.isnull(df_combined.loc[i, "When Active (Very Morning)"]) & \
            (df_combined.loc[i, "When Active (More Morning)"] == "More a 'morning' than 'evening' person") & \
            pd.isnull(df_combined.loc[i, "When Active (More Evening)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (Very Evening)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (Do not know)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (Prefer not to answer)"]):
                df_combined.loc[i, "When Active"] = "More a 'morning' than 'evening' person"        
            
            elif pd.isnull(df_combined.loc[i, "When Active (Very Morning)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (More Morning)"]) & \
            (df_combined.loc[i, "When Active (More Evening)"] == "More an 'evening' than 'morning' person") & \
            pd.isnull(df_combined.loc[i, "When Active (Very Evening)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (Do not know)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (Prefer not to answer)"]):
                df_combined.loc[i, "When Active"] = "More an 'evening' than 'morning' person"  
                
            elif pd.isnull(df_combined.loc[i, "When Active (Very Morning)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (More Morning)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (More Evening)"]) & \
            (df_combined.loc[i, "When Active (Very Evening)"] == "Definitely an 'evening' person") & \
            pd.isnull(df_combined.loc[i, "When Active (Do not know)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (Prefer not to answer)"]):
                df_combined.loc[i, "When Active"] = "Definitely an 'evening' person" 
                
            elif pd.isnull(df_combined.loc[i, "When Active (Very Morning)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (More Morning)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (More Evening)"]) & \
            pd.isnull(df_combined.loc[i, "When Active (Very Evening)"]) & \
            (df_combined.loc[i, "When Active (Do not know)"] == "Do not know") & \
            pd.isnull(df_combined.loc[i, "When Active (Prefer not to answer)"]):
                df_combined.loc[i, "When Active"] = "Do not know" 
                
            else:
                df_combined.loc[i, "When Active"] = "Prefer not to answer"
                
        return df_combined.iloc[:, np.r_[0:2, 8:12]]

#Imputaton for missing data and converting hours to numeric
def convert_hours(df):
    df_convert = df.copy()
    
    median_sleep_hours = np.median(df_convert[~pd.isnull(df_convert['Sleep Hours'])]['Sleep Hours'].astype(float))
    for i in range(len(df_convert)):    
        if pd.isnull(df_convert.loc[i, "Sleep Hours"]):
            df_convert.loc[i, "Sleep Hours"] = median_sleep_hours
    
    df_convert['Sleep Hours'] = df_convert['Sleep Hours'].apply(pd.to_numeric, errors='coerce')
    return df_convert