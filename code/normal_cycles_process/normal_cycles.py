#This contains a list of cycles that appears to be normal. The essence of this is to average the 
# "normal" cycles to obtain a model for comparison with other cycles. you can add more or remove
# from the current ones and run rule 8 of the snakefile (only if results from rule 5 have been)
# obtained.
#

class Normal:
    ################The curation was done manually######################
    normal_cycles = [
                    ["user", "cycle"]
                    ["user", "cycle"]
                    ["user", "cycle"]
                    ["user", "cycle"]
                    ]

normal = Normal().normal_cycles