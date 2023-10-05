#!python
#!/usr/bin/env python3

#############################################################################################
#The “learning_variables.py” script - this is for standardization
#The script expects the output file from the previous rule (cycle_level_data) as input and will 
#output the features to a CSV file. After the the input is read the user level data is computed
#from the cycle level data.
#############################################################################################

import numpy as np
import pandas as pd
import os
import argparse

import tools.tools as tools

parser = argparse.ArgumentParser(description= "A script to filter data")
parser.add_argument('-i', '--input_file', type=str, required=True, help= 'The input dataset')
parser.add_argument('-o', '--output_file', type=str, required=True, help= 'The output dataset')

def the_user_level_variables(INPUT, OUTPUT):
    

if __name__ == "__main__":
    args = parser.parse_args()
    the_user_level_variables(args.input_file, args.output_file)