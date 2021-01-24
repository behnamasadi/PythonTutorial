import numpy as np
import matplotlib.pyplot as plt

true_slope=2

A=np.linspace(0,10,10)
noise=1*np.random.randn(10)
B=true_slope*A+noise+2
plt.scatter(A,B)


A=A.reshape(A.shape[0],-1)
ones=np.ones((10,1))
A=np.hstack((A,ones))

B=B.reshape(B.shape[0],-1)



A_T=np.transpose(A)
A_TxA=np.dot(A_T,A)
A_TxA_inv=np.linalg.inv(A_TxA)
A_TxB=np.dot(A_T,B)
estimted_param=np.dot(A_TxA_inv  , A_TxB )
print(estimted_param)
#
plt.show()