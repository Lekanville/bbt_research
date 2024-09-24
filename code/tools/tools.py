import json
import numpy as np
import pandas as pd
from loguru import logger
pd.options.mode.chained_assignment = None

#My generic algorithm for getting all users in a multi-index
def get_users(grouped_data):
    usershat = []
    for key, group in grouped_data.index:
        if key not in usershat:
            usershat.append(key)
    return usershat

#My generic algorithm for getting all users in a single index
def get_users_cycles(grouped_data):
    usershat = []
    for key in grouped_data.index:
        if key not in usershat:
            usershat.append(key)
    return usershat

#Matrix generator for plotting a grid of subplots
def matrix_generator():
    a=0
    i=0
    j=0
    inc = []
    while a < 1000:
        x = [i,j]
        a += 1
        if (a % 10) == 0:
            i += 1
            j = 0
        else:
            i = i
            j += 1
        inc.append(x)
    return inc

#Loading the model cycle
def load_model_cycle(model_cycle):
    try:
        with open(model_cycle, "r") as f:
            model_cycles = json.load(f)
    except Exception as ex:
        print("Could not load the model cycle: ", ex)
    
    return(model_cycles)

def save_model_cycle(model_cycle, OUTPUT):
    try:
        with open(OUTPUT, "w") as f:
            json.dump(model_cycle, f)
    except Exception as ex:
        print("Error while saving object:", ex)

#Plotting layout
def fig_layout():
    return plt.figure()

#Lenght of a line
def length_of_line(yaxis, xaxis):
    d = 0
    for i in range(len(yaxis)-1):
        y_diff = (yaxis[i] - yaxis[i+1])**2
        x_diff = (xaxis[i] - xaxis[i+1])**2
        s = np.sqrt(np.sum([y_diff, x_diff]))
        d+=s
    return d

#Custom algorithm for getting the amount of warping
def warp_degree(path_x, path_y):
    mag = []
    for i in range(len(path_x)-1):
        if path_x[i] == path_x[i+1]:
            mag.append(path_x[i]) 

    for i in range(len(path_y)-1):
        if path_y[i] == path_y[i+1]:
            mag.append(path_y[i]) 
    return len(mag)

#Algorithm for selecting users with a give criteria
def users_btw_3_and_10(cycles):
    cycle_counts = cycles.groupby("User ID_y").count() #group the cycles table by users and cycles
    users_less_10 = cycle_counts[(cycle_counts["Cycle ID"] >= 3) & (cycle_counts["Cycle ID"] <= 10)] #get the users with the values
    users_10_cycles = get_users_cycles(users_less_10) #now get the the users
    return users_10_cycles

