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


plt.plot(s_,r_, color="red")    
plt.scatter(s,rate)
plt.show()



from scipy.optimize import least_squares

def func(params,x):
    a,b,c,d=params
    y=a*x**3+b*x**2+c*x+1+d
    return y

def residual_function(params,x0, y_observed):

    y_predicted=func(params,x0)
    
    return y_predicted-y_observed
    



a=1.7
b=-2.4
c=-1.3
d=1
params=a,b,c,d

x=np.linspace(-2,3,100)
y_true=func(params,x)

y_noisy=y_true+1.5 * np.random.randn(y_true.shape[0])


a_initial_guess=1
b_initial_guess=2
c_initial_guess=0
d_initial_guess=-1

initial_guess=[a_initial_guess,b_initial_guess,c_initial_guess,d_initial_guess]

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
result =least_squares(fun=residual_function, x0=initial_guess, args=(x, y_noisy),method='lm')


a_estimated,b_estimated,c_estimated,d_estimated=result.x
y_estimated=func(result.x,x)



plt.plot(x,y_noisy)
plt.plot(x,y_true)
plt.plot(x,y_estimated)
plt.show()

