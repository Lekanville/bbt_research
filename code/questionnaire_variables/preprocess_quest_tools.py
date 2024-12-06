import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

#getting and defining row and columns missingness levels
def get_missing(df):
    df_values = df.copy()
    cols = list(df_values.columns)

    #for the rows
    df_values["Missing"] = ""
    for i in range(len(df_values)):
        count = 0
        for j in cols:
            if (df_values.loc[i,j] == "Prefer not to answer") | \
            (df_values.loc[i,j] == "No response") | \
            (df_values.loc[i,j] == "Do not know") | \
            (df_values.loc[i,j] == "Don't remember") | \
            (df_values.loc[i,j] == "I don't remember") | \
            pd.isnull(df_values.loc[i,j]):
                count+=1
        df_values.loc[i,"Missing"] = count
    df_values = df_values[df_values["Missing"] < 5] #taking out users with more than 5 missing values
    
    #for the columns
    # column_data = []
    # for i in list(df_values.columns):
    #     column_missing = \
    #     len(df_values[(df_values[i] == "Prefer not to answer") | \
    #     (df_values[i] =="No response") | \
    #     (df_values[i] =="Do not know") | \
    #     (df_values[i] =="Don't remember") | \
    #     (df_values[i] =="I don't remember") | \
    #     (pd.isnull(df_values[i]))])

    #     column_data.append(column_missing)
        
    # data = {"Field":list(df_values.columns), "Number Missing":column_data}
    # columns_miss = pd.DataFrame(data, columns = ["Field", "Number Missing"])
    
    #return(df_values, columns_miss)
    return(df_values)

