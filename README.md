# bbt_research
Research on Basal Body Temperature

## Prerequisites 

#### Conda (required)

## Setup

"""bash
#Clone the Repo (use https if necessary)
git clone git@github.com:Lekanville/bbt_research.git
cd bbt_research

#Create the Conda Environment
conda env create -f environment.yml
conda activate bbt

#Choose Data Selection Criteria
Open Snakefile
1. Select parameters in "rule sel_cr_1"
    cr_1_1 = Clean out users with records that is less than the selected days
    cr_1_2 = Clean out cycles with less the selected number of days
    cr_1_3 = Clean out users with less than the selected number of cycles

2. Select parameters in "rule sel_cr_2"
    cr_2_1 = Clean out days with less than the specified number of actisl temperature readings (Temperatures that are not zero and not 34500)
    cr_2_2 = Clean out the first set of specified temperature values

#Run the Data Selection Worflow (you can specify the number of core to use with the -c command)

snakemake -r targets -c 1
"""

