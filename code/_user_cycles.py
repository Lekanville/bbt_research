import numpy as np
import pandas as pd
from loguru import logger
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter
import includes

#get temperatures from the cleaned workflow
IN_FILE = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/sel_crt_2.csv"
OUT_FILE = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/images"
temperatures = pd.read_csv(IN_FILE, usecols=["prime","Cycle ID","Start Time","Mean_Temp","Date","Time"])
temperatures["User ID"] = temperatures["prime"].apply(lambda x: x.split("_")[0])
temp_sort = temperatures.sort_values("Date").reset_index(drop = True)
#temp_sort["Cycle ID"] = temp_sort["Cycle ID"].apply(lambda x: x.lower())
temp_sort["Cycle ID"] = temp_sort["Cycle ID"]
temp_sort["Mean_Temp"] = temp_sort["Mean_Temp"].apply(lambda x: int(x))
temp_final = temp_sort[(temp_sort["Mean_Temp"] > 35000) & (temp_sort["Mean_Temp"] < 40000)]
logger.info("Temperatures dataset loaded and sorted by date")

#get cycles from the cleaned workflow
cycles = pd.read_csv("/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/temp_dates_duration.csv", index_col="Unnamed: 0")
cycles = cycles[cycles["Date_Diff"] != "Indeterminate Last Cycle"]
cycles = cycles.sort_values(["Min_date", "Cycle ID"]).reset_index(drop = True)
logger.info("Cycles Data loaded and sorted by date")

def plot_cycles():
    #group the cycles table by users and cycles
    grouped = cycles.groupby(["User ID_y", "Cycle ID"]).first()

    #users with cycles less than 10
    cycle_counts = cycles.groupby("User ID_y").count()
    users_less_10 = cycle_counts[(cycle_counts["Cycle ID"] >= 3) & (cycle_counts["Cycle ID"] <= 10)]

    #get the users
    users_10_cycles = includes.get_users(users_less_10)
    logger.info("users' list created")

    #pick random 100 users from the list of users with less than 10 cycles
    np.random.seed(10)
    rand_100_users = list(np.random.choice(users_10_cycles, 100))
    logger.info("100 random users selected list created")

    #prepare the figure layout 
    fig = plt.figure()
    inc = includes.matrix_generator(1000, 10)
    k = 0
    ax = fig.add_axes([0,0,1,1])
    listOf_Yticks = np.arange(36000, 38000, 100)
    fig, ax = plt.subplots(figsize=(80, 500), nrows=100, ncols=10)
    logger.info("Plot axis created")

    #attempt the plots 
    for u in rand_100_users:
        usr = grouped.xs(u, level = 0).sort_values("Date_y")
        usr_cycles = list(usr.index)
        
        #for users with up to 10 cycles, plot all 10 cycles
        if (10 - len(usr_cycles)) == 0:
            for c in usr_cycles:
                a = inc[k].pop(0)
                b = inc[k].pop(0)

                #offset = int(usr[usr.index == c.lower()]["Offset"])
                offset = int(usr[usr.index == c]["Offset"])
                #Date_Diff = int(usr[usr.index == c.lower()]["Date_Diff"])
                Date_Diff = int(usr[usr.index == c]["Date_Diff"])
                #ovul = usr[usr.index == c.lower()]["Ovulation Day"]
                ovul = usr[usr.index == c]["Ovulation Day"]

                if str(ovul.values) != "[nan]":
                    ovulation = int(ovul)
                else:
                    ovulation = 0

                df_c = temp_sort[temp_sort["Cycle ID"] == c][["Mean_Temp", "Date"]].sort_values("Date").reset_index(drop = True)
                smooth = savgol_filter(df_c["Mean_Temp"], 4, 2)

                x = [e + offset for e in list(range(len(df_c)))]
                y = df_c["Mean_Temp"]


                ax[a,b].plot(x, y, "o", label = "Temperature")
                ax[a,b].plot(x, smooth, "r", label = "Smooth")
                ax[a,b].axvline(x = 0, color = "b", label = "Cycle Start")
                ax[a,b].axvline(x = Date_Diff, color = "r", label = "Cycle End")
                if ovulation != 0:
                    ax[a,b].axvline(x = ovulation, color = "g", label = "Ovulation Day")
                
                ax[a,b].set_xlabel('Cycle Day')
                ax[a,b].set_ylabel(u+' Temp(°C)')
                ax[a,b].set_title(c)
                ax[a,b].legend(loc=0)
                k+=1
        
        #for users with less than 10 cycles; 
        else:
            #first plot available cycles
            for c in usr_cycles:
                a = inc[k].pop(0)
                b = inc[k].pop(0)

                #offset = int(usr[usr.index == c.lower()]["Offset"])
                offset = int(usr[usr.index == c]["Offset"])
                #Date_Diff = int(usr[usr.index == c.lower()]["Date_Diff"])
                Date_Diff = int(usr[usr.index == c]["Date_Diff"])
                #ovul = usr[usr.index == c.()]["Ovulation Day"]
                ovul = usr[usr.index == c]["Ovulation Day"]

                if str(ovul.values) != "[nan]":
                    ovulation = int(ovul)
                else:
                    ovulation = 0

                df_c = temp_sort[temp_sort["Cycle ID"] == c][["Mean_Temp", "Date"]].sort_values("Date").reset_index(drop = True)
                smooth = savgol_filter(df_c["Mean_Temp"], 4, 2)

                x = [e + offset for e in list(range(len(df_c)))]
                y = df_c["Mean_Temp"]


                ax[a,b].plot(x, y, "o", label = "Temperature")
                ax[a,b].plot(x, smooth, "r", label = "Smooth")
                ax[a,b].axvline(x = 0, color = "b", label = "Cycle Start")
                ax[a,b].axvline(x = Date_Diff, color = "r", label = "Cycle End")
                if ovulation != 0:
                    ax[a,b].axvline(x = ovulation, color = "g", label = "Ovulation Day")
                
                ax[a,b].set_xlabel('Cycle Day')
                ax[a,b].set_ylabel(u+' Temp(°C)')
                ax[a,b].set_title(c)
                ax[a,b].legend(loc=0)
                k+=1
            
            # then pad the remainder
            for z in range(10 - len(usr_cycles)):
                a = inc[k].pop(0)
                b = inc[k].pop(0)  
                x = 0
                y = 0
                
                ax[a,b].plot(x, y, "o", label = "Temperature")
                #ax[a,b].axvline(x = 0, color = "b", label = "Cycle Start")
                ax[a,b].set_xlabel('Cycle Day')
                ax[a,b].set_ylabel(u+' Temp(°C)')
                ax[a,b].legend(loc=0)
                
                k+=1

    #plt.yticks(listOf_Yticks)
    plt.ylim([36000, 38000])
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_FILE, "user_cycles.png"), bbox_inches='tight', dpi=100)
    logger.info("plots ready")

if __name__ == "__main__":
    plot_cycles()