#preprocessing and defining categories
def pre_processing(df):
    df_use = df.copy()
    
    #Taking out oulier values
    #df_pro = df_use[~(df_use["BMI"] == "188.1") & ~(df_use["Baby weight (Kg)"] == "28.1")]
    df_pro = df_use

    median_BMI = np.median(df_pro[df_pro["BMI"] != "No response"]["BMI"].astype(float))
    median_sleep_hrs = np.median(df_pro[df_pro["Sleep Hours"] != "No response"]["Sleep Hours"].astype(float))
    median_baby_weight = np.median(df_pro[df_pro["Baby weight (Kg)"] != "No response"]["Baby weight (Kg)"].astype(float))
    #median_menst_age = np.median(df_use[(df_use["Age menstration started"] != "I don't remember") & 
                  #(df_use["Age menstration started"] != "I have not had periods")]["Age menstration started"].astype(float))
    #max_menst_age = np.max(df_use[(df_use["Age menstration started"] != "I don't remember") & 
                  #(df_use["Age menstration started"] != "I have not had periods")]["Age menstration started"].astype(float))


    for i in range(len(df_pro)):
        #imputation for BMI
        if df_pro.iloc[i, 1] == "No response":
            df_pro.iloc[i, 1] = median_BMI

        #imputation for sleep hours
        if df_pro.iloc[i, 3] == "No response":
            df_pro.iloc[i, 3] = median_sleep_hrs    

        #imputation for baby weight
        #if df_pro.iloc[i, 15] == "No response":
            #df_pro.iloc[i, 15] = median_baby_weight

        #categorizing the baby weight
        if (df_pro.iloc[i, 15] == "0.5") | (df_pro.iloc[i, 15] == "1.2") | (df_pro.iloc[i, 15] == "1.5") | \
            (df_pro.iloc[i, 15] == "1.6") | (df_pro.iloc[i, 15] == "1.7") | (df_pro.iloc[i, 15] == "1.8") | \
            (df_pro.iloc[i, 15] == "1.9") | (df_pro.iloc[i, 15] == "2.0") | (df_pro.iloc[i, 15] == "2.1") | \
            (df_pro.iloc[i, 15] == "2.2") | (df_pro.iloc[i, 15] == "2.3") | (df_pro.iloc[i, 15] == "2.4"):
            df_pro.iloc[i, 15] = "Underweight baby"        
        elif (df_pro.iloc[i, 15] == "2.5") | (df_pro.iloc[i, 15] == "2.6") | (df_pro.iloc[i, 15] == "2.7") | \
            (df_pro.iloc[i, 15] == "2.8") | (df_pro.iloc[i, 15] == "2.9") | (df_pro.iloc[i, 15] == "3.0") | \
            (df_pro.iloc[i, 15] == "3.1") | (df_pro.iloc[i, 15] == "3.2") | (df_pro.iloc[i, 15] == "3.3") | \
            (df_pro.iloc[i, 15] == "3.4") | (df_pro.iloc[i, 15] == "3.5") | (df_pro.iloc[i, 15] == "3.6") | \
            (df_pro.iloc[i, 15] == "3.7") | (df_pro.iloc[i, 15] == "3.8") | (df_pro.iloc[i, 15] == "3.9"):
            df_pro.iloc[i, 15] = "Normal weight baby"
        elif (df_pro.iloc[i, 15] == "4.1") | (df_pro.iloc[i, 15] == "4.3") | (df_pro.iloc[i, 15] == "4.4") | \
            (df_pro.iloc[i, 15] == "8.2"):
            df_pro.iloc[i, 15] = "Overweight baby"
        elif (df_pro.iloc[i, 15] == "No response"):
            df_pro.iloc[i, 15] = "No response"
        else:
            df_pro.iloc[i, 15] = "No response"
            
        #categorizing the menstruation age
        if (df_pro.iloc[i, 16] == "6") | (df_pro.iloc[i, 16] == "7") | (df_pro.iloc[i, 16] == "8") | \
            (df_pro.iloc[i, 16] == "9") | (df_pro.iloc[i, 16] == "10"):
            df_pro.iloc[i, 16] = "Early Menstruation Age"
        elif (df_pro.iloc[i, 16] == "11") | (df_pro.iloc[i, 16] == "12") | (df_pro.iloc[i, 16] == "13") | \
            (df_pro.iloc[i, 16] == "14") | (df_pro.iloc[i, 16] == "15"):
            df_pro.iloc[i, 16] = "Normal Menstruation Age"
        elif (df_pro.iloc[i, 16] == "16") | (df_pro.iloc[i, 16] == "17"):
            df_pro.iloc[i, 16] = "Late Menstruation Age"
        elif (df_pro.iloc[i, 16] == "18") | (df_pro.iloc[i, 16] == "19") | (df_pro.iloc[i, 16] == "20") | \
            (df_pro.iloc[i, 16] == "28"):
            df_pro.iloc[i, 16] = "Very Late Menstruation Age"
        elif (df_pro.iloc[i, 16] == "I have not had periods"):
            df_pro.iloc[i, 16] = "I have not had periods"
        elif (df_pro.iloc[i, 16] == "I don't remember"):
            df_pro.iloc[i, 16] = "I don't remember"
        else:
            df_pro.iloc[i, 16] = "No response"
    
    return df_pro



#This was redone for only BMI preprocessing and defining categories ("BMI", "Regular Smoker", "Age menstration started", "Period in last 3 months", "Regular periods", 
# "Heavy periods", "Painful periods)

def pre_processing_redone(df):
    df_pro = df.copy()
    
    median_BMI = np.median(df_pro[df_pro["BMI"] != "No response"]["BMI"].astype(float))

    median_menst_age = np.median(df_pro[(df_pro["Age menstration started"] != "No response") & (df_pro["Age menstration started"] != "I don't remember") & 
                                (df_pro["Age menstration started"] != "I have not had periods")]["Age menstration started"].astype(int))
    # max_menst_age = np.max(df_pro[(df_pro["Age menstration started"] != "No response") & (df_pro["Age menstration started"] != "I don't remember") & 
    #                             (df_pro["Age menstration started"] != "I have not had periods")]["Age menstration started"].astype(int))

    mode_regular_smoker = df_pro["Regular Smoker"].mode().values[0]
    mode_regular_periods = df_pro["Regular periods"].mode().values[0]

    for i in range(len(df_pro)):
        #imputation for BMI
        if df_pro.loc[i, "BMI"] == "No response":
            df_pro.loc[i, "BMI"] = median_BMI

        #imputation for Menstruation Age
        if df_pro.loc[i, "Age menstration started"] == "No response":
            df_pro.loc[i, "Age menstration started"] =  median_menst_age

        elif df_pro.loc[i, "Age menstration started"] == "I don't remember":
            df_pro.loc[i, "Age menstration started"] =  median_menst_age

        # elif df_pro.loc[i, "Age menstration started"] == "I have not had periods":
        #     df_pro.loc[i, "Age menstration started"] =  max_menst_age

        #imputation for Regular Smoker
        if df_pro.loc[i, "Regular Smoker"] == "Prefer not to answer":
            df_pro.loc[i, "Regular Smoker"] =  mode_regular_smoker

        #imputation for Regular Periods
        if df_pro.loc[i, "Regular periods"] == "No response":
            df_pro.loc[i, "Regular periods"] =  mode_regular_periods

    return df_pro


