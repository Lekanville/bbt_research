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
## Task 1: Clean the Data
Run the data cleaning rule (you can specify the number of cores to use with the -c command)
```
snakemake -r data_clean -c 1
```
## Task 2: Decrypt the Data Column
1. Open code/decrypt.js and define the batchsize for the decryption. The set defauult value is 450000

2. Run the data decrypting rule (you can specify the number of core to use with the -c command). You may also need to increase your memory size for this (check point 2 of potential issues below). You can monitor the decrption process my monitorin the "decryption_log" file.

3. You can monitor the decryption progress in the "decryption_log" file and on the console
```
snakemake -r data_decrypt -c 1
```

## Task 3: Prepare and Merge the Decrypted Data
Run the rule to prepare and merge the decrypted data (you can specify the number of core to use with the -c command)
```
snakemake -r process_decrypt -c 1
```

## Task 4: Choose Data Selection Criteria
Open Snakefile
1. Select parameters in "rule sel_cr_1"
    * cr_1_1 = Minimum number of true data (Temperatures that are not zero and not 34500)
    * cr_1_2 = Number of initial data to take out

2. Select parameters in "rule sel_cr_2"
    * cr_2_1 = Minimum number of record days
    * cr_2_2 = Minimum number of days in a cycle
    * cr_2_3 = Minimum number of cycles for a user

Data selection workflow can be run both at once by running the second rule  (you can specify the number of core to use with the -c command)

```bash
snakemake -r sel_cr_2 -c 1
```

or each rule at a time

```bash
snakemake -r sel_cr_1 -c 1
```

then

```bash
snakemake -r sel_cr_2 -c 1
```

## Potential issues that could be met
1. AttributeError: module 'lib' has no attribute 'OpenSSL_add_all_algorithms'
Cause: This is caused by cryptography==39.0.0
Fix: As of the time of writing, downgrading to cryptography==38.0.4 fixes the problem.
From the CLI, enter this
```
pip install cryptography==38.0.4
```

2. FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
Cause: This is due to low memory on the computing system or a low allocted memeory on the computing system
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