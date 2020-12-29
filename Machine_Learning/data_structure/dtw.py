import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw #conda install -c bioconda fastdtw

start=0
end=2*np.pi
step=0.1
k=2

x1=np.arange(start,end,k*step)
x2=np.arange(start,end/k,step)

noise=np.random.uniform(start,end,len(x2))/10

#y1=np.sin(x1)+1*np.sin(2*x1)+noise
y1=np.sin(x1)+1*np.sin(2*x1)

y2=np.sin(k*x2)+1*np.sin(k*2*x2)
sin1=plt.plot(x1,y1)

plt.setp(sin1,color='b',linewidth=2.0)

sin2=plt.plot(x2,y2)
plt.setp(sin2,color='r',linewidth=2.0)

time_series_A=zip(x1,y1)
time_series_B=zip(x2,y2)
distance, path = fastdtw(time_series_A, time_series_B, dist=euclidean)
print (distance)
print (path)



index_a,index_b=zip(*path)
for i in index_a:
    x1=time_series_A[i][0]
    y1=time_series_A[i][1]
    x2=time_series_B[i][0]
    y2=time_series_B[i][1]

    plt.plot([x1, x2], [y1, y2], color='k', linestyle='-', linewidth=2)
plt.show()
