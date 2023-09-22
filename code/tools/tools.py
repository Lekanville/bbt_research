import json
import numpy as np

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
def load_model_cycle():
    try:
        with open("/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/model.json", "r") as f:
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

#custom algorithm for getting the amount of warping
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