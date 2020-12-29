import re


""" 
Regular Expressions
^	Start
$	Stop
.	Any character
*	Match one character 0+ time
+	Match onecharacter 1+ times
?	Non greedy
\s 	Whitespace
\S	Non-whitespace
[abc]	Match one charcter in the specified set
[^abc]	Match one charcter not in the specified set

"""
my_string="Send an email from account@gmail.comto test@user.com 103 times"
result=re.findall('^Sen', my_string)
result=re.findall('[abc]', my_string)
result=re.findall('[0-9]+', my_string)
result=re.findall('[a-d]+', my_string)
result=re.findall('[^a-z]', my_string)
result=re.findall('\S+@\S+', my_string)
print(result)

