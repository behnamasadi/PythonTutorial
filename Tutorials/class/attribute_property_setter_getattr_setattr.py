class Student:
    def __init__(self, name):
        self._name = name
        self._age = 10  # age is attribute

    def getName(self):
        return self._name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


############################  setter, property ############################

student_instance = Student('some name')
print("Getting student name via class method:",student_instance.getName())
print("Accessing student name via property/ setter:", student_instance.name)
student_instance.name = 'new name'


############################  getattr/ setattr ############################
#getattr(object, 'x') is completely equivalent to object.x.

setattr(student_instance, "name","new name")
print(getattr(student_instance, "name"))



#getattr(student_instance, "age") ==>'Student' object has no attribute 'age'
#getattr will raise AttributeError if attribute with the given name does not exist in the object:

#But you can pass a default value as the third argument, which will be returned if such attribute does not exist:
value="exists" if getattr(student_instance, "age",-1)!=-1  else "doesn't exists"
print( "the attribute age {}".format(value)    )


# You can use getattr along with dir to iterate over all attribute names and get their values:
#print("dir(student_instance):",dir(student_instance))

list_of_attributes=dir(student_instance)




for i in range(len(list_of_attributes)) :
	if(True != list_of_attributes[i].startswith("__")   ):
		print(list_of_attributes[i])
	


