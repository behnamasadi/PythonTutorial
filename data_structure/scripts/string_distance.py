from difflib import SequenceMatcher
import Levenshtein
import numpy as np
from scipy.spatial.distance import  pdist 


#https://en.wikipedia.org/wiki/String_metric
#1)Levenshtein
#2)Jaro-Winkler distance
#3)Damerau-Levenshtein distance
#4)Hamming

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


str1='a'
str2='c'



print similar(str1,str2)

#print Levenshtein.ratio('hello world', 'hello')

str1='kitten'
str2='sitting'
print 'Levenshtein'
print Levenshtein.distance(str1, str2)
#.ratio(


############ user defiend pdist() function ################
def hamdist(str1, str2):
    "Count the # of differences between equal length strings str1 and str2"
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
            if ch1 != ch2:
                    diffs += 1
    return diffs

print hamdist(str1, str2)


#Convert string to some int value for computing distance
X=[['a'],['b'],['c'],['d'],['e']]
d=np.array(['a', 'b', 'c', 'd', 'e', 'f'], dtype='|S5')
numeric_d = d.view(np.uint8).reshape((len(d),-1))
print numeric_d
print len(X)
dm = pdist(numeric_d, hamdist)
dm = pdist(numeric_d)
print dm




X= [[i] for i in [2, 8, 0, 4, 1, 9, 9, 0]]
dm = pdist(X, lambda u, v: np.sqrt(((u-v)**2).sum()))

#If you want to use a regular function instead of a lambda function
def dfun(u, v):
    return np.sqrt(((u-v)**2).sum())

dm = pdist(X, dfun)



