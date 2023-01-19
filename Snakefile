include: "sel_crt_1.py"

rule sel_cr_1:
    input:
        data = "data/all_recordings.csv"
    output:
        "data/sel_crt_1.csv"
    params:
        cr_1 = 30,
        cr_2 = 10,
        cr_3 = 3
    run:
        shell(process_temp("input.data", {params.cr_1}, {params.cr_2}, {params.cr_3}))

