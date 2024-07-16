#!python
#!/usr/bin/env python3

#############################################################################################
#The “cycle_learning_variables.py” script
#The script expects the output file from the previous rule (cycle_level_data) as input and will 
#output the machine learning results to defined folder. After the input is read the data split into k-folds
#and learning with k-folds cross validation and ROC is carried out on the data at the cycle level
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
parser.add_argument('-i', '--input_file', type=str, required=True, help= 'The input dataset')
parser.add_argument('-k', '--splits', type=int, required=True, help= 'The number of splits')
parser.add_argument('-o', '--output_folder', type=str, required=True, help= 'The output folder')

def cycle_level_learning(INPUT, SPLITS, OUTPUT):
    #reading the data
    logger.info("Reading cycle level variables for learning")
    df = pd.read_csv(INPUT) 
    logger.info("Dataset read")

    print("The length of the dataframe is", len(df))
    
    the_value_counts = df["PCOS"].value_counts()
    print("Counts of the values are \n", the_value_counts)

    #splitting the data into k-folds
    logger.info("Splitting the dataframe into " +str(SPLITS)+ " folds")
    splitted_df = CustomKFold(n_splits = SPLITS, df = df, level="Cycle Level").customSplit()
    print("The splits \n", splitted_df[1])

    print(splitted_df[0]["PCOS"].value_counts())
   
    #the splitted data
    df_for_learning = splitted_df[2]

    #create output folder if not exists
    Path(OUTPUT).mkdir(parents=True, exist_ok=True)

    #RFC classifier
    logger.info("Performing Random Forest Classification")
    rfc_model = classifier_roc_cross_val("Cycle Level", "RFC", df_for_learning, OUTPUT)
    #RFC variable importance
    plot_importance("Cycle Level", "RFC Model Importance", rfc_model, OUTPUT)

    #SVM classifier
    logger.info("Performing Support Vector Machine Classification")
    svm_model = classifier_roc_cross_val("Cycle Level", "SVM", df_for_learning, OUTPUT)
    #SVM variable importance
    plot_importance("Cycle Level", "SVM Model Importance", svm_model, OUTPUT)

    #LogReg classifier
    logger.info("Performing Logistic Regression")
    logreg_model = classifier_roc_cross_val("Cycle Level", "LogReg", df_for_learning, OUTPUT)
    #LogReg variable importance
    plot_importance("Cycle Level", "LogReg Model Importance", logreg_model, OUTPUT)

    #DT classifier
    # logger.info("Performing Decsion Tree Classification")
    # dt_model = classifier_roc_cross_val("Cycle Level", "DT", df_for_learning, OUTPUT)
    # #LogReg variable importance
    # plot_importance("Cycle Level", "DT Model Importance", dt_model.feature_importances_, OUTPUT)

if __name__ == "__main__":
    args = parser.parse_args()
    cycle_level_learning(args.input_file, args.splits, args.output_folder)