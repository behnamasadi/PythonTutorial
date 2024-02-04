import  matplotlib.pyplot as plt
import numpy as np

def error_cv(x):
    return 30/np.exp(x)+50

def error_training(x):
    return 7*np.log(x)+30

def underlying_unkown_function(x):
    y=np.power(x,0.4)
    noise=0.05*np.random.randn(x.shape[0])
    return y+noise


def ideal_model(x):
    y=np.power(x,0.4)
    return y

fig,axes=plt.subplots(2,2)
plt.axis(ymin=0,ymax=+80)

####################################### (0,0)  ######################################
x=np.linspace(0.01,2,5)
y=underlying_unkown_function(x)

axes[0,0].set_xlabel("training set size")
axes[0,0].set_ylabel("price")
axes[0,0].scatter(x,y,color='blue',label='training set items',marker='x')

axes[0,0].plot(x,(1.2/2)*x+0.3,color='green',label='under fit high bias model')
axes[0,0].plot(x,ideal_model(x),color='cyan',label='good fit model')


####################################### (0,1)  ######################################

x=np.linspace(0.01,2,20)
y=underlying_unkown_function(x)

axes[0,1].set_xlabel("training set size")
axes[0,1].set_ylabel("price")
axes[0,1].scatter(x,y,color='blue',label='training set items',marker='x')
under_fit_high_bias_model,=axes[0,1].plot(x,(1.2/2)*x+0.3,color='green',label='under fit high bias model')
legend_y_fit_model,=axes[0,1].plot(x,ideal_model(x),color='cyan',label='good fit model')

####################################### (1,0)  ######################################

epsilon=0.00001
x=np.linspace(0.01,2,100)

y_error_cv=error_cv(x)
y_error_training=error_training(x)

legend_y_error_cv,=axes[1,0].plot(x,y_error_cv,color='blue',label='cross validation error')
legend_y_error_training,=axes[1,0].plot(x,y_error_training,color='red',label='training error')
axes[1,0].set_aspect('auto',adjustable='datalim')

axes[1,0].set_xlabel("training set size")
axes[1,0].set_ylabel("error")

####################################### (1,1)  ######################################

x=np.linspace(0+epsilon,15,100)

y_error_cv=error_cv(x)
y_error_training=error_training(x)

legend_y_error_cv,=axes[1,1].plot(x,y_error_cv,color='blue',label='cross validation error')
legend_y_error_training,=axes[1,1].plot(x,y_error_training,color='red',label='training error')

axes[1,1].set_xlabel("training set size")
axes[1,1].set_ylabel("error")


fig.legend(handles=[legend_y_error_cv,legend_y_error_training,legend_y_fit_model,under_fit_high_bias_model])
plt.show()