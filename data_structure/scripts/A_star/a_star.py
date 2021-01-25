import matplotlib.pyplot as plt



data = [
    [0,0,0,0,0,1,1,1,1,0],
    [0,0,0,0,0,1,0,0,1,0],
    [0,0,1,0,1,0,1,1,0,0],
    [0,0,1,0,0,1,1,0,1,0],
    [0,0,1,0,1,0,0,1,1,0],
    [1,0,0,1,0,1,0,0,1,0],
    [0,1,0,0,0,1,1,1,1,1],
    [0,1,0,0,0,0,1,1,1,1],
    [1,0,0,0,1,1,1,0,1,0],
    [1,1,1,1,0,0,0,1,1,0]
]

#plt.imshow(data, cmap=plt.cm.bwr)
#plt.imshow(data)
#plt.show()


#The coordinates of the quadrilateral corners. The quadrilateral for C[i,j] has corners at:
#(X[i+1, j], Y[i+1, j])          (X[i+1, j+1], Y[i+1, j+1])
#                      +--------+
#                      | C[i,j] |
#                      +--------+
#    (X[i, j], Y[i, j])          (X[i, j+1], Y[i, j+1]),



from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
cmap = colors.ListedColormap(['Blue','red'])
plt.figure(figsize=(6,6))
plt.pcolor(data[::-1],cmap=cmap,edgecolors='k', linewidths=3)
plt.xticks(np.arange(0.5,10.5,step=1))
plt.yticks(np.arange(0.5,10.5,step=1))
plt.show()