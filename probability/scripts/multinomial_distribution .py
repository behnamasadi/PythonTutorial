import numpy as np

probabilities_of_each_side_of_dice=[1/6,1/6,1/6,1/6,1/6,1/6] # or simply [1/6.]*6
number_of_experiments=2000
output_shape=1
result=np.random.multinomial(number_of_experiments,probabilities_of_each_side_of_dice,output_shape)
print(result)