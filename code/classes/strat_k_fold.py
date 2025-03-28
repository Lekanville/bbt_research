import numpy as np
import pandas as pd
import os
import loguru
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold

import questionnaire_variables.preprocess_quest_tools as preprocess
#############################################################################################
#The “custom_k_fold.py” script
#This script contains a class which splits the data into k folds for k-1 training data set and
#1 test dataset. It ensures that ratio of the postive and negative outcomes are maintained
#in each k for the users and cycles and equally ensures that all cycles for each user belong
#to the same k for the cycle level
#############################################################################################

class StratFunctions:
    
    ############################For User and Cycle Level Splitting####################################
    def user_and_cycle_groups_list(self, grped_df):
        grps = list(set(grped_df["Group"].values))

        #To see the number of users and cycles in each group
        grps_list = [] #empty groups list
        cycles_list = [] #empty cycles list
        
        cycle_groups = list(grped_df.groupby(["Group", "Cycle"]).count().index) #group by the groups and cycles
        user_groups = list(grped_df.groupby(["Group", "User"]).count().index) #group by the groups and users
        
        for i in grps:
            x = sum(1 for j in user_groups if j[0] == i)
            y = sum(1 for j in cycle_groups if j[0] == i)
            
            x_count = {"Group":i, "User_Count":x} #a dictionary of the group and user counts
            y_count = {"Group":i, "Cycle_Count":y} #a dictionary of the group and cycle counts
            
            grps_list.append(x_count) #append the group and user count
            cycles_list.append(y_count) #append the group and cycle count
        
        return(grps_list, cycles_list) #return the functions
     
    ############################For User and Cycle Level Splitting####################################   
    def user_groups_list(self, grped_df):
        grps = list(set(grped_df["Group"].values))

        #To see the number of users in each group
        grps_list = [] #empty groups list
        user_groups = list(grped_df.groupby(["Group", "User"]).count().index) #group by the groups and users
        
        for i in grps:
            x = sum(1 for j in user_groups if j[0] == i)

            x_count = {"Group":i, "User_Count":x} #a dictionary of the group and user counts
            grps_list.append(x_count) #append the group and user count
        return(grps_list) #return the functions

    ###################################################################################################          
    def fold_data(self, grped_df):
        grps = list(set(grped_df["Group"].values))

        the_folds = [] #an empty fold list
        
        for i in grps:
            testing_data = grped_df[grped_df["Group"] == i] 
            training_data = grped_df[~(grped_df["Group"] == i)]

            df_train = training_data[self.independent_variables] #independent variables for training
            y_train = list(training_data[self.dependent_variable]) #listing the dependent variable for training

            df_test = testing_data[self.independent_variables] #independent variables for testing
            y_test = list(testing_data[self.dependent_variable]) #listing the dependent variable for testing

            X_train, X_test = preprocess.imputation_scaling_and_dummies(df_train, df_test, self.level)
        
            train = {"train":{"X_train":X_train, "y_train":y_train}} #dictionary of training data for each fold
            test = {"test":{"X_test":X_test, "y_test":y_test}} #dictionary of testing data for each fold
            
            fold = (train, test) #bundling the fold
            the_folds.append(fold) #appending the fold
            
        return (the_folds) #returning the fold

