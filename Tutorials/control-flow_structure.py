############################# Replacements for switch statement in Python ############################# 

#switch ($value) {
#    case 'a':
#        $result = $x * 5;
#        break;
#    case 'b':
#        $result = $x + 7;
#        break;
#    case 'c':
#        $result = $x - 2;
#        break;
#}
#And here’s the equivalent code in Python:


x=2
value='b'
result = {
  'a': lambda x: x * 5,
  'b': lambda x: x + 7,
  'c': lambda x: x - 2
}[value](x)
print(result)


x=3
result={
'a': 1,
'b': 2
}.get(x, 'd')    # 9 is default if x not found
print(result)


drinks=['water', 'milk', 'beer']
for i, drink in enumerate(drinks):
	print("drink name {} and index is:{}".format(drink,i))

meals=['steak', 'hamburger','stew']

for drink,meal in zip(drinks,meals):
	print("drink {} comes with {}".format(drink,meal) )

menu=dict(zip(drinks,meals))

for key,value in menu.items():
	print("key is {} and value is {}".format(key, value)) 


print('#################################### while vs for loop iterator ####################################')

my_string = "geeksforgeeks"

for i in my_string: 
    print(i, end =" ") 

i = "o"
while i in my_string: 
    print(i, end =" ")

i = "o"
while i in my_string: 
    print(i, end =" ")


print('#################################### Ternary Operators ####################################')

# Blueprint: value would a if Boolean is true otherwise false
# value=(a,b)[Boolean]
a = 1
b = 2

print((a, b)[True])

# Blueprint: condition_if_true if condition else condition_if_false

x = 1
value = "good" if x > 2 else "bad"
print(value)


