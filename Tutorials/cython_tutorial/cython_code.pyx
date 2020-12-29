#You can call from c/c++ and vice versa
#1) Install the Cython: conda install Cython
#2) python setup.py build_ext --inplace
#The --inplace option creates the shared object file (with .so suffix) 


def test(x):
	y=0
	for i in range(x):
		y+=i
	return y




