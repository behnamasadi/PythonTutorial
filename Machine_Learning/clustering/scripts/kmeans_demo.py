import time

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib.pyplot as plt

from sklearn import cluster, datasets
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler

from sklearn.cluster import KMeans
from matplotlib.mlab import bivariate_normal

from sklearn import preprocessing
import numpy as np
import csv

csv_training_data="/home/behnam/Desktop/testData6.csv"
samples=[]
with open(csv_training_data,'r') as csv_file:
    reader = csv.DictReader(csv_file,delimiter=';')
    for row in reader:
        sample=[float(row['a']) , float(row['b']) , float(row['c'])  ]
        samples.append(sample)

samples = preprocessing.scale(samples)


training_set=samples[0: int( 0.97* len(samples) )  ]
test_set=samples[int( 0.97* len(samples) ): len(samples)  ]


data=np.array(training_set)


kmeans = KMeans(init='k-means++', n_clusters=4)
kmeans.fit(data)

centers=kmeans.cluster_centers_

i=1
new=test_set[i]
Z = kmeans.predict(test_set[i])

#print Z

#for i in np.arange(len(test_set)):
#Z = kmeans.predict(test_set[i])
    
    #print Z

print centers

