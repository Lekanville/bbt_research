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
            self.independent_variables = ['Data_Length','Next Cycle Difference','Cycle Completeness','Curve_by_Data','max_of_2_periods',
                                            'max_pos_of_2_periods','max_of_3_periods','max_pos_of_3_periods','Change Point Day','Change Point Mean Diff',
                                            'cost_with_diff','path_length_with_diff','Standard_nadir_temp_actual',
                                            'Standard_peak_temp_actual','Standard_low_to_high_temp',
                                            #'Standard_nadir_day','Standard_peak_day','Standard_nadir_to_peak',
                                            'Expanded_nadir_day', 'Expanded_peak_day', 'Expanded_nadir_to_peak'
                                            ]
        
        elif level == "User Level":
            self.independent_variables = ['med_pair_distances','med_pair_lengths',
            
                                            'min_Data_Length','min_Cycle_Length','min_Cycle_Completeness','min_Curve_by_Data','min_Max_of_2_Periods',
                                            'min_Max_Pos_of_2_Periods','min_Max_of_3_Periods','min_Max_Pos_of_3_Periods','min_Change_Point_Day',
                                            'min_Change_Point_Mean_Diff','min_Path_Length_with_Diff',
                                            'min_Standard_Nadir_Temp_Actual','min_Standard_Peak_Temp_Actual','min_Low_to_High_Temp','min_Cost_with_Diff',
                                            #'min_Standard_Nadir_Day','min_Standard_Peak_Day','min_Nadir_to_Peak',
                                            'min_Expanded_Nadir_Day', 'min_Expanded_Peak_Day', 'min_Expanded_Nadir_to_Peak',
                                            
                                            'max_Data_Length','max_Cycle_Length','max_Cycle_Completeness','max_Curve_by_Data','max_Max_of_2_Periods',
                                            'max_Max_Pos_of_2_Periods','max_Max_of_3_Periods','max_Max_Pos_of_3_Periods','max_Change_Point_Day',
                                            'max_Change_Point_Mean_Diff','max_Path_Length_with_Diff',
                                            'max_Standard_Nadir_Temp_Actual','max_Standard_Peak_Temp_Actual','max_Low_to_High_Temp','max_Cost_with_Diff',
                                            #'max_Standard_Nadir_Day','max_Standard_Peak_Day','max_Nadir_to_Peak',
                                            'max_Expanded_Nadir_Day', 'max_Expanded_Peak_Day', 'max_Expanded_Nadir_to_Peak',

                                            'med_Data_Length','med_Cycle_Length','med_Cycle_Completeness','med_Curve_by_Data','med_Max_of_2_Periods',
                                            'med_Max_Pos_of_2_Periods','med_Max_of_3_Periods','med_Max_Pos_of_3_Periods','med_Change_Point_Day',
                                            'med_Change_Point_Mean_Diff','med_Path_Length_with_Diff',
                                            'med_Standard_Nadir_Temp_Actual','med_Standard_Peak_Temp_Actual','med_Low_to_High_Temp','med_Cost_with_Diff',
                                            #'med_Standard_Nadir_Day','med_Standard_Peak_Day','med_Nadir_to_Peak',
                                            'med_Expanded_Nadir_Day', 'med_Expanded_Peak_Day', 'med_Expanded_Nadir_to_Peak',
                                            
                                            'rge_Data_Length','rge_Cycle_Length','rge_Cycle_Completeness','rge_Curve_by_Data','rge_Max_of_2_Periods',
                                            'rge_Max_Pos_of_2_Periods','rge_Max_of_3_Periods','rge_Max_Pos_of_3_Periods','rge_Change_Point_Day',
                                            'rge_Change_Point_Mean_Diff','rge_Path_Length_with_Diff',
                                            'rge_Standard_Nadir_Temp_Actual','rge_Standard_Peak_Temp_Actual','rge_Low_to_High_Temp','rge_Cost_with_Diff',
                                            #'rge_Standard_Nadir_Day','rge_Standard_Peak_Day','rge_Nadir_to_Peak',
                                            'rge_Expanded_Nadir_Day','rge_Expanded_Peak_Day','rge_Expanded_Nadir_to_Peak'
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

                                            'med_pair_distances','med_pair_lengths',
            
                                            'min_Data_Length','min_Cycle_Length','min_Cycle_Completeness','min_Curve_by_Data','min_Max_of_2_Periods',
                                            'min_Max_Pos_of_2_Periods','min_Max_of_3_Periods','min_Max_Pos_of_3_Periods','min_Change_Point_Day',
                                            'min_Change_Point_Mean_Diff','min_Path_Length_with_Diff',
                                            'min_Standard_Nadir_Temp_Actual','min_Standard_Peak_Temp_Actual','min_Low_to_High_Temp','min_Cost_with_Diff',
                                            #'min_Standard_Nadir_Day','min_Standard_Peak_Day','min_Nadir_to_Peak',
                                            "min_Expanded_Nadir_Day","min_Expanded_Peak_Day","min_Expanded_Nadir_to_Peak",
                                            
                                            'max_Data_Length','max_Cycle_Length','max_Cycle_Completeness','max_Curve_by_Data','max_Max_of_2_Periods',
                                            'max_Max_Pos_of_2_Periods','max_Max_of_3_Periods','max_Max_Pos_of_3_Periods','max_Change_Point_Day',
                                            'max_Change_Point_Mean_Diff','max_Path_Length_with_Diff',
                                            'max_Standard_Nadir_Temp_Actual','max_Standard_Peak_Temp_Actual','max_Low_to_High_Temp','max_Cost_with_Diff',
                                            #'max_Standard_Nadir_Day','max_Standard_Peak_Day','max_Nadir_to_Peak',
                                            "max_Expanded_Nadir_Day","max_Expanded_Peak_Day","max_Expanded_Nadir_to_Peak",

                                            'med_Data_Length','med_Cycle_Length','med_Cycle_Completeness','med_Curve_by_Data','med_Max_of_2_Periods',
                                            'med_Max_Pos_of_2_Periods','med_Max_of_3_Periods','med_Max_Pos_of_3_Periods','med_Change_Point_Day',
                                            'med_Change_Point_Mean_Diff','med_Path_Length_with_Diff',
                                            'med_Standard_Nadir_Temp_Actual','med_Standard_Peak_Temp_Actual','med_Low_to_High_Temp','med_Cost_with_Diff',
                                            #'med_Standard_Nadir_Day','med_Standard_Peak_Day','med_Nadir_to_Peak',
                                            "med_Expanded_Nadir_Day","med_Expanded_Peak_Day","med_Expanded_Nadir_to_Peak",
                                            
                                            'rge_Data_Length','rge_Cycle_Length','rge_Cycle_Completeness','rge_Curve_by_Data','rge_Max_of_2_Periods',
                                            'rge_Max_Pos_of_2_Periods','rge_Max_of_3_Periods','rge_Max_Pos_of_3_Periods','rge_Change_Point_Day',
                                            'rge_Change_Point_Mean_Diff','rge_Path_Length_with_Diff',
                                            'rge_Standard_Nadir_Temp_Actual','rge_Standard_Peak_Temp_Actual','rge_Low_to_High_Temp','rge_Cost_with_Diff',
                                            #'rge_Standard_Nadir_Day','rge_Standard_Peak_Day','rge_Nadir_to_Peak',
                                            'rge_Expanded_Nadir_Day', 'rge_Expanded_Peak_Day', 'rge_Expanded_Nadir_to_Peak'  
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