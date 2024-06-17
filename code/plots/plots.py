#for platting varous types of data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from classes.classes import Frames
import tools.tools as tools

def fig_layout():
    return plt.figure()

#A single cycle. Use the features dataset
def plot_single(cycle, data):
    #use the processed temperatures from features_dtw_SS
    chunks = pd.read_csv(data, chunksize=5000)
    features = pd.concat(chunk_temperatures)

    offset = features[features["Cycle"] == cycle]["Offset"]
    end = features[features["Cycle"] == cycle]["Next Cycle Difference"].values[0]

    actual_str = features[features["Cycle"] == cycle]["Temps"].values[0]
    actual_split = actual_str.replace("[", "").replace("]", "").split(", ")
    actual_temps = [float(x) for x in actual_split]

    smooth_str = features[features["Cycle"] == cycle]["Smooth_Temp"].values[0]
    smooth_split = smooth_str.replace("[", "").replace("]", "").split(", ")
    smooth_temps = [float(x) for x in smooth_split]

    xaxis = list(range(len(smooth_temps)))
    xaxis = [i+offset for i in xaxis]

    fig = plt.figure()
    ax = fig.add_axes([0,0, 1, 1])
    ax.plot(xaxis, actual_temps, "o", label = "Temperature")
    ax.plot(xaxis, smooth_temps, "r", label = "Smooth")


    missing_temps_str = features[features["Cycle"] == cycle]["Missing_Days_Temp"].values[0]
    missing_temps_split = missing_temps_str.replace("[", "").replace("]", "").split(", ")

    if missing_temps_split != ['']:
        missing_temps = [float(x) for x in missing_temps_split]

        missing_days_str = features[features["Cycle"] == cycle]["Missing_Days"].values[0]
        missing_days_split = missing_days_str.replace("[", "").replace("]", "").split(", ")
        missing_days = [float(i)+offset for i in missing_days_split]

        ax.plot(missing_days, missing_temps, "o", color = "red", label = "Interpolated Value")

    ax.axvline(x = 0, color = "b", label = "Indicated Start Day")
    ax.axvline(x = end, color = "r", label = "Indicated End Day")

    #plt.xlim(0, end+1)
    ax.set_xlabel('Cycle Day')
    ax.set_ylabel('Temp(°C)')
    ax.set_title('Mean and Smooth Mean Cycle Length')
    ax.legend(loc=0)

    plt.show()

#All cycles for a user. Use the features dataset
def plot_user_cycles(u, data):
    #use the processed temperatures from features_dtw_SS
    chunks = pd.read_csv(data, chunksize=5000)
    features = pd.concat(chunks)
    new_user_cycles = features.groupby("User")

    user_cycles = new_user_cycles.get_group(u).set_index("Cycle")
    len_cycles = len(user_cycles)
    
    fig = fig_layout()
    fig, ax_1 = plt.subplots(figsize=(6*len_cycles, 5), nrows=1, ncols=len_cycles)
    j = 0
    
    for c in user_cycles.index:
        
        offset = user_cycles[user_cycles.index == c]["Offset"]
        end = user_cycles[user_cycles.index == c]["Next Cycle Difference"].values[0]

        actual_str = user_cycles[user_cycles.index == c]["Temps"].values[0]
        actual_split = actual_str.replace("[", "").replace("]", "").split(", ")
        actual_temps = [float(x) for x in actual_split]

        smooth_str = user_cycles[user_cycles.index == c]["Smooth_Temp"].values[0]
        smooth_split = smooth_str.replace("[", "").replace("]", "").split(", ")
        smooth_temps = [float(x) for x in smooth_split]


        xaxis = list(range(len(smooth_temps)))
        xaxis = [i+offset for i in xaxis]


        ax_1[j].plot(xaxis, actual_temps, "o", label = "Temperature")
        ax_1[j].plot(xaxis, smooth_temps, "r", label = "Smooth")



        missing_temps_str = user_cycles[user_cycles.index == c]["Missing_Days_Temp"].values[0]
        missing_temps_split = missing_temps_str.replace("[", "").replace("]", "").split(", ")

        if missing_temps_split != ['']:
            missing_temps = [float(x) for x in missing_temps_split]

            missing_days_str = user_cycles[user_cycles.index == c]["Missing_Days"].values[0]
            missing_days_split = missing_days_str.replace("[", "").replace("]", "").split(", ")
            missing_days = [float(i)+offset for i in missing_days_split]

            ax_1[j].plot(missing_days, missing_temps, "o", color = "red", label = "Interpolated Value")

        ax_1[j].axvline(x = 0, color = "b", label = "Indicated Start Day")
        ax_1[j].axvline(x = end, color = "r", label = "Indicated End Day")

        #plt.xlim(0, end+1)
        ax_1[j].set_xlabel('Cycle Day')
        ax_1[j].set_ylabel('Temp(°C)')
        ax_1[j].set_title('Mean and Smooth Mean Cycle Length')
        ax_1[j].legend(loc=0)

        #plt.show()
        plt.tight_layout()
        
        j+=1
        
        #plt.savefig(u+"_"+'.png')


