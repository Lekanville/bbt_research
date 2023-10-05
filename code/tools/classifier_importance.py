import os
import matplotlib.pyplot as plt

def plot_importance(level, title, model_importance, OUTPUT_FOLDER):
    fig, ax_1 = plt.subplots(figsize=(16, 9))

    if level == "Cycle Level":
        data = ["DTW_Dist_to_Model", "Nadir_day","Peak_day","Nadir_Temp", "Peak_Temp","Nadir_to_Peak","Low_to_High_Temp",
                            "Path_Length","Warp_Degree","Curve_Length","Data_Length","Curve_by_Data"]
    else:
        data = ['Med_Pair_Distances','Med_Pair_Lengths','Min_Dist_to_Model','Min_Nadir_Days','Min_Peak_Days','Min_Nadir_Temps',
                'Min_Peak_Temps','Min_Nadirs_to_Peaks','Min_Low_to_High_temps', 'Min_Path_Length_to_Model','Min_Warp_Degree_with_Model',
                'Min_Curve_Lengths','Min_Data_Lengths','Min_Curves_by_Data',
                                      
                'Max_Dist_to_Model','Max_Nadir_Days','Max_Peak_Days','Max_Nadir_Temps','Max_Peak_Temps','Max_Nadirs_to_Peaks',
                'Max_Low_to_High_Temps','Max_Path_Length_to_Model','Max_Warp_Degree_with_Model','Max_Curve_Lengths','Max_Data_Lengths',
                'Max_Curves_by_Data',
                                      
                'Med_Dist_to_Model','Med_Nadir_Days','Med_Peak_Days','Med_Nadir_Temps','Med_Peak_Temps','Med_Nadirs_to_Peaks',
                'Med_Low_to_High_Temps','Med_Path_Length_to_Model','Med_Warp_Degree_with_Model','Med_Curve_Lengths',
                'Med_Data_Lengths','Med_Curves_by_Data',
                                      
                'Rge_Dist_to_Model','Rge_Nadir_Days','Rge_Peak_Days','Rge_Nadir_Temps','Rge_Peak_Temps','Rge_Nadirs_to_Peaks',
                'Rge_Low_to_High_Temps','Rge_Path_Length_to_Model','Rge_Warp_Wegree_with_Model','Rge_Curve_Lengths',
                'Rge_Data_Lengths','Rge_Curves_by_Data']
        

    #plot the importance
    ax_1.barh(data, model_importance)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax_1.spines[s].set_visible(False)
    
    # Remove x, y Ticks
    ax_1.xaxis.set_ticks_position('none')
    ax_1.yaxis.set_ticks_position('none')
    
    # Add padding between axes and labels
    ax_1.xaxis.set_tick_params(pad = 5)
    ax_1.yaxis.set_tick_params(pad = 10)
    
    #add x, y gridlines
    ax_1.grid(b = True, color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)
    
    # Show top values
    #ax_1.invert_yaxis()

    #add annotation to bars
    #for i in ax_1.patches:
    #    if i.get_width() > 0:
    #        plt.text(i.get_width()+0.002, i.get_y()+0.3,
    #                str(round((i.get_width()), 2)),
    #                fontsize = 10, fontweight ='bold',
    #                color ='grey')
    #    else:
    #        plt.text(i.get_width()-0.02, i.get_y()+0.3,
    #                str(round((i.get_width()), 2)),
    #                fontsize = 10, fontweight ='bold',
    #                color ='grey')       

    # Add Plot Title
    title_name = title + "-" + level
    ax_1.set_title(title_name, loc ='left')
    filename = "_".join(title.split(" "))+"_"+level+".png"
    plt.savefig(os.path.join(OUTPUT_FOLDER,filename))