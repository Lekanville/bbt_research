import numpy as np
import pandas as pd
import os
import loguru
from sklearn.preprocessing import StandardScaler
#############################################################################################
#The “custom_k_fold.py” script
#This script contains a class which splits the data into k folds for k-1 training data set and
#1 test dataset. It ensures that ratio of the postive and negative outcomes are maintained
#in each k for the users.
#############################################################################################

class CustomKFold:
    def __init__(self, n_splits, df):
        self.n_splits = n_splits
        self.df = df
        self.independent_variables = ['med_pair_distances','med_pair_lengths',
                                      
                                      'min_dist_to_model','min_nadir_days','min_peak_days','min_nadir_temps',
                                      'min_peak_temps','min_nadirs_to_peaks','min_low_to_high_temps',
                                      'min_path_length_to_model','min_warp_degree_with_model','min_Curve_Lengths',
                                      'min_Data_Lengths','min_Curves_by_Data',
                                      
                                      'max_dist_to_model','max_nadir_days','max_peak_days','max_nadir_temps',
                                      'max_peak_temps','max_nadirs_to_peaks','max_low_to_high_temps',
                                      'max_path_length_to_model','max_warp_degree_with_model','max_Curve_Lengths',
                                      'max_Data_Lengths','max_Curves_by_Data',
                                      
                                      'med_dist_to_model','med_nadir_days','med_peak_days','med_nadir_temps',
                                      'med_peak_temps','med_nadirs_to_peaks','med_low_to_high_temps',
                                      'med_path_length_to_model','med_warp_degree_with_model','med_Curve_Lengths',
                                      'med_Data_Lengths','med_Curves_by_Data',
                                      
                                      'rge_dist_to_model','rge_nadir_days','rge_peak_days','rge_nadir_temps',
                                      'rge_peak_temps','rge_nadirs_to_peaks','rge_low_to_high_temps',
                                      'rge_path_length_to_model','rge_warp_degree_with_model','rge_Curve_Lengths',
                                      'rge_Data_Lengths','rge_Curves_by_Data']
        
        self.dependent_variable = "PCOS"
        
    def customSplit(self):
        df_sorted = self.df.sort_values(by = ["User"]) #sort df by the users
        
        df_npcos = self.df[self.df["PCOS"] == 0] #get the non-PCOS cycles
        df_pcos = self.df[self.df["PCOS"] == 1] #get the PCOS cycles
        
        npcos_users = list(set(self.df[self.df["PCOS"] == 0]["User"].values)) #get the non-PCOS users
        pcos_users = list(set(self.df[self.df["PCOS"] == 1]["User"].values)) #get the PCOS users
        
        npcos_users_len = len(npcos_users) #get the length of non-PCOS users
        pcos_users_len = len(pcos_users) #get the length of PCOS users
        all_users_len = len(set(self.df["User"].values)) #get the length of all users

        npcos_ratio = float("{0:.2f}".format((npcos_users_len)/(all_users_len))) #ratio of non-PCOS users
        pcos_ratio = float("{0:.2f}".format((pcos_users_len)/(all_users_len)))   #ratio of PCOS users   
        
        group_compostion = float("{0:.0f}".format(all_users_len/self.n_splits)) #number of users to be in a group
        npcos_composition = float("{0:.0f}".format(group_compostion * npcos_ratio)) #number of non-pcos in a group
        pcos_composition = float("{0:.0f}".format(group_compostion * pcos_ratio)) #number of pcos in a group
        
        groups = []
        ############################This for the non-PCOS user#############################
        i = 0 #for iterating over the non-pcos users
        a = 0 #for iterating over the groups
        
        while i < len(npcos_users): #not going outside the non-PCOS users
            if (i % npcos_composition) != 0: #counting to ensure the group composition is met
                User = npcos_users[i] #selecting a user at a location
                Group = a #assign the current group value to the current selected user
                user_group = {"User":User, "Group":Group} #the user and the assigned group
                groups.append(user_group) #append to the list
                
            else:
                a = a + 1
                User = npcos_users[i] #selecting a user at a location
                Group = a #assign the current group value to the current selected user
                user_group = {"User":User, "Group":Group} #the user and the assigned group
                groups.append(user_group) #append to the list
                
            i = i + 1 #increment the position
        ###################################################################################
        
        ############################This for the PCOS user################################    
        i = 0 #for iterating over the pcos users
        a = 0 #for iterating over the groups
        
        while i < len(pcos_users): #not going outside the PCOS users
            if (i % pcos_composition) != 0: #counting to ensure the group composition is met
                User = pcos_users[i] #selecting a user at a location
                Group = a #assign the current group value to the current selected user
                user_group = {"User":User, "Group":Group} #the user and the assigned group
                groups.append(user_group) #append to the list
                
            else:
                a = a + 1
                User = pcos_users[i] #selecting a user at a location
                Group = a #assign the current group value to the current selected user
                user_group = {"User":User, "Group":Group} #the user and the assigned group
                groups.append(user_group) #append to the list
                
            i = i + 1 #increment the position
        ###################################################################################
        
        initial_user_groups = pd.DataFrame(groups) #convert the list of groups and labels to a dataframe
        
        def edit_outstanding_groups(grped_users, splits):
            df = grped_users
            x = list(df["Group"].value_counts()) #list of the groups
            y = x[1:] #list of the groups starting from 1
            
            #trying to pad incomplete groups if the exist (happens if the dicision isnt up to the defined split)
            try:
                incomplete_value = [j for i,j in zip(x,y) if i != j][0] #finding the start of incomplete groups
                outgroup_val = [j for i,j in zip(x,y) if i != j][-1] #group outside defined set
                incomplete_start = [i for i,j in enumerate(x) if j == incomplete_value][0] #positing incomplete groups

                outgroup_val = [j for i,j in zip(x,y) if i != j][-1] #group outside defined set
                outgroup = [i for i,j in enumerate(x) if j == outgroup_val][0] + 1 #positing incomplete groups (+1 gives the exact group)

                pad_groups = [] 
                for i in list(range((incomplete_start),(splits))):
                    pad_groups.append(i+1) #the incomplete groups

                for i in pad_groups:
                    edit = df[df["Group"] == outgroup].index[0] #get the first outgroup 
                    df.loc[edit, "Group"] = i #edit it to an incomplete group
                    
            except IndexError as e:
                print ("Groups are Okay")
            
            #try to edit users that fell out of groups (happens if the division has remainders)
            try:
                outgroup_val = [j for i,j in zip(x,y) if i != j][-1] #group outside defined set
                outgroup = [i for i,j in enumerate(x) if j == outgroup_val][0] + 1
                edit = list(df[df["Group"] == outgroup].index)

                i = 0 #to start the list iteration
                a = 1 #to start grouping again from the start of the group
                while (a < 10) and (i < len(edit)):
                        df.loc[edit[i], "Group"] = a #edit it to a complete group
                        a = a + 1 #increment the group
                        i = i + 1 #move to the next element in the set
                     
            except IndexError as e:
                print ("No groups out of range")
        
            return(df)
        
        user_grouped = edit_outstanding_groups(initial_user_groups, self.n_splits) #edit the user groups for uniformity
        df_merged = pd.merge(df_sorted, user_grouped, how = 'inner', on = "User") #merge the df with the original
        df_grouped = df_merged.sort_values(by = ["User", "Group"]) #sort by the users and groups
        
        groups = list(range(self.n_splits)) #a list of the groups  
       
    
        def user_groups_list(grped_df, grps): 
            #To see the number of users in each group
            grps_list = [] #empty groups list
            user_groups = list(grped_df.groupby(["Group", "User"]).count().index) #group by the groups and users
            
            for i in grps:
                x = sum(1 for j in user_groups if j[0] == i+1) #count the users in each group (+1 is necessary because
                                                                #the initial counting satrted at 1)  
                x_count = {"Group":i, "User_Count":x} #a dictionary of the group and user counts
                grps_list.append(x_count) #append the group and user count
            return(grps_list) #return the functions
        
        def fold_data(grped_df, grps):
            the_folds = [] #an empty fold list
            
            for i in grps:
                testing_data = grped_df[grped_df["Group"] == i+1] #testing data is the group at i (+1 is necessary cos
                                                                #the initial counting satrted at 1) 
                training_data = grped_df[~(grped_df["Group"] == i+1)]#training data is all other groups (+1 is necessary
                                                                    #cos the initial counting satrted at 1) 
                scaler = StandardScaler() #using scaling
                
                
                ###start from here by defining the independednt variables
                ###I might not need scaling again
                
                testing_data_independent = testing_data[self.independent_variables] #independent variables for testing
                scaler.fit(testing_data_independent) #fitting the independent variables for testing
                X_test = scaler.transform(testing_data_independent) #Transforming the independent variables for testing
                y_test = list(testing_data[self.dependent_variable]) #listing the dependent variable for testing
                
                training_data_independent = training_data[self.independent_variables] #independent variables for training              
                scaler.fit(training_data_independent) #fitting the independent variables for training
                X_train = scaler.transform(training_data_independent) #fitting the independent variables for training
                y_train = list(training_data[self.dependent_variable]) #listing the dependent variable for training        
                
                
                #X_test = testing_data_independent
                #y_test = list(testing_data[self.dependent_variable])
                #X_train = training_data_independent
                #y_train = list(training_data[self.dependent_variable])
                
                train = {"train":{"X_train":X_train, "y_train":y_train}} #dictionary of training data for each fold
                test = {"test":{"X_test":X_test, "y_test":y_test}} #dictionary of testing data for each fold
                
                fold = (train, test) #bundling the fold
                the_folds.append(fold) #appending the fold
                
            return (the_folds) #returning the fold
                
        grps_list = user_groups_list(df_grouped, groups) #getting the groupa nd cycle lists
        folds = fold_data(df_grouped, groups) #getting the folds
        return (df_grouped, grps_list, folds) #returning the folds"""