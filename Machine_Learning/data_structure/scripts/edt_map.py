from PIL import Image
import numpy as np

sizeX=100;
sizeY=100;

arr=np.random.randint(0,256,sizeX*sizeY)
arr.resize((sizeX,sizeY))
#print arr

img=Image.fromarray(arr.astype('uint8'),'L')  # cast to uint8
new_arr=np.array(img)
#print new_arr

#img.show()




#http://pillow.readthedocs.io/en/3.1.x/handbook/concepts.html#concept-modes
#img=Image.fromarray(arr.astype('uint8'),'F')  # cast to 32-bit floating point pixels



#map_file = open('/home/behnam/sample_based_optimisation_based_path_planner_sw/devel/lib/sample_based_optimisation_based_path_planner/map.txt', 'r')
map_file = open('mat2.txt', 'r')


lines = map_file.readlines()
print (len(lines))
map_file.close()

# initialize some variable to be lists:
x = []
y = []

distances=[]

# scan the rows of the file stored in lines, and put the values into some variables:
for line in lines:
    
    p = line.split(' , ')
    #del p[100]
    p = map(float, p)
    distances.append(p)
    
    
x=np.array(distances)


x.resize((sizeX,sizeY))
#print arr



img=Image.fromarray(x.astype('uint8'),'L')  # cast to uint8
new_arr=np.array(img)
#print new_arr

#img.show()
img.save('map.png')