#This algorithm takes out outliers for a normalized data
def trimming_for_outliers(df):
    logger.info("================Cycle filtering using derived features started==================")
    counts = dict(df["PCOS"].value_counts())
    logger.info(f"Total cycle length before trimmimg: {counts}")

    #1. nan Nadir days
    df = df[~(pd.isnull(df["Standard_nadir_day"]))] #Trim out cycles with nadirs null nadirs. This is typical of long cycles lenghts without much 
    counts = dict(df["PCOS"].value_counts())   #temperature records
    logger.info(f"The length after cleaning out null nadirs: {counts}")

    #Trimming value for peak day
    peak_day_mean = float("{0:.2f}".format(np.mean(df["Standard_peak_day"].values))) #the mean of the peak days
    peak_day_std = float("{0:.2f}".format(np.std(df["Standard_peak_day"].values))) #the standard deviation of the peak days
    peak_day_trim = peak_day_mean+(3*peak_day_std) #trim peak day upto 3 times the std after mean

    #Trimming value for Nadir temperature
    nadir_temp_mean = float("{0:.2f}".format(np.mean(df["Standard_nadir_temp_actual"].values))) #mean of the nadir temps
    nadir_temp_std = float("{0:.2f}".format(np.std(df["Standard_nadir_temp_actual"].values))) #std of the nadir temps
    nadir_temp_trim_left = nadir_temp_mean-(3*nadir_temp_std) #trim nadir temps upto 3 times std before the mean
    nadir_temp_trim_right = nadir_temp_mean+(3*nadir_temp_std) #trim nadir temps upto 3 times std after the mean

    #Trimming value for Cycle length
    mean_length = float("{0:.2f}".format(np.mean(df["Data_Length"].values))) #mean of the data length
    std_length = float("{0:.2f}".format(np.std(df["Data_Length"].values))) #std of the data length
    length_trim_left = mean_length-(3*std_length)
    length_trim_right = mean_length+(3*std_length)

    
    #cycles with more than 9 data records
    #first convert the days to a proper list
    # df["Days"] = df["Days"].apply(lambda x: list(map(int, (x.replace("[", "").replace("]", "").split(","))))) 
    # df["Len_Days"] = df["Days"].apply(lambda x: len(x))
    # df = df[df["Len_Days"] > 9]
    # counts = dict(df["PCOS"].value_counts())
    # logger(f"The length after cleaning out cycles with lengths less than 10: {counts}")

    #2. Nadirs more than 50 - same
    # df = df[(df["Standard_nadir_day"] <= 50)] #Trim out cycles with nadirs greater than 50
    # counts = dict(df["PCOS"].value_counts())
    # logger.info(f"The length after cleaning out cycles with nadirs greater than 50: {counts}")
    
    #3. Upper outlier peaks days - same
    # df = df[(df["Standard_peak_day"] <= peak_day_trim)] #Trim out cycles with peaks greater than trim 
    # counts = dict(df["PCOS"].value_counts())
    # logger.info(f"The length after cleaning out upper oulier peaks: {counts}")

    #4. Nadirs equalling peaks
    df = df[(df["Standard_nadir_day"] != df["Standard_peak_day"])] #Trim out cycles with nadirs equalling peaks. This is peculiar
    counts = dict(df["PCOS"].value_counts())        #of cycles that are basically descends
    logger.info(f"The length after cleaning out cycles having nadirs equalling peaks: {counts}")       

    #5. Lower outlier nadir temps
    # df = df[(df["Standard_nadir_temp_actual"] > nadir_temp_trim_left)]
    # counts = dict(df["PCOS"].value_counts())
    # logger.info(f"The length after cleaning out lower outlier nadir temps: {counts}")

    #6. Upper outlier nadir temps
    # df = df[(df["Standard_nadir_temp_actual"] < nadir_temp_trim_right)]
    # counts = dict(df["PCOS"].value_counts())
    # logger.info(f"The length after cleaning out upper outlier nadir temps: {counts}")

    #7. Negative high to low temperatures
    # df = df[(df["Standard_low_to_high_temp"] > 0)] #Trim out cycles with a negative high and low temp. difference. This is peculiar of 
    # counts = dict(df["PCOS"].value_counts()) #cycles that a near flat temperature reading at the nadir and peak positions
    # logger.info(f"The length after cleaning out negative high and low temp: {counts}")


    #8. Negative high to low Difference in Nadir and Peak Days
    df = df[(df["Standard_nadir_to_peak"] > 0)] #Trim out cycles with a negative high and low temp. difference. This is peculiar of 
    counts = dict(df["PCOS"].value_counts()) #cycles that a near flat temperature reading at the nadir and peak positions
    logger.info(f"The length after cleaning out negative Difference in Nadir and Peak Days: {counts}")

    #9. Non last cycles
    # df = df[~(df["Next Cycle Difference"].isnull())] #remove last cycles most of which are largely incomplete
    # counts = dict(df["PCOS"].value_counts())
    # logger.info(f"The non last cycles: {counts}") 

    #10. Data lenghts more than 100
    # df = df[(df["Data_Length"] < 101)] #remove cycles with more than 100 days
    # counts = dict(df["PCOS"].value_counts())
    # logger.info(f"The length after cleaning data lengths that are more than 100: {counts}")
    
    #11.
    df = df[(df["Data_Length"] >= length_trim_left) & (df["Data_Length"] <= length_trim_right)] #Trim out cycles lenght outliers. 
    counts = dict(df["PCOS"].value_counts())
    logger.info(f"The length after cleaning out cycles with outlier data lengths: {counts}")

    logger.info("================Cycle filtering using derived features ended==================")
    return df