#All cycles for a user. Use the features dataset
def plot_nadir_peak_StandardScaler(u, data):
    #use the processed temperatures from features_dtw_SS
    chunks = pd.read_csv(data, chunksize=5000)
    features = pd.concat(chunks)
    new_user_cycles = features.groupby("User")

    user_cycles = new_user_cycles.get_group(u).set_index("Cycle")
    len_cycles = len(user_cycles)
    
    fig = fig_layout()
    fig, ax = plt.subplots(figsize=(7*len_cycles, 5), nrows=1, ncols=len_cycles)
    fig, ax_1 = plt.subplots(figsize=(6*len_cycles, 5), nrows=1, ncols=len_cycles)
    j = 0
    k = 0

    for c in user_cycles.index:
        model_cycle_array = user_cycles[user_cycles.index == c]["Standard_model_cycle"]
        Standard_model_cycle = list(map(float, model_cycle_array[0].replace("[", "").replace("]", "").split("\n ")))
        
        Standard_smooth_array = user_cycles[user_cycles.index == c]["Standard_smooth_temps"]
        Standard_smooth_temps = list(map(float, Standard_smooth_array[0].replace("[", "").replace("]", "").split("\n ")))
        
        Standard_path = user_cycles[user_cycles.index == c]["Standard_path"].values[0]
        Standard_path = list(map(int, Standard_path.replace("[", "").replace("]", "").replace("(", "").replace(")", "").split(", ")))
        Standard_path = [(Standard_path[i], Standard_path[i+1]) for i,j in enumerate(Standard_path) if i%2 == 0 ]
        
        Standard_distance = str(user_cycles[user_cycles.index == c]["Standard_distance"].values[0])
        Curve_Length =  str("{0:.2f}".format(user_cycles[user_cycles.index == c]["Curve_Length"].values[0]))
        
        lower_day = user_cycles[user_cycles.index == c]["Standard_nadir_day"].values[0]
        lower_smooth = float(user_cycles[user_cycles.index == c]["Standard_nadir_temp"].values[0].replace("[", "").replace("]", ""))
        
        upper_day = user_cycles[user_cycles.index == c]["Standard_peak_day"].values[0]
        upper_smooth = float(user_cycles[user_cycles.index == c]["Standard_peak_temp"].values[0].replace("[", "").replace("]", ""))
        
        for [map_x, map_y] in Standard_path:
            ax[j].plot([map_x, map_y], [Standard_model_cycle[map_x], Standard_smooth_temps[map_y]], "--k", linewidth=1, alpha = 0.5)
        
        ax[j].plot(Standard_smooth_temps, "-ro", label = "Standard Cycle Temp", linewidth=2, markersize = 5, markerfacecolor = "skyblue", markeredgecolor = "skyblue")
        ax[j].plot(Standard_model_cycle, "-bo", label = "Standard Model Temp", linewidth=2, markersize =5, markerfacecolor = "lightcoral", markeredgecolor = "lightcoral")
        
        ax[j].plot(lower_day, lower_smooth, label = "Standard_Nadir_Smooth", marker="o", markersize=20,
            markerfacecolor="yellow", markeredgecolor="green",  markeredgewidth=2, alpha=0.5)

        ax[j].plot(upper_day, upper_smooth, label = "Standard_Peak_Smooth", marker="o", markersize=20,
            markerfacecolor="red", markeredgecolor="green",  markeredgewidth=2, alpha=0.5)

        ax[j].set_xlabel('Cycle Day')
        ax[j].set_ylabel(u+' Temp(°C)')
        ax[j].set_title(c+"\n Dtw Distance:"+ Standard_distance + " Curve_Length:"+Curve_Length)
        ax[j].legend(loc=0)
        plt.tight_layout()
        #j+=1
        
        plt.savefig(u+'.png')
        
        temps = list(map(float, user_cycles[user_cycles.index == c]["Smooth_Temp"].values[0].replace("[", "").replace("]", "").split(", ")))
        Days = list(map(float, user_cycles[user_cycles.index == c]["Days"].values[0].replace("[", "").replace("]", "").split(", ")))
        
        lower_smooth_actual = user_cycles[user_cycles.index == c]["Standard_nadir_temp_actual"].values[0]
        upper_smooth_actual = user_cycles[user_cycles.index == c]["Standard_peak_temp_actual"].values[0]
        
        ax_1[j].plot(Days,temps, "-ro", label = "Standard Cycle Temp", linewidth=2, markersize = 5, markerfacecolor = "skyblue", markeredgecolor = "skyblue")        
        
        ax_1[j].plot(lower_day, lower_smooth_actual, label = "Standard_Nadir_Smooth_Actual", marker="o", markersize=20,
            markerfacecolor="yellow", markeredgecolor="green",  markeredgewidth=2, alpha=0.5)

        ax_1[j].plot(upper_day, upper_smooth_actual, label = "Standard_Peak_Smooth_Actual", marker="o", markersize=20,
            markerfacecolor="red", markeredgecolor="green",  markeredgewidth=2, alpha=0.5)
        
        ax_1[j].set_xlabel('Cycle Day')
        ax_1[j].set_ylabel(u+' Temp(°C)')
        ax_1[j].set_title(c+"\n Dtw Distance:"+ Standard_distance + " Curve_Length:"+Curve_Length)
        ax_1[j].legend(loc=0)
        plt.tight_layout()
        
        j+=1


