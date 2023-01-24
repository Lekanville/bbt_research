rule targets:
    input:
        "data/sel_crt_1.csv",
        "data/sel_crt_2.csv"

rule sel_cr_1:
    input:
        input_file = "data/all_recordings.csv"
    output:
        output_file = "data/sel_crt_1.csv"
    params:
        cr_1_1 = 30,
        cr_1_2 = 10,
        cr_1_3 = 3
    shell:"""
        python -m sel_crt_1 -d '{input.input_file}' -r {params.cr_1_1} -n {params.cr_1_2} -c {params.cr_1_3} > {output.output_file}
        """
rule sel_cr_2:
    input:
        input_file = "data/sel_crt_1.csv"
    output:
         output_file = "data/sel_crt_2.csv"
    params:
        cr_2_1 = 10,
        cr_2_2 = 5,
    shell:"""
        python -m sel_crt_2 -d '{input.input_file}' -x {params.cr_2_1} -y {params.cr_2_2} > {output.output_file}
        """