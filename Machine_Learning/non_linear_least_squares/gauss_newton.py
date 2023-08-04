import numpy as np
import sympy
import matplotlib.pyplot as plt

s=np.array([0.038, 0.194, 0.425, 0.626, 1.253, 2.500, 3.740])
rate=np.array([0.050,0.127,0.094,0.2122,0.2729,0.2665,0.3317])
r=np.zeros(rate.shape)


def J_r(x_1,x_2):
    j_r=np.zeros([7,2])
    for i in np.arange(7):
        j_r[i,0]=-s[i]/(x_2 +s[i])
        j_r[i,1]=x_1*s[i]/(x_2+s[i])**2
    return j_r 

def residual(x_1,x_2):
    r=np.zeros([7,1])
    for i in np.arange(7):
        r[i,0]= rate[i]- (x_1*s[i])/(x_2+s[i])
    return r    



x_1=0.9
x_2=0.2



for i in np.arange(5):
   delta_x_1,delta_x_2= np.linalg.inv(np.transpose(J_r(x_1,x_2))@J_r(x_1,x_2))@ np.transpose(J_r(x_1,x_2))@residual(x_1,x_2)
   x_1=x_1-delta_x_1
   x_2=x_2-delta_x_2

print(x_1, x_2)


s_ = np.arange(0,8,0.1)
r_=(x_1*s_)/(x_2+s_)

print("r_",r_.shape)
print("s_",s_.shape)
plt.plot(s_,r_, color="red")    
plt.scatter(s,rate)
plt.show()