#Plot all cycles for various users in a embedded list eg [{"user":"iiii","ref_cycles":"jjjj"}, {"user":"xxxx","ref_cycles":"yyyy"}]
def plot_refs(ref_users, data):
    #use the processed temperatures from features_dtw_SS
    chunks = pd.read_csv(data, chunksize=5000)
    features = pd.concat(chunk_temperatures)

    for i in range(len(ref_users)):
        user_cycles = ref_users[i]['ref_cycles']
        len_cycles = len(user_cycles)

        fig = fig_layout()
        fig, ax_1 = plt.subplots(figsize=(6*len_cycles, 5), nrows=1, ncols=len_cycles)
        j = 0

        for c in user_cycles:
            offset = features[features["Cycle"] == c]["Offset"]
            end = features[features["Cycle"] == c]["Next Cycle Difference"].values[0]

            actual_str = features[features["Cycle"] == c]["Temps"].values[0]
            actual_split = actual_str.replace("[", "").replace("]", "").split(", ")
            actual_temps = [float(x) for x in actual_split]

            smooth_str = features[features["Cycle"] == c]["Smooth_Temp"].values[0]
            smooth_split = smooth_str.replace("[", "").replace("]", "").split(", ")
            smooth_temps = [float(x) for x in smooth_split]


            xaxis = list(range(len(smooth_temps)))
            xaxis = [i+offset for i in xaxis]


            ax_1[j].plot(xaxis, actual_temps, "o", label = "Temperature")
            ax_1[j].plot(xaxis, smooth_temps, "r", label = "Smooth")



            missing_temps_str = features[features["Cycle"] == c]["Missing_Days_Temp"].values[0]
            missing_temps_split = missing_temps_str.replace("[", "").replace("]", "").split(", ")

            if missing_temps_split != ['']:
                missing_temps = [float(x) for x in missing_temps_split]

                missing_days_str = features[features["Cycle"] == c]["Missing_Days"].values[0]
                missing_days_split = missing_days_str.replace("[", "").replace("]", "").split(", ")
                missing_days = [float(i)+offset for i in missing_days_split]

                ax_1[j].plot(missing_days, missing_temps, "o", color = "red", label = "Interpolated Value")

            ax_1[j].axvline(x = 0, color = "b", label = "Indicated Start Day")
            ax_1[j].axvline(x = end, color = "r", label = "Indicated End Day")

            #plt.xlim(0, end+1)
            ax_1[j].set_xlabel('Cycle Day')
            ax_1[j].set_ylabel('Temp(°C)')
            ax_1[j].set_title('Mean and Smooth Mean Cycle Length')
            ax_1[j].legend(loc=0)

            #plt.show()
            plt.tight_layout()

            j+=1

            #plt.savefig(u+"_"+'.png')