#I may need this because Louise asks that we imput for each of the folds. 
def missing_imputation(df_train, df_test):
        
    median_BMI = np.median(df_train[df_train["BMI"] != "No response"]["BMI"].astype(float))
    median_menst_age = np.median(df_train[(df_train["Age menstration started"] != "No response") &
                                (df_train["Age menstration started"] != "I don't remember")]["Age menstration started"].astype(int))
    mode_regular_smoker = df_train["Regular Smoker"].mode().values[0]
    mode_regular_periods = df_train["Regular periods"].mode().values[0]

    #for the training data
    for i in range(len(df_train)):
        #imputation for BMI
        if df_train.loc[i, "BMI"] == "No response":
            df_train.loc[i, "BMI"] = median_BMI
 
        #imputation for Menstruation Age
        if df_train.loc[i, "Age menstration started"] == "No response":
            df_train.loc[i, "Age menstration started"] =  median_menst_age

        elif df_train.loc[i, "Age menstration started"] == "I don't remember":
            df_train.loc[i, "Age menstration started"] =  median_menst_age

        #imputation for Regular Smoker
        if df_train.loc[i, "Regular Smoker"] == "Prefer not to answer":
            df_train.loc[i, "Regular Smoker"] =  mode_regular_smoker

        #imputation for Regular Periods
        if df_train.loc[i, "Regular periods"] == "No response":
            df_train.loc[i, "Regular periods"] =  mode_regular_periods

    #for the testing data
    for i in range(len(df_test)):
        #imputation for BMI
        if df_test.loc[i, "BMI"] == "No response":
            df_test.loc[i, "BMI"] = median_BMI

        #imputation for Menstruation Age
        if df_test.loc[i, "Age menstration started"] == "No response":
            df_test.loc[i, "Age menstration started"] =  median_menst_age

        elif df_test.loc[i, "Age menstration started"] == "I don't remember":
            df_test.loc[i, "Age menstration started"] =  median_menst_age

        #imputation for Regular Smoker
        if df_test.loc[i, "Regular Smoker"] == "Prefer not to answer":
            df_testn.loc[i, "Regular Smoker"] =  mode_regular_smoker

        #imputation for Regular Periods
        if df_test.loc[i, "Regular periods"] == "No response":
            df_test.loc[i, "Regular periods"] =  mode_regular_periods

    final_quest_ml_train = pd.get_dummies(df_train, drop_first=True)
    # df_init_train = df_train[["User", "BMI", "Age menstration started", "PCOS"]]
    # final_quest_ml_train = pd.concat([df_init_train, dummies_train], axis = 1)
    # dummies_train = pd.get_dummies(df_train, drop_first=True)

    final_quest_ml_test = pd.get_dummies(df_test, drop_first=True)
    # df_init_test = df_test[["User", "BMI", "Age menstration started", "PCOS"]]
    # final_quest_ml_test = pd.concat([df_init_test, dummies_test], axis = 1)
    # dummies_test = pd.get_dummies(df_test, drop_first=True)

    return (final_quest_ml_train, final_quest_ml_test)


