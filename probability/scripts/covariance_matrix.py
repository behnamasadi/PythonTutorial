import numpy as np
x=np.array([[4. ,  4.2 , 3.9 , 4.3 , 4.1 ],
 [2.  , 2.1 , 2.  , 2.1  ,2.2 ],
 [0.6 , 0.59 ,0.58 ,0.62 ,0.63]])

number_of_dimentions=x.shape[0]
number_of_samples=x.shape[1]
mu=np.mean(x, axis=1)
mu_outer=np.outer(mu, np.ones(number_of_samples))
x_hat=x-mu_outer
print((1/number_of_samples)*np.dot(x_hat,np.transpose(x_hat)))
