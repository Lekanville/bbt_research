import json
import numpy as np
import pandas as pd

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

#This algorithm takes outliers for standardized data
def trimming_for_outliers(df):
    #Trimming value for peak day
    peak_day_mean = float("{0:.2f}".format(np.mean(df["Standard_peak_day"].values))) #the mean of the peak days
    peak_day_std = float("{0:.2f}".format(np.std(df["Standard_peak_day"].values))) #the standard deviation of the peak days
    peak_day_trim = peak_day_mean+(3*peak_day_std) #trim peak day upto 3 times the std after mean

    #Trimming value for Nadir temperature
    nadir_temp_mean = float("{0:.2f}".format(np.mean(df["Standard_nadir_temp_actual"].values))) #mean of the nadir temps
    nadir_temp_std = float("{0:.2f}".format(np.std(df["Standard_nadir_temp_actual"].values))) #std of the nadir temps
    nadir_temp_trim_left = nadir_temp_mean-(3*nadir_temp_std) #trim nadir temps upto 3 times std before the mean
    nadir_temp_trim_right = nadir_temp_mean+(3*nadir_temp_std) #trim nadir temps upto 3 times std after the mean

    df = df[(df["Standard_nadir_day"] <= 50) & #Trim out cycles with nadirs greater than 50 
                    (df["Standard_peak_day"] <= peak_day_trim) & #Trim out cycles with peaks greater than trim 
                    (df["Standard_nadir_day"] != df["Standard_peak_day"]) & #Trim out cycles with nadirs 
                                                                                    #equalling peaks. This is peculiar
                                                                                    #of cycles that are basically 
                                                                                    #descends
                    (df["Standard_nadir_temp_actual"] > nadir_temp_trim_left) &
                    (df["Standard_nadir_temp_actual"] < nadir_temp_trim_right) &
                    (df["Standard_low_to_high_temp"] > 0) & #Trim out cycles with a negative high and low temp.
                                                                #difference. This is peculiar of cycles that a near 
                                                                #flat temperature reading at the nadir and peak positions
                    ~(df["Date_Diff"].isnull())& #remove last cycles most of which are largely incomplete
                    (df["Data_Length"] < 101) #remove cycles with more than 100 days
                   ]

    return df

#This algorithm takes outliers for normalized data
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

#editing wrong inputs
def edit_wrong_inputs(df):
    df_to_edit = df.copy()
    for i in range(len(df)):
        if df_to_edit.loc[i, "User ID"] == "YhfYIQ3a5Z":
            df_to_edit.iloc[i, 29] = 164
            
        if df_to_edit.loc[i, "User ID"] == "3JnGCssgii":
            df_to_edit.iloc[i, 29] = 162.56
    
    return df_to_edit

#getting the units of measurements for each user by searching the various units columns
def get_units(df):
    df_funct = df.copy()
    df_funct["Weight_Unit"] = ""
    df_funct["Height_Unit"] = ""
    df_funct["Hip_Unit"] = ""
    df_funct["Waist_Unit"] = ""
    df_funct["Bust_Cir_Unit"] = ""
    
    #This get the units of the weight for each woman by checking the 4 columns (Stones, Kilograms, Pounds 
    #and those not giving their weights) and putting the value in the weight unit column
    for i in range(len(df_funct)):
        if "Stones" in list(df_funct.iloc[i,1:5]):
            df_funct.loc[i,"Weight_Unit"] = "Stones"
        elif "Pounds (US)" in list(df_funct.iloc[i,1:5]):
            df_funct.loc[i,"Weight_Unit"] = "Pounds (US)"
        elif "Kilos" in list(df_funct.iloc[i,1:5]):
            df_funct.loc[i,"Weight_Unit"] = "Kilos"
        else:
            df_funct.loc[i,"Weight_Unit"] = "None"
            
    #This get the units of the height for each woman by checking the 3 columns (Feets and Inches, Centimeters 
    #and those not giving their heights) and putting the value in the height unit column
        if "Feet and inches" in list(df_funct.iloc[i,24:27]):
            df_funct.loc[i,"Height_Unit"] = "Inches"
        elif "Centimeters" in list(df_funct.iloc[i,24:27]):
            df_funct.loc[i,"Height_Unit"] = "Centimeters"
        else:
            df_funct.loc[i,"Height_Unit"] = "None"
            
    #This get the units of the hip size for each woman by checking the 3 columns (Inches, Centimeters 
    #and those not giving their hip sizes) and putting the value in the hip unit column
        if "Inches" in list(df_funct.iloc[i,9:12]):
            df_funct.loc[i,"Hip_Unit"] = "Inches"
        elif "Centimeters" in list(df_funct.iloc[i,9:12]):
            df_funct.loc[i,"Hip_Unit"] = "Centimeters"
        else:
            df_funct.loc[i,"Hip_Unit"] = "None"
            
    #This get the units of the waist size for each woman by checking the 3 columns (Inches, Centimeters 
    #and those not giving their hip sizes) and putting the value in the waist unit column
        if "Inches" in list(df_funct.iloc[i,13:16]):
            df_funct.loc[i,"Waist_Unit"] = "Inches"
        elif "Centimeters" in list(df_funct.iloc[i,13:16]):
            df_funct.loc[i,"Waist_Unit"] = "Centimeters"
        else:
            df_funct.loc[i,"Waist_Unit"] = "None"
            
    #This get the units of the waist size for each woman by checking the 3 columns (Inches, Centimeters 
    #and those not giving their hip sizes) and putting the value in the waist unit column    
        if "Inches" in list(df_funct.iloc[i,20:23]):
            df_funct.loc[i,"Bust_Cir_Unit"] = "Inches"
        elif "Centimeters" in list(df_funct.iloc[i,20:23]):
            df_funct.loc[i,"Bust_Cir_Unit"] = "Centimeters"
        else:
            df_funct.loc[i,"Bust_Cir_Unit"] = "None"

    return df_funct