#Cleaning null responses before spliiting at the questionnaire learning
def clean_null_responses(df):
    cols_to_clean = ["BMI", "Age menstration started", "Regular Smoker", "Regular periods"]
    null_responses = ["No response", "I don't remember", "Prefer not to answer"]
    
    for i in range(len(df)):
        for j in cols_to_clean:
            for k in null_responses:
                if df.loc[i, j] == k:
                    df.loc[i, j] = np.nan
                    
    return (df)

#Imputation, scaling and dummy variables creation
def imputation_scaling_and_dummies(train, test, level):
    
    df_train = train.copy()
    df_test = test.copy()
    
    to_dummy = ["Regular Smoker", "Period in last 3 months", "Regular periods", "Heavy periods", "Painful periods"]
    all_cols = df_train.columns.tolist()
    to_scale = [i for i in all_cols if i not in to_dummy]
    
    #Imputation for missing values with traing mean and modes
    if (level == "Questionnaire Level") | (level == "User and Quest Level"):
        median_BMI = np.median(df_train[~pd.isnull(df_train["BMI"])]["BMI"].astype(float))
        median_menst_age = np.median(df_train[~pd.isnull(df_train["Age menstration started"])]["Age menstration started"].astype(float))
        mode_regular_smoker = df_train[~pd.isnull(df_train["Regular Smoker"])]["Regular Smoker"].mode().values[0]
        mode_regular_periods = df_train[~pd.isnull(df_train["Regular periods"])]["Regular periods"].mode().values[0]
        
        #for i in range(len(df_train)):
        df_train["BMI"] = df_train["BMI"].fillna(median_BMI)
        df_train["Age menstration started"] = df_train["Age menstration started"].fillna(median_menst_age)
        df_train["Regular Smoker"] = df_train["Regular Smoker"].fillna(mode_regular_smoker)
        df_train["Regular periods"] = df_train["Regular periods"].fillna(mode_regular_periods)
        
        df_test["BMI"] = df_test["BMI"].fillna(median_BMI)
        df_test["Age menstration started"] = df_test["Age menstration started"].fillna(median_menst_age)
        df_test["Regular Smoker"] = df_test["Regular Smoker"].fillna(mode_regular_smoker)
        df_test["Regular periods"] = df_test["Regular periods"].fillna(mode_regular_periods)
    
    
    #Selecting values to be scaled scaling
    df_train_to_scale = df_train[to_scale].reset_index(drop = True)
    df_test_to_scale = df_test[to_scale].reset_index(drop = True)
    
    
    #Scaling - Scaling values obtained from training dataset...
    scaler = StandardScaler()
    scaler.fit(df_train_to_scale)
    
    #Scaling - ...and imputed for both training and testing datasets
    df_train_scaled = pd.DataFrame(scaler.transform(df_train_to_scale), columns=to_scale)
    df_test_scaled = pd.DataFrame(scaler.transform(df_test_to_scale), columns=to_scale)
    
    #Creating dummy variables
    if (level == "Questionnaire Level") | (level == "User and Quest Level"):
        df_train_to_dummy = df_train[to_dummy].reset_index(drop = True)
        df_test_to_dummy = df_test[to_dummy].reset_index(drop = True)

        df_train_dummies = pd.get_dummies(df_train_to_dummy, drop_first=True, dtype=int)
        df_test_dummies = pd.get_dummies(df_test_to_dummy, drop_first=True, dtype=int)


        #Combine both dummy and scaled values                   
        df_train_combined = pd.concat([df_train_scaled, df_train_dummies], axis = 1)
        df_test_combined = pd.concat([df_test_scaled, df_test_dummies], axis = 1)    
    else:
        df_train_combined = df_train_scaled
        df_test_combined = df_test_scaled
        
    #Incase dummies misses out any dummy cols, then padd those columns
    train_cols = df_train_combined.columns.to_list()
    test_cols = df_test_combined.columns.to_list()

    columns_missed_out_in_dummies = [i for i in train_cols if i not in test_cols]

    if len(columns_missed_out_in_dummies) > 0:
        for i in columns_missed_out_in_dummies:
            df_test_combined[i] = 0

    df_test_combined = df_test_combined[train_cols]

    return (df_train_combined, df_test_combined)