#This algorithm takes out outliers for a normalized data
def trimming_for_outliers_MM(df):
    #Trimming value for peak day
    peak_day_mean = float("{0:.2f}".format(np.mean(df["MinMax_peak_day"].values))) #the mean of the peak days
    peak_day_std = float("{0:.2f}".format(np.std(df["MinMax_peak_day"].values))) #the standard deviation of the peak days
    peak_day_trim = peak_day_mean+(3*peak_day_std) #trim peak day upto 3 times the std after mean

    #Trimming value for Nadir temperature
    nadir_temp_mean = float("{0:.2f}".format(np.mean(df["MinMax_nadir_temp_actual"].values))) #mean of the nadir temps
    nadir_temp_std = float("{0:.2f}".format(np.std(df["MinMax_nadir_temp_actual"].values))) #std of the nadir temps
    nadir_temp_trim_left = nadir_temp_mean-(3*nadir_temp_std) #trim nadir temps upto 3 times std before the mean
    nadir_temp_trim_right = nadir_temp_mean+(3*nadir_temp_std) #trim nadir temps upto 3 times std after the mean

    df = df[(df["MinMax_nadir_day"] <= 50) & #Trim out cycles with nadirs greater than 50 
                    (df["MinMax_peak_day"] <= peak_day_trim) & #Trim out cycles with peaks greater than trim 
                    (df["MinMax_nadir_day"] != df["MinMax_peak_day"]) & #Trim out cycles with nadirs 
                                                                                    #equalling peaks. This is peculiar
                                                                                    #of cycles that are basically 
                                                                                    #descends
                    (df["MinMax_nadir_temp_actual"] > nadir_temp_trim_left) &
                    (df["MinMax_nadir_temp_actual"] < nadir_temp_trim_right) &
                    (df["MinMax_low_to_high_temp"] > 0) & #Trim out cycles with a negative high and low temp.
                                                                #difference. This is peculiar of cycles that a near 
                                                                #flat temperature reading at the nadir and peak positions
                    ~(df["Date_Diff"].isnull())& #remove last cycles most of which are largely incomplete
                    (df["Data_Length"] < 101) #remove cycles with more than 100 days
                   ]

    return df

#select 3 cycles each from the users
def select_3_cycles(df):
    df_3 = pd.DataFrame()
    for j in list(df["User"].unique()):
        user_cycles = list(df[df["User"] == j]["Cycle"]) #Getting cycles for a user
        
        rng = np.random.default_rng(seed=101)
        rand_3_cycles = list(rng.choice(user_cycles, 3, replace=False))
        
        for i in rand_3_cycles:
            df_cycle = df[df["Cycle"] == i] #Data for each of the selected cycles
            df_3 = pd.concat([df_3, df_cycle], axis = 0) #add to the data for learning
    return df_3

#clean up the excel questionnaire file
def clean_quest(df):
    df_funct = df.copy()
    #rename the ID Column
    
    df_funct.rename({"Unnamed: 0":"User ID"}, inplace = True, axis = 1)
    
    #Select the data portions and reset index
    df_funct = df_funct.iloc[2:,:]

    #drop partial duplicates
    df_funct["count"] = df_funct.isnull().sum(1)

    df_new = df_funct.sort_values("count").drop_duplicates(subset = ["User ID"], keep='first').drop(columns = 'count')
    
    df_new.reset_index(inplace = True, drop = True)
    return df_new