#getting the actual values for each user by searching the various value columns
def get_values(df):
    df_w_u = df.copy()
    
    df_w_u["Weight_Values"] = ""
    df_w_u["Height_Values"] = ""
    df_w_u["Hip_Values"] = ""
    df_w_u["Waist_Values"] = ""
    df_w_u["Bust_Cir_Values"] = ""
    
    for i in range(len(df_w_u)):
        #1. Getting the weight values
        #Getting the weight values for the Stones and Pounds. Column 5 is for stones and 6 is for pounds
        if (str(df_w_u.iloc[i,5]) not in ["nan", "Cigarettes"]) & (df_w_u.loc[i,"Weight_Unit"] == "Stones"):
            x = df_w_u.iloc[i,5]
            y = 0
            if str(df_w_u.iloc[i,6]) != "nan":
                y = df_w_u.iloc[i,6]
            y = y*0.0714286
            z = x+y
            df_w_u.loc[i,"Weight_Values"] = z
            
        #Getting the weight values for Kilograms. Column 7 is for Kilograms
        if (str(df_w_u.iloc[i,7]) != "nan") & (df_w_u.loc[i,"Weight_Unit"] == "Kilos"):
            df_w_u.loc[i,"Weight_Values"] = df_w_u.iloc[i,7]
            
        #Getting the weight values for Pounds (US). Column 8 is for Pounds (US)
        if (str(df_w_u.iloc[i,8]) != "nan") & (df_w_u.loc[i,"Weight_Unit"] == "Pounds (US)"):
            df_w_u.loc[i,"Weight_Values"] = df_w_u.iloc[i,8]     
            
            
        #2. Getting the height values
        #Getting the height values for the Feet and Inches. Column 27 is for stones and 28 is for pounds
        if (str(df_w_u.iloc[i,27]) != "nan") & (df_w_u.loc[i,"Height_Unit"] == "Inches"):
            x = df_w_u.iloc[i,27] * 12
            y = 0
            if str(df_w_u.iloc[i,28]) != "nan":
                y = df_w_u.iloc[i,28]
            z = x+y
            df_w_u.loc[i,"Height_Values"] = z
            
        #Getting the height values for Centimeters. Column 29 is for Centimeters
        if (str(df_w_u.iloc[i,29]) != "nan") & (df_w_u.loc[i,"Height_Unit"] == "Centimeters"):
            df_w_u.loc[i,"Height_Values"] = df_w_u.iloc[i,29]
            
            
        #3. Getting the hip values
        if (str(df_w_u.iloc[i,12]) != "nan"):
            df_w_u.loc[i,"Hip_Values"] = df_w_u.iloc[i,12]     
            
        #4. Getting the waist values
        if (str(df_w_u.iloc[i,19]) != "nan"):
            df_w_u.loc[i,"Waist_Values"] = df_w_u.iloc[i,19]
            
        #5. Getting the burst circumference values
        if (str(df_w_u.iloc[i,23]) != "nan"):
            df_w_u.loc[i,"Bust_Cir_Values"] = df_w_u.iloc[i,23]
            
    return df_w_u

