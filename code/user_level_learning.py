#!python
#!/usr/bin/env python3

#############################################################################################
#The “user_learning_variables.py” script
#The script expects the output file from the previous rule (user_level_data) as input and will 
#output the features to defined folder. After the input is read the data split into k-folds
#and learning with k-folds cross validation and ROC is carried out on the data at the user level
#############################################################################################

import numpy as np
import pandas as pd
import os
import argparse
from loguru import logger
from pathlib import Path

#from classes.custom_k_fold import CustomKFold
from classes.strat_k_fold import StratKFold
from tools.classifier_roc_cross_val import classifier_roc_cross_val
from tools.classifier_importance import plot_importance
from tools.classifier_importance import shap_explainer

parser = argparse.ArgumentParser(description= "A script to filter data")
parser.add_argument('-i', '--input_file', type=str, required=True, help= 'The input dataset')
parser.add_argument('-k', '--splits', type=int, required=True, help= 'The number of splits')
parser.add_argument('-o', '--output_folder', type=str, required=True, help= 'The output folder')

def user_level_learning(INPUT, SPLITS, OUTPUT):
    #reading the data
    logger.info("Reading user level variables for learning")
    df = pd.read_csv(INPUT) 
    logger.info("Dataset read")

    print("The length of the dataframe is", len(df))
    
    the_value_counts = df["PCOS"].value_counts()
    print("Counts of the values are \n", the_value_counts)

    #splitting the data into k-folds
    logger.info("Splitting the dataframe into " +str(SPLITS)+ " folds")
    splitted_df = StratKFold(n_splits = SPLITS, df = df, level="User Level").customSplit()
    print("The splits \n", splitted_df[1])

    print(splitted_df[0]["PCOS"].value_counts())

    #the splitted data
    df_for_learning = splitted_df[2]

    #create output folder if not exists
    Path(OUTPUT).mkdir(parents=True, exist_ok=True)

    #RFC classifier
    logger.info("Performing Random Forest Classification")
    #rfc_importance, explainers, x_tests = classifier_roc_cross_val("Questionnaire Level", "RFC", df_for_learning, OUTPUT)
    rfc_importance, shap_values = classifier_roc_cross_val("User Level", "RFC", df_for_learning, OUTPUT)
    #RFC SHAP Explainer
    #shap_explainer("Questionnaire Level", "RFC", explainers, x_tests, OUTPUT)
    shap_explainer("Questionnaire Level", "RFC",shap_values, OUTPUT)
    #RFC variable importance
    #shap_file = os.path.join(OUTPUT, "rfc_explainers.pkl")
    #joblib.dump(shap_values, shap_file)

    #plot_importance("Questionnaire Level", "RFC Model Importance", rfc_importance, OUTPUT)

    #SVM classifier
    logger.info("Performing Support Vector Machine Classification")
    #svm_importance, explainers, x_tests = classifier_roc_cross_val("Questionnaire Level", "SVM", df_for_learning, OUTPUT)
    svm_importance, shap_values = classifier_roc_cross_val("User Level", "SVM", df_for_learning, OUTPUT)
    #SVM SHAP Explainer
    #shap_explainer("Questionnaire Level", "SVM", explainers, x_tests, OUTPUT)
    shap_explainer("Questionnaire Level", "SVM", shap_values, OUTPUT)
    #SVM variable importance
    #shap_file = os.path.join(OUTPUT, "svm_explainers.pkl")
    #joblib.dump(shap_values, shap_file)

    #plot_importance("Questionnaire Level", "SVM Model Importance", svm_importance, OUTPUT)

    #LogReg classifier
    logger.info("Performing Logistic Regression")
    #logreg_importance, explainers, x_tests = classifier_roc_cross_val("Questionnaire Level", "LogReg", df_for_learning, OUTPUT)
    logreg_importance, shap_values = classifier_roc_cross_val("User Level", "LogReg", df_for_learning, OUTPUT)
    #LogReg SHAP Explainer
    #shap_explainer("Questionnaire Level", "LogReg", explainers, x_tests, OUTPUT)
    shap_explainer("Questionnaire Level", "LogReg", shap_values, OUTPUT)
    #LogReg variable importance
    #shap_file = os.path.join(OUTPUT, "logreg_explainers.pkl")
    #joblib.dump(shap_values, shap_file)
    #plot_importance("Questionnaire Level", "LogReg Model Importance", logreg_importance, OUTPUT)

    #DT classifier
    # logger.info("Performing Decsion Tree Classification")
    # dt_model = classifier_roc_cross_val("User Level", "DT", df_for_learning, OUTPUT)
    # #LogReg variable importance
    # plot_importance("User Level", "DT Model Importance", dt_model.feature_importances_, OUTPUT)

if __name__ == "__main__":
    args = parser.parse_args()
    user_level_learning(args.input_file, args.splits, args.output_folder)