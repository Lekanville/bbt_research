rule targets:
    input:
        "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/cleaned.csv",
        "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/decrypted.csv",
        "code/decrypt_merge.py",
        "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/sel_crt_1.csv",
        "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/sel_crt_2.csv"

rule data_clean:
    input: 
        input_script = "code/dat_clean.py"
    output: 
        output_file = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/cleaned.csv"
    shell:"""
        python -m dat_clean > {output.output_file}
    """

rule data_decrypt:
    input: 
        input_dataset = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/cleaned.csv",
        input_script_js = "code/decrypt.js"

    output: 
        output_log = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/decryption_log",
        
    shell:"""
        node {input.input_script_js} > {output.output_log}
    """
rule process_decrypt:
    input:
        input_check = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/decryption_log",
        input_script_py = "code/decrypt_merge_2.py"
    output:
        output_file = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/decrypted.csv"
    shell:"""
        python -m decrypt_merge_2 > {output.output_file}
    """
rule sel_cr_1:
    input:
        input_file = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/decrypted.csv"
    output:
        output_file = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/sel_crt_1.csv"
    params:
        cr_1_1 = 30,
        cr_1_2 = 10,
        cr_1_3 = 3
    shell:"""
        python -m sel_crt_1 -d '{input.input_file}' -r {params.cr_1_1} -n {params.cr_1_2} -c {params.cr_1_3} > {output.output_file}
        """
rule sel_cr_2:
    input:
        input_file = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/sel_crt_1.csv"
    output:
         output_file = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/sel_crt_2.csv"
    params:
        cr_2_1 = 10,
        cr_2_2 = 5,
    shell:"""
        python -m sel_crt_2 -d '{input.input_file}' -x {params.cr_2_1} -y {params.cr_2_2} > {output.output_file}
        """