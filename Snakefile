#!python
#!/usr/bin/env python3

from variables_preprocessing import variables
from variables_learning import learning

rule targets:
    input:
        ##variables.merged_decrypted["output_file"],
        #variables.sel_cr_1["output_file"],
        #variables.sel_cr_2["output_file"],
        #variables.process_cycles["output_file"],
        #variables.process_quest["output_file"],
        #variables.cycle_level_data["model_cycle"],
        #variables.cycle_level_data["output_file"],
        #learning.get_learning_variables["output_file"],
        learning.cycle_level_learning["output_folder"],
        #learning.user_level_variables["output_file"],
        learning.user_level_learning["output_folder"],
        #learning.get_BMI["output_file"]
        learning.quest_level_learning["output_folder"],
        learning.user_and_quest_level_learning["output_folder"]

rule data_clean:
    input: 
        input_folder = variables.data_cleaning["input_folder"],
        
    output: 
        output_file = variables.data_cleaning["output_file"]

    shell:"""
        python -m dat_clean -i '{input.input_folder}' -o '{output.output_file}'
    """

rule data_decrypt:
    input:
        input_script_js = "code/decrypt.js",
        input_file = variables.data_decryption["input_file"],

    output:
        output_folder = directory(variables.data_decryption["output_folder"]), 
        output_log = variables.data_decryption["log"]
        
    shell:"""
        node {input.input_script_js} {input.input_file} {output.output_folder} > {output.output_log}
    """
rule merged_decrypted:
    input:
        input_folder = variables.merged_decrypted["input_folder"]
    output:
        output_file = variables.merged_decrypted["output_file"]
    shell:"""
         python -m decrypt_merge_2 -i '{input.input_folder}' -o '{output.output_file}'
    """
rule sel_cr_1:
    input:
        input_file = variables.sel_cr_1["input_file"]
    output:
         output_file = variables.sel_cr_1["output_file"]
    params:
        cr_1_1 = variables.sel_cr_1["cr_1_1"],
        cr_1_2 = variables.sel_cr_1["cr_1_2"],
    shell:"""
        python -m sel_crt_1 -i '{input.input_file}' -o '{output.output_file}' -x {params.cr_1_1} -y {params.cr_1_2} > {output.output_file}
        """
rule sel_cr_2:
    input:
        input_file = variables.sel_cr_2["input_file"]
    output:
        output_file = variables.sel_cr_2["output_file"]
    params:
        cr_2_1 = variables.sel_cr_2["cr_2_1"],
        cr_2_2 = variables.sel_cr_2["cr_2_2"],
        cr_2_3 = variables.sel_cr_2["cr_2_3"]
    shell:"""
        python -m sel_crt_2 -i '{input.input_file}' -o {output.output_file} -r {params.cr_2_1} -n {params.cr_2_2} -c {params.cr_2_3} > {output.output_file}
        """

rule process_cycles:
    input:
        input_folder = variables.process_cycles["input_folder"],
        input_file = variables.process_cycles["input_file"]
    output:
        output_file = variables.process_cycles["output_file"]
    shell:"""
        python -m process_cycles -i '{input.input_folder}' -j '{input.input_file}' -o {output.output_file} > {output.output_file}
    """

rule process_quest:
    input:
        input_file = variables.process_quest["input_file"],
        input_cycles = variables.process_quest["input_cycles"]
    output:
        output_temps_dur = variables.process_quest["output_file_1"],
        output_quest = variables.process_quest["output_file_2"]
    shell:"""
        python -m process_quest -i '{input.input_file}' -j '{input.input_cycles}' -o {output.output_temps_dur} -q {output.output_quest} 
    """

rule model_cycle:
    input:
        input_file = "model_cycle.sh"
    output:
        output_file = variables.cycle_level_data["model_cycle"]
    shell:"""
        sh '{input.input_file}'
    """

rule cycle_level_data:
    input:
        input_temps = variables.cycle_level_data["input_temps"],
        input_cycles = variables.cycle_level_data["input_cycles"],
        model_cycle = variables.cycle_level_data["model_cycle"]
    output:
        output_file = variables.cycle_level_data["output_file"]
    shell:"""
        python -m nadirs_and_peaks -i '{input.input_temps}' -j '{input.input_cycles}' -m {input.model_cycle} -o {output.output_file}
    """

rule get_learning_variables:
    input: 
        #input_temps = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/features_dtw_MM.csv"
        input_temps = learning.get_learning_variables["input_file"]
    output:
        output_file = learning.get_learning_variables["output_file"]
        #python -m learning_variables_MM -i {input.input_temps} -o {output.output_file}
    shell:"""
        python -m learning_variables -i {input.input_temps} -o {output.output_file}
    """

rule cycle_level_learning:
    input: 
        input_variables = learning.cycle_level_learning["input_file"]
    params:
        input_splits = learning.cycle_level_learning["number_of_splits"]
    output:
        output_file = directory(learning.cycle_level_learning["output_folder"])
        #output_log = learning.cycle_level_learning_variable["log"]
    shell:"""
        python -m cycle_level_learning -i {input.input_variables} -k {params.input_splits} -o {output.output_file}
    """

rule user_level_variables:
    input: 
        input_variables = learning.user_level_variables["input_file"]
    output:
        output_file = learning.user_level_variables["output_file"]
    shell:"""
        python -m user_level_variables -i {input.input_variables} -o {output.output_file}
    """

rule user_level_learning:
    input: 
        input_variables = learning.user_level_learning["input_file"]
    params:
        input_splits = learning.user_level_learning["number_of_splits"]
    output:
        output_file = directory(learning.user_level_learning["output_folder"])
    shell:"""
        python -m user_level_learning -i {input.input_variables} -k {params.input_splits} -o {output.output_file}
    """

rule preprocess_quest:
    input: 
        input_file = learning.preprocess_quest["input_file"]
    output:
        output_file = learning.preprocess_quest["output_file"]
    shell:"""
        python -m quest_preprocess -i {input.input_file} -o {output.output_file}
    """

rule quest_level_learning:
    input: 
        input_variables = learning.quest_level_learning["input_file"]
    params:
        input_splits = learning.quest_level_learning["number_of_splits"]
    output:
        output_file = directory(learning.quest_level_learning["output_folder"])
    shell:"""
         python -m quest_level_learning -i {input.input_variables} -k {params.input_splits} -o {output.output_file}
    """

rule user_and_quest_level_learning:
    input: 
        input_variables_1 = learning.user_and_quest_level_learning["input_file_1"],
        input_variables_2 = learning.user_and_quest_level_learning["input_file_2"]      
    params:
        input_splits = learning.user_and_quest_level_learning["number_of_splits"]
    output:
        output_file = directory(learning.user_and_quest_level_learning["output_folder"])
    shell:"""
         python -m user_and_quest_learning -i {input.input_variables_1} -j {input.input_variables_2} -k {params.input_splits} -o {output.output_file}
    """