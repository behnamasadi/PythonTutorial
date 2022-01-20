import matplotlib.pyplot as plt
import numpy as np

def discreteSeriesPlotter(x):
    t=np.arange(x.shape[0])

    tmin=-1
    tmax=x.shape[0]+1
    xmin=0
    xmax=x.max(axis=0)+1


    plt.axis([tmin,tmax,xmin,xmax])

    plt.scatter(t,x)

    for i in range(x.shape[0]):
        plt.vlines(x=t[i], ymin=0, ymax=x[i], colors='k')


    plt.show()

x=np.array([1,3,1,2])
discreteSeriesPlotter(x)


h=np.array([2,1,3])
discreteSeriesPlotter(h)
