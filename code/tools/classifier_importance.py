import os
import matplotlib.pyplot as plt

def plot_importance(title, model_importance, OUTPUT_FOLDER):
    fig, ax_1 = plt.subplots(figsize=(16, 9))
    data = ["DTW_Dist_to_Model", "Nadir_day","Peak_day","Nadir_Temp", "Peak_Temp","Nadir_to_Peak","Low_to_High_Temp",
                            "Path_Length","Warp_Degree","Curve_Length","Data_Length","Curve_by_Data"]


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
    for i in ax_1.patches:
        if i.get_width() > 0:
            plt.text(i.get_width()+0.002, i.get_y()+0.3,
                    str(round((i.get_width()), 2)),
                    fontsize = 10, fontweight ='bold',
                    color ='grey')
        else:
            plt.text(i.get_width()-0.02, i.get_y()+0.3,
                    str(round((i.get_width()), 2)),
                    fontsize = 10, fontweight ='bold',
                    color ='grey')       

    # Add Plot Title
    ax_1.set_title(title, loc ='left')
    filename = "_".join(title.split(" "))+".png"
    plt.savefig(os.path.join(OUTPUT_FOLDER,filename))