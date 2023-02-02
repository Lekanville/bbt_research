#! usr/bin/env python3

import numpy as np
import pandas as pd
import os
import glob
import csv
from loguru import logger

ABSOLUTE = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/decrypted"
OUT_FILE = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/"

decrytped_path = os.path.join(ABSOLUTE, "*.csv") 
decrytped_files = glob.glob(decrytped_path)

df = pd.DataFrame()
for f in decrytped_files:
    with open(f, "r") as file:
        csv_file=csv.reader(file)
        records = list(csv_file)

        if (len(records[0]) < 199):
            pad_top = []
            for i in range(199-len(records[0])):
                pad_top.append("Data"+str(i))
            records[0][6:7] += pad_top 

        for row in records[1:]:
            if (len(row) < 199):
                pad_body = []
                for i in range(199-len(row)):
                    pad_body.append("NaN")
                row[-1:-2] += pad_body     

        for row in records:
            if (len(row) != 199):
                print(row)
        

        data = pd.DataFrame(records)
    df = pd.concat([df, data], ignore_index=True, axis = 0)
    file_name = f.split("/")[-1]
    logger.info(file_name+" has been decrypted and stored")
        

# read the csv file
print(df.head())
print(df.info())

#decrytped = pd.concat(map(pd.read_csv, decrytped_files), ignore_index = True)

#decrytped.to_csv(os.path.join(OUT_FILE, "decrypted.csv"))