# Tuples

The differences between tuples and lists are, the tuples cannot be changed unlike lists and tuples use parentheses `(,)`, whereas lists use square brackets`[,]`.

```python
tup1 = ('physics', 'chemistry', 1997, 2000)
tup2 = (1, 2, 3, 4, 5 )
tup3 = "a", "b", "c", "d"

print ("tup1[0]: ", tup1[0])
print ("tup2[1:5]: ", tup2[1:5])
```
Following action is not valid for tuples
```
tup1[0] = 100;
```
# List
A list  can be written as a list of comma-separated values (items) between square brackets `[,]`.

```python
list1 = ['physics', 'chemistry', 1997, 2000];
list2 = [1, 2, 3, 4, 5, 6, 7,"bamboo","?" ];
list2.append(8)
#list2.insert(index, value)
len(list2)
index_int=1
list2.pop(index_int)
list2.remove("bamboo")
print ("list1[0]: ", list1[0])
print ("list1[1:5]: ", list2[0:5])
print ("list1 reverse(list1[::-1]): ", list2[::-1])
print ("list2: ", list2)
```
negative indexes:
```
print ("list2[-1]: ", list2[-1])
```

List Comprehension

```
list=[ expr for val in collestion ]
list=[ expr for val in collestion if <> and if <> ]
```
example 1:

```
movies=["The Shawshank Redemption" , "The Godfather", "The Godfather: Part II", "The Dark Knight" ,"Angry Men" ,"Pulp Fiction"]
movies_start_with_the=[title for title in movies if title.startswith("The")]
print("movies start with 'the': ",movies_start_with_the)
```

example 2:

```
movies=[("The Shawshank Redemption",1994) , ("The Godfather",1972), ("The Godfather: Part II",1974), ("The Dark Knight",2008) ,("Angry Men",1957) ,("Pulp Fiction",1994)]

movies_start_with_the_after_1990=[title for (title,year) in movies if title.startswith("The") and year>1990]
print("movies start with 'the' after 1990: ",movies_start_with_the_after_1990)
```

```
A=[1,2,3]
B=['a','b']
cartesian_product_A_B=[(a,b) for a in A for b in B ]
print(cartesian_product_A_B) 
```

# Array 
If all you're doing is creating arrays of simple data types and doing I/O, the array module will do just fine. If, on the other hand, you want to do any kind of numerical calculations,
the array module doesn't provide any help with that. NumPy (and SciPy) give you a wide variety of operations:

