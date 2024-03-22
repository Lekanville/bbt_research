# bbt_research
Research on Basal Body Temperature

## Prerequisites 

#### Conda (required)
#### NodeJS (required)
#### DanfoJS (required)

## Setup

```bash
#Clone the Repo (use https if necessary)
git@github.com:MRCIEU/bbt_research.git
cd bbt_research

#Create the Conda Environment
conda env create -f environment.yml
conda activate bbt

#Add module directory to python path
cd code
pwd
export PYTHONPATH=$PYTHONPATH:pwd
```

## General
It is advised that you run each rule in the pipeline separately and sequentially when running the various sections of the pipeline for the first time. However, you can run the entire pipeline all at once also.
Two variable files have been created for the entire pipeline- One mainly for the preprocessing stages (variables_preprocessing.py for rules 1-9) and the other for the machine learning stages (variables_learning.py for rules 10-16). For each rule, ensure you provide the appropriate variables.
For all the rules, '''-c''' indicates the number of cores.

For a dry run of the entire pipeline - 

```bash
snakemake -n
```

To run the entire pipeline -

```bash
snakemake -c 1
```

## Rule 1 (data_clean): Initial Data Cleaning (variables - variables_preprocessing.py)
Add the following in the variables file and run the rule-
1. Specify the folder containing the raw temperatures (the temperature files are prefixed with "allrecordings")                                                                     
2. Define the output folder

```bash
snakemake -r data_clean -c 1
```
## Rule 2 (data_decrypt): Decrypt the Data Column (variables - variables_preprocessing.py)
The current batch size dor the decryption is set at 450000 (code/decrypt.js). You may also need to increase your memory size for this (check point 2 of potential issues below). You can monitor the decrption process on the console and also in "decryption_log" file. If there is a need to run rule 2 again without the need to run rule 1, just delete the log file (or copy it to a different location). Rule 2 will then be available for a re-run.
The variables for this rule are below-
1. The input folder is the same as the output of rule 1 (the data_clean rule). This will has been automated and you do not need to provide it again
2. Define the ouput folder. Can be anywhere but the same folder as the previous result is recommended.
3. The log will be created where the output folder is.

Run the rule with the code below.
```bash
snakemake -r data_decrypt -c 1
```

## Rule 3 (process_decrypt): Merge the Decrypted Data (variables - variables_preprocessing.py)
This rule merges the decrypted data. The variables and code are given below
1. The input folder is the same as the output of rule 2 (the data_decrypt rule). This has been automated
2. Define the ouput file. Can be anywhere but the same folder as the previous rule is recommended.

```bash
snakemake -r process_decrypt -c 1
```

## Rule 4 (sel_cr_1): Stage 2 Data Cleaning for the Nightly values (variables - variables_preprocessing.py)
This rule cleans ensures data quality by taking out the worng inputs and device initialization values. It then computes the mean of the night values. The variables and code are given below.
1. The input file must be the same as the output of rule 3 (merged_decrypted) - automated
2. Define the ouput file. Can be anywhere but the same folder as the previous rule is recommended.
3. Define the minimum number of true data (data that is not NaN,34500.0 or 0.0) in each daily record. This is necessary for row validity
4. Define the data start point (Nightly values before this point will be deleted)  

```bash
snakemake -r sel_cr_1 -c 1
```

## Rule 5 (sel_cr_2): Stage 3 Data Cleaning for the Cycles and Users (variables - variables_preprocessing.py)
This rule ensures data quality by ensuring that only cycles and users with a good number of data are included in the analysis. The variables and code are given below.
1. The input file must be the same as the output of the "sel_cr_1" rule (rule 4) - automated
2. Define the ouput file. Can be anywhere but the same folder as the previous rule is recommended. Note that is is a CSV file  
3. Define the minimum number of total temperature values across all cycles recorded for a user
4. Define the minimum number of daily temperatures that must be recorded in a cycle
5. Define the minimum number of cycles that must be recorded for a user  

```bash
snakemake -r sel_cr_2 -c 1
```

