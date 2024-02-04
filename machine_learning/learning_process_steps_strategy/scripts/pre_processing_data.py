import numpy as np
import matplotlib.pyplot as plt

n_samples=1000
n_dim=2
X=np.random.randn(n_samples,n_dim)

tetha=np.pi/4
rotation_mat=np.array([  [ np.cos(tetha),-np.sin(tetha)], [np.sin(tetha),np.cos(tetha) ]])

Sx=5.5
Sy=0.4
scaling_mat=np.array([  [ Sx,0], [0,Sy ]])

X=np.dot(X,scaling_mat)
X=np.dot(X,rotation_mat)

X[:,0]=X[:,0]+2
X[:,1]=X[:,1]+4

plt.scatter(X[:,0],X[:,1])



# each example in a row
# axis=0 means columnwise
X=X-np.mean(X,axis=0)
X=X/np.std(X,axis=0)
plt.scatter(X[:,0],X[:,1])
plt.show()
