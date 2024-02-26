import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

def plot_importance(level, title, model_importance, OUTPUT_FOLDER):
    fig, ax_1 = plt.subplots(figsize=(16, 9))

    if level == "Cycle Level":
        data = ["DTW_Dist_to_Model", "Nadir_day","Peak_day","Nadir_Temp", "Peak_Temp","Nadir_to_Peak","Low_to_High_Temp",
                            "Path_Length","Warp_Degree","Curve_Length","Data_Length","Curve_by_Data"]
    elif level == "User Level":
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
    elif level == "Questionnaire Level":
        data = ["BMI", "Sleep Hours", "Regular Smoker_Prefer not to answer", "Regular Smoker_Yes", 
                 "Night Sleep Troubles_Sometimes", "Night Sleep Troubles_Usually", 
                 "Unintentional Day Sleep_Never/ rarely", "Unintentional Day Sleep_Often", 
                 "Unintentional Day Sleep_Prefer not to answer", "Unintentional Day Sleep_Sometimes",
                 "When Active_Definitely an 'evening' person", "When Active_Do not know", 
                 "When Active_More a 'morning' than 'evening' person", 
                 "When Active_More an 'evening' than 'morning' person",
                 "When Active_Prefer not to answer", "Currently Pregnant_Prefer not to answer", 
                 "Currently Pregnant_Yes", "Time before current preg_6-11 months", 
                 "Time before current preg_Less than 6 months", "Time before current preg_No response", 
                 "Previous Pregancies_10.0", "Previous Pregancies_2.0", "Previous Pregancies_3.0",
                 "Previous Pregancies_4.0", "Previous Pregancies_5.0", "Previous Pregancies_6.0", 
                 "Previous Pregancies_7.0", "Previous Pregancies_8.0", "Previous Pregancies_9.0",
                 "Previous Pregancies_No response", "Time before one preg_6-11 months",
                 "Time before one preg_Don't remember", "Time before one preg_Less than 6 months",
                 "Time before one preg_No response", "Time before one preg_Pregnancy wasn't planned",
                 "Live birth_No response", "Live birth_Prefer not to answer", "Live birth_Yes", 
                 "Baby weight (Kg)_Normal weight baby", "Baby weight (Kg)_Overweight baby", 
                 "Baby weight (Kg)_Underweight baby", "Age menstration started_I don't remember",
                 "Age menstration started_I have not had periods", "Age menstration started_Late Menstruation Age",
                 "Age menstration started_Normal Menstruation Age",
                 "Age menstration started_Very Late Menstruation Age", "Period in last 3 months_No response", 
                 "Period in last 3 months_Yes", "Acceptable?_No response", "Acceptable?_Yes", 
                 "Regular periods_No response", "Regular periods_Yes", "Heavy periods_Moderately", 
                 "Heavy periods_No response", "Heavy periods_Not at all", "Heavy periods_Very",
                 "Painful periods_Moderately", "Painful periods_No response", "Painful periods_Not at all", 
                 "Painful periods_Very"]

    elif level == "User and Quest Level":
        data = ['BMI', 'Sleep Hours', 'Regular Smoker_Prefer not to answer', 
                 'Regular Smoker_Yes', 'Night Sleep Troubles_Sometimes', 'Night Sleep Troubles_Usually',
                 'Unintentional Day Sleep_Never/ rarely', 'Unintentional Day Sleep_Often', 
                 'Unintentional Day Sleep_Prefer not to answer', 'Unintentional Day Sleep_Sometimes',
                 "When Active_Definitely an 'evening' person", 'When Active_Do not know', 
                 "When Active_More a 'morning' than 'evening' person", 
                 "When Active_More an 'evening' than 'morning' person", 'When Active_Prefer not to answer',
                 'Currently Pregnant_Prefer not to answer', 'Currently Pregnant_Yes',
                 'Time before current preg_6-11 months', 'Time before current preg_Less than 6 months',
                 'Time before current preg_No response', 'Previous Pregancies_10.0', 'Previous Pregancies_2.0',
                 'Previous Pregancies_3.0', 'Previous Pregancies_4.0', 'Previous Pregancies_5.0', 
                 'Previous Pregancies_6.0', 'Previous Pregancies_7.0', 'Previous Pregancies_8.0', 
                 'Previous Pregancies_9.0', 'Previous Pregancies_No response', 'Time before one preg_6-11 months',
                 "Time before one preg_Don't remember", 'Time before one preg_Less than 6 months', 
                 'Time before one preg_No response', "Time before one preg_Pregnancy wasn't planned", 
                 'Live birth_No response', 'Live birth_Prefer not to answer', 'Live birth_Yes', 
                 'Baby weight (Kg)_Normal weight baby', 'Baby weight (Kg)_Overweight baby', 
                 'Baby weight (Kg)_Underweight baby', "Age menstration started_I don't remember", 
                 'Age menstration started_I have not had periods', 'Age menstration started_Late Menstruation Age',
                 'Age menstration started_Normal Menstruation Age', 
                 'Age menstration started_Very Late Menstruation Age',
                 'Period in last 3 months_No response', 'Period in last 3 months_Yes', 'Acceptable?_No response',
                 'Acceptable?_Yes', 'Regular periods_No response', 'Regular periods_Yes', 
                 'Heavy periods_Moderately', 'Heavy periods_No response', 'Heavy periods_Not at all', 
                 'Heavy periods_Very', 'Painful periods_Moderately', 'Painful periods_No response', 
                 'Painful periods_Not at all', 'Painful periods_Very',
                 'med_pair_distances', 'med_pair_lengths', 'min_dist_to_model', 'min_nadir_days', 'min_peak_days',
                 'min_nadir_temps', 'min_peak_temps', 'min_nadirs_to_peaks', 'min_low_to_high_temps', 
                 'min_path_length_to_model', 'min_warp_degree_with_model', 'min_Curve_Lengths', 'min_Data_Lengths',
                 'min_Curves_by_Data', 'max_dist_to_model', 'max_nadir_days', 'max_peak_days', 'max_nadir_temps',
                 'max_peak_temps', 'max_nadirs_to_peaks', 'max_low_to_high_temps', 'max_path_length_to_model', 
                 'max_warp_degree_with_model', 'max_Curve_Lengths', 'max_Data_Lengths', 'max_Curves_by_Data', 
                 'med_dist_to_model', 'med_nadir_days', 'med_peak_days', 'med_nadir_temps', 'med_peak_temps', 
                 'med_nadirs_to_peaks', 'med_low_to_high_temps', 'med_path_length_to_model', 
                 'med_warp_degree_with_model', 'med_Curve_Lengths', 'med_Data_Lengths', 'med_Curves_by_Data', 
                 'rge_dist_to_model', 'rge_nadir_days', 'rge_peak_days', 'rge_nadir_temps', 'rge_peak_temps', 
                 'rge_nadirs_to_peaks', 'rge_low_to_high_temps', 'rge_path_length_to_model', 
                 'rge_warp_degree_with_model', 'rge_Curve_Lengths', 'rge_Data_Lengths','rge_Curves_by_Data']

        """data = ['max_Data_Lengths', 'max_dist_to_model', 'max_path_length_to_model', 'med_Data_Lengths', 'med_nadir_days',
                'med_nadirs_to_peaks', 'med_path_length_to_model', 'med_peak_days', 'min_Curve_Lengths', 'rge_dist_to_model',
                'rge_low_to_high_temps', 'BMI', 'Baby weight (Kg)_Normal weight baby', 'Baby weight (Kg)_Overweight baby',
                'Baby weight (Kg)_Underweight baby', 'Live birth_Yes', 'Night Sleep Troubles_Sometimes',
                'Painful periods_Moderately', 'Regular periods_Yes', 'Sleep Hours','Time before one preg_Less than 6 months']"""

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

    imp = list(np.abs(model_importance))
    imp_dict = {"var":data, title:imp}
    imp_df = pd.DataFrame(imp_dict, columns = ["var", title])

    print ("The top 10 predictors for", title_name, "are:")
    print(imp_df.sort_values(by = title, ascending = False).head(10))