#Plot selected cycles in a list eg ["xxx","xxxx"]
def plot_refs_cycles(ref_users, data):
    #use the processed temperatures from features_dtw_SS
    chunks = pd.read_csv(data, chunksize=5000)
    features = pd.concat(chunks)

    #ref_cycles = ref_users[i]['ref_cycles']
    len_cycles = len(ref_users)

    fig = fig_layout()
    fig, ax_1 = plt.subplots(figsize=(6*len_cycles, 5), nrows=1, ncols=len_cycles)
    j = 0

    for c in ref_users:
        offset = features[features["Cycle"] == c]["Offset"]
        end = features[features["Cycle"] == c]["Next Cycle Difference"].values[0]

        actual_str = features[features["Cycle"] == c]["Temps"].values[0]
        actual_split = actual_str.replace("[", "").replace("]", "").split(", ")
        actual_temps = [float(x) for x in actual_split]

        smooth_str = features[features["Cycle"] == c]["Smooth_Temp"].values[0]
        smooth_split = smooth_str.replace("[", "").replace("]", "").split(", ")
        smooth_temps = [float(x) for x in smooth_split]

        xaxis = list(range(len(smooth_temps)))
        xaxis = [i+offset for i in xaxis]

        ax_1[j].plot(xaxis, actual_temps, "o", label = "Temperature")
        ax_1[j].plot(xaxis, smooth_temps, "r", label = "Smooth", alpha=0.4)

        missing_temps_str = features[features["Cycle"] == c]["Missing_Days_Temp"].values[0]
        missing_temps_split = missing_temps_str.replace("[", "").replace("]", "").split(", ")

        if missing_temps_split != ['']:
            missing_temps = [float(x) for x in missing_temps_split]

            missing_days_str = features[features["Cycle"] == c]["Missing_Days"].values[0]
            missing_days_split = missing_days_str.replace("[", "").replace("]", "").split(", ")
            missing_days = [float(i)+offset for i in missing_days_split]

            ax_1[j].plot(missing_days, missing_temps, "o", color = "red", label = "Interpolated Value")

        ax_1[j].axvline(x = 0, color = "b", label = "Indicated Start Day")
        ax_1[j].axvline(x = end, color = "r", label = "Indicated End Day")

        #plt.xlim(0, end+1)
        ax_1[j].set_xlabel('Cycle Day')
        ax_1[j].set_ylabel('Temp(°C)')
        ax_1[j].set_title('Mean and Smooth Mean Cycle Length')
        ax_1[j].legend(loc=0)

        #plt.show()
        plt.tight_layout()

        j+=1