## For Rule 6 (process_cycles) - Processing the Cycles (variables - variables_preprocessing.py)
This rule reads the cycle data, merges the temperatures table with the cycles table, computes the cycle lengths, computes the temperature date offsets, and compute the duration of the temperature recordings for each cycle. The variables and code are given below.
1. The first input is the output of the "sel_cr_2" rule (rule 5) - automated
2. Specify the folder that contains the input cycles (the cycle files are prefixed with "allusercycles")
3. Specify the ouput file. Can be anywhere but the same folder as the previous rule is recommended

```bash
snakemake -r process_cycles -c 1
```


## For Rule 7 (process_questionnaire) - (variables - variables_preprocessing.py)
This rule reads the questionnaire file, cleans it (removes duplicates), codes the PCOS column,  and gets the following questionnaire variables; BMI, smoking, sleep and daily activities, the other ailments variables, the pregnancy-related variables, the menstruation-related variables, reads the cleaned temperatures dataset and adds the PCOS label for each user, and finally, save the cleaned questionnaire and the updated temperatures datasets. The variables and code are given below.
1. The first input is the questionnaire data (This is an excel file)
2. The second input is the output of the "process_cycles" rule (rule 6) - automated
3. Specify the ouput file for temperatures and duration. Can be anywhere but the same folder as the previous rule is recommended.
4. Specify the ouput file for cleaned questionnaire    

```bash
snakemake -r process_quest -c 1
```

## For Rule 8 (model_cycle) - 
The variable for this is defined in model_cycle.sh. It will select the data for the idividuals from the output of the "sel_cr_2" rule (rule 5). It create a reference cycle from these afterwards. If there is a need to add more cycles or remove some from the current set, please open code/normal_cycles_process/normal_cycles.py and add the User and Cycle IDs to be included in the referencing. You can then run the rule. For subsequent processing, there is no need to re-run this rule (except if list of refrence cycles are edited). Use the code below to run this rule.

```bash
snakemake -r model_cycle -c 1
```

## For Rule 9 (cycle_level_data) - (variables - variables_preprocessing.py)
This rule reads the temperatures dataset from "sel_crt_2" rule (rule 5), the "temp_dates_duration_pcos.csv" dataset from process_quest(rule 7) and combines them. It then gets actual day of each temperature in a cycle (with interpolation for missing days), the nadirs and peaks (and related data) by comparing the cycle with the reference cycle and the cycle lengths (and related data). The variables and code are given below.
1. The first input is the temperature dataset. This is the output of the "sel_cr_2" rule (rule 5)  - automated
2. The second input is the cycles dataset with PCOS column. This is the temp_dates_duration_pcos.csv from the output of the "process_questionnaire" rule (rule 7) - automated
3. Specify the file location of the model cycle which is the output of rule 8 (open model_cycle.sh to check).
4. Specify the ouput file. Can be anywhere but the same folder as the previous rule is recommended.  

```bash
snakemake -r cycle_level_data -c 1
```

## For Rule 10 (get_learning_variables) - (variables - variables_learning.py)
The rule reads the output file from the "cycle_level_data" rule (rule 9) as input and will output the features to a CSV file. After the the input is read the outliers on the peak day are trimmed upto 3 times the std after mean. Outliers on the nadir temp are equally trimmed upto 3 times the standard deviation before abd after the mean. Records that have their nadir days to be greater than 50 were also trimmed out. Records that have difference between their nadirs and peaks days as zero, incomplete cycles (mostly last cycles) and cycles with data lengths more than 101 are also taken out. The variables and code are given below.
1. The first input is the file containing the preprocessed temperatures data. This is the output of cycle_level_data (rule 9) - automated                                                                
2. Specify the output file to save the cycle-level variables.

```bash
snakemake -r get_learning_variables -c 1
```

## For Rule 11 (cycle_level_learning) - (variables - variables_learning.py)
This rule reads the output file from the "cycle_level_data" rule (rule 10) as input. Afterwards machine learning is carried out on the k-folds with cross validation and ROC for the cycle_level data. The results are then saved in the specified output folder. The variables and code are given below.
1. The first input is the file containing the dependent and independent variables of the cycle level data. This is the output of get_learning_variables rule (rule 10) - automated
3. Specify the number of k-splits

