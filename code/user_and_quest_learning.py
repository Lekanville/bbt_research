#!python
#!/usr/bin/env python3

#############################################################################################
#The “user_and_quest_learning.py” script
#The script reads the output of both the user_level_variables rule (rule 12) and the preprocess_quest rule (rule 14). 
# It will combine both dataset and then perform machine learning on the combined dataset with k-folds cross validation and ROC. 
# The results are then saved in the specified output folder. The variables and code are given below.
#############################################################################################

import numpy as np
import pandas as pd
import os
import argparse
from loguru import logger
from pathlib import Path
import joblib
import matplotlib.pyplot as plt

import questionnaire_variables.preprocess_quest_tools as preprocess
#from classes.custom_k_fold import CustomKFold
from classes.strat_k_fold import StratKFold
from tools.classifier_roc_cross_val import classifier_roc_cross_val
from tools.classifier_importance import plot_importance
from tools.classifier_importance import shap_explainer

parser = argparse.ArgumentParser(description= "A script to filter data")
parser.add_argument('-i', '--input_file_1', type=str, required=True, help= 'The user level input dataset')
parser.add_argument('-j', '--input_file_2', type=str, required=True, help= 'The questionnaire level input dataset')
parser.add_argument('-k', '--splits', type=int, required=True, help= 'The number of splits')
parser.add_argument('-o', '--output_folder', type=str, required=True, help= 'The output folder')

