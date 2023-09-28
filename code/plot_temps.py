#!usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import os
import argparse
from loguru import logger

OUT_FILE = "/projects/MRC-IEU/research/projects/ieu2/p6/063/working/data/results/images"
parser = argparse.ArgumentParser(description="A script to plot cycle temperatures")
parser.add_argument("-d", "--data", type=str, required=True, help="The dataset")

def plot_temps(file):
    df = pd.read_csv(file)
    cycles = list(df.groupby("Cycle ID").first().index)
    rand_20_cycles = list(np.random.choice(cycles, 20))

    j = 0
    for i in rand_20_cycles:
        fig =plt.figure(figsize=(10,7))
        ax_j = fig.add_axes([0,0,1,1])
        df_i = df[df["Cycle ID"] == i][["Date","Mean_Temp"]]\
                .sort_values("Date").reset_index(drop = True)
        smooth_i = savgol_filter(df_i["Mean_Temp"], len(df_i), 4)
        ax_j.plot(list(range(len(df_i))), df_i["Mean_Temp"], "o", label = "Temperature")
        ax_j.plot(list(range(len(df_i))), smooth_i, "r", label = "Smooth")
        ax_j.set_xlabel('Cycle Day')
        ax_j.set_ylabel('Temp(°C)')
        ax_j.set_title('Mean and Smooth Mean Cycle Length')
        ax_j.legend(loc=0)
        plt.savefig(os.path.join(OUT_FILE, i+".jpg"), bbox_inches='tight', dpi=150)
        logger.info("Cycle ID: "+i+" plotted")
        j+=1
    
if __name__ == "__main__":
    args = parser.parse_args()
    plot_temps(args.data)