Refs: [1](https://docs.python.org/3/library/array.html)

```
import array

#'b' ==> signed char, 'i' ==> signed int
my_array = array.array('i',[1,2,3,4])#array('data type', data)
del my_array[2]
print (my_array)
```

append(), extend(), insert (i,x) , remove(), zip

```
list1=[2,3,1]
list2=[4,0,8]


for i, j in zip(list1,list2):
	print(i,j)

print("list1+list2:\n",list1+list2) #[2,3,1,4,0,8]
print("list1*2:\n",list1*2) #[2,3,1,2,3,1]
```

`extend()`: Iterates over its argument and adding each element to the list and extending the list. 

```
list1.extend(list2)
print(list1) #[2,3,1,4,0,8]


print("list1remove(3):\n",list1.remove(3))

list1.append(list2)
print("list1.append(list2):\n", list1) 
```

A string is an iterable, so if you extend a list with a string, you’ll append each character as you iterate over the string.
```
list1=[2,3,1]
list1.extend('geeks')
print(list1)
```
# Dictionaries
```
my_dict={"book":1,"hello":2, "beer":3}
print(my_dict["hello"])
my_dict["book"]=0
print(my_dict["book"])
```


use get() key instead of [] if you are not sure about the existence  of key 
```
print( my_dict.get("jumbo") )
print(my_dict.get("jumbo","key not found!"))
```


dictionary from a lists
```
list1= (['a', 1, 'b', 2, 'c', 3]) 
print( {list1[i]: list1[i+1]   for i in range( 0, len(list1), 2 )  } )
```

dictionary from two lists
```
keys = ['a', 'b', 'c']
values = [1, 2, 3]
print("dictionary from two lists:",{ key:value   for key,value in zip( keys,values )})
print("dictionary from two lists:", dict(zip(keys,values) ) )
```

updating dictionaries
```
dictionary1 = {'Google' : 1, 
               'Facebook' : 2, 
               'Microsoft' : 3
               } 
dictionary2 = {'GFG' : 1, 
               'Microsoft' : 2, 
               'Youtube' : 3
               } 
dictionary1.update(dictionary2)
for key, values in dictionary1.items(): 
    print(key, values) 
```

dictionary duplicate key:
```
dictionary1 = {'GFG' : 1, 
               'Google' : 2, 
               'GFG' : 3
               } 
print(dictionary1['GFG']) # Here, GFG is the duplicate key. Duplicate keys are not allowed in python. If there are same keys in a dictionay, then the value assigned mostly recently is assigned to the that key.
```



Dictionaries are unordered. So any key value pairs can be added at any location within a dictionary. Any of the output may come.

```
temp = {'GFG' : 1, 
        'Facebook' : 2, 
        'Google' : 3
        } 
for (key, values) in temp.items(): 
    print(key, values, end = " ") 

```
print("\n############################### Set ###############################")
#A set is a collection which is unordered and unindexed. In Python sets are written with curly brackets.
#You cannot access items in a set by referring to an index, since sets are unordered the items has no index.

# When to use the other types:
# - Use lists if you have a collection of data that does not need random access. Try to choose lists when you need a simple, iterable collection that is modified frequently.
# - Use a set if you need uniqueness for the elements.
# - Use tuples when your data cannot change.

fruit_set = {"apple", "banana", "cherry"}
fruit_set.add("orange")
#Add multiple items to a set, using the update() method:
fruit_set.update(["orange", "mango", "grapes"])
fruit_set.discard("banana")# If the item to remove does not exist, remove() will raise an error.


for fruit in fruit_set:
	print(fruit)

print("banana" in fruit_set)

drink_set={"water", "beer"}
union_set = drink_set.union(fruit_set)
print(union_set)

#difference: operator - gets items in the first set but not in the second.

#intersection: operator & gets items only in both.

#issubset()

thisset = set(("apple", "banana", "cherry")) # note the double round-brackets


a = set('abracadabra')
b = set('alacazam')
a                                  # unique letters in a
#{'a', 'r', 'b', 'c', 'd'}
a - b                              # letters in a but not in b
{'r', 'd', 'b'}
#a | b                              # letters in a or b or both
{'a', 'c', 'r', 'd', 'b', 'm', 'z', 'l'}
#a & b                              # letters in both a and b
{'a', 'c'}
#a ^ b                              # letters in a or b but not both
{'r', 'd', 'b', 'm', 'z', 'l'}


a = {x for x in 'abracadabra' if x not in 'abc'}

print(a)


print("######################### How to check if it is a list, tuple, set, dictionary, etc ###############################")

print("[] is list:" ,isinstance( [],list)) 
print("() is tuple:" ,isinstance( (),tuple)) 

print("type([])==type([1,2,3]) :" ,type([])==type([1,2,3]) ) 

# Packing and Unpacking 
We use two operators * (for tuples) and ** (for dictionaries).

def fun(a, b, c, d): 
    print(a, b, c, d) 

my_list = [1, 2, 3, 4]

This will rise an error:
```
fun(my_list)
```
Unpacking list into four arguments 
```
fun(*my_list)
d = {'a':2, 'b':4, 'c':10,'d':14} 
fun(**d) 
```
# Packing
When we don’t know how many arguments need to be passed to a python function, we can use Packing to pack all arguments in a tuple.

```
def  sum(*args):
	total=0
	for i in range(0,len(args)):#here we can also simply do args = list(args) 
		total=total+args[i]	
	return total
a=1
b=2
c=5
print("The sum of the {} {} {} is:".format(a,b,c),sum(a,b,c)  )
```

# Zipping and Unzipping

```
x = [1, 2, 3]
y = [4, 5, 6]
print(list(zip(x, y)))
```
zip() in conjunction with the * operator can be used to unzip a list:
```
x2, y2 = zip(*zip(x, y))
print(list(x2))
```

# cloning/ copying/ deep copy

```
old_list=[1,2,3]

#1) 
new_list = old_list.copy()

#2) 
new_list = old_list[:]

#3)
new_list = list(old_list)

#4)
import copy
new_list = copy.copy(old_list)
```
If the list contains objects and you want to copy them as well, use generic `copy.deepcopy()`
```
new_list = copy.deepcopy(old_list)
```
# Counter

```
from  collections import Counter
c=Counter(cats=3,dog=2)
print("c:",c)
print("list(c):",list(c))
print("list(c.elements()):",list(c.elements()))
print("c['cats']:",c['cats'])
print("c['zombie']:",c['zombie'])

list_of_words=['a','a','b' ,'c' , 'b', 'a' ,'a','b']
c=Counter(list_of_words)
print("Top two most common elements are:",c.most_common(2))

set1=Counter(a=4,b=3,c=0,e=2)
l=[a,b]
set1.subtract(l)
print("set1-l:",set1)
set1.update(l)
print("set1+l:",set1)

set1=Counter(a=4,b=2,c=0,d=-2)
set2=Counter(['a','b' , 'b' ,'c'])
print("set1 intersection set2:", set1 & set2)
print("set1 union set2:", set1 | set2)
```


Checking if two words are anagrams
```
print(   Counter('hello') == Counter('holle') )
```
# deque


# namedTuple


# Orderddict

# defaultdict

