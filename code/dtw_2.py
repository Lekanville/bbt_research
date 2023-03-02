import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

x = np.array([1, 2, 3, 3, 7])
y = np.array([1, 2, 2, 2, 2, 2, 2, 4])

z = [1, 2, 3, 3, 7]
k = [1, 2, 2, 2, 2, 2, 2, 4]
distance, path = fastdtw(x,y)
#distance, path = fastdtw(x, y, dist=euclidean)

print(distance)
print(path)