def get_nadirs_and_peaks(std_temps_list, path, smooth_temps, model_cycle, cycle):

    Standard_smooth_temps = std_temps_list
    Standard_path = path
    model_cycle = model_cycle

    if len(np.where(~(np.isnan(Standard_smooth_temps)))[0]) > 0 :

        #The positions of the non NaN values on the cycle
        first = np.where(~np.isnan(Standard_smooth_temps))[0][0]
        last = np.where(~np.isnan(Standard_smooth_temps))[0][-1]
        
        #The position of the least on the entire model cycle
        model_least_position = np.where(np.array(model_cycle) == min(model_cycle))[0][0]

        #The other half of the model after least of the model cycle
        model_cycle_other_half = model_cycle[model_least_position:]

        #The position of the maximum on the entire model cycle
        model_max_position = np.where(np.array(model_cycle) == max(model_cycle_other_half))[0][0]

        #This was don using DTW with missigness. We have reverted to the regular DTW.
        #Corresponding positions of the non NaN values on the model
        #model_cycle_part = model_cycle[first:last+1]

        #The maximum and minimum positions of the model in retropect to the cycle
        #The position of the least on the partial model cycle
        #model_least_position_on_partial = np.where(np.array(model_cycle_part) == min(model_cycle_part))[0][-1]
        #The position of the least on the enite model cycle
        #model_least_position = np.where(np.array(model_cycle) == min(model_cycle_part))[0][0]

        #The other half of the model starting from the position of the least of the partial model cycle
        #model_cycle_part_other_half = model_cycle_part[model_least_position_on_partial:]
        #The maximum of the model in retropect to the partial model cycle and the cycle to be warped
        #model_max_position = np.where(np.array(model_cycle) == max(model_cycle_part_other_half))[0][0]

        #Computing nadir and peak using DTW and standardized temperature values
        #The minimum temperature warped to the least of the model
        Standard_nadir_temp_list = [Standard_smooth_temps[mapy] for mapx, mapy in Standard_path if mapx == model_least_position ] 
        Standard_nadir_temp = min(Standard_nadir_temp_list)
        # print(Standard_nadir_temp)
        #The position of the nadir among the warped leasts
        Standard_nadir_position = [i for i, e in enumerate(Standard_nadir_temp_list) if e == Standard_nadir_temp][-1]

        #All positions warped to the least of the model
        Standard_nadir_day_list = [[mapx, mapy] for mapx, mapy in Standard_path if mapx == model_least_position]
        #Actual position of the nadir on cycle
        Standard_nadir_day = Standard_nadir_day_list[Standard_nadir_position][1]
        #The actual nadir smooth temperature
        Standard_nadir_temp_actual = smooth_temps[Standard_nadir_day]
        
        #The maximum temperature warped to the highest of the model
        #the maximum value warped to the maximum of model
        Standard_peak_temp_list = [Standard_smooth_temps[mapy] for mapx, mapy in Standard_path if mapx == model_max_position] #All values warped to the maximum of model
        Standard_peak_temp = max(Standard_peak_temp_list) #the maximum value warped to the maximum of model
        #The position of the peak among the warped highests 
        Standard_peak_position = [i for i, e in enumerate(Standard_peak_temp_list) if e == Standard_peak_temp][0]

        #All positions warped to the highest of the model
        Standard_peak_day_list = [[mapx, mapy] for mapx, mapy in Standard_path if mapx == model_max_position]
        #Actual position of the peak on cycle 
        Standard_peak_day = Standard_peak_day_list[Standard_peak_position][1]
        #The actual peak smooth temperature  
        Standard_peak_temp_actual = smooth_temps[Standard_peak_day]

        #position of the least temperature on the model
        #model_least_position = [i for i, e in enumerate(model_cycle) if e == min(model_cycle)].pop()
        
        #position of the highest temperature on the model    
        #model_max_position = [i for i, e in enumerate(model_cycle) if e == max(model_cycle)].pop()


        #Computing nadir and peak using DTW and standardized temperature values
        
        #The minimum temperature warped to the least of the model
        #Standard_nadir_temp_list = [Standard_smooth_temps[mapy] for mapx, mapy in Standard_path if mapx == model_least_position] 
        #Standard_nadir_temp = min(Standard_nadir_temp_list)
        
        #The position of the nadir among the warped leasts
        #Standard_nadir_position = [i for i, e in enumerate(Standard_nadir_temp_list) if e == Standard_nadir_temp][-1]
        
        #All positions warped to the least of the model
        #Standard_nadir_day_list = [[mapx, mapy] for mapx, mapy in Standard_path if mapx == model_least_position]
        
        #Actual position of the nadir on cycle
        #Standard_nadir_day = Standard_nadir_day_list[Standard_nadir_position][1]
        
        #The actual nadir smooth temperature
        #Standard_nadir_temp_actual = smooth_temps[Standard_nadir_day]
        
        #The maximum temperature warped to the highest of the model
        #Standard_peak_temp_list = [Standard_smooth_temps[mapy] for mapx, mapy in Standard_path if mapx == model_max_position] #All values warped to the maximum of model
        #Standard_peak_temp = max(Standard_peak_temp_list) #the maximum value warped to the maximum of model
        #The position of the peak among the warped highests 
        #    
        # try:
        #     Standard_peak_position = [i for i, e in enumerate(Standard_peak_temp_list) if e == Standard_peak_temp][0] #position of the maximum 
        # except IndexError :
        #     print ("*************************************")
        #     print (cycle)
        #     print (smooth_temps)
        #All positions warped to the highest of the model
        #Standard_peak_day_list = [[mapx, mapy] for mapx, mapy in Standard_path if mapx == model_max_position] #Position of the maximum warps
        
        #Actual position of the peak on cycle   
        #Standard_peak_day = Standard_peak_day_list[Standard_peak_position][1]
        
        #The actual peak smooth temperature   
        #Standard_peak_temp_actual = smooth_temps[Standard_peak_day]

        if str(Standard_peak_temp_actual) == "nan":
            print ("Cycle: ", cycle)
            print ("Temps: ", smooth_temps)

    else:
        Standard_nadir_day = np.nan
        Standard_nadir_temp = np.nan
        Standard_nadir_temp_actual = np.nan
        Standard_peak_day = np.nan
        Standard_peak_temp = np.nan
        Standard_peak_temp_actual = np.nan

    results = (Standard_nadir_day, Standard_nadir_temp, Standard_nadir_temp_actual, 
                Standard_peak_day, Standard_peak_temp, Standard_peak_temp_actual)
    return (results)