#standardizing the values
def get_standard_values(df):
    df_funct = df.copy()
    df_funct["Weight(KG)"] = ""
    df_funct["Height(m)"] = ""
    df_funct["Waist(Inches)"] = ""
    df_funct["Hip(Inches)"] = ""
    df_funct["Bust_Cir(Inches)"] = ""

    
    for i in range(len(df_funct)):
        #standardizing the weights, Stones and Pounds are converted to KG
        if (df_funct.loc[i, "Weight_Unit"] == "Stones") & (df_funct.loc[i, "Weight_Values"] != ""):
            df_funct.loc[i, "Weight(KG)"] = "{0:.1f}".format(df_funct.loc[i, "Weight_Values"] * 6.35029)
        elif (df_funct.loc[i, "Weight_Unit"] == "Pounds (US)") & (df_funct.loc[i, "Weight_Values"] != ''):
            df_funct.loc[i, "Weight(KG)"] = "{0:.1f}".format(df_funct.loc[i, "Weight_Values"] * 0.453592)
        elif (df_funct.loc[i, "Weight_Unit"] == "Kilos") & (df_funct.loc[i, "Weight_Values"] != ''):
            df_funct.loc[i, "Weight(KG)"] = "{0:.1f}".format(df_funct.loc[i, "Weight_Values"])
            
        #standardizing the heights, Inches and Centimeters are converted to Meters
        if (df_funct.loc[i, "Height_Unit"] == "Inches") & (df_funct.loc[i, "Height_Values"] != ""):
            df_funct.loc[i, "Height(m)"] = "{0:.2f}".format(df_funct.loc[i, "Height_Values"] * 0.0254)
        elif (df_funct.loc[i, "Height_Unit"] == "Centimeters") & (df_funct.loc[i, "Height_Values"] != ""):
            df_funct.loc[i, "Height(m)"] = "{0:.2f}".format(df_funct.loc[i, "Height_Values"] * 0.01)
            
        #standardizing the hip sizes, Centimeters converted to Inches
        if (df_funct.loc[i, "Hip_Unit"] == "Inches") & (df_funct.loc[i, "Hip_Values"] != ""):
            df_funct.loc[i, "Hip(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Hip_Values"])
        elif (df_funct.loc[i, "Hip_Unit"] == "Centimeters") & (df_funct.loc[i, "Hip_Values"] != ""):
            df_funct.loc[i, "Hip(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Hip_Values"] * 0.393701)
        
        #standardizing the waist sizes, Centimeters converted to Inches
        if (df_funct.loc[i, "Waist_Unit"] == "Inches") & (df_funct.loc[i, "Waist_Values"] != ""):
            df_funct.loc[i, "Waist(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Waist_Values"])
        elif (df_funct.loc[i, "Waist_Unit"] == "Centimeters") & (df_funct.loc[i, "Waist_Values"] != ""):
            df_funct.loc[i, "Waist(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Waist_Values"] * 0.393701)        
        
        #standardizing the  sizes, Centimeters converted to Inches
        if (df_funct.loc[i, "Bust_Cir_Unit"] == "Inches") & (df_funct.loc[i, "Bust_Cir_Values"] != ""):
            df_funct.loc[i, "Bust_Cir(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Bust_Cir_Values"])
        elif (df_funct.loc[i, "Bust_Cir_Unit"] == "Centimeters") & (df_funct.loc[i, "Bust_Cir_Values"] != ""):
            df_funct.loc[i, "Bust_Cir(Inches)"] = "{0:.2f}".format(df_funct.loc[i, "Bust_Cir_Values"] * 0.393701)
              
    return df_funct

#getting the BMI
def get_bmi(df):
    df_funct = df.copy()
    df_funct["BMI"] = ""
    
    for i in range(len(df_funct)):
        if (df_funct.loc[i, "Weight(KG)"] != "" ) & (df_funct.loc[i, "Height(m)"] != ""):
            weight = float(df_funct.loc[i, "Weight(KG)"])
            height = float(df_funct.loc[i, "Height(m)"])
            df_funct.loc[i, "BMI"] = "{0:.1f}".format(weight/height**2)
    return df_funct.iloc[:, np.r_[0, 11, 17]]

#imputation for missing BMIs
def missing_bmi_imputation(df):
    df_funct = df.copy()
    
    bmis_0 = df_funct[df_funct['PCOS'] == 0]["BMI"].values
    bmis_0 = [float(i) for i in bmis_0 if i != ""]
    
    bmis_1 = df_funct[df_funct['PCOS'] == 1]["BMI"].values
    bmis_1 = [float(i) for i in bmis_1 if i != ""]
    
    median_bmi_0 = np.median(bmis_0)
    median_bmi_1 = np.median(bmis_1)
    
    print(median_bmi_0)
    print(median_bmi_1)

    for i in range(len(df_funct)):
        if (df_funct.loc[i, "BMI"] == "") & (df_funct.loc[i, "PCOS"] == 0):
            df_funct.loc[i, "BMI"] = median_bmi_0
            
        if (df_funct.loc[i, "BMI"] == "") & (df_funct.loc[i, "PCOS"] == 1):
            df_funct.loc[i, "BMI"] = median_bmi_1        
        
    df_funct['BMI'] = df_funct['BMI'].apply(pd.to_numeric, errors='coerce')
    return df_funct