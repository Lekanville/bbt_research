#! usr/bin/env python3

import numpy as np
import pandas as pd
import os, sys
from loguru import logger
pd.options.mode.chained_assignment = None 

ABSOLUTE = "/projects/MRC-IEU/research/data/fertility_focus/ovusense/released/2022-11-30/data/temperature/"
OUT_FILE = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/"
CSV_2017 = "alluserrecordings.20221117122530-2015-2017.csv"
CSV_2018 = "alluserrecordings.20221117123037-2018.csv"
CSV_2019 = "alluserrecordings.20221117123329-2019.csv"
CSV_2020 = "alluserrecordings.20221117123857-2020.csv"
CSV_2021 = "alluserrecordings.20221117124425-2021.csv"
CSV_2022 = "alluserrecordings.20221117124952-2022.csv"

FILE_2017 =  os.path.join(ABSOLUTE, CSV_2017)
FILE_2018 =  os.path.join(ABSOLUTE, CSV_2018)
FILE_2019 =  os.path.join(ABSOLUTE, CSV_2019)
FILE_2020 =  os.path.join(ABSOLUTE, CSV_2020)
FILE_2021 =  os.path.join(ABSOLUTE, CSV_2021)
FILE_2022 =  os.path.join(ABSOLUTE, CSV_2022)

def remove_bin(df):
   for i in range(len(df)):
    if df.loc[i, "Data"].startswith("Bin"):
        df.loc[i, "Data"] = df.loc[i, "Data"][10:522]
   return df

   
def dat_clean():
    logger.info("loading the datasets...\n")

    rec_2017 = pd.read_csv(FILE_2017, parse_dates=['Start Time'])
    logger.info("2017 dataset loaded \n")

    rec_2018 = pd.read_csv(FILE_2018, parse_dates=['Start Time'])
    logger.info("2018 dataset loaded \n")

    rec_2019 = pd.read_csv(FILE_2019, parse_dates=['Start Time'])
    logger.info("2019 dataset loaded \n")

    rec_2020 = pd.read_csv(FILE_2020, parse_dates=['Start Time'])
    logger.info("2020 dataset loaded \n")

    rec_2021 = pd.read_csv(FILE_2021, parse_dates=['Start Time'])
    logger.info("2021 dataset loaded \n")

    rec_2022 = pd.read_csv(FILE_2022, parse_dates=['Start Time'])
    logger.info("2022 dataset loaded \n")

    logger.info("All datasets loaded \n")

    rec_full = pd.concat([rec_2017, rec_2018, rec_2019, rec_2020, rec_2021, rec_2022], axis = 0)

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