def other_dtw_values(best_path, paths_values, cycle_least_pos, cycle_max_pos):
    # Note: with_diff means that the computation is done between the maximum and minimum of multiple warps 
    # at the tail ends
    
    least = max([x for x in best_path if x[1] == cycle_least_pos])
    maximum = min([x for x in best_path if x[1] == cycle_max_pos])
    # print (least, maximum)
    
    
    # This gets the difference in dtw positions between the first and last one-on-one maps between the model 
    # and the cycle
    for i, j in enumerate(best_path):
        #print (j)
        if j == least:
            index_least = i
        if j == maximum:
            index_max = i
            
    pos_count_with_diff = (index_max - index_least)/((cycle_max_pos - cycle_least_pos) + 1) # + 1 caters for the index
    ## print("The index after the initial multiple warps: ", index_least)
    ## print("The index before the last multiple warps: ", index_max)
    # print("The difference tail warp positions: ", diff)        
    
    
    ## This is to test the equation for the length of the line
    ## I feel this will be needed but Louise feels it isnt
    curr_path = best_path[index_least:index_max+1]
    y_axis = [i[0] for i in curr_path]
    x_axis = [i[1] for i in curr_path]
    path_length_with_diff = (length_of_line(y_axis, x_axis))/((cycle_max_pos - cycle_least_pos) + 1) # + 1 caters for the index
    ## print("The difference tail warp positions using curve equation: ", curve_diff)
    
    
    least_path = [least[0]+1, least[1]+1]
    maximum_path = [maximum[0]+1, maximum[1]+1]

    
    # This gets the difference in dtw costs between the first and last one-on-one maps between the model 
    # and the cycle
    least_path_x = least_path[0]
    least_path_y = least_path[1]
    maximum_path_x = maximum_path[0]
    maximum_path_y = maximum_path[1]

    least_cost = paths_values[least_path_x, least_path_y]
    max_cost = paths_values[maximum_path_x, maximum_path_y]
    cost_with_diff = (max_cost - least_cost)/((cycle_max_pos - cycle_least_pos) + 1) # + 1 caters for the index
    ## print([least_path_x, least_path_y], [maximum_path_x, maximum_path_y])
    ## print(least_cost, max_cost)
    
    # print("The difference tail warp costs: ", cost_diff)
    
    return (pos_count_with_diff, path_length_with_diff, cost_with_diff)



