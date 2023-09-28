#####################################################################
#####Define all learning variables accroding to the instructions#####
#####################################################################
from variables_preprocessing import variables

class Learning:
        ############################################################################################
    ### For Rule 10 (get_learning_variables) - 
    ### 1. The first input is the file containing the preprocessed data - the output of 
    ### cycle_level_data (rule 9)                                                                    
    ### 2. Specify the output folder
        ############################################################################################"
    get_learning_variables_output =  "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/features_learning.csv"
    #get_learning_variables_output =  "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/features_learning_MM.csv"

        ############################################################################################
    ### For Rule 11 (cycle_level_learning_results) - 
    ### 1. The first input is the file containing the preprocessed data - the output of 
    ### cycle_level_data (rule 9)                                                                    
    ### 2. Specify the output folder
        ############################################################################################"
    cycle_level_learning_results_folder =  "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/learning_results/"

#######################################You do not need to edit aything beyond this point#######################################
    #rule 10 data
    get_learning_variables_input_file = variables.cycle_level_data["output_file"]
    get_learning_variables_output_file = get_learning_variables_output
    get_learning_variables = {"input_file":get_learning_variables_input_file,
                    "output_file": get_learning_variables_output_file
    }


learning = Learning()