class StratKFold(StratFunctions):
    def __init__(self, n_splits, df, level):
        self.n_splits = n_splits
        self.df = df
        self.level = level

        if level == "Cycle Level":
            self.independent_variables = [#'Data_Length','Next Cycle Difference','Cycle Completeness','Curve_by_Data','max_of_2_periods',
                                            #'max_pos_of_2_periods','max_of_3_periods','max_pos_of_3_periods','Change Point Day','Change Point Mean Diff',
                                            #'cost_with_diff','path_length_with_diff','Standard_nadir_temp_actual',
                                            #'Standard_peak_temp_actual','Standard_low_to_high_temp',
                                            ##'Standard_nadir_day','Standard_peak_day','Standard_nadir_to_peak',
                                            #'Expanded_nadir_day', 'Expanded_peak_day', 'Expanded_nadir_to_peak'
                                            'Data length','Cycle length','Recorded period cycle proportion','Length of the cycle curve',
                                            'Temperature of largest three-day period','Position of temperature of largest three-day period',
                                            'Temperature of largest four-day period','Position of temperature of largest four-day period',
                                            'Day of temperature change','Diff in temperature before and after temperature change',
                                            'DTW distance','Length of optimal warping path','Nadir day','Peak day','Nadir temperature',
                                            'Peak temperature','Time to peak','Difference between nadir and peak temperatures'
                                            ]
        
        elif level == "User Level":
            self.independent_variables = [
                                            "Median of paired distances", "Median of paired curve lengths",

                                            "Minimum data length", "Minimum cycle length", "Minimum recorded period cycle proportion", "Minimum length of the cycle curve",
                                            "Minimum temp of largest three-day period", "Minimum of position of temp of largest three-day period", "Minimum temp of largest four-day period",
                                            "Minimum of position of temp of largest four-day period", "Minimum day of temperature change", "Minimum diff in temp before and after temp change",
                                            "Minimum DTW distance", "Minimum length of optimal warping path", "Minimum nadir Temp", "Minimum peak Temp", "Minimum Diff btw nadir and peak temps",
                                            "Minimum nadir day",  "Minimum peak day", "Minimum time to peak",

                                            "Maximum data length", "Maximum cycle length", "Maximum recorded period cycle proportion", "Maximum length of the cycle curve",
                                            "Maximum temp of largest three-day period", "Maximum of position of temp of largest three-day period", "Maximum temp of largest four-day period",
                                            "Maximum of position of temp of largest four-day period", "Maximum day of temperature change", "Maximum diff in temp before and after temp change",
                                            "Maximum DTW distance", "Maximum length of optimal warping path", "Maximum nadir Temp", "Maximum peak Temp", "Maximum Diff btw nadir and peak temps",
                                            "Maximum nadir day",  "Maximum peak day",  "Maximum time to peak",
                                                
                                            "Median data length", "Median cycle length", "Median recorded period cycle proportion", "Median length of the cycle curve", 
                                            "Median temp of largest three-day period", "Median of position of temp of largest three-day period", "Median temp of largest four-day period",
                                            "Median of position of temp of largest four-day period", "Median day of temperature change", "Median diff in temp before and after temp change",
                                            "Median DTW distance", "Median length of optimal warping path", "Median nadir Temp", "Median peak Temp", "Median Diff btw nadir and peak temps",
                                            "Median nadir day",  "Median peak day",  "Median time to peak",

                                            "Range of data length", "Range of cycle length", "Range of recorded period cycle proportion", "Range of length of the cycle curve", 
                                            "Range of temp of largest three-day period", "Range of position of temp of largest three-day period", "Range of temp of largest four-day period",
                                            "Range of position of temp of largest four-day period", "Range of day of temperature change", "Range of diff in temp before and after temp change",
                                            "Range of DTW distance", "Range of length of optimal warping path", "Range of nadir Temp", "Range of peak Temp", "Range of Diff btw nadir and peak temps",
                                            "Range of nadir day",  "Range of peak day", "Range of time to peak",
                                            
                                            #'min_Standard_Nadir_Day','min_Standard_Peak_Day','min_Nadir_to_Peak',
                                            #'max_Standard_Nadir_Day','max_Standard_Peak_Day','max_Nadir_to_Peak',
                                            #'med_Standard_Nadir_Day','med_Standard_Peak_Day','med_Nadir_to_Peak',
                                            #'rge_Standard_Nadir_Day','rge_Standard_Peak_Day','rge_Nadir_to_Peak',
                                            ]

        elif level == "Questionnaire Level":
            # self.independent_variables = ['BMI','Age menstration started',
            #                                 'Regular Smoker_Yes',
            #                                 'Period in last 3 months_Yes',
            #                                 'Regular periods_Yes',
            #                                 'Heavy periods_Moderately','Heavy periods_Not at all','Heavy periods_Very',
            #                                 'Painful periods_Moderately','Painful periods_Not at all','Painful periods_Very']
            self.independent_variables = ["BMI", "Age menstration started", 
                                            "Regular Smoker", "Period in last 3 months", "Regular periods", "Heavy periods", "Painful periods"]

        elif level == "User and Quest Level":
            self.independent_variables = [#'BMI','Age menstration started', 'Regular Smoker_Yes', 'Period in last 3 months_Yes', 'Regular periods_Yes',
                                        #'Heavy periods_Moderately','Heavy periods_Not at all','Heavy periods_Very', 'Painful periods_Moderately','Painful periods_Not at all','Painful periods_Very',
                                            "BMI", "Age menstration started", 
                                            "Regular Smoker", "Period in last 3 months", "Regular periods", "Heavy periods", "Painful periods",

                                            "Median of paired distances", "Median of paired curve lengths",

                                            "Minimum data length", "Minimum cycle length", "Minimum recorded period cycle proportion", "Minimum length of the cycle curve",
                                            "Minimum temp of largest three-day period", "Minimum of position of temp of largest three-day period", "Minimum temp of largest four-day period",
                                            "Minimum of position of temp of largest four-day period", "Minimum day of temperature change", "Minimum diff in temp before and after temp change",
                                            "Minimum DTW distance", "Minimum length of optimal warping path", "Minimum nadir Temp", "Minimum peak Temp", "Minimum Diff btw nadir and peak temps",
                                            "Minimum nadir day",  "Minimum peak day", "Minimum time to peak",

                                            "Maximum data length", "Maximum cycle length", "Maximum recorded period cycle proportion", "Maximum length of the cycle curve",
                                            "Maximum temp of largest three-day period", "Maximum of position of temp of largest three-day period", "Maximum temp of largest four-day period",
                                            "Maximum of position of temp of largest four-day period", "Maximum day of temperature change", "Maximum diff in temp before and after temp change",
                                            "Maximum DTW distance", "Maximum length of optimal warping path", "Maximum nadir Temp", "Maximum peak Temp", "Maximum Diff btw nadir and peak temps",
                                            "Maximum nadir day",  "Maximum peak day",  "Maximum time to peak",
                                                
                                            "Median data length", "Median cycle length", "Median recorded period cycle proportion", "Median length of the cycle curve", 
                                            "Median temp of largest three-day period", "Median of position of temp of largest three-day period", "Median temp of largest four-day period",
                                            "Median of position of temp of largest four-day period", "Median day of temperature change", "Median diff in temp before and after temp change",
                                            "Median DTW distance", "Median length of optimal warping path", "Median nadir Temp", "Median peak Temp", "Median Diff btw nadir and peak temps",
                                            "Median nadir day",  "Median peak day",  "Median time to peak",

                                            "Range of data length", "Range of cycle length", "Range of recorded period cycle proportion", "Range of length of the cycle curve", 
                                            "Range of temp of largest three-day period", "Range of position of temp of largest three-day period", "Range of temp of largest four-day period",
                                            "Range of position of temp of largest four-day period", "Range of day of temperature change", "Range of diff in temp before and after temp change",
                                            "Range of DTW distance", "Range of length of optimal warping path", "Range of nadir Temp", "Range of peak Temp", "Range of Diff btw nadir and peak temps",
                                            "Range of nadir day",  "Range of peak day", "Range of time to peak",
                                            
                                            #'min_Standard_Nadir_Day','min_Standard_Peak_Day','min_Nadir_to_Peak',
                                            #'max_Standard_Nadir_Day','max_Standard_Peak_Day','max_Nadir_to_Peak',
                                            #'med_Standard_Nadir_Day','med_Standard_Peak_Day','med_Nadir_to_Peak',
                                            #'rge_Standard_Nadir_Day','rge_Standard_Peak_Day','rge_Nadir_to_Peak',
                                        ]

        self.dependent_variable = "PCOS"

    def customSplit(self):
   
        df_sorted = self.df.sort_values(by = ["User"]) #sort df by the users
        df_users = df_sorted.groupby("User").first().reset_index()[["User", "PCOS"]] # The unique list of users and their PCOS label
        skf = StratifiedKFold(n_splits=self.n_splits, shuffle=True, random_state=1)

        #The training and validation datasets
        X = df_users["User"]
        y = df_users[self.dependent_variable]
        i = 0
        new_df = pd.DataFrame()

        for train_index, test_index in skf.split(X, y):
            x_train_fold, x_test_fold = X.loc[train_index], X.loc[test_index]
            #y_train_fold, y_test_fold = y.loc[train_index], y.loc[test_index]
            #x_test_fold = pd.concat([x_test_fold, y_test_fold], axis = 1)
            
            x_test_fold = pd.DataFrame(x_test_fold)
            x_test_fold["Group"] = i

            new_df = pd.concat([new_df, x_test_fold], axis = 0)

            i+=1
        
        
        df_merged = pd.merge(df_sorted, new_df, how = 'inner', on = "User") #merge the df with the original
        df_grouped = df_merged.sort_values(by = ["User", "Group"]) #sort by the users and groups
        
        if self.level == "Cycle Level":
            grps_list = self.user_and_cycle_groups_list(df_grouped) #getting the group and cycle lists for cycle level only
        else:
             grps_list = self.user_groups_list(df_grouped) #getting the group lists for user level only

        folds = self.fold_data(df_grouped) #getting the folds

        return (df_grouped, grps_list, folds) #returning the folds