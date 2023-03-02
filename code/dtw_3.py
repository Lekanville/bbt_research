from scipy.io import wavfile
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

# Read stored audio files for comparison
fs_1, data_1 = wavfile.read("../data/clip1.wav")
fs_2, data_2 = wavfile.read("../data/clip2.wav")
fs_3, data_3 = wavfile.read("../data/clip3.wav")
fs_4, data_4 = wavfile.read("../data/clip4.wav")

# Set plot style
plt.style.use('seaborn-whitegrid')

# Create subplots
#ax = plt.subplot(2, 2, 1)
#ax.plot(data, color='#67A0DA')

#fig = plt.figure()
#ax = fig.add_axes([0,0, 1, 1])
#plt.plot(data, color='#67A0DA')
# Display created figure


fig, ax = plt.subplots(figsize=(10 ,10), nrows=2, ncols=2)
ax[0,0].plot(data_1, "b")
ax[0,1].plot(data_2, "r")
ax[1,0].plot(data_3, "g")
ax[1,1].plot(data_4, "y")

fig=plt.show()
plt.savefig("../data/clips.png")
#display(fig)