def get_expanded_values(smooth_temps):
    len_values = len(smooth_temps)
    x = np.linspace(0,1,len_values)
    to_interp = np.linspace(0,1,51)
    
    first = np.where(~np.isnan(smooth_temps))[0][0]
    last = np.where(~np.isnan(smooth_temps))[0][-1]
    
    x_val_first = x[first]
    x_val_last = x[last]
    
    to_interp_index_first = np.where(to_interp>=x_val_first)[0][0]
    to_interp_index_last = np.where(to_interp<=x_val_last)[0][-1]
    
    interpedSeq = list(np.interp(to_interp[to_interp_index_first:to_interp_index_last+1], x[first:last+1], smooth_temps[first:last+1]))
    
    first_part = list([np.nan]*(to_interp_index_first))
    last_part = list([np.nan]*(len(to_interp) - (to_interp_index_last + 1)))
    
    final = first_part + interpedSeq + last_part
    return (final)


def cycle_completeness(df):
    logger.info("================Cycle filtering started==================")
    logger.info(f"The initial set of cycles: {len(df)}")

    #1. Non-last cycles
    df_non_last = df[(df["Date_Diff"] != 'Indeterminate Last Cycle')]
    counts = dict(df_non_last["PCOS"].value_counts())
    counts_users = dict(df_non_last["User ID"].value_counts())
    logger.info(f"Non last cycles: {counts}")
    logger.info(f"Number of Users: {counts_users}")

    #2. Non-negative offsets
    df_non_neg_offset = df_non_last[df_non_last["Offset"] >= 0]
    counts = dict(df_non_neg_offset["PCOS"].value_counts())
    counts_users = dict(df_non_neg_offset["User ID"].value_counts())
    logger.info(f"Non negative offsets: {counts}")
    logger.info(f"Number of Users: {counts_users}")
    df_non_neg_offset.reset_index(inplace = True, drop = True)

    for i in range(len(df_non_neg_offset)):
        df_non_neg_offset.loc[i, "Date_Diff"] = int(df_non_neg_offset.loc[i, "Date_Diff"])
        if (df_non_neg_offset.loc[i, "Date_Diff"] !=  0.0):
           df_non_neg_offset.loc[i, "cycle_compl"] = (df_non_neg_offset.loc[i, "Data_Dur"])/(df_non_neg_offset.loc[i, "Date_Diff"])
        else:
            df_non_neg_offset.loc[i, "cycle_compl"] = 0
        # if df_non_last.loc[i, "Date_Diff"] < 1.0:
        #     logger.info(df_non_last.loc[i, "Cycle ID"])

    #3. Cycle completeness
    df_complete = df_non_neg_offset[df_non_neg_offset["cycle_compl"] >= 0.4]
    counts = dict(df_complete["PCOS"].value_counts())
    counts_users = dict(df_complete["User ID"].value_counts())
    logger.info(f"The complete cycles: {counts}")
    logger.info(f"Number of Users: {counts_users}")
    logger.info("================Cycle filtering ended==================")

    return df_complete

def clean_expanded(vals):
    y = [i for i in vals if i != ""]
    cleaned_vals = []
    for i in y:
        if i == "nan":
            cleaned_vals.append(np.nan)
        else:
            cleaned_vals.append(float(i))
    
    return cleaned_vals