```bash
snakemake -r cycle_level_learning -c 1
```

## For Rule 12 (user_level_variables) - (variables - variables_learning.py)
This rule reads the output file from "cycle_level_data"rule (rule 10) as input. It then computes the user-level data. The user-level data are the average Pairwise distances and path lengths, the minimum cycle level features, the maximum cycle level features, the median cycle level features and the range of cycle level features. It then saves  user-level data. The variables and code are given below.
1. The first input is the file containing the dependent and independent variables of the cycle-level data. This the output of get_learning_variables rule (rule 10) - automated                                                              
2. Specify the output file to save the user-level variables.

```bash
snakemake -r user_level_variables -c 1
```

## For Rule 13 (user_level_learning) - (variables - variables_learning.py)
This rule reads the output file from the previous rule (user_level_data) as input. Afterwards machine learning is carried out on the k-folds with cross validation and ROC for the user-level data. The results are then saved in the specified output folder. The variables and code are given below.
1. The first input is the file containing the dependent and independent variables of the user-level data. This is the output of user_level_variables rule (rule 12) - automated                                       
2. Specify the output folder to save the machine learning results of the user-level learning
3. Specify the number of k-splits

```bash
snakemake -r user_level_learning -c 1
```
## For Rule 14 (preprocess_quest) - (variables - variables_learning.py)
The rule reads the cleaned questionnaire file as input. It then preprocesses it by taking out rows with missingness, categorizes the data, and then creates dummy variables for the categorical variables. It will then output a preprocessed set of variables as a CSV. 
1. The first input is the cleaned questionnaire data from the "process_questionnaire" rule (the "process_quest_cleaned" variable in rule 7) - automated
2. Specify the output file.

```bash
snakemake -r preprocess_quest -c 1
```

## For Rule 15 (quest_level_learning) - (variables - variables_learning.py)
The reads the output file of the preprocess_quest rule (rule 14) as input. Afterwards machine learning is carried out on the k-folds with cross validation and ROC for the questionnaire-level data. The results are then saved in the specified output folder. The variables and code are given below.
1. The first input is the file containing the dependent and independent variables of questionnaire data. This the output of the preprocess_quest rule (rule 14) - automated                                
2. Specify the output folder to save the learning results of the questionnaire-level learning
3. Specify the number of k-splits

```bash
snakemake -r quest_level_learning -c 1
```

## For Rule 16 (user_and_quest_level_learning) - (variables - variables_learning.py)
The rules reads the output of both the user_level_variables rule (rule 12) and the preprocess_quest rule (rule 14). It will combine both dataset and then perform machine learning on the combined dataset with k-folds cross validation and ROC. The results are then saved in the specified output folder. The variables and code are given below.
1. The first input is the file containing the dependent and independent variables of the user-level data. This is the output of user_level_variables rule (rule 12) - automated
2. The second input is the file containing the dependent and independent variables of the questionnaire data. This is the output of preprocess_quest rule (rule 14) - automated
3. Specify the output folder to save the combine learning results of the questionnaire level learning
4. Specify the number of k-splits

```bash
snakemake -r user_and_quest_level_learning -c 1
```

## Potential issues that could be met
1. AttributeError: module 'lib' has no attribute 'OpenSSL_add_all_algorithms'
Cause: This is caused by cryptography==39.0.0
Fix: As of the time of writing, downgrading to cryptography==38.0.4 fixes the problem.
From the CLI, enter this
```bash
pip install cryptography==38.0.4
```

2. FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
Cause: This is due to low memory on the computing system or a low allocted memory on the computing system
Fix: Increase the allocated memory of the computing system
Check the current allocated memory with the following
```
node -e 'console.log(v8.getHeapStatistics().heap_size_limit/(1024*1024))'
```
then increase memory allocation with 
export NODE_OPTIONS="--max-old-space-size=(X * 1024)" # Increase to X GB where X is the amount of memory in gigabytes
e.g.
```
export NODE_OPTIONS="--max-old-space-size=8192" # Increase to 8 GB
```