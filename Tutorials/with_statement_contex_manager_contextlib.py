# When you work wth files you need to open/ close them properly and use the exception handling
# Refs:
# https://www.geeksforgeeks.org/with-statement-in-python/
# https://stackoverflow.com/questions/26342769/meaning-of-with-statement-without-as-keyword
try:
    my_file=open('data/with_statement.txt','w')
    my_file.write('some text')

except FileNotFoundError as err:
    print(err)
finally:
    my_file.close()


print('#################################### With Statement ####################################')
# You can use with statement which take care of that: there is no need to call file.close() when using with statement.
# tthe code above takes care of all the exceptions but using the with statement makes the code compact and much more readable.
with open('data/with_statement.txt','w') as my_file:
    my_file.write('mumbo')


print('#################################### With Statement in user defined objects ####################################')


class MyMessage(object):
    def __init__(self, filename):
        self.filename=filename

    def __enter__(self):
        my_file=open(self.filename,'w')
        return my_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        my_file.close()


with MyMessage('data/mymessage.txt') as my_message:
    my_message.write('msg text')

print('#################################### Context Manager ####################################')
# This interface of __enter__() and __exit__() methods which provides the support of with statement in user
# defined objects is called Context Manager

# The context manager can optionally return an object, to be assigned to the identifier named by as.
# And it is the object returned by the __enter__ method that is assigned by as, not necessarily
# the context manager itself.

# Take a database connection. You create the database connection just once, but many database adapters
# let you use the connection as a context manager;

#with db_connection:
    # do something to the database

print('#################################### Contextlib Module ####################################')
