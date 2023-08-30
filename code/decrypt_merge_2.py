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
        csv_file = csv.reader(file)
        records = list(csv_file)
        for row in records[1:]:
            data = row[6:-1]
            row[-1:-2] += [data]
            del row[6:-2]
        data = pd.DataFrame(records[1:], columns = records[0])
    df = pd.concat([df, data], ignore_index=True, axis = 0)
    file_name = f.split("/")[-1]
    logger.info(file_name+" has been decrypted and merged")
    os.remove(f)

df.to_csv(os.path.join(OUT_FILE,"decrypted.csv"))