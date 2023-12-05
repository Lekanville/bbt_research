import numpy as np
import pandas as pd
import re

#selecting the relevant data and renaming the columnns
def select_variables(df):
    df_selected = df.copy()
    columns = np.r_[0, 188:191, 198:201, 214, 216, 218, 220, 222, 224, 226, 678]
    df_process = df_selected.iloc[:, columns]
    
    x = {
        "Have you ever had diabetes?":"Diabetes (Yes)",
        "Unnamed: 189":"Diabetes (No)",
        "Unnamed: 190":"Diabetes (Prefer not to answer)",
        "Have you ever had hypertension (high blood pressure)?":"HBP (Yes)",
        "Unnamed: 199":"HBP (No)",
        "Unnamed: 200":"HBP (Prefer not to answer)",
        "Please describe the problem, and the regular treatment or medication (please include the name of any drug/ medicine and the dose and frequency that you take)":"Ailment_1",
        "Unnamed: 216":"Ailment_2",
        "Unnamed: 218":"Ailment_3",
        "Unnamed: 220":"Ailment_4",
        "Unnamed: 222":"Ailment_5",
        "Unnamed: 224":"Ailment_6",
        "Unnamed: 226":"Ailment_others"
    }
    
    df_renamed = df_process.rename(columns = x)
    df_sorted = df_renamed.sort_values("User ID").reset_index().drop(columns = "index")
    return df_sorted

#combining (Collapsing) the diabetes and HBD columns¶
def combining_diabetes_hbd_columns(df):
        df_combined = df.copy()
        df_combined["Diabetes"] = ""
        df_combined["HBP"] = ""
        
        for i in range(len(df_combined)):
            if (df_combined.loc[i, "Diabetes (Yes)"] == "Yes") & \
            pd.isnull(df_combined.loc[i, "Diabetes (No)"]) & \
            pd.isnull(df_combined.loc[i, "Diabetes (Prefer not to answer)"]):
                df_combined.loc[i, "Diabetes"] = "Yes"
                
            elif pd.isnull(df_combined.loc[i, "Diabetes (Yes)"]) & \
            (df_combined.loc[i, "Diabetes (No)"] == "No") & \
            pd.isnull(df_combined.loc[i, "Diabetes (Prefer not to answer)"]):
                df_combined.loc[i, "Diabetes"] = "No"
                
            else:
                df_combined.loc[i, "Diabetes"] = "Prefer not to answer"
              
            
            if (df_combined.loc[i, "HBP (Yes)"] == "Yes") & \
            pd.isnull(df_combined.loc[i, "HBP (No)"]) & \
            pd.isnull(df_combined.loc[i, "HBP (Prefer not to answer)"]):
                df_combined.loc[i, "HBP"] = "Yes"
                
            elif pd.isnull(df_combined.loc[i, "HBP (Yes)"]) & \
            (df_combined.loc[i, "HBP (No)"] == "No") & \
            pd.isnull(df_combined.loc[i, "HBP (Prefer not to answer)"]):
                df_combined.loc[i, "HBP"] = "No"
                
            else:
                df_combined.loc[i, "HBP"] = "Prefer not to answer" 
        
        return df_combined.iloc[:, np.r_[0, 7:17]]

#getting the other ailments
def other_ailments(df):

    PCOS_Check = [r".*pcos+", r"\Apol"]
    Endocrine_Problems = [r"thyroid", r"hashimotos", "throidism", r"prolactin", r"estrogen",r"hormonal imbalance"]
    Autoimmune_Problems = [r"asthma", r"allergies", r"lupus", r"autoimmune", r"rheumatoid arthritis", r"psoriasis",
                            r"cfs", r"hay-fever", r"pomph", r"graves disease", r"antiphospholipid"]
    Cardiometabolic_Problems = [r"insulin", r"trombophilia", r"b12 deficient", r"protein", r"glucose", r"diabetes",
                                r"anemic", r"tachycardia", r"iron", r"anaemia", r"diabetic", r"leiden", 
                                r"killer cells"]
    Other_Problems = [r"non union femur", r"fracture tibia", r"pelvic.*floor.*dysfunction.*", r"ehlers-danlos", 
                        r"gallbladder", r"broken vertebrae", r"spondylolysis", r"ankylosing spondylitis", 
                        r"hidradenitis supporitiva", r"vsg", r"herpes b", r"syatica", r"sclerosus", r"nasal drip",
                        r"fungus", r"hives", r"ance", r"vertigo", r"dermatographia",
                        r"migraine", r"back pain", r"fibromyalgia", r"headache",
                        r"ulcerative colitis", r"hiatus hernia", r"heart burn", r"gerd", 
                        r"eosinophic eophagitis", r"ibs", r"digestive", r"eosinophilic", r"crohn",
                        r"interstitial cystitis", r"^ic", r"\bbladder", r".*detrusor.*muscle.*",
                        r"hypersomnia", r"sleep.*disorder", r"insomnia", r"sleep.*apnea",
                        r"depression", r"mental health", r"bipolar", r"anxiety", r"adhd", r"agorophobia",
                        r"epilepsy", r"trigeminal",  r'gad', r"deprssion", r"bpd", 
                        r"binge.*eating.*", r"panic"
                    ]
    ailment_groups = {"PCOS_Check":PCOS_Check, "Endocrine_Problems":Endocrine_Problems, 
                  "Autoimmune_Problems":Autoimmune_Problems,
                  "Cardiometabolic_Problems":Cardiometabolic_Problems, "Other_Problems":Other_Problems}

    ailments_columns = {"Ailment_1", "Ailment_2", "Ailment_3", "Ailment_4", "Ailment_5", "Ailment_6", "Ailment_others"}
    
    df_ailments = df.copy()
                
    for i in ailment_groups: #for the entire ailment groups
        df_ailments[i] = "" #create a column for each group
        for j in ailment_groups[i]: # for each string in each group
            for k in range(len(df_ailments)): #and for each row in the df
                for l in ailments_columns: #and for each column of ailment
                    if re.search(j, str(df_ailments.loc[k, l]).lower()): #search the string in each of the row
                            df_ailments.loc[k, i] = "Yes" #return a yes if true to the current column

    return df_ailments.iloc[:, np.r_[0, 8:16]]

#combining the diabetes and HBD Columns with the Cardiometabolic column
def clean_cardiometabolic(df):
    df_cardiometabolic = df.copy()
    for i in range(len(df_cardiometabolic)):
        if ((df_cardiometabolic.loc[i, "Diabetes"] == "Yes") | \
             (df_cardiometabolic.loc[i, "HBP"] == "Yes")) & \
            ~(df_cardiometabolic.loc[i, "Cardiometabolic_Problems"] == "Yes"):
             df_cardiometabolic.loc[i, "Cardiometabolic_Problems"] = "Yes"
        
    return df_cardiometabolic

#adding the PCOS in other ailments columns to the main PCOS column (because some specidied it in 
# ailments and not the main PCOs column)
def clean_wrong_pcos_values(df):
    df_cleaned_pcos = df.copy()
    for i in range(len(df_cleaned_pcos)):
        if ((df_cleaned_pcos.loc[i, "PCOS"] == 0) & \
             (df_cleaned_pcos.loc[i, "PCOS_Check"] == "Yes")):
            df_cleaned_pcos.loc[i, "PCOS"] = 1
     
    return df_cleaned_pcos