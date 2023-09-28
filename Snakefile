#!python
#!/usr/bin/env python3

from variables_preprocessing import variables
from variables_learning import learning

rule targets:
    input:
        variables.merged_decrypted["output_file"],
        variables.sel_cr_1["output_file"],
        variables.sel_cr_2["output_file"],
        variables.process_cycles["output_file"],
        variables.process_quest["output_file"],
        variables.cycle_level_data["model_cycle"],
        variables.cycle_level_data["output_file"],
        learning.get_learning_variables["output_file"]

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
        output_file = variables.process_quest["output_file"]
    shell:"""
        python -m process_quest -i '{input.input_file}' -j '{input.input_cycles}' -o {output.output_file}
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