#Plot actual reference cycles
def plot_refs_cycles_actual(data):
    ref_df = pd.read_csv(data)  

    #use the all model dataset from normal cycles
    ref_df.rename({"Unnamed: 0":"Cycle Position"}, axis = 1, inplace = True)
    model_grouped = ref_df.groupby(["User ID", "Cycle ID"])
    
    #get the user cycle list in the order of their occurence
    the_users = list(ref_df["User ID"].unique())
    model_list = []
    for i in the_users:
        users_temps = ref_df[ref_df["User ID"] == i]
        user_cycles = list(users_temps["Cycle ID"].unique())
        for j in user_cycles:
            the_tuple = tuple([i, j])
            model_list.append(the_tuple)
    ##########################################################
    
    model_list_len = len(model_list)
    
    fig = fig_layout()
    fig, ax_1 = plt.subplots(figsize=(6*model_list_len, 5), nrows=1, ncols=model_list_len)
    j = 0
    
    for c in model_list:
        cycle_df = model_grouped.get_group(c)
        
        df_to_plot = cycle_df[cycle_df["Missing_Day"] == False]

        actual_temps = df_to_plot["Mean_Temp"].to_list()
        #smooth_temps = cycle_df["Smooth_Temp"].to_list()
        cycle_pos = df_to_plot["Cycle Position"].to_list()
        end = cycle_df["Date_Diff"].unique()[0]
        
        ax_1[j].plot(cycle_pos, actual_temps, "o", label = "Temperature")
        #ax_1[j].plot(cycle_pos, smooth_temps, "r", label = "Smooth", alpha=0.4)
        
        missing =  df_to_plot[ df_to_plot["Missing_Day"] == True]
        if len(missing) > 0:
            missing_temps = missing["Mean_Temp"].to_list()
            missing_pos = missing["Cycle Position"].to_list()
            
            ax_1[j].plot(missing_pos, missing_temps, "o", color = "red", label = "Interpolated Value")

          
        ax_1[j].axvline(x = 0, color = "b", label = "Indicated Start Day")
        ax_1[j].axvline(x = end, color = "r", label = "Indicated End Day")
        
        ax_1[j].set_xlabel('Cycle Day')
        ax_1[j].set_ylabel('Temp(°C)')
        ax_1[j].set_title('Cycle Temperatures')
        ax_1[j].legend(loc=0)
        
        plt.tight_layout()

        j+=1



#Plot imputed preprocessed reference cycles
def plot_refs_cycles_imputation(data):
    ref_df = pd.read_csv(data)  

    #use the all model dataset from normal cycles
    ref_df.rename({"Unnamed: 0":"Cycle Position"}, axis = 1, inplace = True)
    model_grouped = ref_df.groupby(["User ID", "Cycle ID"])
    
    #get the user cycle list in the order of their occurence
    the_users = list(ref_df["User ID"].unique())
    model_list = []
    for i in the_users:
        users_temps = ref_df[ref_df["User ID"] == i]
        user_cycles = list(users_temps["Cycle ID"].unique())
        for j in user_cycles:
            the_tuple = tuple([i, j])
            model_list.append(the_tuple)
    ##########################################################
    
    model_list_len = len(model_list)
    
    fig = fig_layout()
    fig, ax_1 = plt.subplots(figsize=(6*model_list_len, 5), nrows=1, ncols=model_list_len)
    j = 0
    
    for c in model_list:
        cycle_df = model_grouped.get_group(c)
        
        actual_temps = cycle_df["Mean_Temp"].to_list()
        #smooth_temps = cycle_df["Smooth_Temp"].to_list()
        cycle_pos = cycle_df["Cycle Position"].to_list()
        end = cycle_df["Date_Diff"].unique()[0]
        
        ax_1[j].plot(cycle_pos, actual_temps, "o", label = "Temperature")
        #ax_1[j].plot(cycle_pos, smooth_temps, "r", label = "Smooth", alpha=0.4)
        
        missing = cycle_df[cycle_df["Missing_Day"] == True]
        if len(missing) > 0:
            missing_temps = missing["Mean_Temp"].to_list()
            missing_pos = missing["Cycle Position"].to_list()
            
            ax_1[j].plot(missing_pos, missing_temps, "o", color = "red", label = "Interpolated Value")

          
        ax_1[j].axvline(x = 0, color = "b", label = "Indicated Start Day")
        ax_1[j].axvline(x = end, color = "r", label = "Indicated End Day")
        
        ax_1[j].set_xlabel('Cycle Day')
        ax_1[j].set_ylabel('Temp(°C)')
        ax_1[j].set_title('Cycle Temperatures with Imputation')
        ax_1[j].legend(loc=0)
        
        plt.tight_layout()

        j+=1


