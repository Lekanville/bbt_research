#!python
#!/usr/bin/env python3

#############################################################################################
#The “user_learning_variables.py” script
#The script expects the output file from the previous rule (cycle_level_data) as input and will 
#output the features to defined folder. After the input is read the data splitted into k-folds
#and learning with k-folds cross validation and ROC is carried ou on the data at the user level
#############################################################################################

import numpy as np
import pandas as pd
import os
import argparse
from loguru import logger
from pathlib import Path

from classes.custom_k_fold import CustomKFold
from tools.classifier_roc_cross_val import classifier_roc_cross_val
from tools.classifier_importance import plot_importance

parser = argparse.ArgumentParser(description= "A script to filter data")
parser.add_argument('-i', '--input_file_1', type=str, required=True, help= 'The user level input dataset')
parser.add_argument('-j', '--input_file_2', type=str, required=True, help= 'The questionnaire level input dataset')
parser.add_argument('-k', '--splits', type=int, required=True, help= 'The number of splits')
parser.add_argument('-o', '--output_folder', type=str, required=True, help= 'The output folder')

def user_level_learning(INPUT_1, INPUT_2, SPLITS, OUTPUT):
    #reading the data
    logger.info("Reading user level variables for learning")
    df_user_level_features = pd.read_csv(INPUT_1) 
    logger.info("Dataset read")
    df_user_level = df_user_level_features.drop(["Unnamed: 0", "PCOS"], axis = 1)
    print("The length of the user level data dataframe is", len(df_user_level))

    logger.info("Reading questionnaire level variables for learning")
    df_quest = pd.read_csv(INPUT_2) 
    logger.info("Dataset read")

    print("The length of the user level data dataframe is", len(df_quest))
    
    logger.info("Merging the dataframes (type is inner)")
    df = pd.merge(df_quest, df_user_level, on = "User", how = "inner")

    the_value_counts = df["PCOS"].value_counts()
    print("Counts of the values are \n", the_value_counts)

    #splitting the data into k-folds
    logger.info("Splitting the dataframe into " +str(SPLITS)+ " folds")
    splitted_df = CustomKFold(n_splits = SPLITS, df = df, level="User and Quest Level").customSplit()
    print("The splits \n", splitted_df[1])

    print(splitted_df[0]["PCOS"].value_counts())

    #the splitted data
    df_for_learning = splitted_df[2]

    #create output folder if not exists
    Path(OUTPUT).mkdir(parents=True, exist_ok=True)

    #RFC classifier
    logger.info("Performing Random Forest Classification")
    rfc_model = classifier_roc_cross_val("User and Quest Level", "RFC", df_for_learning, OUTPUT)
    #RFC variable importance
    plot_importance("User and Quest Level", "RFC Model Importance", rfc_model.feature_importances_, OUTPUT)

    #SVM classifier
    logger.info("Performing Support Vector Machine Classification")
    svm_model = classifier_roc_cross_val("User and Quest Level", "SVM", df_for_learning, OUTPUT)
    #SVM variable importance
    plot_importance("User and Quest Level", "SVM Model Importance", svm_model.coef_[0], OUTPUT)

    #LogReg classifier
    logger.info("Performing Logistic Regression")
    logreg_model = classifier_roc_cross_val("User and Quest Level", "LogReg", df_for_learning, OUTPUT)
    #LogReg variable importance
    plot_importance("User and Quest Level", "LogReg Model Importance", logreg_model.coef_[0], OUTPUT)

    #DT classifier
    logger.info("Performing Decsion Tree Classification")
    dt_model = classifier_roc_cross_val("User and Quest Level", "DT", df_for_learning, OUTPUT)
    #LogReg variable importance
    plot_importance("User and Quest Level", "DT Model Importance", dt_model.feature_importances_, OUTPUT)

if __name__ == "__main__":
    args = parser.parse_args()
    user_level_learning(args.input_file_1, args.input_file_2, args.splits, args.output_folder)