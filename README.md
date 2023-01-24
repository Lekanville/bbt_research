# bbt_research
Research on Basal Body Temperature

## Prerequisites 

#### Conda (required)

## Setup

```bash
#Clone the Repo (use https if necessary)
git clone git@github.com:Lekanville/bbt_research.git
cd bbt_research

#Create the Conda Environment
conda env create -f environment.yml
conda activate bbt

#Add module directory to python path
cd code
pwd
export PYTHONPATH=$PYTHONPATH:pwd
```

## Choose Data Selection Criteria

Open Snakefile
1. Select parameters in "rule sel_cr_1"
    * cr_1_1 = Minimum number of record days
    * cr_1_2 = Minimun number of days in a cycle
    * cr_1_3 = Minimum number of cycles for a user

2. Select parameters in "rule sel_cr_2"
    * cr_2_1 = Minimun number of true data (Temperatures that are not zero and not 34500)
    * cr_2_2 = Number of initial data to take out

## Run the Data Selection Worflow (you can specify the number of core to use with the -c command)

```bash
snakemake -r targets -c 1
```