#Plot smoothed preprocessed reference cycles
def plot_refs_cycles_with_smoothing(data):
    ref_df = pd.read_csv(data)  

    #use the all model dataset from normal cycles
    ref_df.rename({"Unnamed: 0":"Cycle Position"}, axis = 1, inplace = True)
    model_grouped = ref_df.groupby(["User ID", "Cycle ID"])
    
    #get the user cycle list in the order of their occurence
    the_users = list(ref_df["User ID"].unique())
    model_list = []
    for i in the_users:
        users_temps = ref_df[ref_df["User ID"] == i]
        user_cycles = list(users_temps["Cycle ID"].unique())
        for j in user_cycles:
            the_tuple = tuple([i, j])
            model_list.append(the_tuple)
    ##########################################################
    
    model_list_len = len(model_list)
    
    fig = fig_layout()
    fig, ax_1 = plt.subplots(figsize=(6*model_list_len, 5), nrows=1, ncols=model_list_len)
    j = 0
    
    for c in model_list:
        cycle_df = model_grouped.get_group(c)
        
        actual_temps = cycle_df["Mean_Temp"].to_list()
        smooth_temps = cycle_df["Smooth_Temp"].to_list()
        cycle_pos = cycle_df["Cycle Position"].to_list()
        end = cycle_df["Date_Diff"].unique()[0]
        
        ax_1[j].plot(cycle_pos, actual_temps, "o", label = "Temperature")
        ax_1[j].plot(cycle_pos, smooth_temps, "r", label = "Smooth", alpha=0.4)
        
        missing = cycle_df[cycle_df["Missing_Day"] == True]
        if len(missing) > 0:
            missing_temps = missing["Mean_Temp"].to_list()
            missing_pos = missing["Cycle Position"].to_list()
            
            ax_1[j].plot(missing_pos, missing_temps, "o", color = "red", label = "Interpolated Value")

          
        ax_1[j].axvline(x = 0, color = "b", label = "Indicated Start Day")
        ax_1[j].axvline(x = end, color = "r", label = "Indicated End Day")
        
        ax_1[j].set_xlabel('Cycle Day')
        ax_1[j].set_ylabel('Temp(°C)')
        ax_1[j].set_title('Smoothing the Cycle Temperatures')
        ax_1[j].legend(loc=0)
        
        plt.tight_layout()

        j+=1


#Plot standardized preprocessed reference cycles
def plot_refs_cycles_standardized(data):
    ref_df = pd.read_csv(data)  

    #use the all model dataset from normal cycles
    ref_df.rename({"Unnamed: 0":"Cycle Position"}, axis = 1, inplace = True)
    model_grouped = ref_df.groupby(["User ID", "Cycle ID"])
    
    #get the user cycle list in the order of their occurence
    the_users = list(ref_df["User ID"].unique())
    model_list = []
    for i in the_users:
        users_temps = ref_df[ref_df["User ID"] == i]
        user_cycles = list(users_temps["Cycle ID"].unique())
        for j in user_cycles:
            the_tuple = tuple([i, j])
            model_list.append(the_tuple)
    ##########################################################
    
    model_list_len = len(model_list)
    
    fig = fig_layout()
    fig, ax_1 = plt.subplots(figsize=(6*model_list_len, 5), nrows=1, ncols=model_list_len)
    j = 0
    
    for c in model_list:
        cycle_df = model_grouped.get_group(c)
        
        #std_mean_temps = cycle_df["Standard_mean_temps"].to_list()
        std_smooth_temps = cycle_df["Standard_smooth_temps"].to_list()
        #cycle_pos = cycle_df["Cycle Position"].to_list()
        cycle_pos = cycle_df["Normal_Positions"].to_list()
        #end = cycle_df["Date_Diff"].unique()[0]
        
        #ax_1[j].plot(cycle_pos, std_mean_temps, "o", label = "Temperature")
        ax_1[j].plot(cycle_pos, std_smooth_temps, "o", label = "Temperature")
        ax_1[j].plot(cycle_pos, std_smooth_temps, "r", label = "Smooth", alpha=0.4)
        
        #missing = cycle_df[cycle_df["Missing_Day"] == True]
        #if len(missing) > 0:
            #missing_temps = missing["Standard_mean_temps"].to_list()
            #missing_pos = missing["Cycle Position"].to_list()
            
            #ax_1[j].plot(missing_pos, missing_temps, "o", color = "red", label = "Interpolated Value")

          
        #ax_1[j].axvline(x = 0, color = "b", label = "Indicated Start Day")
        #ax_1[j].axvline(x = end, color = "r", label = "Indicated End Day")
        
        ax_1[j].set_xlabel('Cycle Day')
        ax_1[j].set_ylabel('Temp(°C)')
        ax_1[j].set_title('Standardizing the Smooth Temperatures')
        ax_1[j].legend(loc=0)
        
        plt.tight_layout()

        j+=1


