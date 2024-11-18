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
    logger.info("Dataset read")
    df_user_level = df_user_level_features.drop(["PCOS"], axis = 1)
    print("The length of the user level data dataframe is", len(df_user_level))

    #reading the data - questionnaire variables
    logger.info("Reading questionnaire level variables for learning")
    df_quest = pd.read_csv(INPUT_2) 
    logger.info("Dataset read")
    #Replace missing vales with NaN
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

    #RFC classifier
    logger.info("Performing Random Forest Classification")
    #RFC variable importance
    rfc_importance, explainers, x_tests = classifier_roc_cross_val("User and Quest Level", "RFC", df_for_learning, OUTPUT)
    #RFC SHAP Explainer
    shap_explainer("User and Quest Level", "RFC", explainers, x_tests, OUTPUT)
    #RFC variable importance
    plot_importance("User and Quest Level", "RFC Model Importance", rfc_importance, OUTPUT)

    #SVM classifier
    logger.info("Performing Support Vector Machine Classification")
    svm_importance, explainers, x_tests = classifier_roc_cross_val("User and Quest Level", "SVM", df_for_learning, OUTPUT)
    #SVM SHAP Explainer
    shap_explainer("User and Quest Level", "SVM", explainers, x_tests, OUTPUT)
    #SVM variable importance
    plot_importance("User and Quest Level", "SVM Model Importance", svm_importance, OUTPUT)

    #LogReg classifier
    logger.info("Performing Logistic Regression")
    logreg_importance, explainers, x_tests = classifier_roc_cross_val("User and Quest Level", "LogReg", df_for_learning, OUTPUT)
    #LogReg SHAP Explainer
    shap_explainer("User and Quest Level", "LogReg", explainers, x_tests, OUTPUT)
    #LogReg variable importance
    plot_importance("User and Quest Level", "LogReg Model Importance", logreg_importance, OUTPUT)

    #DT classifier
    # logger.info("Performing Decsion Tree Classification")
    # dt_model = classifier_roc_cross_val("User and Quest Level", "DT", df_for_learning, OUTPUT)
    # #LogReg variable importance
    # plot_importance("User and Quest Level", "DT Model Importance", dt_model.feature_importances_, OUTPUT)

if __name__ == "__main__":
    args = parser.parse_args()
    user_level_learning(args.input_file_1, args.input_file_2, args.splits, args.output_folder)