def user_level_learning(INPUT_1, INPUT_2, SPLITS, OUTPUT):
    #reading the data - user variables
    logger.info("Reading user level variables for learning")
    df_user_level_features = pd.read_csv(INPUT_1) 
    renaming = {"med_pair_distances":"Median of paired distances","med_pair_lengths":"Median of paired curve lengths",

    "min_Data_Length":"Minimum data length",
    "min_Cycle_Length":"Minimum cycle length",
    "min_Cycle_Completeness":"Minimum recorded period cycle proportion",
    "min_Curve_by_Data":"Minimum length of the cycle curve",
    "min_Max_of_2_Periods":"Minimum temp of largest three-day period",
    "min_Max_Pos_of_2_Periods":"Minimum of position of temp of largest three-day period",
    "min_Max_of_3_Periods":"Minimum temp of largest four-day period",
    "min_Max_Pos_of_3_Periods":"Minimum of position of temp of largest four-day period",
    "min_Change_Point_Day":"Minimum day of temperature change",
    "min_Change_Point_Mean_Diff":"Minimum diff in temp before and after temp change",
    "min_Cost_with_Diff":"Minimum DTW distance",
    "min_Path_Length_with_Diff":"Minimum length of optimal warping path",
    "min_Standard_Nadir_Temp_Actual":"Minimum nadir Temp",
    "min_Standard_Peak_Temp_Actual":"Minimum peak Temp",
    "min_Low_to_High_Temp":"Minimum Diff btw nadir and peak temps",
    "min_Expanded_Nadir_Day":"Minimum nadir day", 
    "min_Expanded_Peak_Day":"Minimum peak day", 
    "min_Expanded_Nadir_to_Peak":"Minimum time to peak",

    "max_Data_Length":"Maximum data length",
    "max_Cycle_Length":"Maximum cycle length",
    "max_Cycle_Completeness":"Maximum recorded period cycle proportion",
    "max_Curve_by_Data":"Maximum length of the cycle curve",
    "max_Max_of_2_Periods":"Maximum temp of largest three-day period",
    "max_Max_Pos_of_2_Periods":"Maximum of position of temp of largest three-day period",
    "max_Max_of_3_Periods":"Maximum temp of largest four-day period",
    "max_Max_Pos_of_3_Periods":"Maximum of position of temp of largest four-day period",
    "max_Change_Point_Day":"Maximum day of temperature change",
    "max_Change_Point_Mean_Diff":"Maximum diff in temp before and after temp change",
    "max_Cost_with_Diff":"Maximum DTW distance",
    "max_Path_Length_with_Diff":"Maximum length of optimal warping path",
    "max_Standard_Nadir_Temp_Actual":"Maximum nadir Temp",
    "max_Standard_Peak_Temp_Actual":"Maximum peak Temp",
    "max_Low_to_High_Temp":"Maximum Diff btw nadir and peak temps",
    "max_Expanded_Nadir_Day":"Maximum nadir day", 
    "max_Expanded_Peak_Day":"Maximum peak day", 
    "max_Expanded_Nadir_to_Peak":"Maximum time to peak",
    
    "med_Data_Length":"Median data length",
    "med_Cycle_Length":"Median cycle length",
    "med_Cycle_Completeness":"Median recorded period cycle proportion",
    "med_Curve_by_Data":"Median length of the cycle curve",
    "med_Max_of_2_Periods":"Median temp of largest three-day period",
    "med_Max_Pos_of_2_Periods":"Median of position of temp of largest three-day period",
    "med_Max_of_3_Periods":"Median temp of largest four-day period",
    "med_Max_Pos_of_3_Periods":"Median of position of temp of largest four-day period",
    "med_Change_Point_Day":"Median day of temperature change",
    "med_Change_Point_Mean_Diff":"Median diff in temp before and after temp change",
    "med_Cost_with_Diff":"Median DTW distance",
    "med_Path_Length_with_Diff":"Median length of optimal warping path",
    "med_Standard_Nadir_Temp_Actual":"Median nadir Temp",
    "med_Standard_Peak_Temp_Actual":"Median peak Temp",
    "med_Low_to_High_Temp":"Median Diff btw nadir and peak temps",
    "med_Expanded_Nadir_Day":"Median nadir day", 
    "med_Expanded_Peak_Day":"Median peak day", 
    "med_Expanded_Nadir_to_Peak":"Median time to peak",

    "rge_Data_Length":"Range of data length",
    "rge_Cycle_Length":"Range of cycle length",
    "rge_Cycle_Completeness":"Range of recorded period cycle proportion",
    "rge_Curve_by_Data":"Range of length of the cycle curve",
    "rge_Max_of_2_Periods":"Range of temp of largest three-day period",
    "rge_Max_Pos_of_2_Periods":"Range of position of temp of largest three-day period",
    "rge_Max_of_3_Periods":"Range of temp of largest four-day period",
    "rge_Max_Pos_of_3_Periods":"Range of position of temp of largest four-day period",
    "rge_Change_Point_Day":"Range of day of temperature change",
    "rge_Change_Point_Mean_Diff":"Range of diff in temp before and after temp change",
    "rge_Cost_with_Diff":"Range of DTW distance",
    "rge_Path_Length_with_Diff":"Range of length of optimal warping path",
    "rge_Standard_Nadir_Temp_Actual":"Range of nadir Temp",
    "rge_Standard_Peak_Temp_Actual":"Range of peak Temp",
    "rge_Low_to_High_Temp":"Range of Diff btw nadir and peak temps",
    "rge_Expanded_Nadir_Day":"Range of nadir day", 
    "rge_Expanded_Peak_Day":"Range of peak day", 
    "rge_Expanded_Nadir_to_Peak":"Range of time to peak",
    
    }
    df_user_level_features.rename(columns = renaming, inplace=True)
    logger.info("Dataset read")
    df_user_level = df_user_level_features.drop(["PCOS"], axis = 1)
    print("The length of the user level data dataframe is", len(df_user_level))

    #reading the data - questionnaire variables
    logger.info("Reading questionnaire level variables for learning")
    df_quest = pd.read_csv(INPUT_2) 
    logger.info("Dataset read")
    #Replace missing values with NaN
    df_quest = preprocess.clean_null_responses(df_quest)

    print("The length of the user level data dataframe is", len(df_quest))

    logger.info("Merging the dataframes (type is inner)")
    df = pd.merge(df_quest, df_user_level, on = "User", how = "inner")

    the_value_counts = df["PCOS"].value_counts()
    print("Counts of the values are \n", the_value_counts)

    #splitting the data into k-folds
    logger.info("Splitting the dataframe into " +str(SPLITS)+ " folds")
    splitted_df = StratKFold(n_splits = SPLITS, df = df, level="User and Quest Level").customSplit()
    print("The splits \n", splitted_df[1])

    print(splitted_df[0]["PCOS"].value_counts())

    #the splitted data
    df_for_learning = splitted_df[2]

    #create output folder if not exists
    Path(OUTPUT).mkdir(parents=True, exist_ok=True)

    #Empty variables to store data
    mean_fpr = np.linspace(0, 1, 100)
    all_mean_tpr = []
    all_mean_auc = [] 
    all_std_auc = []
    all_tprs_upper = []
    all_tprs_lower = []

    algorithms = ["RFC", "SVM", "LogReg"]
    colors = ["r", "b", "g"]
    fill_colors = ["lightcoral", "lightskyblue", "lightgreen"]

    #This runs the ML using all algorithms
    for alg in algorithms:
        logger.info("Performing "+ alg)
        shap_values, mean_tpr, mean_auc, std_auc, tprs_upper, tprs_lower = classifier_roc_cross_val("User and Quest Level", alg, df_for_learning, OUTPUT)
        all_mean_tpr.append(mean_tpr)
        all_mean_auc.append(mean_auc)
        all_std_auc.append(std_auc)
        all_tprs_upper.append(tprs_upper)
        all_tprs_lower.append(tprs_lower)

        shap_explainer("User and Quest Level", alg, shap_values, OUTPUT)
    
    #This plots the mean AUCs of the algorithms
    fig, ax = plt.subplots(figsize=(6, 6))   
    ax.plot([0,1], [0,1], ls='--')
    for i, mean_tpr in enumerate(all_mean_tpr):
        ax.plot(
            mean_fpr, 
            mean_tpr,
            color=colors[i],
            label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)-" % (all_mean_auc[i], all_std_auc[i]) + algorithms[i],
            lw=1.5,
            alpha=0.8,
        )
        ax.fill_between(
            mean_fpr,
            all_tprs_lower[i],
            all_tprs_upper[i],
            color=fill_colors[i],
            alpha=0.2,
            #label=r"$\pm$ 1 std. dev.",
        )
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Mean ROC for Combined User and Questionnaire Level Learning')
    plt.legend(loc="lower right")
    filename = "user_and_questionnaire_level_ML.png"
    plt.savefig(os.path.join(OUTPUT, filename))

    # #RFC classifier
    # logger.info("Performing Random Forest Classification")
    # #rfc_importance, explainers, x_tests = classifier_roc_cross_val("User and Quest Level", "RFC", df_for_learning, OUTPUT)
    # #rfc_importance, shap_values = classifier_roc_cross_val("User and Quest Level", "RFC", df_for_learning, OUTPUT)
    # shap_values, mean_tpr, mean_auc, std_auc = classifier_roc_cross_val("User and Quest Level", "RFC", df_for_learning, OUTPUT)
    # all_mean_tpr.append(mean_tpr)
    # all_mean_auc.append(mean_auc)
    # all_std_auc.append(std_auc)

    # #RFC SHAP Explainer
    # #shap_explainer(User and Quest Level", "RFC", explainers, x_tests, OUTPUT)
    # shap_explainer("User and Quest Level", "RFC", shap_values, OUTPUT)
    # #RFC variable importance
    # #shap_file = os.path.join(OUTPUT, "rfc_explainers.pkl")
    # #joblib.dump(shap_values, shap_file)

    # #plot_importance("Questionnaire Level", "RFC Model Importance", rfc_importance, OUTPUT)

    # #SVM classifier
    # logger.info("Performing Support Vector Machine Classification")
    # #svm_importance, explainers, x_tests = classifier_roc_cross_val("User and Quest Level", "SVM", df_for_learning, OUTPUT)
    # #svm_importance, shap_values = classifier_roc_cross_val("User and Quest Level", "SVM", df_for_learning, OUTPUT)
    # shap_values, mean_tpr, mean_auc, std_auc = classifier_roc_cross_val("User and Quest Level", "SVM", df_for_learning, OUTPUT)
    # all_mean_tpr.append(mean_tpr)
    # all_mean_auc.append(mean_auc)
    # all_std_auc.append(std_auc)

    # #SVM SHAP Explainer
    # #shap_explainer("User and Quest Level", "SVM", explainers, x_tests, OUTPUT)
    # shap_explainer("User and Quest Level", "SVM", shap_values, OUTPUT)
    # #SVM variable importance
    # #shap_file = os.path.join(OUTPUT, "svm_explainers.pkl")
    # #joblib.dump(shap_values, shap_file)

    # #plot_importance("Questionnaire Level", "SVM Model Importance", svm_importance, OUTPUT)

    # #LogReg classifier
    # logger.info("Performing Logistic Regression")
    # #logreg_importance, explainers, x_tests = classifier_roc_cross_val("User and Quest Level", "LogReg", df_for_learning, OUTPUT)
    # #logreg_importance, shap_values = classifier_roc_cross_val("User and Quest Level", "LogReg", df_for_learning, OUTPUT)
    # shap_values, mean_tpr, mean_auc, std_auc = classifier_roc_cross_val("User and Quest Level", "LogReg", df_for_learning, OUTPUT)
    # all_mean_tpr.append(mean_tpr)
    # all_mean_auc.append(mean_auc)
    # all_std_auc.append(std_auc)

    # #LogReg SHAP Explainer
    # #shap_explainer("User and Quest Level", "LogReg", explainers, x_tests, OUTPUT)
    # shap_explainer("User and Quest Level", "LogReg", shap_values, OUTPUT)
    # #LogReg variable importance
    # #shap_file = os.path.join(OUTPUT, "logreg_explainers.pkl")
    # #joblib.dump(shap_values, shap_file)
    # #plot_importance("Questionnaire Level", "LogReg Model Importance", logreg_importance, OUTPUT)

    # #DT classifier
    # # logger.info("Performing Decsion Tree Classification")
    # # dt_model = classifier_roc_cross_val("User and Quest Level", "DT", df_for_learning, OUTPUT)
    # # #LogReg variable importance
    # # plot_importance("User and Quest Level", "DT Model Importance", dt_model.feature_importances_, OUTPUT)

if __name__ == "__main__":
    args = parser.parse_args()
    user_level_learning(args.input_file_1, args.input_file_2, args.splits, args.output_folder)