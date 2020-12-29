#2D grid example taken frrom: https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html

#color map https://matplotlib.org/examples/color/colormaps_reference.html
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial import distance


cols=6
rows=7

grid = np.zeros([rows,cols])

start_row_idx=2
start_col_idx=1


goal_row_idx=5
goal_col_idx=4

grid[start_row_idx,start_col_idx]=1
grid[goal_row_idx,goal_col_idx]=1
#print(grid)
blocks=np.array([[4,1],[2,3], [4,3], [5,3]])




for i in range(rows):
    for j in range(cols):
        grid[i,j]=distance.cityblock([goal_row_idx, goal_col_idx], [i,j])

for block in blocks:
    grid[block[0],block[1]]=-1
fig, ax = plt.subplots()
im = ax.imshow(grid,cmap=plt.cm.coolwarm)



ax.set_xticks(np.arange(cols))
ax.set_yticks(np.arange(rows))


# Loop over data dimensions and create text annotations.
for i in range(rows):
    for j in range(cols):
        for block in blocks:
            if [i, j]==[block[0],block[1]]:
                text = ax.text(j, i, "Blocked", ha="center", va="center", color="w")
                break
        
        if [i, j]==[start_row_idx,start_col_idx]:
            text = ax.text(j, i, "start", ha="center", va="center", color="w")
        elif [i, j]==[goal_row_idx,goal_col_idx]:
            text = ax.text(j, i, "goal", ha="center", va="center", color="w")
        else:        
            text = ax.text(j, i, grid[i, j], ha="center", va="center", color="w")

fig.tight_layout()
plt.show()



def getNeighbours(i,j, grid):
    rows, cols=grid.shape
    #print (rows, cols)
    neighboursList=[]
    distances=[]
    for I in np.arange(i-1,i+2,1):
        for J in np.arange(j-1,j+2,1):
            if I>-1 and J >-1 and I<rows and J< cols and [i,j]!=[I,J] :
                #print (I,J)
                #print( np.round(10*np.sqrt((i-I)**2 + (j-J)**2) )   )
                distances.append(np.round(10*np.sqrt((i-I)**2 + (j-J)**2) ) )   
                neighboursList.append([I,J])
    return neighboursList,distances
openSet=[]
closedSet=[]

closedSet=[ [start_row_idx,start_col_idx] ]

neighboursList,distances=getNeighbours(start_row_idx,start_col_idx, grid)
#print(neighboursList)
print("start square")
print(start_row_idx,start_col_idx)

for i in range(len(neighboursList)):
#    print(neighboursList[i])
#    print(grid[neighboursList[i][0],neighboursList[i][1]] )
#    print(distances[i])
    print(distances[i]+grid[neighboursList[i][0],neighboursList[i][1]] )
#    print (grid[neighboursList[i[0]],neighboursList[i[1]]])
#for i in distances:
#    print (i)

hScore=grid
cameFrom =np.zeros([rows,cols])
openSet=[ [start_row_idx,start_col_idx] ]
gScore= np.full((rows,cols), np.inf)


gScore[start_row_idx,start_col_idx] = 0
print(gScore)


#F=G+H
fScore= np.full((rows,cols), np.inf)
fScore[start_row_idx,start_col_idx]=hScore[start_row_idx,start_col_idx]
while len(openSet)>0:
    #current := the node in openSet having the lowest fScore[] value
    for i in range(len(openSet)):
        print(openSet[i])
