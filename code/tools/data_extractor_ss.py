#!python
#!/usr/bin/env python3

#############################################################################################
#The “data_extractor.py” script - this version use z-normalization (standard scaling)
#This script extracts the cycle level features of the data. To make it faster, horizontal scaling
#usimg multiprocessing is employed for the task. 
#The first part of the script will tries to locate missing days that are not mre than 10 at a
#single instance and then gets interpolated results for the missings days. 
#The second aspect of the script then compares each cycle for a user with the model cycles.
#This is done first by z-normalizing the cycles and then performaing dynamic time warping on the
#on bothe the model and the cycle. The nadirs, peaks and other related cycle level data are 
#then calculated from dtw results.
#The last part of the script calculates the length of the curve, the length of the data and 
#then calculates the dives the length of the curve by the length of the data.
# The last part is the entry point into the clas and handle the parallelization of the script
#############################################################################################

from dtaidistance import dtw
from multiprocess import Pool
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tqdm import tqdm

import tools.tools as tools

class Extract:
    def __init__(self, users, group_temp, grouped):
        self.users = users
        self.group_temp = group_temp
        self. grouped = grouped

    def actual_day(self, user, cycle):
        group_temp = self.group_temp
        #Computing the actual recording day while considering missing temperature days
        cycle_temp = group_temp.get_group((user, cycle)).sort_values("Date").reset_index(drop=True)#the temperature values of the cycle
        cycle_temp["Date"] = pd.to_datetime(cycle_temp["Date"])
        cycle_temp = cycle_temp.drop_duplicates(subset="Date", keep = "first").set_index("Date")#this deals with cycles with duplicate dates
        start = str(cycle_temp.index.min()).split(" ")[0]
        end = str(cycle_temp.index.max()).split(" ")[0]

        df_reindexed = pd.DataFrame(cycle_temp.reindex(pd.date_range(start, end)).isnull().all(1), columns=["Missing_Day"])
        temperature_vals = pd.merge(cycle_temp,  df_reindexed, left_on=cycle_temp.index, right_on= df_reindexed.index, how = "outer", sort = True)
        
        temperature_vals["Missing_length"] = 0

        for i in (temperature_vals[temperature_vals["Missing_Day"] == True].index):
            last_day_before_miss = temperature_vals.iloc[0:i][temperature_vals.iloc[0:i]["Missing_Day"] == False].tail(1).index
            first_day_after_miss = temperature_vals.iloc[i:][temperature_vals.iloc[i:]["Missing_Day"] == False].head(1).index
            
            temperature_vals.loc[i, "Missing_length"] = first_day_after_miss - last_day_before_miss - 1
            
        try:    
            missed = temperature_vals[temperature_vals["Missing_length"] > 10].head(1).index.values[0] #if there are more than 10 missing days
            temperature_vals = temperature_vals.iloc[0:missed] #drop all recordings after 10 missing days
        except IndexError:
            temperature_vals = temperature_vals #otherwise keep all temperatures with the missing dates
        
        temperature_vals["Mean_Temp"] = temperature_vals["Mean_Temp"].interpolate(method = "linear", limit_direction = "forward")
        temperature_vals["Cycle ID"] = temperature_vals["Cycle ID"].fillna(method = "pad") #fill the missing cycle IDs
        temperature_vals["User ID"] = temperature_vals["User ID"].fillna(method = "pad") #fill the missing user IDs
            
        return temperature_vals


    def slope_nadir_peak(self, user, user_cycles, cycle, temp_vals):
        model_cycle = tools.load_model_cycle()['model']#the model cycle 
        keep = user_cycles[user_cycles.index == cycle]
        date_dur = keep["Data_Dur"].values[0]#get the data duration of the cycle
        offset = int(keep["Offset"])#get the offset of the cycle
        Date_D = keep["Date_Diff"].values#get the cycle length of the cycle
        ovul = user_cycles[user_cycles.index == cycle.lower()]["Ovulation Day"]#get the ovulation date of the cycle
        PCOS = keep["PCOS"].values[0]
        
        if Date_D == "Indeterminate Last Cycle":
            Date_Diff = ""#the last cycle
        else:
            Date_Diff = int(Date_D) #all cycles asides the last cycle    

        if str(ovul.values) == "[nan]":
            ovulation = ""#ovulation dates not found
        else:
            ovulation = int(ovul) #ovulation dates found

        cycle_temp = temp_vals#the temperature data frame of the cycle

        #Smoothing the temperatures    
        try:
            cycle_temp["Smooth_Temp"] = savgol_filter(cycle_temp["Mean_Temp"], 10, 2)#smoothing the temperature values across 10 days and polynomial order 2
        except ValueError:
            cycle_temp["Smooth_Temp"] = savgol_filter(cycle_temp["Mean_Temp"], len(cycle_temp), 2)#if the number of days is not up to 10, we smooth across the entire data

        
        #Computing Nadirs and Peaks with "Dynamic Time Warping" 
        temps = list(cycle_temp["Mean_Temp"])#wrapping the cycle temperatures into a list
        #model_cycle = load_model_cyle()['model']#the model cycle    
        smooth_temps = list(cycle_temp["Smooth_Temp"])#the smoothed cycle temperatures
        
        #standardizing the smooth values    
        scalerStandard = StandardScaler()
        Standard_model_cycle = scalerStandard.fit_transform(np.array(model_cycle).reshape(-1, 1))
        Standard_smooth_temps = scalerStandard.fit_transform(np.array(smooth_temps).reshape(-1, 1))
        
        #New dtw method    
        Standard_path = dtw.warping_path(Standard_model_cycle, Standard_smooth_temps)
        Standard_distance = "{0:.2f}".format(dtw.distance(Standard_model_cycle, Standard_smooth_temps))    
        
        #Getting the length of warping line and warping amount
        path_x_axis = [x[0] for x in Standard_path]
        path_y_axis = [x[1] for x in Standard_path]
        path_length = tools.length_of_line(path_y_axis, path_x_axis)
        warp_deg = tools.warp_degree(path_y_axis, path_x_axis)
        
        #Computing nadir and peak using DTW and standardized temperature values
        Standard_nadir_temp_list = [Standard_smooth_temps[mapy] for mapx, mapy in Standard_path if mapx == 4]
        Standard_nadir_temp = min([Standard_smooth_temps[mapy] for mapx, mapy in  Standard_path if mapx == 4])
        Standard_nadir_position = [i for i, e in enumerate(Standard_nadir_temp_list) if e == Standard_nadir_temp][-1]

        Standard_nadir_day_list = [[mapx, mapy] for mapx, mapy in Standard_path if mapx == 4]
        Standard_nadir_day = Standard_nadir_day_list[Standard_nadir_position][1]
        Standard_nadir_temp_actual = smooth_temps[Standard_nadir_day]
        
        Standard_peak_temp_list = [Standard_smooth_temps[mapy] for mapx, mapy in Standard_path if mapx == 15]
        Standard_peak_temp = max([Standard_smooth_temps[mapy] for mapx, mapy in Standard_path if mapx == 15])
        Standard_peak_position = [i for i, e in enumerate(Standard_peak_temp_list) if e == Standard_peak_temp][0]

        Standard_peak_day_list = [[mapx, mapy] for mapx, mapy in Standard_path if mapx == 15]
        Standard_peak_day = Standard_peak_day_list[Standard_peak_position][1]
        Standard_peak_temp_actual = smooth_temps[Standard_peak_day]
        
        #Nadir and Peak Validity Check
        temp_diffs = [smooth_temps[i+1] - smooth_temps[i] for i in range(len(smooth_temps)-1)]
        lower_curve_list = temp_diffs[:Standard_nadir_day]
        top_curve_list = temp_diffs[Standard_peak_day:]
        
        nadir_valid = any(i < 0 for i in lower_curve_list)
        peak_valid = any(i < 0 for i in top_curve_list)
    
        #Time from nadir to peak using Standard Scaling
        Standard_nadir_to_peak = Standard_peak_day - Standard_nadir_day
        
        #Difference between lowest and highest temperature using Standard Scaling
        Standard_low_to_high_temp = Standard_peak_temp_actual - Standard_nadir_temp_actual
        
        #we create a dictionary of the results for each cycle
        data = {"User":user, "Cycle":cycle, "Temps":temps, "Smooth_Temp":smooth_temps, "Initial_Cycle_Range":date_dur, 
                "Ovulation Day":ovulation, "Date_Diff":Date_Diff, "Offset":offset, "PCOS":PCOS,

                "Standard_model_cycle":Standard_model_cycle, "Standard_smooth_temps":Standard_smooth_temps, 
                "Standard_distance":Standard_distance, "Standard_path":Standard_path, 
                "Standard_nadir_day":Standard_nadir_day, "Standard_peak_day":Standard_peak_day, 
                "Standard_nadir_temp":Standard_nadir_temp, "Standard_peak_temp":Standard_peak_temp,
                "Standard_nadir_temp_actual":Standard_nadir_temp_actual, "Standard_peak_temp_actual":Standard_peak_temp_actual,
                "Standard_nadir_to_peak":Standard_nadir_to_peak, "Standard_low_to_high_temp":Standard_low_to_high_temp,
                "nadir_valid":nadir_valid, "peak_valid":peak_valid,
                "path_length":path_length, "warp_degree":warp_deg
            }
        
        return data


    def curve_by_length(self, nad_and_peak):
        offset = nad_and_peak["Offset"]
        yaxis = nad_and_peak["Smooth_Temp"]
        xaxis = [k + offset for k in range(len(yaxis))]

        curve_length = tools.length_of_line(yaxis, xaxis)
        data_length = len(yaxis)
        curve_by_data = curve_length/(data_length - 1)
        
        distance = {"Curve_Length":curve_length, "Data_Length":data_length, "Curve_by_Data":curve_by_data}
        
        return distance


    def independent_variables(self, user):
        grouped = self.grouped
        user_cycles = grouped.xs(user, level = 0).sort_values("Date_x")#get all users cycles and sort them by date
        user_cycles_list = list(user_cycles.index) #wrap the cycles into a list
        
        results = []
        
        for cycle in user_cycles_list: #for each cycle

            ################Actual Cycle Days##################
            actual_temp_vals = self.actual_day(user, cycle)
            days = {"Days":list(actual_temp_vals.index)}
            
            ##
            if len(days["Days"]) > 9: #This has to be done because removing missing days will reduce some cycle lengths
                missing_days = list(actual_temp_vals[actual_temp_vals["Missing_Day"] == True]["Mean_Temp"].index)
                missing_days_temps = list(actual_temp_vals[actual_temp_vals["Missing_Day"] == True]["Mean_Temp"])
            
                missing = {"Missing_Days":missing_days, "Missing_Days_Temp":missing_days_temps}
                
                ################Nadir and Peak####################
                nad_and_peak = self.slope_nadir_peak(user, user_cycles, cycle, actual_temp_vals)
            
                ################Length of the Curve###############
                curve_distance = self.curve_by_length(nad_and_peak)
            
            
                cycle_est = dict(nad_and_peak, **curve_distance, **days, **missing)
                #cycle_est = dict(nad_and_peak, **days, **missing)
                
                results.append(cycle_est)
                #print(days)
        return results


    def compute_mv(self):
        users = self.users
        max_pool = 50
        #self.independent_variables("06Up8r5PeU")
        with Pool(max_pool) as p:
            pool_outputs = list(tqdm(p.imap(self.independent_variables, users), total=len(users)))
        return pool_outputs