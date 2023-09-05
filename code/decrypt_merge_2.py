#! usr/bin/env python3

#############################################################################################
#The “decrypt_merge.py” script
#The script expects the folder that contains the decrypted files from the previous rule 
#(decrypt.js) and will output the merged file as specified. Each decrypted CSV file is 
#converted into a multidimensional list. Each row in the multidimensional list is a daily 
#temperature record. The actual decrypted values (data) are selected from each row and 
#appropriately added to the row. The encrypted data is then deleted.
#Afterwards, the records are then converted into a data frame and concatenated. The result 
#is then outputted. 
#############################################################################################

import numpy as np
import pandas as pd
import os
import glob
import csv
from loguru import logger
import argparse

parser = argparse.ArgumentParser(description='A script for initial data cleaning')
parser.add_argument('-i','--input_folder', type=str, required=True, help='The input dataset')
parser.add_argument('-o','--output_file', type=str, required=True, help='The output file')


def decrypt_merge(INPUT_FOLDER, OUTPUT_FILE):
    decrytped_path = os.path.join(INPUT_FOLDER, "*.csv") 
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

    df.to_csv(OUTPUT_FILE)

if __name__ == "__main__":
    args = parser.parse_args()
    decrypt_merge(args.input_folder, args.output_file)