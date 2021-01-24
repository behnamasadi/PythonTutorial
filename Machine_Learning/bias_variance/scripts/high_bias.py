import  matplotlib.pyplot as plt
import numpy as np

def error_cv(x):
    return 30/np.exp(x)+50

def error_training(x):
    return 7*np.log(x)+30

epsilon=0.00001
x=np.linspace(0.01,2,100)

fig,axes=plt.subplots(1,2)
plt.axis(ymin=0,ymax=+80)

y_error_cv=error_cv(x)
y_error_training=error_training(x)

legend_y_error_cv,=axes[0].plot(x,y_error_cv,color='blue',label='cross validation error')
legend_y_error_training,=axes[0].plot(x,y_error_training,color='red',label='training error')
axes[0].set_aspect('auto',adjustable='datalim')


x=np.linspace(0+epsilon,15,100)

y_error_cv=error_cv(x)
y_error_training=error_training(x)


legend_y_error_cv,=axes[1].plot(x,y_error_cv,color='blue',label='cross validation error')
legend_y_error_training,=axes[1].plot(x,y_error_training,color='red',label='training error')

fig.legend(handles=[legend_y_error_cv,legend_y_error_training])

plt.show()