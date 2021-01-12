import numpy as np
import matplotlib.pyplot as plt

## normalize_data to 0 1
# Example Data
x = np.random.randint(low=-100, high=100, size=50)

#Normalized Data
normalized = (x-min(x))/(max(x)-min(x))
fig,axes=plt.subplots(nrows=1,ncols=2)
axes[0].hist(x,range(-100,100))
axes[1].hist(normalized,range=(0,1.0))
print(np.arange(0,1.0,10))
plt.show()

# normalize data to mean 0.5 and std 0.5