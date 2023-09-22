#################################################################
#####Define all variables here according to the instructions#####
#################################################################

class Variables:
        ############################################################################################
    ### For Rule 1 (data_clean) - 
    ### 1. Specify the folder of the input temperatures (the temperature files are prefixed with 
    ###     "allrecordings"                                                                      
    ### 2. Define the output folder
        ############################################################################################
    data_clean_input_folder = "/projects/MRC-IEU/research/data/fertility_focus/ovusense/released/2022-11-30/data/temperature/"
    data_clean_output_folder =  "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/"


        #############################################################################################
    ### For Rule 2 (data_decrypt) -  
    ### 1. The input folder must be the same as the output of rule 1 (the data_clean rule) 
    ### 2. Define the ouput folder. Can be anywhere but the same folder as the previous result is 
    ###     reccommended
    ### 3. The log will be created where the output folder is. You do not need to edit this. 
    ###     If there is ever a need to run rule 2 again without the need to run rule 1, just
    ###     delete the log file. Rule 2 will then be availabe for a rerun.                       
        #############################################################################################
    data_decrypt_output = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/decrypted/"
    

        #############################################################################################
    ### For Rule 3 (merged_decrypted) - 
    ### 1. The input folder must be the same as the output of rule 2 (the data_decrypt rule)
    ### 2. Define the ouput file. Can be anywhere but the same folder as the previous rule is 
    ###     reccommended. Note that is is a CSV file                   
        #############################################################################################
    merged_decrypted_output = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/merged_decrypted.csv"  

        #############################################################################################
    ### For Rule 4 (sel_cr_1) -
    ### 1. The input file must be the same as the output of the "merged_decrypted" rule (rule 3)
    ### 2. Define the ouput file. Can be anywhere but the same folder as the previous rule is 
    ###     reccommended. Note that is is a CSV file  
    ### 3. Define the minimum number of true data (not NaN,34500.0 or 0.0) for row validity
    ### 4. Define the data start point (takes out temperature data before this point)                   
        #############################################################################################
    sel_cr_1_output = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/sel_crt_1.csv"
    min_number_of_true_temp_values = 10
    init_point = 5

        #############################################################################################
    ### For Rule 5 (sel_cr_2) -  
    ### 1. The input file must be the same as the output of the "sel_cr_1" rule (rule 4)
    ### 2. Define the ouput file. Can be anywhere but the same folder as the previous rule is 
    ###     reccommended. Note that is is a CSV file  
    ### 3. Define the minimum number of true data (not NaN,34500.0 or 0.0) for row validity
    ### 4. Define the data start point (takes out temperature data before this point)                   
        #############################################################################################
    sel_cr_2_output = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/sel_crt_2.csv"
    min_number_of_total_record_days = 30
    min_days_on_cycle = 10
    min_cycles_for_user = 3

        #############################################################################################
    ### For Rule 6 (process_cycles) - 
    ### 1. The first input is the output of the "sel_cr_1" rule (rule 5)
    ### 2. Specify the folder of the input cycles (the cycle files are prefixed with "allusercycles"
    ### 3. Specify the ouput file. Can be anywhere but the same folder as the previous rule is 
    ###     reccommended. Note that is is a CSV file                  
        #############################################################################################
    process_cycles_input_folder = "/projects/MRC-IEU/research/data/fertility_focus/ovusense/released/2022-11-30/data/temperature/"
    process_cycles_output = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/temp_dates_duration.csv"

      #############################################################################################
    ### For Rule 7 (process_quationnaire) - 
    ### 1. The first input is the questionnaire data (This is an excel file)
    ### 2. The second input is the output of the "sel_cr_2" rule (rule 6)
    ### 3. Specify the ouput file. Can be anywhere but the same folder as the previous rule is 
    ###     reccommended. Note that is is a CSV file         
        #############################################################################################
    process_quest_input_file = "/projects/MRC-IEU/research/data/fertility_focus/ovusense/released/2022-11-30/data/uob-questionnaire/OvuSense_Cycle_Characteristics_Study-Survey-to_18NOV22_anon.xlsx"
    process_quest_output = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/temp_dates_duration_pcos.csv"


        #############################################################################################
    ### For Rule 8 (model_cycle) - 
    ### The variable for this is defined in model_cycle.sh. The only variable to add is the processed
    ### temperature data from "sel_cr_2". There may not be a need to run this process recurrently.
    ### If there is a need to add more to the normal cycles or remove some cycles from 
    ### current set, please open code/normal_cycles_process/normal_cycles.py and add the User and
    ### and Cycle IDs to be added. YOu an the rerun this rule.
        #############################################################################################




#######################################You do not need to edit aything beyond this point#######################################
    #rule 1 data
    data_clean_input_folder = data_clean_input_folder
    data_clean_output_file = data_clean_output_folder + "data_cleaned.csv"
    data_cleaning = {"input_folder":data_clean_input_folder,
                    "output_file": data_clean_output_file
    }
    
    #rule 2 data
    data_decryption_input_file = data_clean_output_file
    data_decryption_output_folder = data_decrypt_output
    data_decryption_output_log =  data_decrypt_output+"decryption_log.txt"
    data_decryption = {
        "input_file":data_decryption_input_file,
        "output_folder":data_decryption_output_folder,
        "log":data_decryption_output_log
    }

    #rule 3 data
    merged_decrypted_input_folder = data_decryption_output_folder
    merged_decrypted_output_file = merged_decrypted_output
    merged_decrypted = {
        "input_folder":merged_decrypted_input_folder,
        "output_file":merged_decrypted_output_file
    }


    #rule 4 data
    sel_cr_1_input_file = merged_decrypted_output_file
    sel_cr_1_output_file = sel_cr_1_output
    cr_1_1 = min_number_of_true_temp_values
    cr_1_2 = init_point
    sel_cr_1 = {
        "input_file":sel_cr_1_input_file,
        "output_file":sel_cr_1_output_file,
        "cr_1_1":cr_1_1,
        "cr_1_2":cr_1_2
    }

    #rule 5 data
    sel_cr_2_input_file = sel_cr_1_output_file
    sel_cr_2_output_file = sel_cr_2_output
    cr_2_1 = min_number_of_total_record_days
    cr_2_2 = min_days_on_cycle
    cr_2_3 = min_cycles_for_user
    sel_cr_2 = {
        "input_file":sel_cr_2_input_file,
        "output_file":sel_cr_2_output_file,
        "cr_2_1":cr_2_1,
        "cr_2_2":cr_2_2,
        "cr_2_3":cr_2_3,
    }

    #rule 6 data
    process_cycles_input_cycles =  process_cycles_input_folder
    process_cycles_input_temps = sel_cr_2_output_file
    process_cycles_output_file = process_cycles_output
    process_cycles = {
        "input_folder":process_cycles_input_cycles,
        "input_file":process_cycles_input_temps,
        "output_file":process_cycles_output_file
    }

    #rule 7 data
    process_quest_input_quest =  process_quest_input_file
    process_quest_input_cycles = process_cycles_output_file
    process_quest_output_file = process_quest_output
    process_quest = {
        "input_file":process_quest_input_quest,
        "input_cycles":process_quest_input_cycles,
        "output_file":process_quest_output_file,
    }
    
    #rule 8 need no furthe processing

variables = Variables()