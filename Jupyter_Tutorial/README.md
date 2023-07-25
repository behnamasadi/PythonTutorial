# Jupyter Notebook Tutorial

### How to run:

```
jupyter notebook
```

To allow access to the notebook from outside:
```
jupyter notebook --ip 0.0.0.0 --port 10000
```
### Headlines
use single # for H1, ## H2 for H2 and ### for  H3

## HTML
use

%%HTML
\<table>
	\<tr>
		\<td>
			1
		\</td>
		\<td>
			2
		\</td>
	\</tr>
\</table>



##  Magic Functions
List currently available magic functions.
```%lsmagic```

you can call bash command by using !
```!conda list```
```!wget```
```!nvidia-smi```


## Example of Plotting
```
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

x=np.arange(-4*np.pi,4*np.pi,0.1)
y=np.sin(x)
y_shifted=np.sin(x-np.pi/4)

xmin=0
xmax=4*np.pi
ymin=0
ymax=2

plt.axis([xmin,xmax,ymin,ymax])
line1=plt.plot(x,y)
plt.setp(line1,color='r',linewidth=1.0)

line2=plt.plot(x,y_shifted)
plt.setp(line2,color='b',linewidth=2.0)
plt.show()
```
## Sympy Examples

```
from sympy import *
%matplotlib inline
init_printing(use_latex=True)
x = symbols('x')
Eq(Integral(exp(x)*cos(x), x), exp(x)*sin(x)/2 + exp(x)*cos(x)/2)
```


```
x = symbols('x')
y = symbols('y')
z = symbols('z')
g = symbols('g')
state=Matrix([x,y,z])
g=Matrix([x**2+y**2,y-z])
g.jacobian(state)
```


