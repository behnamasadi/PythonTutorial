#http://en.wikipedia.org/wiki/Newick_format
#Reading and Writing Newick Trees
#http://packages.python.org/ete2/tutorial/tutorial_trees.html#reading-and-writing-newick-trees



#http://packages.python.org/ete2/tutorial/tutorial_clustering.html#cluster-validation-example

#ETE implements three common distance methods in bioinformatics :
#euclidean, 
#pearson correlation
#spearman correlation distances.


#Once the tree is linked to a table of profiles, the following node properties will be available: 
#PhyloNode.profile, 
#PhyloNode.deviation, 
#PhyloNode.silhoutte, 
#PhyloNode.intercluster_dist, 
#PhyloNode.intracluster_dist, 
#PhyloNode.dunn.

#Similarly, the following methods are provide for convenience 
#PhyloNode.iter_leaf_profiles(), 
#PhyloNode.get_leaf_profiles(), 
#PhyloNode.get_silhouette() 
#PhyloNode.get_dunn() methods.


#Image resulting from a microarray clustering validation analysis. 
#Red bubbles represent a bad silhouette index (S<0), while green represents good silhouette index (S>0). 
#Size of bubbles is proportional to the Silhouette index. 
#Internal nodes are drawn with the average expression profile grouped by their partitions. Leaf node profiles are shown as a heatmap.

from ete2 import ClusterTree, TreeStyle, AttrFace, ProfileFace, TextFace
from ete2.treeview.faces import add_face_to_node

# To operate with numbers efficiently
import numpy

PATH = "./"
# Loads tree and array
#t = ClusterTree(PATH+"diauxic.nw", PATH+"diauxic.array")

matrix = """
#Names\tcol1\tcol2\tcol3\tcol4\tcol5\tcol6\tcol7
A\t-1.23\t-0.81\t1.79\t0.78\t-0.42\t-0.69\t0.58
B\t-1.76\t-0.94\t1.16\t0.36\t0.41\t-0.35\t1.12
C\t-2.19\t0.13\t0.65\t-0.51\t0.52\t1.04\t0.36
D\t-1.22\t-0.98\t0.79\t-0.76\t-0.29\t1.54\t0.93
E\t-1.47\t-0.83\t0.85\t0.07\t-0.81\t1.53\t0.65
F\t-1.04\t-1.11\t0.87\t-0.14\t-0.80\t1.74\t0.48
G\t-1.57\t-1.17\t1.29\t0.23\t-0.20\t1.17\t0.26
H\t-1.53\t-1.25\t0.59\t-0.30\t0.32\t1.41\t0.77
"""


#t = ClusterTree("(((A,B),(C,(D,E))),(F,(G,H)));", text_array=matrix)
t = ClusterTree("((A,B,C,D,E),(F,G,H));", text_array=matrix)
# nodes are linked to the array table
array =  t.arraytable

# Calculates some stats on the matrix. Needed to establish the color
# gradients.
matrix_dist = [i for r in xrange(len(array.matrix))\
               for i in array.matrix[r] if numpy.isfinite(i)]
matrix_max = numpy.max(matrix_dist)
matrix_min = numpy.min(matrix_dist)
matrix_avg = matrix_min+((matrix_max-matrix_min)/2)

# Creates a profile face that will represent node's profile as a
# heatmap
profileFace  = ProfileFace(matrix_max, matrix_min, matrix_avg, \
                                         200, 14, "heatmap")
cbarsFace = ProfileFace(matrix_max,matrix_min,matrix_avg,200,70,"cbars")
nameFace = AttrFace("name", fsize=8)
# Creates my own layout function that uses previous faces
def mylayout(node):
    # If node is a leaf
    if node.is_leaf():
        # And a line profile
        add_face_to_node(profileFace, node, 0, aligned=True)
        node.img_style["size"]=0
        add_face_to_node(nameFace, node, 1, aligned=True)

    # If node is internal
    else:
        print node
        print node.silhouette
        # If silhouette is good, creates a green bubble
        if node.silhouette>0:
            validationFace = TextFace("Silh=%0.2f" %node.silhouette, 
                                      "Verdana", 10, "#056600")
            node.img_style["fgcolor"]="#056600"
        # Otherwise, use red bubbles
        else:
            validationFace = TextFace("Silh=%0.2f" %node.silhouette, 
                                      "Verdana", 10, "#940000")
            node.img_style["fgcolor"]="#940000"

        # Sets node size proportional to the silhouette value.
        node.img_style["shape"]="sphere"
        if node.silhouette<=1 and node.silhouette>=-1:
            node.img_style["size"]= 15+int((abs(node.silhouette)*10)**2)

        # If node is very internal, draw also a bar diagram
        # with the average expression of the partition
        add_face_to_node(validationFace, node, 0)
        if len(node)>100:
            add_face_to_node(cbarsFace, node, 1)

# Use my layout to visualize the tree
ts = TreeStyle()
ts.layout_fn = mylayout
t.show(tree_style=ts)