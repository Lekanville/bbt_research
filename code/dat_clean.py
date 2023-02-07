#! usr/bin/env python3

import numpy as np
import pandas as pd
import os, sys
from loguru import logger
import glob
pd.options.mode.chained_assignment = None 


ABSOLUTE = "/projects/MRC-IEU/research/data/fertility_focus/ovusense/released/2022-11-30/data/temperature/"
OUT_FILE = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/"

PATH = os.path.join(ABSOLUTE, "alluserrecordings*")
FOLDER = glob.glob(PATH)


def remove_bin(df):
   for i in range(len(df)):
    if df.loc[i, "Data"].startswith("Bin"):
        df.loc[i, "Data"] = df.loc[i, "Data"][10:522]
   return df

   
def dat_clean():
    rec_full  = pd.DataFrame()
    logger.info("loading the datasets...\n")

    for file in FOLDER:
        rec = pd.read_csv(file, parse_dates=['Start Time'])
        rec_full = pd.concat([rec_full, rec], axis = 0)
        dataset_name = file.split("/")[-1]
        logger.info(dataset_name, "loaded \n")

    logger.info("Datasets merged \n")

    rec_full_unique = rec_full.drop_duplicates()
    logger.info("Full duplicates dropped \n")

    rec_clean = rec_full_unique.dropna(subset=['Data'])
    logger.info("Null values dropped \n")

    rec_clean["prime"] = (rec_clean["User ID"]).astype(str)+"_"+(rec_clean["Start Time"]).astype(str)
    logger.info("Primary key created \n")

    rec_clean['count'] = rec_clean.isnull().sum(1)
    rec_clean_t = rec_clean.sort_values(['count']).drop_duplicates(subset=['prime'],keep='first').drop(columns = 'count')
    logger.info("Partial duplicates dropped \n")
    
    rec_clean_t.reset_index(drop=True, inplace=True)
    logger.info("Index reset \n")
    
    cleaned = remove_bin(rec_clean_t)
    logger.info("Improperly formated data removed \n")
    
    cleaned.to_csv(os.path.join(OUT_FILE, 'cleaned.csv'))
    logger.info("Data succesfully cleaned and saved")

if __name__ == "__main__":
    dat_clean()