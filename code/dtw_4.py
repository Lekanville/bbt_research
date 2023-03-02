from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np

from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

# Read stored audio files for comparison
fs_1, data_1 = wavfile.read("../data/clip1.wav")
fs_2, data_2 = wavfile.read("../data/clip2.wav")
fs_3, data_3 = wavfile.read("../data/clip3.wav")
fs_4, data_4 = wavfile.read("../data/clip4.wav")

# Take the max values along axis
data1 = np.amax(data_1, axis=1)
data2 = np.amax(data_2, axis=1)
data3 = np.amax(data_3, axis=1)
data4 = np.amax(data_4, axis=1)

#get the distance
#print (fastdtw(data1, data2)[0])

# Set plot style
plt.style.use('seaborn-whitegrid')

# Create plots
plt.plot(data_1, "#67A0DA")
plt.plot(data_2, "r", alpha=0.05)
plt.plot(data_3, "g", alpha=0.1)
plt.plot(data_4, "y", alpha=0.1)


fig=plt.show()
plt.savefig("../data/clips2.png")
#display(fig)