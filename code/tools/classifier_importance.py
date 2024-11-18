import numpy as np
import pandas as pd
import os
import shap
import matplotlib.pyplot as plt

def plot_importance(level, title, model_importance, OUTPUT_FOLDER):
    fig, ax_1 = plt.subplots(figsize=(16, 9))

    if level == "Cycle Level":

        data = ['Data_Length','Next Cycle Difference','Cycle Completeness','Curve_by_Data','max_of_2_periods',
                'max_pos_of_2_periods','max_of_3_periods','max_pos_of_3_periods','Change Point Day','Change Point Mean Diff',
                'cost_with_diff','path_length_with_diff','Standard_nadir_temp_actual',
                'Standard_peak_temp_actual','Standard_low_to_high_temp',
                #'Standard_nadir_day','Standard_peak_day','Standard_nadir_to_peak',
                'Expanded_nadir_day', 'Expanded_peak_day', 'Expanded_nadir_to_peak']
        

    elif level == "User Level":
        data = ['med_pair_distances','med_pair_lengths',
            
                'min_Data_Length','min_Cycle_Length','min_Cycle_Completeness','min_Curve_by_Data','min_Max_of_2_Periods',
                'min_Max_Pos_of_2_Periods','min_Max_of_3_Periods','min_Max_Pos_of_3_Periods','min_Change_Point_Day',
                'min_Change_Point_Mean_Diff','min_Path_Length_with_Diff',
                'min_Standard_Nadir_Temp_Actual','min_Standard_Peak_Temp_Actual','min_Low_to_High_Temp','min_Cost_with_Diff',
                #'min_Standard_Nadir_Day','min_Standard_Peak_Day','min_Nadir_to_Peak',
                'min_Expanded_Nadir_Day', 'min_Expanded_Peak_Day', 'min_Expanded_Nadir_to_Peak',
                
                'max_Data_Length','max_Cycle_Length','max_Cycle_Completeness','max_Curve_by_Data','max_Max_of_2_Periods',
                'max_Max_Pos_of_2_Periods','max_Max_of_3_Periods','max_Max_Pos_of_3_Periods','max_Change_Point_Day',
                'max_Change_Point_Mean_Diff','max_Path_Length_with_Diff',
                'max_Standard_Nadir_Temp_Actual','max_Standard_Peak_Temp_Actual','max_Low_to_High_Temp','max_Cost_with_Diff',
                #'max_Standard_Nadir_Day','max_Standard_Peak_Day','max_Nadir_to_Peak',
                'max_Expanded_Nadir_Day', 'max_Expanded_Peak_Day', 'max_Expanded_Nadir_to_Peak',

                'med_Data_Length','med_Cycle_Length','med_Cycle_Completeness','med_Curve_by_Data','med_Max_of_2_Periods',
                'med_Max_Pos_of_2_Periods','med_Max_of_3_Periods','med_Max_Pos_of_3_Periods','med_Change_Point_Day',
                'med_Change_Point_Mean_Diff','med_Path_Length_with_Diff',
                'med_Standard_Nadir_Temp_Actual','med_Standard_Peak_Temp_Actual','med_Low_to_High_Temp','med_Cost_with_Diff',
                #'med_Standard_Nadir_Day','med_Standard_Peak_Day','med_Nadir_to_Peak',
                'med_Expanded_Nadir_Day', 'med_Expanded_Peak_Day', 'med_Expanded_Nadir_to_Peak',
                
                'rge_Data_Length','rge_Cycle_Length','rge_Cycle_Completeness','rge_Curve_by_Data','rge_Max_of_2_Periods',
                'rge_Max_Pos_of_2_Periods','rge_Max_of_3_Periods','rge_Max_Pos_of_3_Periods','rge_Change_Point_Day',
                'rge_Change_Point_Mean_Diff','rge_Path_Length_with_Diff',
                'rge_Standard_Nadir_Temp_Actual','rge_Standard_Peak_Temp_Actual','rge_Low_to_High_Temp','rge_Cost_with_Diff',
                #'rge_Standard_Nadir_Day','rge_Standard_Peak_Day','rge_Nadir_to_Peak',
                'rge_Expanded_Nadir_Day', 'rge_Expanded_Peak_Day', 'rge_Expanded_Nadir_to_Peak'
                ]

    elif level == "Questionnaire Level":
        data = ['BMI', 'Age menstration started',
                'Regular Smoker_Yes', 'Period in last 3 months_Yes', 'Regular periods_Yes',
                'Heavy periods_Moderately', 'Heavy periods_Not at all', 'Heavy periods_Very',
                'Painful periods_Moderately', 'Painful periods_Not at all', 'Painful periods_Very']


    elif level == "User and Quest Level":
        data = ['BMI', 'Age menstration started',
                'Regular Smoker_Yes', 'Period in last 3 months_Yes', 'Regular periods_Yes',
                'Heavy periods_Moderately', 'Heavy periods_Not at all', 'Heavy periods_Very',
                'Painful periods_Moderately', 'Painful periods_Not at all', 'Painful periods_Very',

                'med_pair_distances','med_pair_lengths',

                'min_Data_Length','min_Cycle_Length','min_Cycle_Completeness','min_Curve_by_Data','min_Max_of_2_Periods',
                'min_Max_Pos_of_2_Periods','min_Max_of_3_Periods','min_Max_Pos_of_3_Periods','min_Change_Point_Day',
                'min_Change_Point_Mean_Diff','min_Path_Length_with_Diff',
                'min_Standard_Nadir_Temp_Actual','min_Standard_Peak_Temp_Actual','min_Low_to_High_Temp','min_Cost_with_Diff',
                #'min_Standard_Nadir_Day','min_Standard_Peak_Day','min_Nadir_to_Peak',
                'min_Expanded_Nadir_Day', 'min_Expanded_Peak_Day', 'min_Expanded_Nadir_to_Peak',
                
                'max_Data_Length','max_Cycle_Length','max_Cycle_Completeness','max_Curve_by_Data','max_Max_of_2_Periods',
                'max_Max_Pos_of_2_Periods','max_Max_of_3_Periods','max_Max_Pos_of_3_Periods','max_Change_Point_Day',
                'max_Change_Point_Mean_Diff','max_Path_Length_with_Diff',
                'max_Standard_Nadir_Temp_Actual','max_Standard_Peak_Temp_Actual','max_Low_to_High_Temp','max_Cost_with_Diff',
                #'max_Standard_Nadir_Day','max_Standard_Peak_Day','max_Nadir_to_Peak',
                'max_Expanded_Nadir_Day', 'max_Expanded_Peak_Day', 'max_Expanded_Nadir_to_Peak',

                'med_Data_Length','med_Cycle_Length','med_Cycle_Completeness','med_Curve_by_Data','med_Max_of_2_Periods',
                'med_Max_Pos_of_2_Periods','med_Max_of_3_Periods','med_Max_Pos_of_3_Periods','med_Change_Point_Day',
                'med_Change_Point_Mean_Diff','med_Path_Length_with_Diff',
                'med_Standard_Nadir_Temp_Actual','med_Standard_Peak_Temp_Actual','med_Low_to_High_Temp','med_Cost_with_Diff',
                #'med_Standard_Nadir_Day','med_Standard_Peak_Day','med_Nadir_to_Peak',
                'med_Expanded_Nadir_Day', 'med_Expanded_Peak_Day', 'med_Expanded_Nadir_to_Peak',
                
                'rge_Data_Length','rge_Cycle_Length','rge_Cycle_Completeness','rge_Curve_by_Data','rge_Max_of_2_Periods',
                'rge_Max_Pos_of_2_Periods','rge_Max_of_3_Periods','rge_Max_Pos_of_3_Periods','rge_Change_Point_Day',
                'rge_Change_Point_Mean_Diff','rge_Path_Length_with_Diff',
                'rge_Standard_Nadir_Temp_Actual','rge_Standard_Peak_Temp_Actual','rge_Low_to_High_Temp','rge_Cost_with_Diff',
                #'rge_Standard_Nadir_Day','rge_Standard_Peak_Day','rge_Nadir_to_Peak',
                'rge_Expanded_Nadir_Day', 'rge_Expanded_Peak_Day', 'rge_Expanded_Nadir_to_Peak'  
                ]

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
    ax_1.grid(b = True, color ='grey',linestyle ='-.', linewidth = 0.5,alpha = 0.2)
    
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


def shap_explainer(level, classifier_name, explainers, x_tests, OUTPUT_FOLDER):

    for i, j in enumerate(explainers):
        fig = plt.figure()
        ax = fig.add_axes([0,0, 1, 1])

        explainer = explainers[i]
        x_test = x_tests[i]
        shap_values = explainer(x_test)
        shap.plots.beeswarm(shap_values, show=False)

        shap_file = level+"_"+classifier_name+"_"+str(i)+".png"
        plt.savefig(os.path.join(OUTPUT_FOLDER,shap_file), format='png', dpi=700, bbox_inches='tight')