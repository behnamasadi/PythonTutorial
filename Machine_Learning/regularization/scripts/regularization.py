import numpy as np
import matplotlib.pylab as plt

# empty_like
# ones_like
# full_like
# zeros
#ones=np.ones(number_of_samples)
#x_extended_with_ones=np.column_stack((x,ones))

# ridge regression
def tikhonovRegularizedLeastSquares(x,y,alpha):
    # x mxn where m is number of samples and n is number of params
    # y mx1
    # theta nx1 is the params
    # y=np.dot(x, theta)
    # if alpha is very large we care more about reducing parameter magnitude than reducing mean square error,
    # alpha -> inf theta -> 0
    # it reduce the variance but it will increase the bias
    n=x.shape[1]
    x_t=np.transpose(x)
    theta=np.dot(np.dot(np.linalg.inv(np.dot(x_t, x)+alpha*np.eye(n)), x_t),y)
    return theta

def xPolynominalExtender(x,PolynominalOrder=1 ):
    number_of_rows=x.shape[0]
    number_of_cols=PolynominalOrder+1
    new_x=np.ones((number_of_rows,number_of_cols))
    for n in range(PolynominalOrder,0,-1):
        #print(n)
        new_x[ :,PolynominalOrder-n] =np.power(x[:,0],n)
    return new_x

# coefficients[0]*x^n + coefficients[1]*x^(n-1) + coefficients[2]*x^(n-2)
def polynominalFunction(x,coefficients):
    y=np.zeros_like(x)
    #print(x.shape)
    #print(y.shape)
    for n in range(len(coefficients)):
        y=y+np.power(x, n)* coefficients[-n-1]
    return y



def pseudoInverseSolver(x,y):
    return np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(x), x)), np.transpose(x)), y)


noise_magnitude=8
number_of_samples=100
x_min=-5
x_max=5
m=3
b=2

x= np.linspace(x_min,x_max, number_of_samples  )
x= np.reshape(x,(x.shape[0],-1))

y= polynominalFunction(x,[m,b])
y =y +noise_magnitude*np.random.randn(number_of_samples,1)
plt.scatter(x,y)
actual_y=polynominalFunction(x,[m,b])

labels=[]
data_without_noise, =plt.plot(x,actual_y,color='r',label='data without noise' )
labels.append(data_without_noise)

regularization_alpha = 20000

for i in range(10,13):
    polynominal_order=i
    new_x=xPolynominalExtender(x,polynominal_order )

    params=pseudoInverseSolver(new_x,y)
    y = polynominalFunction(x, params)
    random_color = list(np.random.random(3))
    params_label, = plt.plot(x, y, color=random_color, label=str(i))
    labels.append(params_label)



    regularized_params=tikhonovRegularizedLeastSquares(new_x, y, regularization_alpha)
    y_regularized = polynominalFunction(x, regularized_params)
    random_color = list(np.random.random(3))
    regularized_params_label,=plt.plot(x, y_regularized, color=random_color,label=str(i)+' regularized')
    labels.append(regularized_params_label)

    #print('diff between params and regularized params:',params-regularized_params)

plt.legend(handles=labels)
plt.show()








