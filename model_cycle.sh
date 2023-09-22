#!usr/bin/env bash

#please ensure you have obtained results from  executed rule 5 from the snakefile before
#executing this script (also to be executed from the snake file). You need to defime the 
#location of the result from rule 5 below (-i)

mkdir -p data
python -m normal_cycles_process.model_cycle \
-i /projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/sel_crt_2.csv