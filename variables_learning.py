#####################################################################
#####Define all learning variables accroding to the instructions#####
#####################################################################
from variables_preprocessing import variables

class Learning:
        ############################################################################################
    ### For Rule 10 (get_learning_variables) - 
    ### 1. The first input is the file containing the preprocessed data - the output of 
    ### cycle_level_data (rule 9)                                                                    
    ### 2. Specify the output file
        ############################################################################################"
    get_learning_variables_output =  "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/features_learning.csv"
    #get_learning_variables_output =  "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/features_learning_MM.csv"

        ############################################################################################
    ### For Rule 11 (cycle_level_learning) - 
    ### 1. The first input is the file containing the dependent and independent variables of the cycle level data
    ###  - the output of get_learning_variables (rule 10)                                                                    
    ### 2. Specify the output folder to save the learning results of the cycle level learning
    ###  3. Specify the number of k-splits
        ############################################################################################"
    cycle_level_learning_results =  "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/cycle_learning_results/"
    cycle_level_learning_number_of_k_splits =  10

        ############################################################################################
    ### For Rule 12 (user_level_variables) - 
    ### 1. The first input is the file containing the dependent and independent variables
    ###  - the output of get_learning_variables (rule 10)                                                                    
    ### 2. Specify the output folder to save the learning results of the user level data
        ############################################################################################"
    user_level_variables_output =  "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/user_level_variables.csv"

        ############################################################################################
    ### For Rule 13 (user_level_learning) - 
    ### 1. The first input is the file containing the dependent and independent variables of the user level data
    ###  - the output of get_learning_variables (rule 12)                                                                    
    ### 2. Specify the output folder to save the learning results of the user level learning
    ##  3. Specify the number of k-splits
        ############################################################################################"
    user_level_learning_results =  "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/user_learning_results/"
    user_level_learning_number_of_k_splits =  10

        ############################################################################################
    ### For Rule 14 (preprocess_quest rule) - 
    ### 1. The first input is the cleaned questionnaire data - from Rule 7 (process_questionnaire) i.e process_quest_cleaned
    ### 2. Specify the output file. This should be a CSV file
        ############################################################################################"
    #get_BMI_input = "/projects/MRC-IEU/research/data/fertility_focus/ovusense/released/2022-11-30/data/uob-questionnaire/OvuSense_Cycle_Characteristics_Study-Survey-to_18NOV22_anon.xlsx"
    quest_preprocessed_output = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/df_questionnaire_ml.csv"

        ############################################################################################
    ### For Rule 15 (quest_level_learning) - 
    ### 1. The first input is the file containing the dependent and independent variables
    ###  - the output of preprocess_quest rule (rule 14)                                                                    
    ### 2. Specify the output folder to save the learning results of the questionnaire level learning
    ##  3. Specify the number of k-splits
        ############################################################################################"
    quest_level_learning_results =  "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/quest_learning_results/"
    quest_level_learning_number_of_k_splits =  10


        ############################################################################################
    ### For Rule 16 (user_and_quest_level_learning) - 
    ### 1. The first input is the file containing the dependent and independent variables of the user level data
    ###  - the output of get_learning_variables (rule 12) 
    ### 2. The second input is the file containing the dependent and independent variables of the questionnaire data
    ###  - the output of preprocess_quest rule (rule 14)                                                                    
    ### 2. Specify the output folder to save the learning results of the questionnaire level learning
    ##  3. Specify the number of k-splits
        ############################################################################################"
    user_and_quest_level_learning_results =  "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/user_and_quest_learning_results/"
    user_and_quest_level_learning_number_of_k_splits =  10


#######################################You do not need to edit aything beyond this point#######################################
    #rule 10 data
    get_learning_variables_input_file = variables.cycle_level_data["output_file"]
    get_learning_variables_output_file = get_learning_variables_output
    get_learning_variables = {"input_file":get_learning_variables_input_file,
                    "output_file": get_learning_variables_output_file
    }

    #rule 11 data
    cycle_level_learning_input_file = get_learning_variables_output_file
    cycle_level_learning_output_folder = cycle_level_learning_results
    #cycle_level_learning_output_log = cycle_level_learning_output_folder + "log"
    cycle_level_learning_number_of_k_splits = cycle_level_learning_number_of_k_splits
    cycle_level_learning = {"input_file":cycle_level_learning_input_file,
                    "output_folder": cycle_level_learning_output_folder,
                    "number_of_splits":cycle_level_learning_number_of_k_splits,
                    #"log": cycle_level_learning_output_log
    }

    #rule 12 data
    user_level_variables_input_file = get_learning_variables_output_file
    user_level_variables_output = user_level_variables_output
    user_level_variables = {"input_file":user_level_variables_input_file,
                                    "output_file":user_level_variables_output}

    #rule 13 data
    user_level_learning_input_file = user_level_variables_output
    user_level_learning_output_folder = user_level_learning_results
    user_level_learning_number_of_k_splits = user_level_learning_number_of_k_splits
    user_level_learning = {"input_file":user_level_learning_input_file,
                    "output_folder":user_level_learning_output_folder,
                    "number_of_splits":user_level_learning_number_of_k_splits,
                    #"log": cycle_level_learning_output_log
    }

    #rule 14 data
    quest_preprocess_input = variables.process_quest["output_file_2"]
    quest_preprocessed_output = quest_preprocessed_output
    preprocess_quest = {"input_file":quest_preprocess_input,
                    "output_file":quest_preprocessed_output
    }

    #rule 15 data
    quest_level_learning_input_file = quest_preprocessed_output
    quest_level_learning_output_folder = quest_level_learning_results
    quest_level_learning_number_of_k_splits = quest_level_learning_number_of_k_splits
    quest_level_learning = {"input_file":quest_level_learning_input_file,
                    "output_folder":quest_level_learning_output_folder,
                    "number_of_splits":quest_level_learning_number_of_k_splits,
                    #"log": cycle_level_learning_output_log
    }

    #rule 16 data
    user_and_quest_level_learning_input_file_1 = user_level_variables_output
    user_and_quest_level_learning_input_file_2 = quest_preprocessed_output
    user_and_quest_level_learning_output_folder = user_and_quest_level_learning_results
    user_and_quest_level_learning_number_of_k_splits = user_and_quest_level_learning_number_of_k_splits
    user_and_quest_level_learning = {"input_file_1":user_and_quest_level_learning_input_file_1,
                    "input_file_2":user_and_quest_level_learning_input_file_2,
                    "output_folder":user_and_quest_level_learning_output_folder,
                    "number_of_splits":quest_level_learning_number_of_k_splits,
                    #"log": cycle_level_learning_output_log
    }
learning = Learning()