#Plot user averaged preprocessed reference cycles
def plot_refs_cycles_averaged(data):
    model_list = tools.load_model_cycle(data)
    model_list_len = len(model_list)
    fig = fig_layout()
    fig, ax_1 = plt.subplots(figsize=(6*model_list_len, 5), nrows=1, ncols=model_list_len)
    j = 0
    
    for avg in model_list:

        avg_temps = avg["user_averaged"]

        pos_actual = range(len(avg_temps))

        #normalized = MinMaxScaler()
        #pos_normalized = normalized.fit_transform(np.array(pos_actual).reshape(-1, 1))
        #pos_normalized  = [i for j in pos_normalized for i in j]
        pos_normalized = avg["normal_positions"]

        #cycle_pos = cycle_df["Normal_Positions"].to_list()
        #end = cycle_df["Date_Diff"].unique()[0]
        
        #ax_1[j].plot(cycle_pos, std_mean_temps, "o", label = "Temperature")
        #ax_1[j].plot(cycle_pos, std_smooth_temps, "r", label = "Smooth", alpha=0.4)

        ax_1[j].plot(pos_normalized, avg_temps, "o", label = "Data Points")
        ax_1[j].plot(pos_normalized, avg_temps, "r", label = "Smooth", alpha=0.4)
        #missing = cycle_df[cycle_df["Missing_Day"] == True]
        #if len(missing) > 0:
            #missing_temps = missing["Standard_mean_temps"].to_list()
            #missing_pos = missing["Cycle Position"].to_list()
            
            #ax_1[j].plot(missing_pos, missing_temps, "o", color = "red", label = "Interpolated Value")

          
        #ax_1[j].axvline(x = 0, color = "b", label = "Indicated Start Day")
        #ax_1[j].axvline(x = end, color = "r", label = "Indicated End Day")
        
        ax_1[j].set_xlabel('Cycle Day')
        ax_1[j].set_ylabel('Temp(°C)')
        ax_1[j].set_title('User Reference Average ')
        ax_1[j].legend(loc=0)
        
        plt.tight_layout()

        j+=1

#Plot final reference cycles
def plot_refs_cycles_final(data):
    model_data = tools.load_model_cycle(data)
    fig = fig_layout()
    ax = fig.add_axes([0,0, 1, 1])

    model_cycle = model_data["model_cycle"]
    pos_actual = range(len(model_cycle))
    
    #normalized = MinMaxScaler()
    #pos_normalized = normalized.fit_transform(np.array(pos_actual).reshape(-1, 1))
    #pos_normalized  = [i for j in pos_normalized for i in j]
    pos_normalized = model_data["normal_positions"]

    #cycle_pos = cycle_df["Normal_Positions"].to_list()
    #end = cycle_df["Date_Diff"].unique()[0]
    
    #ax_1[j].plot(cycle_pos, std_mean_temps, "o", label = "Temperature")
    #ax_1[j].plot(cycle_pos, std_smooth_temps, "r", label = "Smooth", alpha=0.4)
    ax.plot(pos_normalized, model_cycle, "o", label = "Data Points")
    ax.plot(pos_normalized, model_cycle, "r", label = "Reference Cycle", alpha=0.4)
    #missing = cycle_df[cycle_df["Missing_Day"] == True]
    #if len(missing) > 0:
        #missing_temps = missing["Standard_mean_temps"].to_list()
        #missing_pos = missing["Cycle Position"].to_list()
        
        #ax_1[j].plot(missing_pos, missing_temps, "o", color = "red", label = "Interpolated Value")

        
    #ax_1[j].axvline(x = 0, color = "b", label = "Indicated Start Day")
    #ax_1[j].axvline(x = end, color = "r", label = "Indicated End Day")
    
    ax.set_xlabel('Cycle Day')
    ax.set_ylabel('Temp(°C)')
    ax.set_title('Average Model Cycle')
    ax.legend(loc=0)
    
    #plt.tight_layout()
